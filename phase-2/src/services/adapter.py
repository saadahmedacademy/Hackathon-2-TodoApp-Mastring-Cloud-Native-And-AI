"""Adapter pattern to reuse Phase-I domain logic in Phase-II backend."""
import sys
import os
# Add the phase-1 directory to the Python path to import Phase-I modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'phase-1'))

from src.services.todo_service import TodoService as PhaseOneTodoService
from src.models.todo import TodoItem as PhaseOneTodoItem
from ..models.todo import Todo as PhaseTwoTodo, TodoCreate, TodoUpdate


class TodoAdapter:
    """Adapter to convert between Phase-I domain objects and Phase-II database models."""

    @staticmethod
    def phase_one_to_phase_two(phase_one_todo: PhaseOneTodoItem) -> PhaseTwoTodo:
        """Convert Phase-I TodoItem to Phase-II Todo model."""
        # Import here to avoid circular imports
        from ..models.todo import Todo
        return Todo(
            id=phase_one_todo.id,
            user_id="",  # Will be set when saving to database
            title=phase_one_todo.title,
            description=phase_one_todo.description,
            completed=phase_one_todo.completed,
            created_at=None,  # Will be set by database
            updated_at=None   # Will be set by database
        )

    @staticmethod
    def phase_two_to_phase_one(phase_two_todo: PhaseTwoTodo) -> PhaseOneTodoItem:
        """Convert Phase-II Todo model to Phase-I TodoItem."""
        return PhaseOneTodoItem(
            id=phase_two_todo.id,
            title=phase_two_todo.title,
            description=phase_two_todo.description
        )

    @staticmethod
    def todo_create_to_phase_one(todo_create: TodoCreate) -> dict:
        """Convert Phase-II TodoCreate schema to Phase-I compatible format."""
        return {
            "title": todo_create.title,
            "description": todo_create.description
        }

    @staticmethod
    def todo_update_to_phase_one(todo_update: TodoUpdate) -> dict:
        """Convert Phase-II TodoUpdate schema to Phase-I compatible format."""
        result = {}
        if todo_update.title is not None:
            result["title"] = todo_update.title
        if todo_update.description is not None:
            result["description"] = todo_update.description
        if todo_update.completed is not None:
            result["completed"] = todo_update.completed
        return result