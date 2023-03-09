from sqlalchemy import insert
from random import choice, randint

from source.db.database import session
from source.db.models import Student, Group, Course
from db_upload.school_data import first_names, last_names, middle_names, groups, courses


def load_data() -> None:
    s = session()
    if s:
        try:
            data = insert(Group).values([{'name': value} for value in groups])
            result = s.execute(data)
            if result.rowcount == len(groups):
                s.commit()
            else:
                raise Exception('Failed to insert groups.')

            data = insert(Student).values([{'group_id': randint(1, 10), 'first_name': choice(first_names),
                     'last_name': choice(last_names), 'middle_name': choice(middle_names)}
                    for _ in range(200)])
            s.execute(data)
            s.commit()

            data = insert(Course).values([{'name': value} for value in courses])
            s.execute(data)
            s.commit()

            db_courses = s.query(Course).all()
            db_students = s.query(Student).all()
            for student in db_students:
                student.courses.extend(list({db_courses[randint(0, len(db_courses) - 1)]
                                                 for _ in range(randint(1, 6))}))
            s.commit()
        except Exception:
            s.rollback()
        finally:
            s.close()
    else:
        raise Exception('Unable to create session.')


if __name__ == '__main__':
    load_data()
