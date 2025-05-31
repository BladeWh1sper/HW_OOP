#include <iostream>
#include <vector>
#include <string>
#include <cassert>
#include <memory>
#include <sstream>

using namespace std;

class Printable {
public:
    virtual void print(const string& prefix = "", bool isLast = false) const = 0;
    virtual unique_ptr<Printable> clone() const = 0;
    virtual ~Printable() = default;
};

class Component : public Printable {
protected:
    int numeric_val;
public:
    Component(int numeric_val = 0) : numeric_val(numeric_val) {}
};

class Address : public Printable {
    string address;
public:
    Address(const string& addr) : address(addr) {}

    void print(const string& prefix = "", bool isLast = false) const override {
        cout << prefix << (isLast ? "\\-" : "+-") << address << endl;
    }

    unique_ptr<Printable> clone() const override {
        return make_unique<Address>(*this);
    }
};

class CPU : public Component {
    int cores;
    int mhz;
public:
    CPU(int cores, int mhz) : cores(cores), mhz(mhz) {}

    void print(const string& prefix = "", bool isLast = false) const override {
        cout << prefix << (isLast ? "\\-" : "+-") << "CPU, " << cores << " cores @ " << mhz << "MHz" << endl;
    }

    unique_ptr<Printable> clone() const override {
        return make_unique<CPU>(*this);
    }
};

class Memory : public Component {
public:
    Memory(int size) : Component(size) {}

    void print(const string& prefix = "", bool isLast = false) const override {
        cout << prefix << (isLast ? "\\-" : "+-") << "Memory, " << numeric_val << " MiB" << endl;
    }

    unique_ptr<Printable> clone() const override {
        return make_unique<Memory>(*this);
    }
};

class Disk : public Component {
public:
    enum Type { SSD, MAGNETIC };
private:
    Type storage_type;
    vector<pair<int, string>> partitions;
public:
    Disk(Type type, int size) : Component(size), storage_type(type) {}

    Disk& addPartition(int size, const string& name) {
        partitions.emplace_back(size, name);
        return *this;
    }

    void print(const string& prefix = "", bool isLast = false) const override {
        cout << prefix << (isLast ? "\\-" : "+-") << (storage_type == SSD ? "SSD" : "HDD") << ", " << numeric_val << " GiB" << endl;
        string child_prefix = prefix + (isLast ? "  " : "| ");
        for (size_t i = 0; i < partitions.size(); ++i) {
            bool last = (i == partitions.size() - 1);
            cout << child_prefix << (last ? "\\-" : "+-") << "[" << i << "]: " << partitions[i].first << " GiB, " << partitions[i].second << endl;
        }
    }

    unique_ptr<Printable> clone() const override {
        auto copy = make_unique<Disk>(storage_type, numeric_val);
        copy->partitions = partitions;
        return copy;
    }
};

class Computer : public Printable {
    string name;
public:
    vector<unique_ptr<Printable>> addresses;
    vector<unique_ptr<Printable>> components;

    Computer(const string& name) : name(name) {}

    Computer& addAddress(const string& addr) {
        addresses.emplace_back(make_unique<Address>(addr));
        return *this;
    }

    Computer& addComponent(unique_ptr<Printable> comp) {
        components.emplace_back(std::move(comp));
        return *this;
    }

    void print(const string& prefix = "", bool isLast = false) const override {
        cout << prefix << (isLast ? "\\-" : "+-") << "Host: " << name << endl;
        string child_prefix = prefix + (isLast ? "  " : "| ");
        vector<const Printable*> all;
        for (const auto& a : addresses) all.push_back(a.get());
        for (const auto& c : components) all.push_back(c.get());
        for (size_t i = 0; i < all.size(); ++i) {
            all[i]->print(child_prefix, i == all.size() - 1);
        }
    }

    unique_ptr<Printable> clone() const override {
        auto comp = make_unique<Computer>(name);
        for (const auto& a : addresses) comp->addresses.emplace_back(a->clone());
        for (const auto& c : components) comp->components.emplace_back(c->clone());
        return comp;
    }

    const string& getName() const { return name; }

    Computer* find(const string& target_name) {
        if (name == target_name) return this;
        return nullptr;
    }
};

class Network : public Printable {
    string name;
    vector<unique_ptr<Computer>> computers;
public:
    Network(const string& name) : name(name) {}

    Network& addComputer(unique_ptr<Computer> comp) {
        computers.emplace_back(std::move(comp));
        return *this;
    }

