from fastapi import HTTPException, status
from sqlalchemy import select, func

from source.api.schemas.students_schemas import StudentsIdsScheme
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import association_table


class CoursesService(BaseServices):
    def enroll_students(self, id_students: StudentsIdsScheme, id_course: int, student_model: Model) -> dict:
        course_data = self.db.query(self.model).filter_by(id=id_course).one_or_none()
        if not course_data:
            raise HTTPException(
                detail="Course don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        enrolled_students = {student.id for student in course_data.students}
        new_students = set(id_students.student_ids).difference(enrolled_students)
        if not new_students:
            raise HTTPException(
                detail='Students already enrolled',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        students_data = self.db.query(student_model).filter(student_model.id.in_(new_students))
        if len(students_data.all()) != len(new_students):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        course_data.students.extend(students_data)
        self.db.commit()
        return {'detail': 'Successful'}

    def expel_students(self, id_students: StudentsIdsScheme, id_course: int, student_model: Model) -> None:
        course_data = self.db.query(self.model).filter_by(id=id_course).one_or_none()
        if not course_data:
            raise HTTPException(
                detail="Course don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        check_students = self.db.query(student_model).filter(student_model.id.in_(id_students.student_ids))
        if len(check_students.all()) != len(id_students.student_ids):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        enrolled_students = {student.id for student in course_data.students}
        updated_enrolled_students = enrolled_students.difference(set(id_students.student_ids))
        if len(updated_enrolled_students) == len(enrolled_students):
            raise HTTPException(
                detail='These students are not enrolled in this course anyway',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        students_data = self.db.query(student_model).filter(student_model.id.in_(updated_enrolled_students)).all()
        course_data.students = students_data
        self.db.commit()
        return

    def get_courses(self, count_students: int):
        query = select(self.model)
        if count_students:
            filter_ = (
                select(association_table.c.course_id)
                .having(func.count(association_table.c.students_id) <= count_students)
                .group_by(association_table.c.course_id)
            )
            query = select(self.model).filter(self.model.id.in_(filter_))
        return self.db.execute(query).scalars().all()


