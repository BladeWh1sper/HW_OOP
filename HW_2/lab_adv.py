"""
Разработайте систему для управления учебным процессом с соблюдением принципов инкапсуляции. Система должна поддерживать работу с курсами, студентами, преподавателями и оценками.
Требования:

Управление курсами:

Создание и редактирование курсов
Установка требований для поступления
Ограничение по количеству студентов
Управление расписанием занятий


Управление студентами:

Регистрация и отчисление
Запись на курсы с проверкой требований
Отслеживание успеваемости
Система предупреждений об академических задолженностях


Управление преподавателями:

Назначение на курсы
Отслеживание нагрузки
Управление расписанием


Система оценивания:

Различные типы оценок (экзамены, проекты, домашние задания)
Расчет средних баллов
История изменений оценок
Автоматический расчет итоговых оценок
"""

from typing import List, Dict, Optional

class Course:
    def __init__(self, name: str, capacity: int, requirements: Optional[List[str]] = None):
        self.name = name
        self.capacity = capacity
        self.requirements = requirements or []
        self.schedule = []
        self.students = []

    def edit_course(self, name: Optional[str] = None, capacity: Optional[int] = None):
        if name:
            self.name = name
        if capacity:
            self.capacity = capacity

    def set_schedule(self, schedule: List[str]):
        self.schedule = schedule

    def enroll_student(self, student: "Student") -> bool:
        if len(self.students) < self.capacity and student.check_requirements(self.requirements):
            self.students.append(student)
            student.enroll(self)
            return True
        return False


class Student:
    def __init__(self, name: str, student_id: int):
        self.name = name
        self.student_id = student_id
        self.skills = []
        self.courses = []
        self.grades = {}
        self.warnings = 0

    def add_skill(self, skill: str):
        self.skills.append(skill)

    def check_requirements(self, requirements: List[str]) -> bool:
        return all(req in self.skills for req in requirements)

    def enroll(self, course: Course):
        self.courses.append(course)

    def add_grade(self, course: Course, grade_type: str, grade_value: float):
        if course.name not in self.grades:
            self.grades[course.name] = []
        self.grades[course.name].append({"type": grade_type, "value": grade_value})

    def calculate_average(self, course: Course) -> Optional[float]:
        grades = self.grades.get(course.name, [])
        if grades:
            return sum(g["value"] for g in grades) / len(grades)
        return None

    def check_academic_status(self):
        if self.warnings >= 3:
            print(f"Предупреждение: Студент {self.name} подлежит отчислению.")
        else:
            print(f"Студент {self.name}: количество предупреждений {self.warnings}.")


class Teacher:
    def __init__(self, name: str, teacher_id: int):
        self.name = name
        self.teacher_id = teacher_id
        self.courses = []

    def assign_course(self, course: Course):
        self.courses.append(course)

    def get_workload(self):
        return len(self.courses)


class GradingSystem:
    def __init__(self):
        self.grade_history = []

    def add_grade(self, student: Student, course: Course, grade_type: str, grade_value: float):
        student.add_grade(course, grade_type, grade_value)
        self.grade_history.append({
            "student": student.name,
            "course": course.name,
            "type": grade_type,
            "value": grade_value
        })

    def calculate_final_grades(self, student: Student, course: Course) -> Optional[float]:
        return student.calculate_average(course)


if __name__ == "__main__":
    course1 = Course("Математика", 30, ["Базовые знания математики"])
    student1 = Student("Иван Иванов", 101)
    teacher1 = Teacher("Петр Петров", 201)

    student1.add_skill("Базовые знания математики")

    teacher1.assign_course(course1)
    course1.set_schedule(["Понедельник 10:00", "Среда 10:00"])

    if course1.enroll_student(student1):
        print(f"{student1.name} успешно записан на курс {course1.name}")
    else:
        print(f"{student1.name} не прошёл требования для курса {course1.name}")

    grading_system = GradingSystem()
    grading_system.add_grade(student1, course1, "Экзамен", 4.5)
    grading_system.add_grade(student1, course1, "Домашнее задание", 5.0)

    final = grading_system.calculate_final_grades(student1, course1)
    print(f"Итоговая оценка: {final}")
