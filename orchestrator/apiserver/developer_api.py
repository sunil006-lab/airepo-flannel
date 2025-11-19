from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
#from orchestrator.schema_model.models import Node, Workload, Event, HealthCheck, GPU, ResourceMetric, SecurityToken, Log, Registry, User, SchedulingQueue, MPod
#from orchestrator.db.databse_query import get_async_session
from orchestrator.models.core_models import Node, Workload, Event, MPod
from orchestrator.db.database_query import get_async_session
from orchestrator.schema_model.schema import NodeCreate, WorkloadCreate, EventCreate, MPODOut
from orchestrator.schema_model.schema import MPODCreate
from typing import List
#from orchestrator.models.schema_models import MPODOutist



app = FastAPI(title="OptiFlow Developer API")

# ----- NODE OPERATIONS -----
@app.post("/nodes/")
async def create_node(node: NodeCreate, session: AsyncSession = Depends(get_async_session)):
    new_node = Node(**node.dict())
    session.add(new_node)
    await session.commit()
    await session.refresh(new_node)
    return new_node

@app.get("/nodes/")
async def get_nodes(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Node))
    return result.scalars().all()

# ----- WORKLOAD OPERATIONS -----
@app.post("/workloads/")
async def create_workload(workload: WorkloadCreate, session: AsyncSession = Depends(get_async_session)):
    new_workload = Workload(**workload.dict())
    session.add(new_workload)
    await session.commit()
    await session.refresh(new_workload)
    return new_workload

@app.get("/workloads/")
async def get_workloads(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Workload))
    return result.scalars().all()


# ---------MPODS OPERATIONS------------
@app.get("/mpods/", response_model=List[MPODOut])
async def list_mpods(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(MPod))
    return result.scalars().all()

@app.post("/mpods/", response_model=MPODOut)
async def create_mpod(mpod: MPODCreate, session: AsyncSession = Depends(get_async_session)):
    new_mpod = MPod(**mpod.dict())
    session.add(new_mpod)
    await session.commit()
    await session.refresh(new_mpod)
    return new_mpod

@app.delete("/mpods/{mpod_id}", status_code=204)
async def delete_mpod(mpod_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(MPOD).where(MPOD.id == mpod_id))
    mpod = result.scalar_one_or_none()
    if mpod is None:
        raise HTTPException(status_code=404, detail="MPOD not found")
    await session.delete(mpod)
    await session.commit()

# ----- Health check Operations ------
@app.get("/health", tags=["Health Check"])
async def health_check():
    return JSONResponse(content={"status": "ok", "message": "Service is healthy"}, status_code=200)


# ----- EVENT OPERATIONS -----
@app.post("/events/")
async def create_event(event: EventCreate, session: AsyncSession = Depends(get_async_session)):
    new_event = Event(**event.dict())
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)
    return new_event

@app.get("/events/")
async def get_events(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Event))
    return result.scalars().all()

# Extend similarly for: HealthCheck, GPU, ResourceMetric, SecurityToken, Log, Registry, User, SchedulingQueue, MPod

# You can add GET/POST routes for each one like above.

# Placeholder: Health checks root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to OptiFlow Developer API"}

