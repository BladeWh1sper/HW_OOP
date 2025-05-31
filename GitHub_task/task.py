from abc import ABC, abstractmethod
from typing import List, Optional
import copy

class Printable(ABC):
    """Base abstract class for printable objects."""
    
    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        """Base printing method for the tree structure display.
        Implement properly to display hierarchical structure."""
        # To be implemented
        pass
        
    @abstractmethod
    def clone(self):
        """Create a deep copy of this object."""
        pass

class BasicCollection(Printable):
    """Base class for collections of items."""
    def __init__(self):
        self.items = []
    
    def add(self, elem):
        self.items.append(elem)
        return self
    
    def find(self, name):
        for item in self.items:
            if isinstance(item, Computer) and item.name == name:
                return item
            if isinstance(item, BasicCollection):
                found = item.find(name)
                if found:
                    return found
        return None


class Component(Printable):
    """Base class for computer components."""
    def __init__(self, numeric_val=0):
        self.numeric_val = numeric_val
        
    def clone(self):
        return copy.deepcopy(self)

class Address(Printable):
    """Class representing a network address."""
    def __init__(self, addr):
        self.address = addr
    
    # To be implemented
    def print_me(self, prefix="", is_last=False, no_slash=False, is_root=False) -> str:
        symbol = "\\-" if is_last else "+-"
        return f"{prefix}{symbol}{self.address}\n"

    
    def clone(self):
        return Address(self.address)

class Computer(BasicCollection, Component):
    """Class representing a computer with addresses and components."""
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.addresses = []
        self.components = []
    
    def add_address(self, addr):
        self.addresses.append(Address(addr))
        return self
    
    def add_component(self, comp):
        self.components.append(comp)
        return self
    
    def find(self, name):
        if self.name == name:
            return self
        for comp in self.components:
            if isinstance(comp, BasicCollection):
                found = comp.find(name)
                if found:
                    return found
        return None

    
    def print_me(self, prefix="", is_last=False, no_slash=False, is_root=False) -> str:
        symbol = "\\-" if is_last else "+-"
        result = f"{prefix}{symbol}Host: {self.name}\n"
        child_prefix = prefix + ("  " if is_last else "| ")
        total = self.addresses + self.components
        for i, item in enumerate(total):
            result += item.print_me(child_prefix, is_last=(i == len(total) - 1))
        return result

    def clone(self):
        new_comp = Computer(self.name)
        new_comp.addresses = [a.clone() for a in self.addresses]
        new_comp.components = [c.clone() for c in self.components]
        return new_comp

class Network(Printable):
    """Class representing a network of computers."""
    def __init__(self, name):
        self.name = name
        self.computers = []
    
    def add_computer(self, comp):
        self.computers.append(comp)
        return self
    
    def find_computer(self, name):
        for c in self.computers:
            found = c.find(name)
            if found:
                return found
        return None
    
    # Другие методы...
    def clone(self):
        new_net = Network(self.name)
        new_net.computers = [c.clone() for c in self.computers]
        return new_net
    
    def print_me(self, prefix="", is_last=False, no_slash=False, is_root=False) -> str:
        result = f"Network: {self.name}\n"
        for i, comp in enumerate(self.computers):
            result += comp.print_me("", is_last=(i == len(self.computers) - 1))
        return result

    def __str__(self):
        return self.print_me().strip()

class Disk(Component):
    """Disk component class with partitions."""
    # Определение типов дисков
    SSD = 0
    MAGNETIC = 1
    
    def __init__(self, storage_type, size):
        # Initialize properly
        super().__init__(size)
        self.storage_type = storage_type
        self.partitions = []
    
    def add_partition(self, size, name):
        self.partitions.append((size, name))
        return self
    
    def print_me(self, prefix="", is_last=False, no_slash=False, is_root=False) -> str:
        symbol = "\\-" if is_last else "+-"
        typ = "SSD" if self.storage_type == Disk.SSD else "HDD"
        result = f"{prefix}{symbol}{typ}, {self.numeric_val} GiB\n"
        child_prefix = prefix + ("  " if is_last else "| ")
        for i, part in enumerate(self.partitions):
            part_symbol = "\\-" if i == len(self.partitions) - 1 else "+-"
            result += f"{child_prefix}{part_symbol}[{i}]: {part[0]} GiB, {part[1]}\n"
        return result

    def clone(self):
        new_disk = Disk(self.storage_type, self.numeric_val)
        new_disk.partitions = copy.deepcopy(self.partitions)
        return new_disk
    
    def __str__(self):
        return self.print_me().strip()

