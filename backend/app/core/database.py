import datetime
import uuid
from enum import Enum
from typing import List, Optional, Any, Dict
from sqlalchemy import ForeignKey, String, Text, DateTime, func, create_engine, JSON, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from core.config import Config

class Status(Enum):
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4

class AgentType(Enum):
    CODE_REVIEW = 1
    DEPENDENCY_SECURITY = 2
    CICD_ANALYZER = 3
    LOGS = 4

class OutcomeStatus(Enum):
    PROPOSED = 1
    APPLIED = 2
    VALIDATED = 3
    REJECTED = 4

engine = create_engine(str(Config.DB_URL), echo=True)

class Base(DeclarativeBase):
    pass

class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(10))
    uuid_val: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True, nullable=False)
    status: Mapped[Status] = mapped_column(default=Status.PENDING, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)


class AgentFinding(Base):
    __tablename__ = "agent_findings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid_val: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True, nullable=False)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployments.id"), nullable=False)
    agent_type: Mapped[AgentType] = mapped_column(default=AgentType.CODE_REVIEW, nullable=False)
    find_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class Outcome(Base):
    __tablename__ = "outcomes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid_val: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True, nullable=False)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployments.id"), nullable=False)
    root_cause: Mapped[str] = mapped_column(String(50))
    suggested_fix: Mapped[str] = mapped_column(String(50))
    status: Mapped[OutcomeStatus] = mapped_column(default=OutcomeStatus.PROPOSED, nullable=False)


#Base.metadata.create_all(engine)