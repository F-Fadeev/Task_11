from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from source.api.schemas.base_schemas import (
    ErrorResponseScheme,
    DefaultResponseScheme,
)
from source.api.services.utils import get_db
from source.api.services.crud.groups_crud import GroupsService
from source.api.schemas.groups_schemas import (
    GroupScheme,
    GroupCreateScheme,
    GroupUpdateScheme,
)
from source.api.schemas.students_schemas import StudentsIdsScheme
from source.db.models import (
    Group,
    Student,
)


groups_router = APIRouter(prefix='/api/groups', tags=['Groups'])


@groups_router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[GroupScheme],
)
def get_all_groups(
        count_students: int = None,
        db: Session = Depends(get_db),
) -> list[GroupScheme]:
    return GroupsService(
        db=db,
        model=Group,
    ).get_groups(
        count_students=count_students,
    )


@groups_router.get(
    '/{group_id}',
    status_code=status.HTTP_200_OK,
    response_model=GroupScheme,
)
def get_specific_group(
        group_id: int,
        db: Session = Depends(get_db),
) -> GroupScheme:
    return GroupsService(
        db=db,
        model=Group,
    ).get_data_id(
        data_id=group_id,
    )


@groups_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=GroupScheme,
)
def create_group(
        group: GroupCreateScheme,
        db: Session = Depends(get_db),
) -> GroupScheme:
    return GroupsService(
        db=db,
        model=Group,
    ).create(
        scheme=group,
        return_values=['id', 'name'],
    )


@groups_router.delete(
    '/delete/{id_group}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_group(
        id_group: int,
        db: Session = Depends(get_db),
) -> None:
    GroupsService(
        model=Group,
        db=db,
    ).delete(
        id_row=id_group,
    )
    return


@groups_router.put(
    '/update/{id_group}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=GroupScheme,
)
def update_group(
        id_group: int,
        scheme: GroupUpdateScheme,
        db: Session = Depends(get_db),
) -> None | GroupScheme:
    return GroupsService(
        model=Group,
        db=db,
    ).update(
        scheme=scheme,
        id_course=id_group,
        return_values=['id', 'name'],
    )


@groups_router.post(
    '/enroll/{id_group}',
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=DefaultResponseScheme,
)
def enrolling_students_to_group(
        id_group: int,
        id_students: StudentsIdsScheme,
        db: Session = Depends(get_db),
) -> dict:
    return GroupsService(
        db=db,
        model=Group,
    ).enroll_students(
        id_students=id_students,
        id_group=id_group,
        student_model=Student,
    )


@groups_router.delete(
    '/expel/{id_group}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponseScheme}},
    response_model=None,
)
def expel_students_from_group(
        id_group: int,
        id_students: StudentsIdsScheme,
        db: Session = Depends(get_db),
) -> None:
    return GroupsService(
        db=db,
        model=Group,
    ).expel_students(
        id_students=id_students,
        id_group=id_group,
        student_model=Student,
    )