class CPU(Component):
    """CPU component class."""
    def __init__(self, cores, mhz):
        super().__init__()
        self.cores = cores
        self.mhz = mhz
    
    def print_me(self, prefix="", is_last=False, no_slash=False, is_root=False) -> str:
        symbol = "\\-" if is_last else "+-"
        return f"{prefix}{symbol}CPU, {self.cores} cores @ {self.mhz}MHz\n"

    def clone(self):
        return CPU(self.cores, self.mhz)

class Memory(Component):
    """Memory component class."""
    def __init__(self, size):
        super().__init__(size)
        self.size = size
    
    def print_me(self, prefix="", is_last=False, no_slash=False, is_root=False) -> str:
        symbol = "\\-" if is_last else "+-"
        return f"{prefix}{symbol}Memory, {self.size} MiB\n"

    def clone(self):
        return Memory(self.size)

# Пример использования (может быть неполным или содержать ошибки)
def main():
    # Создание тестовой сети
    n = Network("MISIS network")
    
    # Добавляем первый сервер с одним CPU и памятью
    n.add_computer(
        Computer("server1.misis.ru")
        .add_address("192.168.1.1")
        .add_component(CPU(4, 2500))
        .add_component(Memory(16000))
    )
    
    # Добавляем второй сервер с CPU и HDD с разделами
    n.add_computer(
        Computer("server2.misis.ru")
        .add_address("10.0.0.1")
        .add_component(CPU(8, 3200))
        .add_component(
            Disk(Disk.MAGNETIC, 2000)
            .add_partition(500, "system")
            .add_partition(1500, "data")
        )
    )
    
    # Выводим сеть для проверки форматирования
    print("=== Созданная сеть ===")
    print(n)
    
    # Тест ожидаемого вывода
    expected_output = """Network: MISIS network
+-Host: server1.misis.ru
| +-192.168.1.1
| +-CPU, 4 cores @ 2500MHz
| \-Memory, 16000 MiB
\-Host: server2.misis.ru
  +-10.0.0.1
  +-CPU, 8 cores @ 3200MHz
  \-HDD, 2000 GiB
    +-[0]: 500 GiB, system
    \-[1]: 1500 GiB, data"""
    
    assert str(n) == expected_output, "Формат вывода не соответствует ожидаемому"
    print("✓ Тест формата вывода пройден")
    
    # Тестируем глубокое копирование
    print("\n=== Тестирование глубокого копирования ===")
    x = n.clone()
    
    # Тестируем поиск компьютера
    print("Поиск компьютера server2.misis.ru:")
    c = x.find_computer("server2.misis.ru")
    print(c)
    
    # Модифицируем найденный компьютер в копии
    print("\nДобавляем SSD к найденному компьютеру в копии:")
    c.add_component(
        Disk(Disk.SSD, 500)
        .add_partition(500, "fast_storage")
    )
    
    # Проверяем, что оригинал не изменился
    print("\n=== Модифицированная копия ===")
    print(x)
    print("\n=== Исходная сеть (должна остаться неизменной) ===")
    print(n)
    
    # Проверяем ассерты для тестирования системы
    print("\n=== Выполнение тестов ===")
    
    # Тест поиска
    assert x.find_computer("server1.misis.ru") is not None, "Компьютер не найден"
    print("✓ Тест поиска пройден")
    
    # Тест независимости копий
    original_server2 = n.find_computer("server2.misis.ru")
    modified_server2 = x.find_computer("server2.misis.ru")
    
    original_components = sum(1 for _ in original_server2.components)
    modified_components = sum(1 for _ in modified_server2.components)
    
    assert original_components == 2, f"Неверное количество компонентов в оригинале: {original_components}"
    assert modified_components == 3, f"Неверное количество компонентов в копии: {modified_components}"
    print("✓ Тест независимости копий пройден")
    
    # Проверка типов дисков
    disk_tests = [
        (Disk(Disk.SSD, 256), "SSD"),
        (Disk(Disk.MAGNETIC, 1000), "HDD")
    ]
    
    for disk, expected_type in disk_tests:
        assert expected_type in str(disk), f"Неверный тип диска в выводе: {str(disk)}"
    print("✓ Тест типов дисков пройден")
    
    print("\nВсе тесты пройдены!")

if __name__ == "__main__":
    main()