from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from source.api.schemas.students_schemas import StudentFilters
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import Course


class GetFilteredStudentsService(BaseServices):
    def __init__(self, db: Session, model: Model, filter_param: StudentFilters):
        super().__init__(db, model)
        self.filter_param = filter_param

    def _validate(self) -> None:
        pass

    def _execute(self) -> Any:
        filters = self.filter_param.dict(exclude_none=True)
        query = select(self.model)
        if filters:
            query_filter = []
            for key in filters:
                if key in {'first_name', 'last_name', 'middle_name'}:
                    query_filter.append(getattr(self.model, key).ilike(f'%{filters[key]}%'))
                elif key == 'group_id':
                    query_filter.append(self.model.group_id == filters[key])
                elif key == 'course_id':
                    query_filter.append(self.model.courses.any(Course.id == filters[key]))
            query = query.filter(and_(*query_filter))
        return self.db.execute(query).scalars().all()


class GetSpecificStudentService(BaseServices):
    def __init__(self, db: Session, model: Model, student_id: int):
        super().__init__(db, model)
        self.student_id = student_id

    def _validate(self) -> None:
        pass

    def _execute(self) -> Any:
        query = select(self.model).where(self.model.id == self.student_id)
        return self.db.execute(query).scalars().first()


