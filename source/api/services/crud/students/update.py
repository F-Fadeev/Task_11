from typing import Any

from sqlalchemy import update
from sqlalchemy.orm import Session

from source.api.schemas.students_schemas import StudentUpdateScheme
from source.api.services.crud.base_crud import BaseServices, Model


class UpdateStudentService(BaseServices):
    def __init__(self, db: Session, model: Model, scheme: StudentUpdateScheme, return_values: list, id_student: int):
        super().__init__(db, model)
        self.scheme = scheme
        self.return_values = return_values
        self.id_student = id_student

    def _validate(self) -> None:
        pass

    def _execute(self) -> Any:
        fields = [getattr(self.model, value) for value in self.return_values]
        scheme = self.scheme.dict(exclude_none=True)
        if scheme:
            data = update(self.model).where(self.model.id == self.id_student).values(**scheme).returning(*fields)
            result = self.db.execute(data).one()
            self.db.commit()
            return result
