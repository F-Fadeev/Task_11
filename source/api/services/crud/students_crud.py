
from sqlalchemy import select, and_

from source.api.schemas.students_schemas import StudentFilters
from source.api.services.crud.base_crud import BaseServices
from source.db.models import Course


class StudentService(BaseServices):
    def get_students(self, filter_param: StudentFilters):
        filters = filter_param.dict(exclude_none=True)
        query = select(self.model)
        if filters:
            query_filter = []
            if filters.get('first_name'):
                query_filter.append(self.model.first_name.ilike(f'%{filters["first_name"]}%'))
            if filters.get('last_name'):
                query_filter.append(self.model.last_name.ilike(f'%{filters["last_name"]}%'))
            if filters.get('middle_name'):
                query_filter.append(self.model.middle_name.ilike(f'%{filters["middle_name"]}%'))
            if filters.get('group_id'):
                query_filter.append(self.model.group_id == filters['group_id'])
            if filters.get('course_id'):
                query_filter.append(Course.id == filters['course_id'])
            query = query.filter(and_(*query_filter))
        return self.db.execute(query).scalars().all()
