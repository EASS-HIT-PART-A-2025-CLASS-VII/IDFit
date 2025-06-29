from deep_translator import GoogleTranslator
import re
import os

TRANSLATION_MAP = {
    "technical_skills": "כישורים טכניים",
    "patience": "סבלנות",
    "clarity": "בהירות",
    "communication": "תקשורת",
    "precision": "דיוק",
    "focus": "מיקוד",
    "analytical_thinking": "חשיבה אנליטית",
    "teamwork": "עבודת צוות",
    "responsibility": {"male": "אחראי", "female": "אחראית"},
    "generous": {"male": " נדיב ואלטרואיסטי", "female": "נדיבה ואלטרואיסטית"},
    "friendly": {"male": "חברותי", "female": "חברותית"},
    "altruistic": {"male": "אלטרואיסטי", "female": "אלטרואיסטית"},
    "expert": {"male": "מומחה ובעל נסיון", "female": "מומחית ובעל נסיון"},
    "organization": "ארגון",
    "problem_solving": "פתרון בעיות",
    "adaptability": {"male": "בעל יכולת הסתגלות", "female": "בעלת יכולת הסתגלות"},
    "traditional": {"male": "מסרותי", "female": "מסורתית"},
    "leadership": {"male": "מנהיג", "female": "מנהיגה"},
    "social": {"male": "סוציאלי", "female": "סוציאלית"},
    "discipline": "משמעת",
    "alertness": "ערנות",
    "empathy": {"male": "אמפתי", "female": "אמפתית"},
    "creativity": {"male": "יצירתי", "female": "יצירתית"},
    "discretion": "שיקול דעת",
    "motivation": "עם מוטיבציה גבוהה",
    "decision_making": "קבלת החלטות",
    "attention_to_detail": "שימת לב לפרטים",
    "technical_aptitude": "יכולת טכנית",
    "robotics": "רובוטיקה",
    "instruction": "הדרכה",
    "information_technology": "טכנולוגיות מידע",
    "drone_operation": "הפעלת רחפנים",
    "aerial_navigation": "ניווט אווירי",
    "electronic_warfare": "לוחמה אלקטרונית",
    "systems_operation": "הפעלה טכנולוגית",
    "networking": "רשתות מחשבים",
    "erp_systems": "מערכות ERP",
    "data_management": "ניהול נתונים",
    "simulation_systems": "מערכות סימולציה",
    "logistics_management": "ניהול לוגיסטיקה",
    "supply_chain": "שרשרת אספקה",
    "intelligence_analysis": "ניתוח מודיעין",
    "data_processing": "עיבוד נתונים",
    "weapon_handling": "שימוש בנשק",
    "field_navigation": "ניווט שטח",
    "first_aid": "עזרה ראשונה",
    "emergency_response": "תגובה למצבי חירום",
    "radar_operation": "הפעלת מכ״ם",
    "systems_maintenance": "תחזוקת מערכות",
    "safety_management": "ניהול בטיחות",
    "vehicle_operation": "תפעול רכב",
    "human_resources": "משאבי אנוש",
    "administration": "ניהול אדמיניסטרטיבי",
    "event_planning": "תכנון אירועים",
    "coordination": "תיאום",
    "nbc_protection": "הגנה אב״כית",
    "education": "חינוך",
    "program_management": "ניהול תוכניות",
    "corrections_management": "ניהול כליאה",
    "inventory_management": "ניהול מלאי",
    "cooking": "בישול",
    "kitchen_management": "ניהול מטבח",
    "equipment_testing": "בדיקת ציוד",
    "ammunition_testing": "בדיקת תחמושת",
    "safety_protocols": "נהלי בטיחות",
    "monitoring": "ניטור",
    "naval_control_systems": "מערכות שליטה ימית",
    "maintenance_management": "ניהול תחזוקה",
    "technology": "טכנולוגיה",
    "project_management": "ניהול פרויקטים",
    "strategy": "אסטרטגיה",
    "operational_planning": "תכנון מבצעי",
    "cultural_awareness": "הבנה תרבותית",
    "logistics": "לוגיסטיקה",
    "electronics": "אלקטרוניקה",
    "tech-savvy": {"male": "טכנולוגי", "female": "טכנולוגית"},
    "computer literate": {"male": "בעל אוריינות מחשבית", "female": "בעלת אוריינות מחשבית"},
    "electronics enthusiast": {"male": "חובב אלקטרוניקה", "female": "חובבת אלקטרוניקה"},
    "analytical": {"male": "אנליטי", "female": "אנליטית"},
    "problem solver": "פתרון בעיות",
    "curious": {"male": "סקרן", "female": "סקרנית"},
    "creative": {"male": "יצירתי", "female": "יצירתית"},
    "leader": {"male": "מנהיג", "female": "מנהיגה"},
    "responsible": {"male": "אחראי", "female": "אחראית"},
    "team player": {"male": "שחקן צוות", "female": "שחקנית צוות"},
    "independent": {"male": "עצמאי", "female": "עצמאית"},
    "organized": {"male": "מאורגן", "female": "מאורגנת"},
    "patient": {"male": "סבלני", "female": "סבלנית"},
    "communicative": {"male": "תקשורתי", "female": "תקשורתית"},
    "empathetic": {"male": "אמפתי", "female": "אמפתית"},
    "disciplined": {"male": "בעל משמעת עצמית", "female": "בעלת משמעת עצמית"},
    "resilient": {"male": "חסין", "female": "חסינה"},
    "detail-oriented": {"male": "שם לב לפרטים", "female": "שמה לב לפרטים"},
    "focused": {"male": "מרוכז", "female": "מרוכזת"},
    "adaptable": {"male": "בעל יכולת הסתגלות", "female": "בעלת יכולת הסתגלות"},
    "cyber_security": "חוש לאבטחת מידע",
    "communication_systems": "ידע במערכות תקשורת חברתיות",
    "signal_analysis": "ניתוח אותות",
    "caring person": {"male": "אכפתי", "female": "אכפתית"},
    "sensitive": {"male": "רגיש", "female": "רגישה"},
    "initiative": {"male": "יוזם", "female": "יוזמת"},
    "resilience": "חוסן מנטלי",
    "language interpretation": "חוש לקליטת שפות",
    "visual_intelligence": "מודיעין חזותי",
    "data_analysis": "ניתוח נתונים",
    "air_defense_systems": {"male": "מתאים לעבודה עם מערכות הגנה", "female": "מתאימה לעבודה עם מערכות הגנה"},
    "naval_operations": "פעולות ימית",
    "weapons_handling": "ידע בשימוש בנשק",
    "tactical_training": "ידע בהדרכה טקטית",
    "navigation_systems": "מערכות ניווט"
    }

def normalize(term: str) -> str:
    return term.strip().lower().replace("-", "_").replace(" ", "_")

def smart_translate(key: str, original: str) -> str:
    """Fallback אוטומטי לתרגום ושמירת מונחים חסרים לקובץ"""
    try:
        translated = GoogleTranslator(source='auto', target='he').translate(original)
        print(f"🔁 תרגום אוטומטי: '{original}' → '{translated}'")
        return translated
    except Exception as e:
        print(f"⚠️ שגיאה בתרגום אוטומטי עבור '{original}': {e}")
        return original

def is_hebrew(text: str) -> bool:
    return any("\u0590" <= c <= "\u05EA" for c in text)

def translate_list(items: list[str], gender: str = "male") -> list[str]:
    result = []
    for item in items:
        key = normalize(item)
        translated_entry = TRANSLATION_MAP.get(key)

        if isinstance(translated_entry, dict):
            translated = translated_entry.get(gender) or translated_entry.get("male")
        else:
            translated = translated_entry

        if not translated:
            print(f"⚠️ לא נמצא תרגום עבור: '{item}' (normalized: '{key}')")
        result.append(translated or item)
    return result
