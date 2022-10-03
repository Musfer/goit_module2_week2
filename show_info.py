import classes
from abc import abstractmethod, ABC


class IShowRecord(ABC):
    @abstractmethod
    def __init__(self, record: classes.Record):
        pass

    @abstractmethod
    def show(self):  # generates a string with info about contact from record
        pass


class IShowContacts(ABC):
    @abstractmethod
    def __init__(self, book: classes.AddressBook, n: int):
        pass

    @abstractmethod
    def show_all(self):  # generates a string with next n contacts
        pass


class IShowNote(ABC):
    @abstractmethod
    def __init__(self, book: classes.AddressBook):
        pass

    @abstractmethod
    def show(self):
        pass


class IShowNotes(ABC):
    @abstractmethod
    def __init__(self, book: classes.AddressBook):
        pass

    @abstractmethod
    def show(self):
        pass


class IShowNoteList(ABC):
    @abstractmethod
    def __init__(self, book: classes.AddressBook):
        pass

    @abstractmethod
    def show(self):
        pass


class IHelper(ABC):
    @abstractmethod
    def __init__(self, commands: list[str, int]):
        pass

    @abstractmethod
    def show(self):
        pass


class Helper(IHelper):
    def __init__(self, commands: list):
        self.commands = commands

    def show(self):
        sorted_commands = sorted(self.commands, key=(lambda x: x[1]))
        sorted_strings = [x[0] for x in sorted_commands]
        return "\t"+"\n\t".join(sorted_strings)


class ShowNoteList(IShowNoteList):
    def __init__(self, book: classes.AddressBook):
        self.notes = book.notes

    def show(self):
        for each in self.notes.data.values():
            print(each._name())
        return ""


class ShowNotes(IShowNotes):
    def __init__(self, book: classes.AddressBook):
        self.notes = book.notes

    def show(self):
        for note_id, note in self.notes.data.items():
            print(f"Note ID: {note_id}")
            print(note)
        return ""


class ShowNote(IShowNote):
    def __init__(self, book: classes.AddressBook):
        self.notes = book.notes

    def show(self):
        try:
            note_id = self.notes.enter_name_id()
            return self.notes.data[note_id]
        except KeyError:
            print("This note does not exists!")
            return ""


class ShowRecord(IShowRecord):
    def __init__(self, record: classes.Record):
        self.record = record

    def show(self):
        string = ""
        if self.record:
            string += f"{self.record.name.value}:"
            if self.record.phones:
                string += f"\n\tPhone numbers: {', '.join([x.value for x in self.record.phones])}"
            if self.record.emails:
                string += f"\n\tE-mails: {', '.join([x.value for x in self.record.emails])}"
            if self.record.birthday:
                birthday = self.record.birthday.value
                if birthday.year > 2:
                    string += f"\n\tBirthday: {birthday.strftime('%d %B %Y')}"
                else:
                    string += f"\n\tBirthday: {birthday.strftime('%d %B')}"
                when_to_congratulate = self.record.birthday.days_to_next_birthday
                if when_to_congratulate is not None:
                    if when_to_congratulate == 0:
                        string += f"\n\tToday is {self.record.name.value}'s birthday."
                    elif when_to_congratulate == 1:
                        string += f"\n\t{self.record.name.value} has birthday tomorrow."
                    else:
                        string += f"\n\t{self.record.name.value}'s birthday is in {when_to_congratulate} days."
            string += "\n"
        return string


class ShowContacts(IShowContacts):
    def __init__(self, book: classes.AddressBook, n: int):
        self.book = book
        self.n = n  # contacts per page

    def show_all(self):
        if not self.book.data:
            return "Your phone book is empty."
        else:
            first = self.book.page * self.n + 1  # first contact to show
            last = min(self.book.page * self.n + self.n, self.book.size)  # last contact to show
            if self.book.size == last:
                pass
            zero_line = f"Showing contacts {first}-{last} from {self.book.size} records:\n"
            if not self.book.showing_records:
                self.book.showing_records = True
                self.book.reset_iterator(self.n)
            try:
                contacts_to_show = next(self.book.show)  # list of names of next contacts to show
                output_line = zero_line
                for name in contacts_to_show:
                    record_reader = ShowRecord(self.book.data.get(name))
                    output_line += record_reader.show()
                if last == self.book.size:
                    output_line += f"End of the address book"
                    self.book.page = 0
                else:
                    output_line += f"Press 'Enter' to show next {self.n} contacts"
                    self.book.page += 1
                return output_line
            except StopIteration:
                self.book.showing_records = False
                self.book.reset_iterator(self.n)
                self.book.page = 0
                return ""
