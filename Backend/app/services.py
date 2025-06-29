import json
import httpx
from bson import ObjectId
from .config import settings
from .repositories import get_all_roles
from .translations import translate_list, TRANSLATION_MAP
import re

def clean_for_json(obj):
    """המרת אובייקטים לא תואמי JSON (כגון ObjectId) למחרוזות."""
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(i) for i in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

async def extract_traits_from_text(text: str, gender: str = "זכר") -> list[str]:
    """
    שולח טקסט חופשי ל־LLM כדי לחלץ תכונות אופי כלליות בעברית,
    ומחזיר רשימה של מפתחות מתוך TRANSLATION_MAP (normalized keys).
    """
    prompt = (
        f"הטקסט הבא הוא תיאור חופשי של מועמד לשירות ביטחוני:\n"
        f"מין: {gender}\n"
        f'"{text}"\n\n'
        "נתח את תכונות האופי מתוך הטקסט בלבד.\n"
        "המטרה היא להסביר אילו תכונות יש למועמד בשפה נגישה וברורה – למשל: חברותי, אחראי, יוזם.\n"
        "אל תחזור על משפטים מהטקסט המקורי.\n"
        "ענה בעברית בלבד.\n"
        "החזר את התכונות בלבד, מופרדות בפסיקים, בלי תוספות או פתיחים.\n"
        "שים לב: אם המין הוא נקבה, החזר תשובה בלשון נקבה בלבד."
    )

    payload = {
        "model": "meta-llama/llama-3-70b-instruct",
        "messages": [
            {"role": "system", "content": "אתה עוזר בסיווג תכונות אישיות לצה״ל."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "HTTP-Referer": "https://github.com/YuvalBZ/fastapi_project",
        "X-Title": "Trait Extractor",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )
        res.raise_for_status()
        content = res.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not content:
            raise ValueError("תשובת ה־API ריקה.")

        # פיצול לתכונות
        raw_traits = re.split(r",| ו|\n|\.|\s-\s", content)
        traits = [t.strip() for t in raw_traits if t.strip() and len(t.strip()) > 1]

        # ניסיון למפות כל תכונה למפתח במפה
        normalized_keys = []
        for trait in traits:
            match_found = False
            for key, val in TRANSLATION_MAP.items():
                if isinstance(val, dict) and trait in val.values():
                    normalized_keys.append(key)
                    match_found = True
                    break
                elif isinstance(val, str) and trait == val:
                    normalized_keys.append(key)
                    match_found = True
                    break
            if not match_found:
                print(f"⚠️ תכונה לא מזוהה: {trait}")
                normalized_keys.append(trait)  # אם אין התאמה – שומר את הטקסט המקורי

        return normalized_keys

    except Exception as e:
        print(f"❌ Trait extraction failed: {e}")
        raise


async def ai_recommend(profile: dict, roles: list[dict] = None, db=None) -> list[dict]:
    """מחזיר 3 תפקידים מתאימים בפורמט: [{score, role: {name, description, requirements...}}]"""
    roles = await get_all_roles()

    system_msg = (
    "אתה מומחה בהתאמת פרופילים אישיים לתפקידים צבאיים בצה\"ל.\n"
    "כל תפקיד מכיל את שדה 'type' שמתאר את הסוג הכללי שלו: לוחמה, מודיעין, טכנולוגי, תומך לחימה, הדרכה, וכו'.\n\n"
    "הפרופיל כולל את: שם, גיל, מין, רמת כושר גופני (1–5), כישורים טכניים, תכונות אופי, שפות, ותיאור חופשי.\n"
    "שים לב:\n"
    "- סקלת הכושר הגופני היא בין 1 (כושר נמוך מאוד) ל־5 (כושר גבוה מאוד).\n"
    "- אל תמליץ על תפקידים עם דרישות כושר גבוהות אם הכושר הוא 1–2.\n"
    "- אם הכושר הגופני הוא 4 או 5, והתכונות כוללות הקרבה, עבודת צוות או ספורטיביות – חובה להמליץ על תפקיד אחד לפחות מסוג קרבי, אל תמליץ על תפקיד עם פרופיל רפואי נמוך מ-82. (type='לוחמה').\n"
    "- אם שפות כמו ערבית או פרסית מופיעות בפרופיל – חובה להמליץ על לפחות תפקיד אחד מסוג מודיעין (type='מודיעין').\n\n"
    "- אם מדובר בנקבה תציע לה תפקיד (type='אנושי') כמו משקית.\n\n"
    "שקל את ההתאמה לפי:\n"
    "- 30% תכונות אופי (traits)\n"
    "- 30% כישורים טכניים (tech)\n"
    "- 25% כושר גופני\n"
    "- 15% שפות\n\n"
    "החזר JSON בלבד. מבנה כל המלצה:\n"
    "- role_id (מזהה התפקיד ממסד הנתונים)\n"
    "- score (ציון התאמה מ-0 עד 100)\n"
    "- עליך להחזיר אך ורק מזהי תפקידים תקפים ממסד הנתונים"
    "החזר בדיוק 3 המלצות. אין לעטוף את התשובה באובייקט נוסף. אם מדובר בנקבה, כתוב בלשון נקבה כולל תכונות בלשון נקבה."
)
    
    system_msg += (
    "\n\n הנחיות חשובות מאוד:\n"
    "- אל תוסיף הסברים או טקסט חופשי.\n"
    "- אל תצרף כותרות, סיבות, או טקסטים נוספים – החזר JSON תקני בלבד!\n"
    "- אל תכתוב 'role:' או 'Reason:'.\n"
    "- החזר אך ורק מערך JSON בפורמט: [{\"role_id\": \"...\", \"score\": 95}, ...]\n"
)

    payload = {
    "model": "meta-llama/llama-3-70b-instruct",
    "messages": [
        {
            "role": "system",
            "content": system_msg
        },
        {
            "role": "user",
            "content": json.dumps({
                "profile": clean_for_json(profile),
                "roles": clean_for_json(roles)
            }, ensure_ascii=False)
        }
    ],
    "temperature": 0.0,
    "max_tokens": 800
}

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "HTTP-Referer": "https://github.com/YuvalBZ/fastapi_project",
        "X-Title": "Role Matcher",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",  
                json=payload,
                headers=headers
            )

        res.raise_for_status()
        print(f"📬 Raw API response: {res.text}")

        content = res.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not content:
            raise ValueError("לא התקבלו תוצאות מה-API, התשובה ריקה.")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            # נסה לחלץ JSON מתוך הטקסט
            match = re.search(r"(\[\s*{.*?}\s*\])", content, re.DOTALL)
            if match:
                parsed = json.loads(match.group(1))
            else:
                raise ValueError("⚠️ לא הצלחתי לחלץ JSON תקני מהתשובה של המודל.")

        if not isinstance(parsed, list) or not all("role_id" in r and "score" in r for r in parsed):
            raise ValueError("📭 פורמט לא צפוי בתשובת ה־API")

        enriched = []
        for r in parsed:
            role_doc = await db.roles.find_one({"_id": ObjectId(r["role_id"])})
            if role_doc:
                enriched.append({
                    "score": r["score"],
                    "role": clean_for_json(role_doc)
                })

        return enriched

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error from API: {e.response.status_code} - {e.response.text}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ שגיאה בפענוח JSON: {e}")
        raise
    except Exception as e:
        print(f"❌ קרתה שגיאה לא צפויה: {e}")
        raise

async def generate_profile_summary(profile: dict) -> str:
    traits = profile.get("personality_traits", [])
    fitness = profile.get("physical_fitness", None)
    languages = profile.get("languages", [])
    tech = profile.get("technical_skills", [])
    gender = profile.get("gender", "זכר")

    is_female = gender == "נקבה"
    pronoun = "את" if is_female else "אתה"
    suffix = "ת" if is_female else ""

    lines = []

    # פתיח עם תכונות
    if traits:
        translated_traits = translate_list(traits[:5], gender="female" if is_female else "male")

        if len(translated_traits) == 1:
            traits_str = translated_traits[0]
        elif len(translated_traits) > 1:
            traits_str = ", ".join(translated_traits[:-1]) + " ו" + translated_traits[-1]
        else:
            traits_str = ""

        if traits_str:
            lines.append(
                f"וואו! תודה על השיתוף. נשמע ש{pronoun} {traits_str}. "
                f"תכונות אלו עשויות להתאים לתפקידים מסוימים בצה\"ל."
            )
        else:
            lines.append("וואו! תודה על השיתוף. נתחיל לבחון את ההתאמה שלך לתפקידים שונים בצה\"ל.")

    # כושר גופני
    if fitness is not None:
        if fitness <= 2:
            lines.append(
                f"הכושר הגופני שלך נמוך יחסית (רמה {fitness} מתוך 5), ולכן המלצנו על תפקידים שאינם דורשים מאמץ פיזי."
            )
        elif fitness >= 4:
            lines.append(
                "רמת הכושר הגופני שלך גבוהה, ולכן פתחנו גם אפשרות לתפקידים עם דרישה פיזית."
            )

    # שפות
    relevant_langs = [lang for lang in languages if lang in ["ערבית", "פרסית", "רוסית"]]
    if relevant_langs:
        langs_str = ", ".join(relevant_langs)
        lines.append(f"שפות שצוינו כמו {langs_str} עשויות להתאים במיוחד לתפקידים מודיעיניים.")

    # כישורים טכניים
    relevant_tech = [t for t in tech if any(x in t.lower() for x in ["תכנות", "סייבר", "טכנולוג", "רובוט"])]
    if relevant_tech:
        tech_str = ", ".join(relevant_tech)
        lines.append(
            f"המערכת זיהתה כישורים טכנולוגיים כמו {tech_str}, ולכן שקלנו תפקידים בתחומים טכנולוגיים והדרכתיים."
        )

    if not lines:
        return "נותחת ההתאמה לפי התכונות שמילאת בטופס והפרטים האישיים שסיפקת."

    return "\n\n".join(lines)
