from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from starlette import status

from source.api.schemas.courses_schemas import CourseCreateScheme
from source.api.schemas.students_schemas import StudentsIdsScheme
from source.api.services.crud.base_crud import BaseServices, Model
from source.db.models import Student, association_table


class EnrolUserCourseService(BaseServices):

    def __init__(self, db: Session, model: Model, id_students: StudentsIdsScheme, id_course: int):

        super().__init__(db, model)
        self.id_students = id_students
        self.id_course = id_course

        self.enrolled_students = None

    def _validate(self) -> None:
        self.data = self._check_course(id_course=self.id_course)
        self._check_students()
        self.enrolled_students = self._check_updated_enrolled_students()

    def _execute(self) -> None:
        query = select(Student).filter(Student.id.in_(self.enrolled_students))
        students_data = self.db.execute(query).scalars().all()
        self.data.students = students_data
        self.db.commit()
        return

    def _check_course(self, id_course: int):
        query = select(self.model).filter_by(id=id_course)
        course_data = self.db.execute(query).scalar_one_or_none()
        if not course_data:
            raise HTTPException(
                detail="Course don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return course_data

    def _check_updated_enrolled_students(self) -> set:
        query = select(association_table).filter_by(course_id=self.id_course)
        enrolled_students = self.db.execute(query).scalars().all()
        updated_enrolled_students = set(enrolled_students).difference(self.id_students.student_ids)

        if len(updated_enrolled_students) == len(enrolled_students):
            raise HTTPException(
                detail='These students are not enrolled in this course anyway',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return updated_enrolled_students

    def _check_students(self) -> None:
        query = select(Student).filter(Student.id.in_(self.id_students.student_ids))
        check_students = self.db.execute(query).scalars().all()

        if len(check_students) != len(self.id_students.student_ids):
            raise HTTPException(
                detail="Some students don't found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class CreateCourseService(BaseServices):

    def __init__(self, db: Session, model: Model, return_values: list[str], scheme: CourseCreateScheme):
        super().__init__(db, model)
        self.return_values = return_values
        self.scheme = scheme

    def _validate(self) -> None:
        return

    def _execute(self):
        fields = [getattr(self.model, value) for value in self.return_values]
        data = insert(self.model).values(**self.scheme.dict()).returning(*fields)
        result = self.db.execute(data).one()
        self.db.commit()
        return result
