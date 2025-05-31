class TextFile:
    def __init__(self, filename):
        self.filename = filename
        self.content = ""

    def write(self, data):
        self.content = data
        print(f"Файл {self.filename} обновлен.")

    def read(self):
        return f"Содержимое файла {self.filename}: {self.content}"


class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.data = None

    def write(self, data):
        self.data = data
        print(f"База данных {self.dbname} обновлена.")

    def read(self):
        return f"Данные из базы {self.dbname}: {self.data}"


class NetworkResource:
    def __init__(self, url):
        self.url = url
        self.request_data = None

    def write(self, data):
        self.request_data = data
        print(f"Отправка данных на {self.url}: {self.request_data}")

    def read(self):
        return f"Ответ с {self.url}: Данные получены."


#DON'T TOUCH UNDER THE LINE
#______________________________________________________________
def process_data(data_source, data=None):
    if data:
        data_source.write(data)
    return data_source.read()

text_file = TextFile("document.txt")
database = Database("users.db")
network = NetworkResource("http://example.com/api")

print(process_data(text_file, "Новый текст"))
print(process_data(database, {"name": "Иван", "age": 25}))
print(process_data(network, "POST data"))
