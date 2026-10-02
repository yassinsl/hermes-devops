from fastapi import FastAPI
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel


class DeploymentCreate(BaseModel):
    trigger_source: str


class DeploymentRead(BaseModel):
    id: UUID
    trigger_source: str
    status: str
    created_at: datetime
    finished_at: datetime | None = None


app = FastAPI()


@app.post("/deployments/", status_code=201)
async def create_deployment(payload: DeploymentCreate) -> DeploymentRead:
    """
    Register a new deployment.

    Args:
        payload (DeploymentCreate): request body containing trigger_source.

    Returns:
        DeploymentRead: the created deployment, with a generated id.
    """
    return DeploymentRead(
        id=uuid4(),
        trigger_source=payload.trigger_source,
        status="pending",
        created_at=datetime.now(timezone.utc),
        finished_at=None,
    )