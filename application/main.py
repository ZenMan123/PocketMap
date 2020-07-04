from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, \
    QCompleter, QPushButton, QMessageBox, QScrollArea, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from interface import Ui_MainWindow

import sqlite3
from csv import reader, writer, QUOTE_MINIMAL

from random import choice
from sys import argv


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start()

    def start(self):
        # Инициализируем изображение карты и координаты для рисования стрелки
        self.init_map()

        # Инициализируем базу данных с основной информацией и пользовательский
        # файл для хранения информации о любимых местах
        self.init_files()

        # Инициализируем списки природных объектов,
        # список для хранения виджетов (виджеты, которые надо удалять с экрана)
        # и переменную для обозначения текущего состояния
        self.init_lists()

        # Инициализируем строку поиска, добавляем к ней QCompliter для дозавершения ввода
        self.init_search_line()

        # Инициализируем все кнопки
        self.init_buttons()

    def init_map(self):
        self.current_coords = [0, 0]

        self.map_pixmap = QPixmap('photos/map.png')
        self.map = MyLabel(self, self.current_coords)  # Переопределяем метод paintEvent в QLabel,
        # чтобы можно было рисовать на виджете
        self.map.move(0, 0)
        self.map.setPixmap(self.map_pixmap)
        self.map.resize(self.map.sizeHint())
        self.map_width, self.map_height = self.map.size().width(), self.map.size().height()

    def init_lists(self):
        self.list_of_countries = [i[0] for i in self.cur.execute('SELECT name FROM countries').fetchall()]
        self.list_of_cities = [i[0] for i in self.cur.execute('SELECT name FROM cities').fetchall()]
        self.list_of_mountains = [i[0] for i in self.cur.execute('SELECT name FROM mountains').fetchall()]
        self.list_of_waterfalls = [i[0] for i in self.cur.execute('SELECT name FROM waterfalls').fetchall()]
        self.list_of_rivers = [i[0] for i in self.cur.execute('SELECT name FROM rivers').fetchall()]
        self.list_of_lakes = [i[0] for i in self.cur.execute('SELECT name FROM lakes').fetchall()]
        self.list_of_monuments = [i[0] for i in self.cur.execute('SELECT name FROM monuments').fetchall()]

        self.list_of_objects = sorted(self.list_of_countries + self.list_of_cities + self.list_of_mountains +
                                      self.list_of_waterfalls + self.list_of_rivers + self.list_of_lakes + self.list_of_monuments,
                                      key=lambda x: x.lower())

        self.used_widgets = []

        self.condition = ''

    def init_search_line(self):
        self.compliter = QCompleter(self.list_of_objects, self.objects)
        self.compliter.setFilterMode(Qt.MatchContains)

        self.objects.addItems(self.list_of_objects)
        self.objects.setCompleter(self.compliter)

    def init_files(self):
        self.con = sqlite3.connect('objects_db.db')
        self.cur = self.con.cursor()

        with open('user_files/chosen_names.txt', encoding='utf-8', mode='r') as self.csvfile:
            self.chosen = list(reader(self.csvfile, delimiter=';', quotechar='"'))
            if self.chosen:
                self.chosen = self.chosen[0]

    def init_buttons(self):
        self.tell_button.clicked.connect(self.tell)
        self.choose_button.clicked.connect(self.tell_about_chosen_items)
        self.countries_button.clicked.connect(self.tell_about_countries)
        self.cities_button.clicked.connect(self.tell_about_cities)
        self.rivers_button.clicked.connect(self.tell_about_rivers)
        self.lakes_button.clicked.connect(self.tell_about_lakes)
        self.monuments_button.clicked.connect(self.tell_about_monuments)
        self.waterfalls_button.clicked.connect(self.tell_about_waterfalls)
        self.mountains_button.clicked.connect(self.tell_about_mountains)
        self.lucky_button.clicked.connect(self.tell_about_random_object)

    def check_before_tell(self):
        """Эта функция удаляет старые виджеты с экрана, чтобы они не мешали новым"""
        if self.condition:
            for widget in self.used_widgets:
                self.layout().removeWidget(widget)
                widget.deleteLater()
                widget.setParent(None)

            self.condition = ''
            self.object_name = ''

    def rewrite_csv(self):
        """Эта функция переписывает файл с пользовательскими избранными местами,
        беря данные из self.chosen"""
        with open('user_files/chosen_names.txt', encoding='utf-8', mode='w') as self.csvfile:
            self.csvfile.write('')
            self.writer = writer(self.csvfile, delimiter=';', quotechar='"', quoting=QUOTE_MINIMAL)
            self.writer.writerow(self.chosen)

    def tell(self):
        """Одна из самых главных функций. По переменной name она выбирает какую функцию
        использовать для вывода информации на экран.
        Если self.condition = 'chosen' или 'lucky', то нам не надо считывать имя из строки поиска
        и мы читаем имя объекта из нажатой кнопки.
        Если мы нажимаем кнопку 'Рассказать', а self.condition in ['chosen', 'lucky'], то мы должны читать текст из self.objects.
        В противном случае, мы вызываем эту функцию нажатием на кнопку-объект и узнаем имя name из названия кнопки."""

        name = self.objects.currentText() if self.condition not in ['chosen',
                                                                    'lucky'] or self.sender().text() == 'Рассказать' else self.sender().text()
        if self.condition == 'lucky':
            name = choice(self.list_of_objects)  # Выбираем случайный элемент из основного списка объектов
        self.check_before_tell()  # Удаляем старые виджеты, при наличии таковых

        if name not in self.list_of_objects:  # При вводе неправильного имени выходит ошибка
            QMessageBox.warning(self, 'Ошибка', 'Географический объект был не найден!', QMessageBox.Ok)
            return

        if name in self.list_of_countries:  # Если имя в списке self.list_of_countries,
            # значит это страна и мы читаем данные из таблицы countries
            population, square, capital, flag, description, density = self.cur.execute("""SELECT population, square, capital, flag, description, density FROM countries
                WHERE name = ?""", (name,)).fetchone()

            self.condition = 'country'

            # Эта функция рассказывает о стране по заданным параметрам
            self.tell_about_country(name, population, square, capital, flag, description, density)

        # Нижеописанные условия работают по тому же принципу, что и name in self.list_of_countries

        if name in self.list_of_cities:
            population, square, flag, description, monuments = self.cur.execute("""SELECT population, square, flag, description, monuments FROM cities
                            WHERE name = ?""", (name,)).fetchone()
            self.condition = 'city'
            self.tell_about_city(name, population, square, flag, description, monuments)

        if name in self.list_of_mountains:
            height, age, country, description, photo = self.cur.execute("""SELECT height, age, country, description, photo FROM mountains
                WHERE name = ?""", (name,)).fetchone()
            self.condition = 'mountain'
            self.tell_about_mountain(name, height, age, country, description, photo)

        if name in self.list_of_waterfalls:
            height, country, description, photo = self.cur.execute("""SELECT height, country, description, photo FROM waterfalls
                WHERE name = ?""", (name,)).fetchone()
            self.condition = 'waterfall'
            self.tell_about_waterfall(name, height, country, description, photo)

        if name in self.list_of_rivers:
            depth, length, country, description, photo = self.cur.execute("""SELECT depth, length, country, description, photo FROM rivers
                            WHERE name = ?""", (name,)).fetchone()
            self.condition = 'river'
            self.tell_about_river(name, length, depth, country, description, photo)

        if name in self.list_of_lakes:
            depth, square, country, description, photo = self.cur.execute("""SELECT depth, square, country, description, photo FROM lakes
                                        WHERE name = ?""", (name,)).fetchone()
            self.condition = 'lake'
            self.tell_about_lake(name, square, depth, country, description, photo)

        if name in self.list_of_monuments:
            date, country, description, photo = self.cur.execute("""SELECT date, country, description, photo FROM monuments
                                        WHERE name = ?""", (name,)).fetchone()
            self.condition = 'monument'
            self.tell_about_monument(name, date, country, description, photo)

        # Задаём координаты вершины стрелки, не создавая нового объекта-списка
        self.current_coords[0], self.current_coords[1] = self.cur.execute("""SELECT coord_x, coord_y FROM coordinates
                                WHERE name = ?""", (name,)).fetchone()

        # Рисуём стрелку
        self.map.update()

    def tell_about_country(self, name, population, square, capital, flag, description, density):
        """Одна из важнейших функций. Эта функция описывает страну по заданным параметрам
        Функция self.make_widgets возвращает имя, картинку, описание уже с CSS кодом. Также, она возвращает
        QLabel для остальных параметров по заданному тексту (например, 'Население:\n' + population + ' чел.').
        В конце она возвращает кнопку для добавления объекта в избранные места.
        """

        name_label, flag_label, area, population_label, square_label, capital_label, density_label, add_button = \
            self.make_widgets(name, flag, description, 'Население:\n' + population + ' чел.', 'Площадь:\n' + square,
                              'Столица:\n' + capital, 'Плотность населения:\n' + density)

        # Код ниже просто задает размер, стиль, координаты виджетам

        name_label.move(80, 750)
        name_label.show()

        flag_label.move(40, 850)
        flag_label.show()

        population_label.move(350, 740)
        population_label.setStyleSheet(
            'color: #99ffcc; font-size: 30px; font-family: "comic sans ms"; border: 1px solid white')
        population_label.resize(population_label.sizeHint())
        population_label.show()

        square_label.setStyleSheet(
            'color: pink; font-size: 30px; font-family: "comic sans ms"; border: 1px solid white')
        square_label.resize(square_label.sizeHint())
        square_label.move(350, 890)
        square_label.show()

        capital_label.setStyleSheet(
            'color: #42aaff; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        capital_label.resize(capital_label.sizeHint())
        capital_label.move(650, 750)
        capital_label.show()

        density_label.setStyleSheet(
            'color: yellow; font-size: 30px; font-family: "comic sans ms"; border: 1px solid white')
        density_label.resize(density_label.sizeHint())
        density_label.move(640, 880)
        density_label.show()

        area.resize(845, 200)
        area.move(1037, 750)
        area.show()

        add_button.move(1880, 720)
        add_button.show()

        # В случае нажатия на кнопку добавить в избранное, имя объекта будет браться из self.object_name
        self.object_name = name

        # Этот список будет использоваться для удаления использованных виджетов
        self.used_widgets = [name_label, flag_label, population_label,
                             square_label, capital_label, density_label, area, add_button]

    # функции ниже работают аналогично с функцией выше

    def tell_about_city(self, name, population, square, flag, description, monuments):
        name_label, flag_label, area, population_label, square_label, monuments_label, add_button = \
            self.make_widgets(name, flag, description, 'Население:\n' + population + ' чел.', 'Площадь:\n' + square,
                              'Достопримечательности:\n' + monuments)

        name_label.move(70, 750)
        name_label.show()

        flag_label.move(40, 850)
        flag_label.show()

        population_label.move(350, 730)
        population_label.setStyleSheet(
            'color: #42aaff; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        population_label.resize(population_label.sizeHint())
        population_label.show()

        square_label.move(360, 900)
        square_label.setStyleSheet(
            'color: pink; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        square_label.resize(square_label.sizeHint())
        square_label.show()

        area.resize(1180, 200)
        area.move(690, 710)
        area.show()

        monuments_label.move(680, 950)
        monuments_label.setStyleSheet(
            'color: #99ffcc; font-size: 30px; font-family: "comic sans ms"; border: 1px solid white')
        monuments_label.resize(monuments_label.sizeHint())
        monuments_label.show()

        add_button.move(1880, 710)
        add_button.show()

        self.object_name = name
        self.used_widgets = [name_label, flag_label, population_label,
                             square_label, area, monuments_label, add_button]

    def tell_about_mountain(self, name, height, age, country, description, photo):
        name_label, photo_label, area, country_label, height_label, age_label, add_button = \
            self.make_widgets(name, photo, description, 'Местоположение:\n' + country, 'Высота:\n' + height,
                              'Возраст:\n' + age)

        name_label.move(790, 940)
        name_label.show()

        photo_label.move(40, 720)
        photo_label.show()

        height_label.move(1700, 930)
        height_label.setStyleSheet(
            'color: #42aaff; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        height_label.resize(height_label.sizeHint())
        height_label.show()

        country_label.move(1260, 930)
        country_label.setStyleSheet(
            'color: pink; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        country_label.resize(country_label.sizeHint())
        country_label.show()

        area.resize(1270, 200)
        area.move(600, 710)
        area.show()

        age_label.move(560, 930)
        age_label.setStyleSheet(
            'color: #99ffcc; font-size: 30px; font-family: "comic sans ms"; border: 1px solid white')
        age_label.resize(age_label.sizeHint())
        age_label.show()

        add_button.move(1880, 710)
        add_button.show()

        self.object_name = name
        self.used_widgets = [name_label, photo_label, height_label,
                             age_label, area, country_label, add_button]

    def tell_about_waterfall(self, name, height, country, description, photo):
        name_label, photo_label, area, country_label, height_label, add_button = \
            self.make_widgets(name, photo, description, 'Местоположение:\n' + country, 'Высота:\n' + height)

        name_label.move(1100, 935)
        name_label.show()

        photo_label.move(40, 720)
        photo_label.show()

        height_label.move(1600, 920)
        height_label.setStyleSheet(
            'color: #99ffcc; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        height_label.resize(height_label.sizeHint())
        height_label.show()

        country_label.move(700, 920)
        country_label.setStyleSheet(
            'color: pink; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        country_label.resize(country_label.sizeHint())
        country_label.show()

        area.resize(1200, 200)
        area.move(650, 710)
        area.show()

        add_button.move(1880, 710)
        add_button.show()

        self.object_name = name
        self.used_widgets = [name_label, photo_label, height_label,
                             area, country_label, add_button]

    def tell_about_river(self, name, length, depth, country, description, photo):
        name_label, photo_label, area, country_label, length_label, depth_label, add_button = \
            self.make_widgets(name, photo, description, 'Местоположение:\n' + country, 'Длина:\n' + length,
                              'Глубина:\n' + depth)

        name_label.move(970, 950)
        name_label.show()

        photo_label.move(40, 720)
        photo_label.show()

        length_label.move(1700, 930)
        length_label.setStyleSheet(
            'color: #42aaff; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        length_label.resize(length_label.sizeHint())
        length_label.show()

        country_label.move(1250, 930)
        country_label.setStyleSheet(
            'color: pink; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        country_label.resize(country_label.sizeHint())
        country_label.show()

        area.resize(1200, 200)
        area.move(650, 710)
        area.show()

        depth_label.move(680, 930)
        depth_label.setStyleSheet(
            'color: #99ffcc; font-size: 30px; font-family: "comic sans ms"; border: 1px solid white')
        depth_label.resize(depth_label.sizeHint())
        depth_label.show()

        add_button.move(1880, 710)
        add_button.show()

        self.object_name = name
        self.used_widgets = [name_label, photo_label, length_label,
                             depth_label, area, country_label, add_button]

    def tell_about_lake(self, name, square, depth, country, description, photo):
        name_label, photo_label, area, country_label, length_label, depth_label, add_button = \
            self.make_widgets(name, photo, description, 'Местоположение:\n' + country, 'Площадь:\n' + square,
                              'Глубина:\n' + depth)

        name_label.move(880, 950)
        name_label.show()

        photo_label.move(40, 720)
        photo_label.show()

        length_label.move(1700, 930)
        length_label.setStyleSheet(
            'color: #42aaff; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        length_label.resize(length_label.sizeHint())
        length_label.show()

        country_label.move(1250, 930)
        country_label.setStyleSheet(
            'color: pink; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        country_label.resize(country_label.sizeHint())
        country_label.show()

        area.resize(1300, 200)
        area.move(500, 710)
        area.show()

        depth_label.move(680, 930)
        depth_label.setStyleSheet(
            'color: #99ffcc; font-size: 30px; font-family: "comic sans ms"; border: 1px solid white')
        depth_label.resize(depth_label.sizeHint())
        depth_label.show()

        add_button.move(1880, 710)
        add_button.show()

        self.object_name = name
        self.used_widgets = [name_label, photo_label, length_label,
                             depth_label, area, country_label, add_button]

    def tell_about_monument(self, name, date, country, description, photo):
        name_label, photo_label, area, country_label, date_label, add_button = \
            self.make_widgets(name, photo, description, 'Местоположение:\n' + country, 'Дата создания:\n' + date)

        name_label.move(1100, 935)
        name_label.show()

        photo_label.move(40, 720)
        photo_label.show()

        date_label.move(1600, 920)
        date_label.setStyleSheet(
            'color: #99ffcc; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        date_label.resize(date_label.sizeHint())
        date_label.show()

        country_label.move(700, 920)
        country_label.setStyleSheet(
            'color: pink; font-size: 35px; font-family: "comic sans ms"; border: 1px solid white')
        country_label.resize(country_label.sizeHint())
        country_label.show()

        area.resize(1400, 200)
        area.move(500, 710)
        area.show()

        add_button.move(1880, 710)
        add_button.show()

        self.object_name = name
        self.used_widgets = [name_label, photo_label, date_label,
                             area, country_label, add_button, area]

    def tell_about_chosen_items(self):
        """Функция выводит QGridLayout, состоящий из кнопок из списка self.chosen.
        При нажатии на кнопку выводится информация об объекте."""
        self.make_grid_for_telling(self.chosen)

    # Функции ниже работают аналогично

    def tell_about_countries(self):
        countries = [i[0] for i in self.cur.execute("""SELECT name FROM countries""").fetchall()]
        self.make_grid_for_telling(countries)

    def tell_about_cities(self):
        cities = [i[0] for i in self.cur.execute("""SELECT name FROM cities""").fetchall()]
        self.make_grid_for_telling(cities)

    def tell_about_rivers(self):
        rivers = [i[0] for i in self.cur.execute("""SELECT name FROM rivers""").fetchall()]
        self.make_grid_for_telling(rivers)

    def tell_about_waterfalls(self):
        waterfalls = [i[0] for i in self.cur.execute("""SELECT name FROM waterfalls""").fetchall()]
        self.make_grid_for_telling(waterfalls)

    def tell_about_lakes(self):
        lakes = [i[0] for i in self.cur.execute("""SELECT name FROM lakes""").fetchall()]
        self.make_grid_for_telling(lakes)

    def tell_about_monuments(self):
        monuments = [i[0] for i in self.cur.execute("""SELECT name FROM monuments""").fetchall()]
        self.make_grid_for_telling(monuments)

    def tell_about_mountains(self):
        mountains = [i[0] for i in self.cur.execute("""SELECT name FROM mountains""").fetchall()]
        self.make_grid_for_telling(mountains)

    def tell_about_random_object(self):
        self.condition = 'lucky'
        self.tell()

    def make_grid_for_telling(self, arr):
        """Создаём QGridLayout из заданного списка"""

        self.check_before_tell()  # Убираем старые виджеты
        arr = sorted(arr)
        self.grid = QGridLayout()

        for pos, item in enumerate(arr):
            # Создаём кнопку
            button = QPushButton(self)
            button.setText(item)
            button.setFixedSize(300, 35)
            button.clicked.connect(self.tell)
            button.setStyleSheet("""
                        QPushButton {
                            color: orange; 
        	                font-family: comic sans ms;
         	                background-color: #151719; 
        	                border-style: solid; 
        	                border-color: white;
        	                border-width: 2px;
        	                border-radius: 7px;
        	                font-size: 22px;
        	                }
        	            QPushButton:hover {
        	                background-color: #99ffcc;
        	                color: blue;
        	                }
        	            QPushButton:pressed {
        	                background-color: white;
        	                }
        	                """)

            self.grid.addWidget(button, pos % 7, pos // 7)  # Максимум 7 строк

        # Мы не можем изменять layout у QMainWindow,
        # поэтому изменяем layout у QWidget и размещаем его на QMainWindow
        self.widget = QWidget(self)
        self.widget.setLayout(self.grid)
        self.widget.move(0, 700)
        self.widget.resize(self.widget.sizeHint())
        self.widget.setStyleSheet('background-color: #161a1f')

        # Создаём область прокрутки, так как размер self.widget может быть слишком большим
        area = QScrollArea(self)
        area.setWidget(self.widget)
        area.setWidgetResizable(True)
        area.move(0, 705)
        area.resize(1920, 320)
        area.show()

        self.condition = 'chosen'
        self.map.update()  # Рисуём карту
        self.used_widgets = [area]  # Добавляем area в список для удаления

    def make_widgets(self, name, flag, description, *widgets):
        my_widgets = []
        # Создаём именной виджет

        name_label = QLabel(self)
        name_label.setText(name)
        name_label.setStyleSheet('color: orange; font-size: 40px; font-family: "Century"')
        name_label.resize(name_label.sizeHint())
        my_widgets.append(name_label)

        # Создаём виджет-картинку

        flag_pixmap = QPixmap('photos/' + flag)
        flag_label = QLabel(self)
        flag_label.setPixmap(flag_pixmap)
        flag_label.resize(flag_label.sizeHint())
        my_widgets.append(flag_label)

        # Открываем файл с описаниями

        f = open('descriptions/' + description, encoding='utf-8')
        description_text = f.read()
        f.close()

        # Создаём виджет-описание

        description_label = QLabel(self)
        description_label.setText(description_text)
        description_label.setStyleSheet(
            'color: #adb7bd; font-size: 22px; font-family: "comic sans ms"; border: 1px solid white; background-color: #161a1f')
        description_label.resize(description_label.sizeHint())

        # Добавляем его в QScrollArea

        area = QScrollArea(self)
        area.setWidget(description_label)
        area.setWidgetResizable(True)
        my_widgets.append(area)

        # Создаём виджеты

        for w in widgets:
            label = QLabel(self)
            label.setText(w)
            my_widgets.append(label)

        # Добавляем кнопку добавления в избранное

        add_button = QPushButton(self)
        add_button.resize(20, 20)
        if name in self.chosen:
            add_button.setStyleSheet('background-color: yellow; border: 1px solid white; border-radius: 10px')
            add_button.color = 1
        else:
            add_button.setStyleSheet('background-color: #99ffcc; border: 1px solid white; border-radius: 10px')
            add_button.color = 0
        add_button.clicked.connect(self.add_name)
        my_widgets.append(add_button)

        return my_widgets

    def add_name(self):
        if self.sender().color == 0:  # Если элемент не в избранном
            self.chosen.append(self.object_name)
            self.sender().setStyleSheet('background-color: yellow; border: 1px solid white; border-radius: 10px')
            self.sender().color = 1
        else:  # Если элемент в избранном
            self.chosen.remove(self.object_name)
            self.sender().setStyleSheet('background-color: #99ffcc; border: 1px solid white; border-radius: 10px')
            self.sender().color = 0
        self.rewrite_csv()

    def paintEvent(self, event):
        # Рисуем разделительную линию

        self.p = QPainter(self)
        self.p.begin(self)

        self.p.setPen(QPen(QColor('#FFA500'), 3))
        self.p.drawLine(self.map_width, self.map_height - 1, self.width(), self.map_height - 1)

        self.p.end()


class MyLabel(QLabel):
    def __init__(self, parent, coords):
        super().__init__(parent)
        self.coords = coords  # Инициализируем координаты один раз,
        # так как self.coords ссылка на объект в памяти

    def paintEvent(self, event):
        super().paintEvent(event)  # Так было на Stack Overflow

        # Рисуем только в том случае, если ex.condition равен country, city, river и др.

        if not (ex.condition and ex.condition not in ['chosen', 'lucky']):
            return
        qp = QPainter(self)
        qp.setPen(QPen(Qt.red, 7))

        qp.begin(self)
        self.drawArrow(qp)  # Рисуем стрелку
        qp.end()

    def drawArrow(self, qp):
        """В зависимости от положения self.coords рисует стрелку"""

        if self.coords[0] - 100 >= 0 and self.coords[1] - 100 >= 0:
            qp.drawLine(self.coords[0] - 100, self.coords[1] - 100, *self.coords)
            qp.drawLine(self.coords[0] - 30, self.coords[1], *self.coords)
            qp.drawLine(self.coords[0], self.coords[1] - 30, *self.coords)
            return

        if self.coords[0] - 100 >= 0:
            qp.drawLine(self.coords[0] - 100, self.coords[1] + 100, *self.coords)
            qp.drawLine(self.coords[0] - 30, self.coords[1], *self.coords)
            qp.drawLine(self.coords[0], self.coords[1] + 30, *self.coords)
            return

        if self.coords[1] - 100 >= 0:
            qp.drawLine(self.coords[0] + 100, self.coords[1] - 100, *self.coords)
            qp.drawLine(self.coords[0] + 30, self.coords[1], *self.coords)
            qp.drawLine(self.coords[0], self.coords[1] - 30, *self.coords)
            return
        qp.drawLine(self.coords[0] + 100, self.coords[1] + 100, *self.coords)
        qp.drawLine(self.coords[0] + 30, self.coords[1], *self.coords)
        qp.drawLine(self.coords[0], self.coords[1] + 30, *self.coords)
        return


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainWindow()
    ex.show()
    app.exec()
