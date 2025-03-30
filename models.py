from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, PrimaryKeyConstraint, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), nullable=False
    )
    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[list["GradeBook"]] = relationship(
        cascade="all, delete", back_populates="student"
    )

    def __repr__(self) -> str:
        return f"Student:(id={self.id}, name={self.name})"


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    students: Mapped[list["Student"]] = relationship(
        cascade="all, delete", back_populates="group"
    )

    def __repr__(self) -> str:
        return f"Group:(id={self.id}, name={self.name})"


class Lecturer(Base):
    __tablename__ = "lecturers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    courses: Mapped[list["Course"]] = relationship(
        cascade="all, delete", back_populates="lecturer"
    )

    def __repr__(self) -> str:
        return f"Lecturer:(id={self.id}, name={self.name})"


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    lecturer_id: Mapped[int] = mapped_column(
        ForeignKey("lecturers.id", ondelete="CASCADE"), nullable=False
    )
    lecturer: Mapped["Lecturer"] = relationship(back_populates="courses")
    grades: Mapped[list["GradeBook"]] = relationship(
        cascade="all, delete", back_populates="course"
    )

    def __repr__(self) -> str:
        return f"Course:(id={self.id}, name={self.name})"


class GradeBook(Base):
    __tablename__ = "gradebooks"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    student: Mapped["Student"] = relationship(back_populates="grades")
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    course: Mapped["Course"] = relationship(back_populates="grades")
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )

    @validates
    def validate_value(self, key, value: int) -> int:
        if value < 1 or value > 12:
            raise ValueError("The grade value must by from 1 to 12")
        return value
