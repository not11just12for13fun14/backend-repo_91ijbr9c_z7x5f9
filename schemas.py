"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

# ---- Vet Clinic App Schemas ----

class Appointment(BaseModel):
    """
    Appointments collection schema
    Collection name: "appointment"
    """
    name: str = Field(..., description="Client full name")
    email: EmailStr = Field(..., description="Client email address")
    phone: Optional[str] = Field(None, description="Client phone number")
    pet_name: str = Field(..., description="Pet name")
    pet_type: Literal["Dog", "Cat", "Bird", "Rabbit", "Other"] = Field(..., description="Type of pet")
    preferred_date: datetime = Field(..., description="Preferred appointment date/time (ISO 8601)")
    message: Optional[str] = Field(None, description="Additional details or concerns")
    status: Literal["requested", "confirmed", "completed", "cancelled"] = Field("requested", description="Appointment status")

class ContactMessage(BaseModel):
    """
    Contact messages collection schema
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    message: str = Field(..., min_length=5, max_length=1000, description="Message content")

# Example schemas retained for reference (not used by the app but available to the viewer):
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
