#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

struct Book {
    string title;
    string author;
    int year;
    string genre;
};

struct LendingRecord {
    string borrower;
    string action;
};

class PersonalLibrary {
private:
    map<int, Book> books;
    map<int, vector<LendingRecord>> lending_history;
    map<int, string> borrowed_books;
    int next_book_id = 1;

public:
    bool add_book(const string& title, const string& author, int year, const string& genre) {
        Book book{title, author, year, genre};
        books[next_book_id] = book;
        lending_history[next_book_id] = {};
        next_book_id++;
        return true;
    }

    bool lend_book(int book_id, const string& borrower) {
        if (books.find(book_id) == books.end() || borrowed_books.find(book_id) != borrowed_books.end()) {
            return false;
        }
        borrowed_books[book_id] = borrower;
        lending_history[book_id].push_back({borrower, "позаимствовано"});
        return true;
    }

    bool return_book(int book_id) {
        auto it = borrowed_books.find(book_id);
        if (it == borrowed_books.end()) {
            return false;
        }
        string borrower = it->second;
        borrowed_books.erase(it);
        lending_history[book_id].push_back({borrower, "возвращено"});
        return true;
    }

    vector<int> find_books(const map<string, string>& criteria) {
        vector<int> result;
        for (const auto& [book_id, book] : books) {
            bool match = true;
            for (const auto& [key, value] : criteria) {
                if ((key == "title" && book.title != value) ||
                    (key == "author" && book.author != value) ||
                    (key == "genre" && book.genre != value) ||
                    (key == "year" && to_string(book.year) != value)) {
                    match = false;
                    break;
                }
            }
            if (match) result.push_back(book_id);
        }
        return result;
    }

    vector<LendingRecord> get_lending_history(int book_id) {
        if (lending_history.find(book_id) != lending_history.end()) {
            return lending_history[book_id];
        }
        return {};
    }

    void print_book(int book_id) {
        if (books.find(book_id) != books.end()) {
            Book b = books[book_id];
            cout << "ID: " << book_id << ", " << b.title << ", " << b.author << ", " << b.year << ", " << b.genre << endl;
        }
    }
};

int main() {
    PersonalLibrary lib;
    lib.add_book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман");
    lib.add_book("Война и мир", "Лев Толстой", 1869, "Роман");

    lib.lend_book(1, "Миша");
    lib.return_book(1);
    lib.lend_book(2, "Дима");

    map<string, string> criteria = {{"author", "Лев Толстой"}};
    vector<int> found = lib.find_books(criteria);
    for (int id : found) {
        lib.print_book(id);
    }

    vector<LendingRecord> history = lib.get_lending_history(1);
    for (const auto& record : history) {
        cout << record.action << " " << record.borrower << endl;
    }

    return 0;
}