from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits long.")
        super().__init__(value)
    
    @staticmethod
    def validate(value):
        return bool(re.match(r'^\d{10}$', value))
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = self.validate_and_convert(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    @staticmethod
    def validate_and_convert(value):
        return datetime.strptime(value, "%d.%m.%Y")
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return True
        return False
    
    def edit_phone(self, old_number, new_number):
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                return True
        return False
    
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone.value
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False
    
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now()
        next_week = today + timedelta(days=7)

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= next_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays
    
if __name__=="__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    # Додавання контактів
    contact1 = Record("Alice")
    contact1.add_phone("1234567890")
    contact1.add_birthday("15.05.1990")
    
    contact2 = Record("Bob")
    contact2.add_phone("0987654321")
    contact2.add_birthday("20.05.1985")

    book.add_record(contact1)
    book.add_record(contact2)

    # Виведення контактів
    for record in book.data.values():
        print(record)

    # Отримання майбутніх днів народження
    upcoming_birthdays = book.get_upcoming_birthdays()
    print("\nUpcoming birthdays:")
    for record in upcoming_birthdays:
        print(record)