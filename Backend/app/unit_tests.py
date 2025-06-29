import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from bson import ObjectId
import app.services as services


@pytest.mark.asyncio
async def test_ai_recommend_returns_sorted_roles():
    profile = {
        "name": "דנה",
        "age": 19,
        "gender": "female",
        "physical_fitness": 5,
        "technical_skills": ["python", "electronics"],
        "personality_traits": ["analytical", "team_player"],
        "languages": ["עברית", "אנגלית"]
    }

    role_ids = [
        ObjectId("60c72b2f9e1d4f1f9c8e3e01"),
        ObjectId("60c72b2f9e1d4f1f9c8e3e02"),
        ObjectId("60c72b2f9e1d4f1f9c8e3e03"),
        ObjectId("60c72b2f9e1d4f1f9c8e3e04"),
    ]

    roles = [
        {
            "_id": role_ids[0],
            "name": "תפקיד 1",
            "description": "תיאור 1",
            "requirements": {},
            "traits": ["team_player", "analytical"],
            "fitness": 3,
            "skills": ["python"],
            "languages": [],
            "type": "טכנולוגי"
        },
        {
            "_id": role_ids[1],
            "name": "תפקיד 2",
            "description": "תיאור 2",
            "requirements": {},
            "traits": ["creative"],
            "fitness": 1,
            "skills": [],
            "languages": [],
            "type": "תומך לחימה"
        },
        {
            "_id": role_ids[2],
            "name": "תפקיד 3",
            "description": "תיאור 3",
            "requirements": {},
            "traits": ["analytical"],
            "fitness": 5,
            "skills": ["electronics"],
            "languages": [],
            "type": "טכנולוגי"
        },
        {
            "_id": role_ids[3],
            "name": "תפקיד 4",
            "description": "תיאור 4",
            "requirements": {},
            "traits": [],
            "fitness": 2,
            "skills": [],
            "languages": [],
            "type": "תומך לחימה"
        }
    ]

    llm_mock_response = {
        "choices": [{
            "message": {
                "content": f"""[
                    {{"role_id": "{str(role_ids[2])}", "score": 95}},
                    {{"role_id": "{str(role_ids[0])}", "score": 85}},
                    {{"role_id": "{str(role_ids[3])}", "score": 60}}
                ]"""
            }
        }]
    }

    with patch("app.services.get_all_roles", new=AsyncMock(return_value=roles)):
        with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
            mock_post.return_value.json = AsyncMock(return_value=llm_mock_response)
            mock_post.return_value.status_code = 200
            mock_post.return_value.raise_for_status = lambda: None

            mock_db = MagicMock()
            mock_db.roles.find_one = AsyncMock(
                side_effect=lambda q: next((r for r in roles if r["_id"] == q["_id"]), None)
            )

            result = await services.ai_recommend(profile, roles=None, db=mock_db)

            assert isinstance(result, list)
            assert len(result) == 3
            assert ObjectId(result[0]["role"]["_id"]) == role_ids[2]
            assert ObjectId(result[1]["role"]["_id"]) == role_ids[0]
            assert ObjectId(result[2]["role"]["_id"]) == role_ids[3]
