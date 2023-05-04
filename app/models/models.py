from datetime import datetime, timezone
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer,String, Text
from sqlalchemy.orm import relationship
from ..database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    code = Column(String, index=True)
    title = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )

    diagnoses = relationship("Diagnosis", back_populates="category")


class Diagnosis(Base):
    __tablename__ = "diagnosis"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    diag_code = Column(String, unique=True, index=True)
    full_code = Column(String)
    abb_desc = Column(String)
    full_desc = Column(String)
    file_upload_id = Column(UUID(as_uuid=True), ForeignKey("file_uploads.id"), unique=True, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    category = relationship("Category", back_populates="diagnoses")
    file_upload = relationship("FileUpload", uselist=False, back_populates="diagnosis")


class FileUpload(Base):
    __tablename__ = "file_uploads"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    email_add = Column(String, index=True, nullable=False)
    file_name = Column(String)
    file_type = Column(String)
    first_content = Column(Text)
    last_content = Column(Text)
    file_path = Column(String)
    size = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )

    diagnosis = relationship("Diagnosis", back_populates="file_upload")
