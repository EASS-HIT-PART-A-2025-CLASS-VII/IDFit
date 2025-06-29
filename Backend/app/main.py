from fastapi import FastAPI, HTTPException, Request, Depends, APIRouter
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List
from .database import connect_to_mongo, close_mongo
from .repositories import load_profile, get_all_roles, save_profile, db as repos_db
from .services import ai_recommend, extract_traits_from_text, generate_profile_summary
from .schemas import Recommendation, Role, ProfileCreate, TraitRequest, TraitResponse, ContactForm
from fastapi.middleware.cors import CORSMiddleware
from .translations import translate_list
import json
import os
from .email import send_confirmation_email
from pathlib import Path

print("📁 CURRENT FILE PATH:", os.path.abspath(__file__))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo()

app = FastAPI(
    title="Role Matcher",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .config import settings
print("✅ Loaded API key:", settings.openrouter_api_key[:8], "...")

@app.get("/", tags=["health"])
def read_root():
    return {"message": "Hello, World!"}

@app.post("/profiles/", tags=["profiles"])
async def create_profile(p: ProfileCreate):
    profile_data = p.model_dump()

    if p.description and not p.personality_traits:
        try:
            traits = await extract_traits_from_text(p.description)
            profile_data["personality_traits"] = traits
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"שגיאה בחילוץ תכונות: {e}")

    try:
        profile_id = await save_profile(profile_data)
        return JSONResponse(content={"id": profile_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה בשמירת פרופיל: {e}")

debug_router = APIRouter()

@debug_router.get("/debug/roles/", tags=["debug"])
async def get_all_roles():
    roles = await repos_db.roles.find().to_list(length=100)
    return {"count": len(roles), "roles": roles}

@app.get("/profiles/{pid}/recommendations/", tags=["recommendations"])
async def recommendations(pid: str):
    profile = await load_profile(pid)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    roles = await get_all_roles()
    if not roles:
        raise HTTPException(status_code=500, detail="לא נמצאו תפקידים במסד הנתונים")

    try:
        raw_recs = await ai_recommend(profile, roles, db=repos_db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה בהמלצות AI: {e}")


    results = []
    for rec in raw_recs:
        role = rec["role"]

        # תרגום רק אחרי שההמלצה כבר בוצעה
        role["requirements"]["traits"] = translate_list(role["requirements"].get("traits", []))
        role["requirements"]["tech"] = translate_list(role["requirements"].get("tech", []))

        results.append({
            "score": rec["score"],
            "role": role
        })

    return {
        "summary": await generate_profile_summary(profile),
        "recommendations": results
    }


@app.post("/traits", response_model=TraitResponse, tags=["traits"])
async def get_traits(req: TraitRequest):
    try:
        traits = await extract_traits_from_text(req.text)
        return TraitResponse(traits=traits)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/debug/load_roles/", tags=["debug"])
async def load_roles_from_file(request: Request):
    try:
        path = Path(__file__).parent.parent / "roles.json"
        with open(path, encoding="utf-8") as f:
            roles = json.load(f)
        await repos_db.roles.delete_many({})
        await repos_db.roles.insert_many(roles)
        return {"status": "✅ roles loaded", "count": len(roles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה בטעינת roles.json: {e}")

@app.post("/contact/")
async def contact_submission(form: ContactForm):
    send_confirmation_email(to_email=form.email, user_name=form.name)
    return {"message": "פנייה התקבלה"}

app.include_router(debug_router)