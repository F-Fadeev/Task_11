from abc import ABC
from typing import TypeVar


from sqlalchemy.orm import Session
from sqlalchemy import (
    insert,
    delete,
    update,
    select,
)


from source.db.models import (
    Student,
    Group,
    Course,
    association_table,
)


Model = TypeVar('Model', type[Student], type[Group], type[Course], type[association_table])


class BaseServices:
    def __init__(self, db: Session, model: Model):
        self.db = db
        self.model = model

    def get_all_data(self):
        query = select(self.model)
        return self.db.execute(query).scalars().all()

    def get_data_id(self, data_id: int):
        query = select(self.model).filter(self.model.id == data_id)
        return self.db.execute(query).scalars().first()

    def create(self, scheme, return_values: list):
        fields = [getattr(self.model, value) for value in return_values]
        data = insert(self.model).values(**scheme.dict()).returning(*fields)
        result = self.db.execute(data).one()
        self.db.commit()
        return result

    def delete(self, id_row: int):
        data = delete(self.model).where(self.model.id == id_row)
        self.db.execute(data)
        self.db.commit()

    def update(self, scheme, id_course: int, return_values: list):
        fields = [getattr(self.model, value) for value in return_values]
        scheme = scheme.dict(exclude_none=True)
        if scheme:
            data = update(self.model).where(self.model.id == id_course).values(**scheme).returning(*fields)
            result = self.db.execute(data).one()
            self.db.commit()
            return result
