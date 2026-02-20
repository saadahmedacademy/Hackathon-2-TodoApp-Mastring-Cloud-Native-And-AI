from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from sqlmodel import Session, select, SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: Session):
        self.model = model
        self.session = session

    def create(self, obj_in: ModelType) -> ModelType:
        self.session.add(obj_in)
        self.session.flush()
        self.session.refresh(obj_in)
        return obj_in

    def get(self, id: UUID) -> Optional[ModelType]:
        return self.session.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, db_obj: ModelType) -> ModelType:
        self.session.add(db_obj)
        self.session.flush()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: UUID) -> Optional[ModelType]:
        obj = self.session.get(self.model, id)
        if obj:
            self.session.delete(obj)
            self.session.flush()
        return obj
