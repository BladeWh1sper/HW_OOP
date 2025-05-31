#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>

using namespace std;

class Student;
class Teacher;

class Course {
private:
    string name;
    int capacity;
    vector<string> requirements;
    vector<string> schedule;
    vector<Student*> students;

public:
    Course(const string& name, int capacity, const vector<string>& requirements = {})
        : name(name), capacity(capacity), requirements(requirements) {}

    void editCourse(const string& newName, int newCapacity) {
        if (!newName.empty()) name = newName;
        if (newCapacity > 0) capacity = newCapacity;
    }

    void setSchedule(const vector<string>& newSchedule) {
        schedule = newSchedule;
    }

    bool enrollStudent(Student* student);

    const string& getName() const { return name; }
    const vector<string>& getRequirements() const { return requirements; }
};

class Student {
private:
    string name;
    int studentId;
    vector<string> skills;
    vector<Course*> courses;
    map<string, vector<pair<string, double>>> grades;
    int warnings = 0;

public:
    Student(const string& name, int studentId) : name(name), studentId(studentId) {}

    void addSkill(const string& skill) {
        skills.push_back(skill);
    }

    bool checkRequirements(const vector<string>& reqs) {
        for (const auto& req : reqs) {
            if (find(skills.begin(), skills.end(), req) == skills.end()) {
                return false;
            }
        }
        return true;
    }

    void enroll(Course* course) {
        courses.push_back(course);
    }

    void addGrade(const string& courseName, const string& type, double value) {
        grades[courseName].emplace_back(type, value);
    }

    double calculateAverage(const string& courseName, bool& hasGrades) {
        hasGrades = false;
        if (grades.count(courseName)) {
            double total = 0;
            int count = 0;
            for (auto& g : grades[courseName]) {
                total += g.second;
                count++;
            }
            if (count > 0) {
                hasGrades = true;
                return total / count;
            }
        }
        return 0.0;
    }

    void checkAcademicStatus() {
        if (warnings >= 3) {
            cout << "Предупреждение: Студент " << name << " подлежит отчислению.\n";
        } else {
            cout << "Студент " << name << ": количество предупреждений " << warnings << ".\n";
        }
    }

    const string& getName() const { return name; }
};

bool Course::enrollStudent(Student* student) {
    if (students.size() < capacity && student->checkRequirements(requirements)) {
        students.push_back(student);
        student->enroll(this);
        return true;
    }
    return false;
}

class Teacher {
private:
    string name;
    int teacherId;
    vector<Course*> courses;

public:
    Teacher(const string& name, int teacherId) : name(name), teacherId(teacherId) {}

    void assignCourse(Course* course) {
        courses.push_back(course);
    }

    int getWorkload() const {
        return courses.size();
    }
};

class GradingSystem {
private:
    vector<tuple<string, string, string, double>> gradeHistory;

public:
    void addGrade(Student* student, Course* course, const string& type, double value) {
        student->addGrade(course->getName(), type, value);
        gradeHistory.emplace_back(student->getName(), course->getName(), type, value);
    }

    double calculateFinalGrade(Student* student, Course* course, bool& hasGrades) {
        return student->calculateAverage(course->getName(), hasGrades);
    }
};

int main() {
    Course math("Математика", 30, {"Базовые знания математики"});
    Student ivan("Иван Иванов", 101);
    Teacher petrov("Петр Петров", 201);

    ivan.addSkill("Базовые знания математики");

    petrov.assignCourse(&math);
    math.setSchedule({"Понедельник 10:00", "Среда 10:00"});

    if (math.enrollStudent(&ivan)) {
        cout << ivan.getName() << " успешно записан на курс " << math.getName() << ".\n";
    } else {
        cout << ivan.getName() << " не прошёл требования для курса " << math.getName() << ".\n";
    }

    GradingSystem gradingSystem;
    gradingSystem.addGrade(&ivan, &math, "Экзамен", 4.5);
    gradingSystem.addGrade(&ivan, &math, "Домашнее задание", 5.0);

    bool hasGrades = false;
    double final = gradingSystem.calculateFinalGrade(&ivan, &math, hasGrades);
    if (hasGrades) {
        cout << "Итоговая оценка: " << final << "\n";
    } else {
        cout << "Нет оценок для курса.\n";
    }

    return 0;
}
