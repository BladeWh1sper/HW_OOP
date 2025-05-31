"""
Создайте следующую иерархию классов:

Animal (базовый класс)
    Mammal
        Dog
        Cat
        Horse
    Bird
        Eagle
        Penguin
    Reptile
        Snake
        Turtle
"""

class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass

class Cat(Mammal):
    pass

class Horse(Mammal):
    pass

class Bird(Animal):
    pass

class Eagle(Bird):
    pass

class Penguin(Bird):
    pass

class Reptile(Animal):
    pass

class Snake(Reptile):
    pass

class Turtle(Reptile):
    pass
