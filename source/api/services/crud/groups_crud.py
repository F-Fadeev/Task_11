from sqlalchemy import select, func

from source.api.schemas.students_schemas import StudentsIdsScheme
from source.db.models import Student
from source.api.services.crud.base_crud import BaseServices, Model
from fastapi import status, HTTPException



class GroupsService(BaseServices):
    def enroll_students(self, id_students: StudentsIdsScheme, id_group: int, student_model: Model) -> dict:
        group_data = self.db.query(self.model).filter_by(id=id_group).one_or_none()
        if not group_data:
            raise HTTPException(
                detail="Course don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        enrolled_students = {student.id for student in group_data.students}
        new_students = set(id_students.student_ids).difference(enrolled_students)
        if not new_students:
            raise HTTPException(
                detail='Students already in this group',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        students_data = self.db.query(student_model).filter(student_model.id.in_(new_students))
        if len(students_data.all()) != len(new_students):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        group_data.students.extend(students_data)
        self.db.commit()
        return {'detail': 'Successful'}

    def expel_students(self, id_students: StudentsIdsScheme, id_group: int, student_model: Model) -> None:
        group_data = self.db.query(self.model).filter_by(id=id_group).one_or_none()
        if not group_data:
            raise HTTPException(
                detail="Group don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        check_students = self.db.query(student_model).filter(student_model.id.in_(id_students.student_ids))
        if len(check_students.all()) != len(id_students.student_ids):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        enrolled_students = {student.id for student in group_data.students}
        updated_enrolled_students = enrolled_students.difference(set(id_students.student_ids))
        if len(updated_enrolled_students) == len(enrolled_students):
            raise HTTPException(
                detail='These students are not in this group anyway',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        students_data = self.db.query(student_model).filter(student_model.id.in_(updated_enrolled_students)).all()
        group_data.students = students_data
        self.db.commit()
        return

    def get_groups(self, count_students: int):
        if count_students:
            query = select(self.model) \
                .join(self.model.students) \
                .group_by(self.model.id) \
                .having(func.count(Student.id) <= count_students)
            return self.db.execute(query).scalars().all()
        query = select(self.model)
        return self.db.execute(query).scalars().all()

