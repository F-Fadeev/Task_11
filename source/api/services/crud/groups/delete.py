from sqlalchemy import delete
from sqlalchemy.orm import Session

from source.api.services.crud.base_crud import BaseServices, Model


class DeleteGroupService(BaseServices):
    def __init__(self, db: Session, model: Model, id_group: int):
        super().__init__(db, model)
        self.id_group = id_group

    def _validate(self):
        pass

    def _execute(self):
        data = delete(self.model).where(self.model.id == self.id_group)
        self.db.execute(data)
        self.db.commit()


