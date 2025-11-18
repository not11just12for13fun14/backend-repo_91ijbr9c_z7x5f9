import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Appointment, ContactMessage

app = FastAPI(title="Vet Clinic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Vet Clinic API is running"}


# Health and DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# -------- API Models for responses --------
class AppointmentResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]
    pet_name: str
    pet_type: str
    preferred_date: str
    message: Optional[str]
    status: str
    created_at: Optional[str] = None


class ContactMessageResponse(BaseModel):
    id: str
    name: str
    email: str
    message: str
    created_at: Optional[str] = None


# -------- Appointment Endpoints --------
@app.post("/api/appointments", response_model=dict)
async def create_appointment(payload: Appointment):
    try:
        inserted_id = create_document("appointment", payload)
        return {"id": inserted_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/appointments", response_model=List[AppointmentResponse])
async def list_appointments(limit: int = 20):
    try:
        docs = get_documents("appointment", limit=limit)
        normalized = []
        for d in docs:
            normalized.append(
                {
                    "id": str(d.get("_id")),
                    "name": d.get("name"),
                    "email": d.get("email"),
                    "phone": d.get("phone"),
                    "pet_name": d.get("pet_name"),
                    "pet_type": d.get("pet_type"),
                    "preferred_date": d.get("preferred_date").isoformat() if d.get("preferred_date") else None,
                    "message": d.get("message"),
                    "status": d.get("status", "requested"),
                    "created_at": d.get("created_at").isoformat() if d.get("created_at") else None,
                }
            )
        return normalized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------- Contact Endpoints --------
@app.post("/api/contact", response_model=dict)
async def send_contact_message(payload: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", payload)
        return {"id": inserted_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the Vet Clinic backend API!"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
