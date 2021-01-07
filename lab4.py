'''
1. Класс должен содержать итератор
2. Должна быть реализована перегрузка стандартных операций (repr, например)
3. Должно быть реализовано наследование
4. Запись значений в свойства - только через __setattr__
5. Возможность доступа к элементам коллекции по индексу (__getitem__)
6. Должны быть реализованы статические методы
7. Должны быть реализованы генераторы

Посты: №, ник автора, текст поста, количество лайков
'''
import csv, os, numpy as np, pandas as pd

class Post_number:
    """Класс для описания номера поста"""
    number = {}
    def __setattr__(self, key, value):
        self.number[key] = int(value)

    def __getitem__(self, key):
        return self.number[key]

    def set_number(self, key, value):
        self.__setattr__(key, value)

    def get_number(self, key):
        return self.__getitem__(key)
    
class Author_nick:
    '''Класс для описания ника автора'''
    nick = {}

    def __setattr__(self, key, value):
        self.nick[key] = str(value)

    def __getitem__(self, key):
        return self.nick[key]

    def set_nick(self, key, value):
        self.__setattr__(key, value)

    def get_nick(self, key):
        return self.__getitem__(key)
    
class Post_text:
    '''Класс для описания поста'''
    post = {}

    def __setattr__(self, key, value):
        self.post[key] = str(value)

    def __getitem__(self, key):
        return self.post[key]

    def set_post(self, key, value):
        self.__setattr__(key, value)

    def get_post(self, key):
        return self.__getitem__(key)

class Likes_amount:
    '''Класс для описания количества лайков'''
    likes = {}

    def __setattr__(self, key, value):
        self.likes[key] = int(value)

    def __getitem__(self, key):
        return self.likes[key]

    def set_likes(self, key, value):
        self.__setattr__(key, value)

    def get_likes(self, key):
        return self.__getitem__(key)

class Static():
    """Класс содержит статические методы"""
    @staticmethod
    def count_files(my_path):
        path = my_path
        files = len(list(i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))))
        print(files)

    @staticmethod
    def print_in_con():
        number = Post_number()
        nick = Author_nick()
        post = Post_text()
        likes = Likes_amount()
        i = 0
        line = []
        while True:
            try:
                line.append({"number": number.get_number(i),
                    "nick": nick.get_nick(i),
                    "post": post.get_post(i),
                    "likes": likes.get_likes(i)})
                i += 1
            except KeyError:
                break
        obj = iter(line)
        while True:
            try:
                print(next(obj))
            except StopIteration:
                break

class file_saver(Static):
    '''
    Класс в котором происходят все действия с данными в таблице:
    запись, вывод, перезапись, сортировка, вывод в консоль по критерию.
    '''
    number = Post_number()
    nick = Author_nick()
    post = Post_text()
    likes = Likes_amount()

    def make_notice(self):
        with open("data4.csv", "w") as d:
            w = csv.DictWriter(d,
                delimiter=";",
                fieldnames=["number", "nick", "post", "likes"],
                lineterminator="\r")
            w.writeheader()
            i = 0
            while True:
                try:
                    w.writerow({
                        "number": self.number.get_number(i),
                        "nick": self.nick.get_nick(i),
                        "post": self.post.get_post(i),
                        "likes": self.likes.get_likes(i)
                    })
                    i += 1
                except KeyError:
                    break

    def read_csv(self):
        '''
        Данный метод осуществляет связь файла и классов для дальнейшей работы
        '''
        with open("data4.csv", 'r') as d:
            r = csv.DictReader(d, delimiter=";")
            for i, row in enumerate(r):
                for j, item in enumerate(row):
                    if j == 0:
                        self.number.set_number(i, row["number"])
                    elif j == 1:
                        self.nick.set_nick(i, row["nick"])
                    elif j == 2:
                        self.post.set_post(i, row["post"])
                    elif j == 3:
                        self.likes.set_likes(i, row["likes"])

    def write_csv(self, field, nick, post, likes):
        v = file_saver()
        v.read_csv()
        field = int(field)-1
        if int(field) == (self.number.get_number(int(field))):
            self.nick.set_nick(int(field), nick)
            self.post.set_post(int(field), post)
            self.likes.set_likes(int(field), int(likes))
            v.make_notice()
        else:
            raise KeyError

    def sort_by_likes(self):
        d = []
        i = 0
        while True:
            try:
                d.append({
                        "number": self.number.get_number(i),
                        "nick": self.nick.get_nick(i),
                        "post": self.post.get_post(i),
                        "likes": self.likes.get_likes(i)})
                i += 1
            except KeyError:
                break
        d.sort(key=lambda item: item["likes"])
        yield d
        
    def show_top(self):
        i = 0
        while True:
            try:
                if self.likes.get_likes(i) > 100:
                    print({"number": self.number.get_number(i),
                           "nick": self.nick.get_nick(i),
                           "post": self.post.get_post(i),
                           "likes": self.likes.get_likes(i)})
                i += 1
            except KeyError:
                break
        
def main():
    '''
    Главная функция из которой вызываются нужны действия с таблицей 
    или с директорией
    '''
    print("Список возможностей программы:")
    print("1 - Вывести все записи")
    print("2 - Вывод записи по критерию(лайки > 100)")
    print("3 - Сортировка по записей по лайкам")
    print("4 - Перезапись данных в файл")
    print("5 - Подсчёт файлов в директории")
    while True:
        v = file_saver()
        v.read_csv()
        mov = input("Выберите действие ")
        if mov == "1":
            v = Static
            v.print_in_con()
        elif mov  == "2":
            v.show_top()
        elif mov  == "3":
            s = v.sort_by_likes()
            print(next(s))
        elif mov  == "4":
            v.write_csv(input(" Введите номер записи "), input( "Введите новый ник " ) ,
                input( "Введите новый пост " ), input( "Введите новое количество лайков " ))
        elif mov  == "5":
            my_path = input( "Путь к файлам:" )
            v.count_files(my_path)
        elif mov == "0":
            print("Завершение работы программы")
            exit(0)
        else:
            print( "Выберите верное действие" )

if __name__ == "__main__":
    main()