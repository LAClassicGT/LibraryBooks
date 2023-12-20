from DataBase.database import BookModel
import os


class LibraryApp:
    def __init__(self):
        """инициализация бд"""
        self.database = BookModel

    def run(self):
        """Основной цикл вечный цикл программы"""
        while True:
            option = input('Введите опцию:\n\n1 - Добавить книгу\n2 - Просмотр списка книг\n3 - Поиск книги\n4 - '
                           'Удалить книгу\n\n>> ')
            os.system('cls')  # очищение консоли
            if option == '1':
                while True:
                    data = input('Введите данные через запятую в формате:\n"title,author,description"\nНазад - 0\n>> ')
                    if data == '0':
                        os.system('cls')  # очищение консоли
                        break
                    dict_data = data.split(',')
                    if len(dict_data) == 3:
                        while True:
                            genres_text = 'Выберите жанр(или введите новый):\nНазад - 0\n\n'
                            genres_text, genres = self.all_genres(genres_text)
                            option = input(genres_text)
                            if option == '0':
                                os.system('cls')  # очищение консоли
                                break
                            if option.isdigit():
                                try:
                                    keys = list(genres.keys())
                                    index = list(genres.values()).index(int(option))
                                    genre = keys[index]
                                except:
                                    os.system('cls')  # очищение консоли
                                    print('\nНекорректный ввод\n')
                                    break
                                dict_data.append(genre)
                                self.add_book(*dict_data)
                            else:
                                dict_data.append(option)
                                self.add_book(*dict_data)
                        pass
                    else:
                        os.system('cls')  # очищение консоли
                        print('\nНекорректный ввод\n')
            elif option == '2':
                while True:
                    genres_text = 'Выберите жанр:\nНазад - 0\n\n-1 - все жанры'
                    genres_text, genres = self.all_genres(genres_text)
                    try:
                        option = int(input(genres_text))
                        if option == 0:
                            os.system('cls')  # очищение консоли
                            break
                        elif option != -1:
                            keys = list(genres.keys())
                            index = list(genres.values()).index(option)
                            genre = keys[index]
                        else:
                            genre = option
                    except:
                        os.system('cls')  # очищение консоли
                        print('\n\nНекорректный ввод\n\n')
                        continue
                    os.system('cls')  # очищение консоли
                    while True:
                        if self.view_books(genre) == 0:
                            os.system('cls')  # очищение консоли
                            print('\n\nНет книг в базе\n\n')
                            break
                        else:
                            try:
                                book_id = int(input('Введите ID книги:\nНазад - 0\n>> '))
                            except:
                                os.system('cls')  # очищение консоли
                                print('\n\nID должен быть числом\n\n')
                                continue
                            if book_id == 0:
                                os.system('cls')  # очищение консоли
                                break
                            if self.info_book(book_id) == 0:
                                os.system('cls')  # очищение консоли
                                print('\n\nТакой книги нет в базе\n\n')
            elif option == '3':
                while True:
                    keyword = input('Введите ключевое слово:\nНазад - 0\n\n>> ')
                    if keyword == '0':
                        os.system('cls')  # очищение консоли
                        break
                    if self.search_books(keyword) == 0:
                        os.system('cls')  # очищение консоли
                        print('\nНет результатов поиска\n')
            elif option == '4':
                while True:
                    try:
                        book_id = int(input('Введите ID книги:\nНазад - 0\n>> '))
                    except:
                        os.system('cls')  # очищение консоли
                        print('\n\nID должен быть числом\n\n')
                        continue
                    if book_id == 0:
                        os.system('cls')  # очищение консоли
                        break
                    if self.remove_book(book_id) == 0:
                        os.system('cls')  # очищение консоли
                        print('\n\nТакой книги нет в базе\n\n')
            else:
                os.system('cls')  # очищение консоли
                print('\n\nНекорректный ввод\n\n')

    def add_book(self, title: str, author: str, description: str, genre: str):
        """Логика добавления книги"""
        self.database.create(title=title, author=author, description=description, genre=genre)
        os.system('cls')  # очищение консоли
        print(f'\n\nДобавлено: {title} - {author}\n\n')

    def view_books(self, genre):
        """Логика просмотра книг"""
        if genre == -1:
            books_list = self.database.select()  # все книги в бд
        else:
            books_list = self.database.select().where(self.database.genre == genre)  # поиск в бд
        if len(books_list) == 0:
            return 0
        print('\n---------------------------------------------\n')
        for book in books_list:
            print(f'{book.book_id} - {book.title}')
        print('\n---------------------------------------------\n')

    def search_books(self, keyword: str):
        """Логика поиска книг"""
        os.system('cls')  # очищение консоли
        books_list = self.database.select().where(self.database.title.contains(keyword) | self.database.author.contains(keyword))  # поиск в бд
        if len(books_list) == 0:
            return 0
        print('\n---------------------------------------------\n')
        for book in books_list:
            print(f'{book.book_id} - {book.title}')
        print('\n---------------------------------------------\n')

    def remove_book(self, book_id: int):
        """Логика удаления книг"""
        try:
            book = self.database.get(self.database.book_id == book_id)  # поиск в бд
            os.system('cls')  # очищение консоли
            print(f'\n\nУдалено: {book.title} - {book.author}\n\n')
            book.delete_instance()
        except:
            return 0

    def info_book(self, book_id: int):
        """Логика вывода информации о книге"""
        os.system('cls')  # очищение консоли
        try:
            book = self.database.get(self.database.book_id == book_id)  # поиск в бд
            print(f'\n---------------------------------------------\nНазвание: {book.title}\nАвтор: {book.author}\nОписание: {book.description}\nЖанр: {book.genre}\n---------------------------------------------\n')
        except:
            return 0

    def all_genres(self, genres_text: str):
        """Логика получения списка всех жанров"""
        genres = {}  # все жанры
        counter = 1  # счетчик
        for book in self.database.select():
            try:
                genres[book.genre]
            except:
                genres[book.genre] = counter
                counter += 1
        for genre in genres:
            genres_text += f'\n{genres[genre]} - {genre}'
        genres_text += '\n\n>> '
        return genres_text, genres
