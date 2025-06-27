from typing import List, Optional, Union
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from langchain_core.messages import BaseMessage

Base = declarative_base()

class AgentState(BaseModel):
    input: str
    messages: List[BaseMessage] = []
    response: Optional[str] = None
    thread_id: Optional[Union[int, str]] = None
    faq: Optional[dict] = None
    needs_clarify: bool = False
    attempts: int = 0

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(30), unique=True, nullable=False)
    level = Column(Integer, default=1)

    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Text, primary_key=True, autoincrement=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "user" o "bot"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String(20), default="text")  # texto, imagen, etc.

    conversation = relationship("Conversation", back_populates="messages")

class AlarmModel(Base):
    __tablename__ = "alarm_models"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    faqs = relationship("Faq", back_populates="alarm")


class Faq(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alarm_id = Column(Integer, ForeignKey("alarm_models.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    link = Column(String(255), nullable=True)

    alarm = relationship("AlarmModel", back_populates="faqs")

class UserFaq(Base):
    __tablename__ = "user_faqs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    faq_id = Column(Integer, ForeignKey("faqs.id"), nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    is_done = Column(Boolean, default=False)

    user = relationship("User")
    faq = relationship("Faq")