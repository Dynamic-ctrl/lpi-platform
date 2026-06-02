import uuid
from datetime import datetime, timezone
from fastapi import APIRouter

from lpi.models import Goal, GoalCreate, GoalUpdate

router = APIRouter()

# Our temporary database!
MOCK_DB = []

@router.post("/", response_model=Goal, status_code=201)
def create_goal(goal: GoalCreate) -> Goal:
    """Create a new goal with SMILE phase tracking."""
    # Convert the incoming GoalCreate payload into a full Goal model
    new_goal = Goal(
        id=str(uuid.uuid4()),
        user_id="seed_user",  # Hardcoded for now
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        title=goal.title,
        description=goal.description,
        priority=goal.priority,
        smile_phase=goal.smile_phase
    )
    MOCK_DB.append(new_goal)
    return new_goal


@router.get("/", response_model=list[Goal])
def list_goals(user_id: str | None = None) -> list[Goal]:
    """List goals, optionally filtered by user."""
    if user_id:
        return [g for g in MOCK_DB if g.user_id == user_id]
    return MOCK_DB


@router.get("/{goal_id}", response_model=Goal)
def get_goal(goal_id: str) -> Goal:
    """Get a specific goal."""
    raise NotImplementedError("Phase 2 task: Adil implements this")


@router.patch("/{goal_id}", response_model=Goal)
def update_goal(goal_id: str, update: GoalUpdate) -> Goal:
    """Update a goal (including SMILE phase transitions)."""
    raise NotImplementedError("Phase 2 task: Adil implements this")


@router.delete("/{goal_id}")
def delete_goal(goal_id: str) -> dict:
    """Delete a goal."""
    raise NotImplementedError("Phase 2 task: Adil implements this")