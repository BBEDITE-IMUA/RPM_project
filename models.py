from sqlalchemy import Column, BigInteger, String, DateTime, func
from db import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(BigInteger, unique=True, index=True)
    language = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
