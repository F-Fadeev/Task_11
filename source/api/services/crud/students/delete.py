from sqlalchemy import delete
from sqlalchemy.orm import Session

from source.api.services.crud.base_crud import BaseServices, Model


class DeleteStudentService(BaseServices):
    def __init__(self, db: Session, model: Model, id_student: int):
        super().__init__(db, model)
        self.id_student = id_student

    def _validate(self) -> None:
        pass

    def _execute(self):
        data = delete(self.model).where(self.model.id == self.id_student)
        self.db.execute(data)
        self.db.commit()