    Computer* findComputer(const string& target_name) {
        for (auto& c : computers) {
            if (auto res = c->find(target_name)) return res;
        }
        return nullptr;
    }

    void print(const string& prefix = "", bool isLast = false) const override {
        cout << "Network: " << name << endl;
        for (size_t i = 0; i < computers.size(); ++i) {
            computers[i]->print("", i == computers.size() - 1);
        }
    }

    unique_ptr<Printable> clone() const override {
        auto net = make_unique<Network>(name);
        for (const auto& c : computers) {
            net->addComputer(unique_ptr<Computer>(dynamic_cast<Computer*>(c->clone().release())));
        }
        return net;
    }
};

string capturePrint(const Printable& obj) {
    stringstream buffer;
    streambuf* oldCout = cout.rdbuf(buffer.rdbuf());
    obj.print();
    cout.rdbuf(oldCout);
    return buffer.str();
}

int main() {
    Network n("MISIS network");

    auto server1 = make_unique<Computer>("server1.misis.ru");
    server1->addAddress("192.168.1.1")
           .addComponent(make_unique<CPU>(4, 2500))
           .addComponent(make_unique<Memory>(16000));
    n.addComputer(std::move(server1));

    auto disk = make_unique<Disk>(Disk::MAGNETIC, 2000);
    disk->addPartition(500, "system").addPartition(1500, "data");

    auto server2 = make_unique<Computer>("server2.misis.ru");
    server2->addAddress("10.0.0.1")
           .addComponent(make_unique<CPU>(8, 3200))
           .addComponent(std::move(disk));
    n.addComputer(std::move(server2));

    cout << "=== Созданная сеть ===" << endl;
    n.print();

    string expected_output =
R"(Network: MISIS network
+-Host: server1.misis.ru
| +-192.168.1.1
| +-CPU, 4 cores @ 2500MHz
| \-Memory, 16000 MiB
\-Host: server2.misis.ru
  +-10.0.0.1
  +-CPU, 8 cores @ 3200MHz
  \-HDD, 2000 GiB
    +-[0]: 500 GiB, system
    \-[1]: 1500 GiB, data
)";

    string actual_output = capturePrint(n);
    assert(actual_output == expected_output && "Формат вывода не соответствует ожидаемому");
    cout << "✓ Тест формата вывода пройден" << endl;

    cout << "\n=== Тестирование глубокого копирования ===" << endl;
    auto x = n.clone();
    auto* cloned_network = dynamic_cast<Network*>(x.get());

    cout << "Поиск компьютера server2.misis.ru:" << endl;
    auto* c = cloned_network->findComputer("server2.misis.ru");
    assert(c != nullptr && "Компьютер server2.misis.ru не найден");
    cout << "✓ Найден" << endl;

    cout << "\nДобавляем SSD к найденному компьютеру в копии:" << endl;
    auto new_disk = make_unique<Disk>(Disk::SSD, 500);
    new_disk->addPartition(500, "fast_storage");
    c->addComponent(std::move(new_disk));

    cout << "\n=== Модифицированная копия ===" << endl;
    cloned_network->print();

    cout << "\n=== Исходная сеть (должна остаться неизменной) ===" << endl;
    n.print();

    cout << "\n=== Выполнение тестов ===" << endl;

    auto* server1_clone = cloned_network->findComputer("server1.misis.ru");
    assert(server1_clone != nullptr && "Компьютер server1.misis.ru не найден");
    cout << "✓ Тест поиска пройден" << endl;

    auto* original_server2 = n.findComputer("server2.misis.ru");
    auto* modified_server2 = cloned_network->findComputer("server2.misis.ru");
    int original_components = original_server2->components.size();
    int modified_components = modified_server2->components.size();

    assert(original_components == 2 && "Неверное количество компонентов в оригинале");
    assert(modified_components == 3 && "Неверное количество компонентов в копии");
    cout << "✓ Тест независимости копий пройден" << endl;

    auto disk1 = make_unique<Disk>(Disk::SSD, 256);
    auto disk2 = make_unique<Disk>(Disk::MAGNETIC, 1000);
    string disk1_out = capturePrint(*disk1);
    string disk2_out = capturePrint(*disk2);
    assert(disk1_out.find("SSD") != string::npos && "Неверный тип диска в выводе");
    assert(disk2_out.find("HDD") != string::npos && "Неверный тип диска в выводе");
    cout << "✓ Тест типов дисков пройден" << endl;

    cout << "\nВсе тесты пройдены!" << endl;

    return 0;
}
