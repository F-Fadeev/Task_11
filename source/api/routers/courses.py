from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session


from source.api.schemas.base_schemas import (
    DefaultResponseScheme,
    ErrorResponseScheme,
)
from source.api.services.utils import get_db
from source.api.services.crud.courses_crud import CoursesService
from source.api.schemas.courses_schemas import (
    CourseScheme,
    CourseCreateScheme,
    CourseUpdateScheme,
)
from source.api.schemas.students_schemas import StudentsIdsScheme
from source.db.models import (
    Course,
    Student,
)

courses_router = APIRouter(prefix='/api/courses', tags=['Courses'])


@courses_router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[CourseScheme],
)
def get_all_courses(
        count_students: int = None,
        db: Session = Depends(get_db),
) -> list[CourseScheme]:
    return CoursesService(
        db=db,
        model=Course,
    ).get_courses(
        count_students=count_students,
    )


@courses_router.get(
    '/{course_id}',
    status_code=status.HTTP_200_OK,
    response_model=CourseScheme,
)
def get_specific_course(
        course_id: int,
        db: Session = Depends(get_db),
) -> CourseScheme:
    return CoursesService(
        db=db,
        model=Course,
    ).get_data_id(
        data_id=course_id,
    )


@courses_router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=CourseScheme,
)
def create_course(
        scheme: CourseCreateScheme,
        db: Session = Depends(get_db),
) -> CourseScheme:
    return CoursesService(
        db=db,
        model=Course,
    ).create(
        scheme=scheme,
        return_values=['id', 'name', 'description'],
    )


@courses_router.delete(
    '/delete/{id_course}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_course(
        id_course: int,
        db: Session = Depends(get_db),
) -> None:
    CoursesService(
        db=db,
        model=Course,
    ).delete(
        id_row=id_course,
    )
    return


@courses_router.put(
    '/update/{id_course}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CourseScheme,
)
def update_course(
        id_course: int,
        scheme: CourseUpdateScheme,
        db: Session = Depends(get_db),
) -> None | CourseScheme:
    return CoursesService(
        model=Course,
        db=db,
    ).update(
        scheme=scheme,
        id_course=id_course,
        return_values=['id', 'name', 'description'],
    )


@courses_router.post(
    '/enroll/{id_course}',
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=DefaultResponseScheme,
)
def enrolling_students_to_course(
        id_course: int,
        id_students: StudentsIdsScheme,
        db: Session = Depends(get_db),
) -> dict:
    return CoursesService(
        db=db,
        model=Course,
    ).enroll_students(
        id_students=id_students,
        id_course=id_course,
        student_model=Student,
    )


@courses_router.delete(
    '/expel/{id_course}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=None,
)
def expel_students_from_course(
        id_course: int,
        id_students: StudentsIdsScheme,
        db: Session = Depends(get_db),
) -> None:
    return CoursesService(
        db=db,
        model=Course,
    ).expel_students(
        id_students=id_students,
        id_course=id_course,
        student_model=Student,
    )
