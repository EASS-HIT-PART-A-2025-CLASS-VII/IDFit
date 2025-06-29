from bson import ObjectId 
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Annotated
from fastapi import Form


class ProfileCreate(BaseModel):
    name: str = Field(..., description="שם המשתמש")
    age: int = Field(..., ge=0, description="גיל המשתמש")
    gender: str = Field(..., description="מין (זכר/נקבה)")
    physical_fitness: int = Field(..., ge=1, le=5, description="רמת כושר גופני (1-5)")
    technical_skills: List[str] = Field(default_factory=list, description="רשימת כישורים טכניים")
    personality_traits: List[str] = Field(default_factory=list, description="תכונות אופי")
    languages: List[str] = Field(default_factory=list, description="שפות")
    description: Optional[str] = Field(None, description="תיאור חופשי של המשתמש")


class RoleRequirements(BaseModel):
    fitness: Optional[int] = Field(None, description="כושר נדרש (1-100)")
    tech: List[str] = Field(default_factory=list, description="כישורים טכניים נדרשים")
    traits: List[str] = Field(default_factory=list, description="תכונות נדרשות")
    profile: Optional[int] = Field(None, description="פרופיל רפואי נדרש")
    dapar: Optional[int] = Field(None, description="דפ\"ר נדרש")
    kaba: Optional[int] = Field(None, description="קב\"א נדרש")


class Role(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    requirements: dict

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}  # ⬅️ המרה תקינה של ObjectId למחרוזת


class Recommendation(BaseModel):
    role: Role
    score: float = Field(..., ge=0, le=100)


class TraitRequest(BaseModel):
    text: str = Field(..., example="אני אוהב לעבוד בצוות ולעזור לאחרים")


class TraitResponse(BaseModel):
    traits: List[str] = Field(..., example=["team player", "empathetic", "supportive"])

class ContactForm(BaseModel):
    name: str
    age: int
    phone: str
    email: EmailStr
    message: str
