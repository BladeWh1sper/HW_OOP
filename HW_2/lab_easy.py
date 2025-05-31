class PersonalLibrary:
    def __init__(self):
        self.books = {}
        self.next_book_id = 1
        self.lending_history = {}
        self.borrowed_books = {}

    def add_book(self, title: str, author: str, year: int, genre: str) -> bool:
        book_id = self.next_book_id

        self.books[book_id] = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre
        }

        self.lending_history[book_id] = []
        self.next_book_id += 1

        return True

    def lend_book(self, book_id: int, borrower: str) -> bool:
        if book_id not in self.books or book_id in self.borrowed_books:
            return False
        
        self.borrowed_books[book_id] = borrower
        self.lending_history[book_id].append({"borrower": borrower, "action": "позаимствовано"})

        return True

    def return_book(self, book_id: int) -> bool:
        if book_id not in self.borrowed_books:
            return False
        
        borrower = self.borrowed_books.pop(book_id)
        self.lending_history[book_id].append({"borrower": borrower, "action": "возвращено"})

        return True

    def find_books(self, **criteria) -> list:
        result = []

        for book_id, book_data in self.books.items():
            match = True
            for key, value in criteria.items():
                if book_data.get(key) != value:
                    match = False
                    break
            
            if match:
                result.append({"book_id": book_id, **book_data})
        
        return result

    def get_lending_history(self, book_id: int) -> list:
        return self.lending_history.get(book_id, [])
    

if __name__ == "__main__":
    lib = PersonalLibrary()
    lib.add_book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман")
    lib.add_book("Война и мир", "Лев Толстой", 1869, "Роман")

    lib.lend_book(1, "Миша")
    lib.return_book(1)
    lib.lend_book(2, "Дима")

    print(lib.find_books(author="Михаил Булгаков"))
    print(lib.get_lending_history(1))