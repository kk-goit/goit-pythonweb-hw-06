from faker import Faker
from random import randint

from connect import session
from models import Student, Group, Lecturer, Course, GradeBook

if __name__ == "__main__":
    fake = Faker()
    students = []

    for group in [
        Group(name="First group"),
        Group(name="Second group"),
        Group(name="Third group"),
    ]:
        for n in range(randint(10, 20)):
            students.append(Student(name=fake.name(), group=group))
        session.add(group)

    lecturers = []
    for n in range(randint(3, 5)):
        lecturers.append(Lecturer(name=f"{fake.prefix()} {fake.name_nonbinary()}"))
    session.add_all(lecturers)

    courses = []
    l_idx = -1
    l_idx_max = len(lecturers) - 1
    for n in range(randint(5, 8)):
        l_idx = l_idx + 1 if l_idx < l_idx_max else randint(0, l_idx_max)
        courses.append(Course(name=fake.job(), lecturer=lecturers[l_idx]))
    session.add_all(courses)

    for student in students:
        for cource in courses:
            for n in range(randint(0, 20)):
                session.add(
                    GradeBook(value=randint(2, 12), student=student, course=cource)
                )

    session.commit()
    session.close()
