"""
1. Создать несколько объектов классов Player, Enemy и Item с разными параметрами
2. Реализовать и запустить игровой цикл, используя предоставленный шаблон
3. Добавить новый класс Boss, который наследуется от Enemy, но имеет специальные способности:
    Особая атака, наносящая больше урона
    Больше здоровья и возможность восстанавливать здоровье
    Способность вызывать союзников (генерировать новых врагов)

4. Проанализировать и объяснить, что произойдет, если изменить порядок наследования в классе Character с (GameObject, Movable) на (Movable, GameObject) и почему
"""

from abc import ABC, abstractmethod
import random

# Базовые абстрактные классы
class GameObject(ABC):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
    
    @abstractmethod
    def update(self):
        pass
    
    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y})"

class Movable(ABC):
    @abstractmethod
    def move(self, dx, dy):
        pass

# Наследники от базовых классов
class Character(GameObject, Movable):
    def __init__(self, x, y, name, health):
        super().__init__(x, y, name)
        self.health = health
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print(f"{self.name} moved to ({self.x}, {self.y})")
    
    def update(self):
        print(f"{self.name} updated, health: {self.health}")
    
    def is_alive(self):
        return self.health > 0

class Player(Character):
    def __init__(self, x, y, name, health, score=0):
        super().__init__(x, y, name, health)
        self.score = score
    
    def update(self):
        super().update()
        print(f"Player score: {self.score}")
    
    def collect_item(self, item):
        self.score += item.value
        print(f"Collected {item.name}, score: {self.score}")

class Enemy(Character):
    def __init__(self, x, y, name, health, damage):
        super().__init__(x, y, name, health)
        self.damage = damage
    
    def update(self):
        super().update()
        print(f"Enemy ready to attack with damage: {self.damage}")
    
    def attack(self, target):
        target.health -= self.damage
        print(f"{self.name} attacked {target.name} for {self.damage} damage")

class Item(GameObject):
    def __init__(self, x, y, name, value):
        super().__init__(x, y, name)
        self.value = value
    
    def update(self):
        print(f"Item {self.name} waiting to be collected")

class Boss(Enemy):
    def __init__(self, x, y, name, health, damage):
        super().__init__(x, y, name, health, damage)
        self.max_health = health

    def special_attack(self, target):
        special_damage = self.damage * 2
        target.health -= special_damage
        print(f"{self.name} использует особую атаку на {target.name} и наносит {special_damage} урона!")

    def heal(self):
        heal_amount = 10
        self.health = min(self.health + heal_amount, self.max_health)
        print(f"{self.name} восстанавливает {heal_amount} здоровья. Текущее здоровье: {self.health}")

    def summon_minion(self):
        minion = Enemy(self.x, self.y, "Миньон", health=15, damage=2)
        print(f"{self.name} призывает {minion.name}!")
        return minion

    def update(self):
        super().update()
        action = None
        if random.random() < 0.3:
            self.heal()
        if random.random() < 0.2:
            return self.summon_minion()
        if random.random() < 0.2:
            return "special_attack"
        return None

# Базовый игровой цикл
def game_loop(player, enemies, items, turns=5):
    print("\n=== GAME START ===\n")
    
    for turn in range(1, turns + 1):
        print(f"\n--- Turn {turn} ---")
        
        # Обновление всех объектов
        player.update()
        for enemy in enemies:
            enemy.update()
        for item in items:
            item.update()
        
        # Враги атакуют игрока
        for enemy in enemies:
            if enemy.is_alive():
                enemy.attack(player)
        
        # Проверка сбора предметов
        for item in items[:]:  # Копия списка для безопасного удаления
            if item.x == player.x and item.y == player.y:
                player.collect_item(item)
                items.remove(item)
        
        # Проверка состояния игрока
        if not player.is_alive():
            print("\nИгрок погиб! Игра окончена.")
            break
        
        # Движение игрока (для примера - случайное)
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        player.move(dx, dy)
    
    print("\n=== GAME END ===")
    print(f"Final score: {player.score}")
    print(f"Player health: {player.health}")

player = Player(0, 0, "Герой", health=100)

enemies = [
    Enemy(1, 0, "Скелет", health=30, damage=5),
    Enemy(0, 1, "Гоблин", health=20, damage=3),
    Boss(1, 1, "Дракон", health=150, damage=20)
]

items = [
    Item(0, 0, "Монета", value=10),
    Item(2, 2, "Зелье", value=20),
]

game_loop(player, enemies, items, turns=5)

"""
Character(GameObject, Movable), потому что GameObject содержит логику и данные (x, y, name), а Movable — только интерфейс (без данных).
"""