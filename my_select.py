from sqlalchemy import func, desc, and_
from sqlalchemy.sql import select

from connect import session
from models import Student, Group, Lecturer, Course, GradeBook


def prep_query_1(session, agg_func, agg_alias: str, course_name: str):
    """Prepared query for Students of some course with drades aggregation"""
    return (
        session.query(Student, agg_func(GradeBook.value).label(agg_alias))
        .select_from(Student)
        .join(Course, Course.name == course_name)
        .join(
            GradeBook,
            and_(Student.id == GradeBook.student_id, Course.id == GradeBook.course_id),
        )
    )


def prep_query_2(session, argument, lecturer_name: str):
    """Prepared query for Courses of the some lecturer"""
    return (
        session.query(argument)
        .select_from(Lecturer)
        .join(Course, Lecturer.id == Course.lecturer_id)
        .filter(Lecturer.name == lecturer_name)
    )


def select_1(session):
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    result = (
        session.query(Student, func.avg(GradeBook.value).label("grade_average"))
        .join(GradeBook, Student.id == GradeBook.student_id)
        .group_by(Student)
        .order_by(desc("grade_average"))
        .limit(5)
        .all()
    )
    print("\n1. 5 студентів із найбільшим середнім балом з усіх предметів:")
    for student, grade_average in result:
        print(f"\t{student} have grade average {grade_average:.2f}.")


def select_2(session, course_name: str):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    (student, grade_average) = (
        prep_query_1(session, func.avg, "grade_average", course_name)
        .group_by(Student)
        .order_by(desc("grade_average"))
        .limit(1)
        .one()
    )
    print(f"\n2. Студент із найвищим середнім балом з предмета '{course_name}':")
    print(f"\t{student} have grade average {grade_average:.2f}.")


def select_3(session, course_name: str):
    """Знайти середній бал у групах з певного предмета."""
    result = (
        session.query(Group, func.avg(GradeBook.value).label("grade_average"))
        .select_from(Course)
        .join(GradeBook, Course.id == GradeBook.course_id)
        .join(Student, GradeBook.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .filter(Course.name == course_name)
        .group_by(Group)
        .all()
    )
    print(f"\n3. Середній бал у групах з предмета '{course_name}':")
    for group, grade_average in result:
        print(f"\t{group} have grade average {grade_average:.2f}")


def select_4(session):
    """Знайти середній бал на потоці (по всій таблиці оцінок)"""
    grade_average = session.query(func.avg(GradeBook.value)).scalar()
    print(f"\n4. Середній бал на потоці (по всій таблиці оцінок): {grade_average:.2f}")


def select_5(session, lecturer_name: str):
    """Знайти які курси читає певний викладач."""
    result = prep_query_2(session, Course, lecturer_name).all()
    print(f"\n5. Викладач {lecturer_name} читає такі курси:")
    for course in result:
        print(f"\t{course}")


def select_6(session, group_name: str):
    """Знайти список студентів у певній групі."""
    result = (
        session.query(Student)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .all()
    )
    print(f"\n6. Список студентів у групі {group_name}:")
    for student in result:
        print(f"\t{student}")


def select_7(session, group_name: str, course_name: str):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    subq = session.query(Group.id).filter(Group.name == group_name).subquery()
    result = (
        prep_query_1(session, func.array_agg, "grades", course_name)
        .filter(Student.group_id.in_(select(subq)))
        .group_by(Student)
    )
    print(f"\n7. Оцінки студентів у групі '{group_name}' з предмета '{course_name}':")
    for student, grades in result:
        print(f"\t{student} have grades: {grades}.")


def select_8(session, lecturer_name: str):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    result = (
        session.query(func.avg(GradeBook.value))
        .select_from(Lecturer)
        .join(Course, Lecturer.id == Course.lecturer_id)
        .join(GradeBook, Course.id == GradeBook.course_id)
        .filter(Lecturer.name == lecturer_name)
        .scalar()
    )
    print(
        f"\n8. Середній бал, який ставить викладач '{lecturer_name}' зі своїх предметів - {result:.2f}"
    )


def select_9(session, student_name: str):
    """Знайти список курсів, які відвідує певний студент."""
    result = (
        session.query(Course)
        .select_from(Student)
        .join(GradeBook, Student.id == GradeBook.student_id)
        .join(Course, GradeBook.course_id == Course.id)
        .filter(Student.name == student_name)
        .all()
    )
    print(f"\n9. Список курсів, які відвідує студент {student_name}:")
    for course in result:
        print(f"\t{course}")


def select_10(session, student_name: str, lecturer_name: str):
    """Список курсів, які певному студенту читає певний викладач."""
    subq = prep_query_2(session, Course.id, lecturer_name).subquery()
    result = (
        session.query(Course)
        .select_from(Student)
        .join(GradeBook, Student.id == GradeBook.student_id)
        .join(Course, GradeBook.course_id == Course.id)
        .filter(Student.name == student_name)
        .filter(Course.id.in_(select(subq)))
        .all()
    )
    print(f"\n10. Список курсів, які студенту {student_name} читає {lecturer_name}:")
    for course in result:
        print(f"\t{course}")


if __name__ == "__main__":
    select_1(session)
    select_2(session, "Energy engineer")
    select_3(session, "Energy engineer")
    select_4(session)
    select_5(session, "Dr. Tammy Perez")
    select_6(session, "Second group")
    select_7(session, "Second group", "Energy engineer")
    select_8(session, "Dr. Tammy Perez")
    select_9(session, "Allison Mcdonald")
    select_10(session, "Allison Mcdonald", "Dr. Tammy Perez")
