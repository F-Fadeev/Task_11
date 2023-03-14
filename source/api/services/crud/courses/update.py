from requests import Session
from sqlalchemy import update

from source.api.schemas.courses_schemas import CourseUpdateScheme
from source.api.services.crud.base_crud import BaseServices, Model


class UpdateCourseService(BaseServices):

    def __init__(
        self,
        db: Session,
        model: Model,
        return_values: list[str],
        scheme: CourseUpdateScheme,
        id_course: int,
    ) -> None:
        super().__init__(db, model)

        self.return_values = return_values
        self.scheme = scheme
        self.id_course = id_course

    def _validate(self) -> None:
        return

    def _execute(self):
        fields = [getattr(self.model, value) for value in self.return_values]
        scheme = self.scheme.dict(exclude_none=True)
        if not scheme:
            return

        data = update(self.model).where(self.model.id == self.id_course).values(**scheme).returning(*fields)
        result = self.db.execute(data).one()
        self.db.commit()
        return result
