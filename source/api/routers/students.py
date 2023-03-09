from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session


from source.api.services.utils import get_db
from source.api.services.crud.students_crud import StudentService
from source.api.schemas.students_schemas import (
    StudentScheme,
    StudentCreateScheme,
    StudentUpdateScheme,
    StudentFilters,
)
from source.db.models import Student


students_router = APIRouter(prefix='/api/students', tags=['Students'])


@students_router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[StudentScheme],
)
def get_all_students(
        filter_param: StudentFilters = Depends(StudentFilters),
        db: Session = Depends(get_db),
) -> list[StudentScheme]:
    return StudentService(
        db=db,
        model=Student,
    ).get_students(
        filter_param=filter_param,
    )


@students_router.get(
    '/{student_id}',
    status_code=status.HTTP_200_OK,
    response_model=StudentScheme,
)
def get_specific_student(
        student_id: int,
        db: Session = Depends(get_db),
) -> StudentScheme:
    return StudentService(
        db=db,
        model=Student,
    ).get_data_id(
        data_id=student_id,
    )


@students_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=StudentScheme,
)
def create_student(
        student: StudentCreateScheme,
        db: Session = Depends(get_db),
) -> StudentScheme:
    return StudentService(
        db=db,
        model=Student,
    ).create(
        scheme=student,
        return_values=['id', 'group_id', 'first_name', 'last_name', 'middle_name'],
    )


@students_router.delete(
    '/delete/{id_student}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_student(
        id_student: int,
        db: Session = Depends(get_db),
) -> None:
    StudentService(
        model=Student,
        db=db,
    ).delete(
        id_row=id_student,
    )
    return


@students_router.put(
    '/update/{id_student}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=StudentScheme,
)
def update_student(
        id_student: int,
        scheme: StudentUpdateScheme,
        db: Session = Depends(get_db),
) -> None | StudentScheme:
    return StudentService(
        model=Student,
        db=db,
    ).update(
        scheme=scheme,
        id_course=id_student,
        return_values=['id', 'group_id', 'first_name', 'last_name', 'middle_name'],
    )
