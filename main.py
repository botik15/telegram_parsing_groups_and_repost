from time import gmtime, strftime
import json
import multiprocessing
import os
import sqlite3
import subprocess
import sys
import threading
import time
import telebot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QWidget, QLabel , QVBoxLayout

multiprocessing.freeze_support()  # чтобы мультипроцессорность запретить (так надо для винды!!!)


class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setStyleSheet('font-size: 16px')
        self.setParent(parent)


#графическое окно заполнение данных инвентаризации
class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle("Программа")

        # Шрифты
        self.font11b = QtGui.QFont()
        self.font11b.setPointSize(11)
        self.font11b.setBold(True)
        self.font11b.setWeight(75)

        self.font20b = QtGui.QFont()
        self.font20b.setPointSize(20)
        self.font20b.setBold(True)
        self.font20b.setWeight(75)

        self.font9 = QtGui.QFont()
        self.font9.setPointSize(9)

        self.font9b = QtGui.QFont()
        self.font9b.setPointSize(9)
        self.font9b.setBold(True)
        self.font9b.setWeight(75)

        ################################## Наполнение тела ##################################
        # Главная надпись
        self.lbl_name1 = QtWidgets.QLabel(self)
        self.lbl_name1.setText("Телеграм")
        self.lbl_name1.setGeometry(QtCore.QRect(0, 0, 800, 50))
        self.lbl_name1.setFont(self.font20b)
        self.lbl_name1.setAlignment(Qt.AlignCenter)

        self.lbl_name2 = QtWidgets.QLabel(self)
        self.lbl_name2.setText("парсинг телеграм постов")
        self.lbl_name2.setGeometry(QtCore.QRect(0, 25, 800, 50))
        self.lbl_name2.setFont(self.font11b)
        self.lbl_name2.setAlignment(Qt.AlignCenter)

        self.lbl_name3 = QtWidgets.QLabel(self)
        self.lbl_name3.setText("Заказ парсинга и ботов ")
        self.lbl_name3.setGeometry(QtCore.QRect(280, 50, 800, 50))
        self.lbl_name3.setFont(self.font11b)
        self.lbl_name3.setStyleSheet("color : red")

        self.label2 = QtWidgets.QLabel(self)
        self.label2 = HyperlinkLabel(self)
        self.linkTemplate = '<a href={0}>{1}</a>'
        self.label2.setText(self.linkTemplate.format('https://чкм21.рф', 'Click Me'))
        self.label2.setGeometry(QtCore.QRect(470, 50, 800, 50))

        ################################### Данные телеграм канала ##################################
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(10, 100, 380, 100))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_tab2 = QtWidgets.QLabel(self.frame_2)
        self.lbl_tab2.setText('Данные телеграм канала')
        self.lbl_tab2.setGeometry(QtCore.QRect(10, 10, 361, 17))
        self.lbl_tab2.setFont(self.font9b)

        # Количество постов
        self.lbl_count_post = QtWidgets.QLabel(self.frame_2)
        self.lbl_count_post.setText('Кол. постов')
        self.lbl_count_post.setGeometry(QtCore.QRect(10, 30, 80, 20))
        self.lbl_count_post.setFont(self.font9)
        self.lbl_count_post.setToolTip("Укажите количество постов")
        self.chng_count_post = QtWidgets.QLineEdit(self.frame_2)
        self.chng_count_post.setGeometry(QtCore.QRect(10, 50, 80, 25))
        self.chng_count_post.setFont(self.font9)
        self.chng_count_post.setText('15')
        self.chng_count_post.setInputMask("00")

        # Ссылка на канал
        self.lbl_url= QtWidgets.QLabel(self.frame_2)
        self.lbl_url.setText('Ссылка на канал')
        self.lbl_url.setGeometry(QtCore.QRect(100, 30, 100, 20))
        self.lbl_url.setFont(self.font9)
        self.lbl_url.setToolTip("Укажите ссылку на телеграм канал")
        self.chng_url = QtWidgets.QLineEdit(self.frame_2)
        self.chng_url.setGeometry(QtCore.QRect(100, 50, 140, 25))
        self.chng_url.setFont(self.font9)

        # Выгрузить
        self.btn_ok = QtWidgets.QPushButton(self.frame_2)
        self.btn_ok.setText('Просмотреть посты')
        self.btn_ok.setGeometry(QtCore.QRect(250, 50, 120, 25))
        self.btn_ok.setToolTip("Просмотреть все посты в песочнице")


        ################################### Отправка уведомлений телеграм ##################################
        self.frame_4 = QtWidgets.QFrame(self)
        self.frame_4.setGeometry(QtCore.QRect(10, 210, 380, 230))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_tab2 = QtWidgets.QLabel(self.frame_4)
        self.lbl_tab2.setText('Отправка уведомлений в телеграм')
        self.lbl_tab2.setGeometry(QtCore.QRect(10, 10, 361, 17))
        self.lbl_tab2.setFont(self.font9b)

        # Токен telegram
        self.lbl_telegram_token = QtWidgets.QLabel(self.frame_4)
        self.lbl_telegram_token.setText('Токен telegram')
        self.lbl_telegram_token.setGeometry(QtCore.QRect(10, 30, 165, 20))
        self.lbl_telegram_token.setFont(self.font9)
        self.lbl_telegram_token.setToolTip("Токен бота. Не знаете где взять? Отпишитесь мне.")

        self.chng_telegram_token = QtWidgets.QLineEdit(self.frame_4)
        self.chng_telegram_token.setGeometry(QtCore.QRect(10, 50, 165, 25))

        # чат id telegram
        self.lbl_сhat_id = QtWidgets.QLabel(self.frame_4)
        self.lbl_сhat_id.setText('Chat ID')
        self.lbl_сhat_id.setGeometry(QtCore.QRect(185, 30, 190, 20))
        self.lbl_сhat_id.setFont(self.font9)
        self.lbl_сhat_id.setToolTip("Токен бота. Не знаете где взять? Отпишитесь мне.")

        self.chng_сhat_id = QtWidgets.QLineEdit(self.frame_4)
        self.chng_сhat_id.setGeometry(QtCore.QRect(185, 50, 190, 25))
        self.chng_сhat_id.setFont(self.font9)

        self.lbl_zamen_text = QtWidgets.QLabel(self.frame_4)
        self.lbl_zamen_text.setText('Замена текста')
        self.lbl_zamen_text.setGeometry(QtCore.QRect(10, 70, 150, 25))
        self.lbl_zamen_text.setToolTip("Замена текста перед отправкой телеграм боту")

        # заменяемый текст
        self.lbl_zamen_text_1 = QtWidgets.QLabel(self.frame_4)
        self.lbl_zamen_text_1.setText('1')
        self.lbl_zamen_text_1.setGeometry(QtCore.QRect(10, 101, 10, 10))

        self.lineEdit_zamen_text_1 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_zamen_text_1.setGeometry(QtCore.QRect(20, 95, 70, 25))

        self.lbl_zamen_text_ = QtWidgets.QLabel(self.frame_4)
        self.lbl_zamen_text_.setText('->')
        self.lbl_zamen_text_.setGeometry(QtCore.QRect(92, 101, 10, 10))

        self.lineEdit_zamen_text_1_1 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_zamen_text_1_1.setGeometry(QtCore.QRect(104, 95, 70, 25))

        # заменить на текст
        self.lbl_zamen_text_2 = QtWidgets.QLabel(self.frame_4)
        self.lbl_zamen_text_2.setText('2')
        self.lbl_zamen_text_2.setGeometry(QtCore.QRect(10, 136, 10, 10))

        self.lineEdit_zamen_text_2 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_zamen_text_2.setGeometry(QtCore.QRect(20, 130, 70, 25))

        self.lbl_zamen_text_ = QtWidgets.QLabel(self.frame_4)
        self.lbl_zamen_text_.setText('->')
        self.lbl_zamen_text_.setGeometry(QtCore.QRect(92, 136, 10, 10))

        self.lineEdit_zamen_text_2_2 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_zamen_text_2_2.setGeometry(QtCore.QRect(104, 130, 70, 25))


        self.lbl_period = QtWidgets.QLabel(self.frame_4)
        self.lbl_period.setText('Периодичность')
        self.lbl_period.setGeometry(QtCore.QRect(184, 70, 150, 25))
        self.lbl_period.setToolTip("Интервал парсинга канала")

        self.lineEdit_period = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_period.setGeometry(QtCore.QRect(184, 95, 40, 25))
        self.lineEdit_period.setInputMask("0000")

        self.lbl_min = QtWidgets.QLabel(self.frame_4)
        self.lbl_min.setText('мин.')
        self.lbl_min.setGeometry(QtCore.QRect(230, 95, 30, 25))

        # Запустить
        self.btn_start_telegram = QtWidgets.QPushButton(self.frame_4)
        self.btn_start_telegram.setText('Запустить')
        self.btn_start_telegram.setGeometry(QtCore.QRect(290, 95, 80, 25))
        # Остановить
        self.btn_stop_telegram = QtWidgets.QPushButton(self.frame_4)
        self.btn_stop_telegram.setText('Остановить')
        self.btn_stop_telegram.setGeometry(QtCore.QRect(290, 130, 80, 25))


        #поиск по слову
        self.lbl_find_text = QtWidgets.QLabel(self.frame_4)
        self.lbl_find_text.setText('Поиск по слову')
        self.lbl_find_text.setGeometry(QtCore.QRect(10, 155, 150, 25))
        self.lbl_find_text.setToolTip("Поиск по слову")

        self.lineEdit_find_text = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_find_text.setGeometry(QtCore.QRect(10, 175, 165, 25))



        ################################### Настройки ##################################
        # Frame3
        self.frame_3 = QtWidgets.QFrame(self)
        self.frame_3.setGeometry(QtCore.QRect(10, 450, 380, 140))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_frame3 = QtWidgets.QLabel(self.frame_3)
        self.lbl_frame3.setText('Настройки')
        self.lbl_frame3.setGeometry(QtCore.QRect(10, 10, 361, 17))
        self.lbl_frame3.setFont(self.font9b)


        self.lbl_invent_n = QtWidgets.QLabel(self.frame_3)
        self.lbl_invent_n.setText('Данные')
        self.lbl_invent_n.setGeometry(QtCore.QRect(10, 30, 161, 20))
        self.lbl_invent_n.setFont(self.font9)


        # Кнопка 1
        self.btn_save = QtWidgets.QPushButton(self.frame_3)
        self.btn_save.setText('Сохранить')
        self.btn_save.setGeometry(QtCore.QRect(10, 50, 80, 25))

        # Кнопка 1
        self.btn_clear = QtWidgets.QPushButton(self.frame_3)
        self.btn_clear.setText('Очистить')
        self.btn_clear.setGeometry(QtCore.QRect(100, 50, 80, 25))
        # Кнопка 1
        self.btn_del = QtWidgets.QPushButton(self.frame_3)
        self.btn_del.setText('Удалить')
        self.btn_del.setGeometry(QtCore.QRect(190, 50, 80, 25))


        # Кнопка 2
        self.lbl_invent_n = QtWidgets.QLabel(self.frame_3)
        self.lbl_invent_n.setText('Выгрузить в ')
        self.lbl_invent_n.setGeometry(QtCore.QRect(10, 80, 161, 20))
        # Кнопка 2
        self.btn_cancel = QtWidgets.QPushButton(self.frame_3)
        self.btn_cancel.setText('EXCEL')
        self.btn_cancel.setGeometry(QtCore.QRect(10, 100, 80, 25))
        # Кнопка 2
        self.btn_cancel = QtWidgets.QPushButton(self.frame_3)
        self.btn_cancel.setText('БД')
        self.btn_cancel.setGeometry(QtCore.QRect(100, 100, 80, 25))


        ################################### текст ##################################
        self.frame_5 = QtWidgets.QFrame(self)
        self.frame_5.setGeometry(QtCore.QRect(400, 100, 380, 490))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_frame3 = QtWidgets.QLabel(self.frame_5)
        self.lbl_frame3.setText('Песочница')
        self.lbl_frame3.setGeometry(QtCore.QRect(10, 10, 361, 17))
        self.lbl_frame3.setFont(self.font9b)
        self.lbl_frame3.setToolTip("Место для тестирования постов, путем замена текста и так далее. Не влияет ни на что. Просто песочница.")

        # текст
        self.textEdit_p = QtWidgets.QTextEdit(self.frame_5)
        self.textEdit_p.setGeometry(QtCore.QRect(10, 30, 360, 385))
        self.textEdit_p.setObjectName("textEdit")

        # заменяемый текст
        self.lineEdit_pesoch_text_1 = QtWidgets.QLineEdit(self.frame_5)
        self.lineEdit_pesoch_text_1.setGeometry(QtCore.QRect(10, 420, 150, 25))
        self.lineEdit_pesoch_text_1.setObjectName("lineEdit")

        self.lbl_pesoch_text_1 = QtWidgets.QLabel(self.frame_5)
        self.lbl_pesoch_text_1.setText('->')
        self.lbl_pesoch_text_1.setGeometry(QtCore.QRect(163, 420, 150, 25))

        # заменить на текст
        self.lineEdit_pesoch_text_2 = QtWidgets.QLineEdit(self.frame_5)
        self.lineEdit_pesoch_text_2.setGeometry(QtCore.QRect(176, 420, 150, 25))
        self.lineEdit_pesoch_text_2.setObjectName("lineEdit")

        # Кнопка 1
        self.btn_replace = QtWidgets.QPushButton(self.frame_5)
        self.btn_replace.setText('V')
        self.btn_replace.setGeometry(QtCore.QRect(335, 420, 25, 25))

        # Кнопка 2
        self.btn_save_p = QtWidgets.QPushButton(self.frame_5)
        self.btn_save_p.setText('Сохранить')
        self.btn_save_p.setGeometry(QtCore.QRect(10, 450, 80, 25))

        # Кнопка 3
        self.btn_del_p = QtWidgets.QPushButton(self.frame_5)
        self.btn_del_p.setText('Очистить')
        self.btn_del_p.setGeometry(QtCore.QRect(100, 450, 80, 25))

        ####################################################################################################
        self.file_name = 'db_info.txt'
        self.file_name_text_parser = 'tele.txt'
        self.stop_theardss = False
        self.btn_stop_telegram.setEnabled(False)
        self.btn_start_telegram.setEnabled(True)
        ###########################################
        try:
            self.connection()
        except:
            print('Ошибка')
            self.app.exec_()

        try:
            self.base_past()
        except:
            print('error')
            pass

        ####################################################################################################
        self.btn_replace.clicked.connect(self.replace_file) #замена в песочнице
        self.btn_ok.clicked.connect(self.read_post) #просметреть все посты
        self.btn_del_p.clicked.connect(self.clear_tab)
        self.btn_save.clicked.connect(self.base_save)
        self.btn_clear.clicked.connect(self.base_clear)
        self.btn_del.clicked.connect(self.base_del)
        self.btn_start_telegram.clicked.connect(self.start_telegram)
        self.btn_stop_telegram.clicked.connect(self.stop_telegram)
        self.bot_chat_id = str(self.chng_сhat_id.text())
        self.bot = telebot.TeleBot(str(self.chng_telegram_token.text()))
        ####################################################################################################


    def date_time(self):
        return str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


    def text_input(self):
        count_post = str(self.chng_count_post.text()) #Кол постов
        url = str(self.chng_url.text()) #ссылка на канал
        token = str(self.chng_telegram_token.text()) #токен
        chat_id = str(self.chng_сhat_id.text()) #сhat_id
        zamena_1 = str(self.lineEdit_zamen_text_1.text()) #Отправка уведомлений замена текста 1
        zamena_1_1 = str(self.lineEdit_zamen_text_1_1.text()) #Отправка уведомлений замена текста 1 -> 1
        zamena_2 = str(self.lineEdit_zamen_text_2.text()) #Отправка уведомлений замена текста 1
        zamena_2_2 = str(self.lineEdit_zamen_text_2_2.text()) #Отправка уведомлений замена текста 1 -> 1
        periods = str(self.lineEdit_period.text()) #Отправка уведомлений замена текста 1 -> 1
        find_text = str(self.lineEdit_find_text.text()) #поиск по слову
        return count_post,url,token,chat_id,zamena_2,zamena_1,zamena_2_2,zamena_1_1,periods,find_text
    def connection(self):
        self.conn = sqlite3.connect('mydatabase.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists telebot(id integer PRIMARY KEY,url text, date text, content text)')
        self.conn.commit()


    def func_start_telegram(self):
        with open(self.file_name_text_parser) as datas:
            for data in datas:
                index = json.loads(data)
                url = index['url']
                date = index['date'].split(('T', 1)[0])[0]
                content = index['content']

                self.cursor.execute("SELECT id FROM telebot WHERE url = ?", (url,))
                if self.cursor.fetchone() is None:
                    # Вставляем данные в таблицу
                    content = str(content).replace(str(self.lineEdit_zamen_text_1.text()),
                                                   str(self.lineEdit_zamen_text_1_1.text()))
                    content = str(content).replace(str(self.lineEdit_zamen_text_2.text()),
                                                   str(self.lineEdit_zamen_text_2_2.text()))
                    slovo = str(self.lineEdit_find_text.text())
                    if content.find(slovo) != -1:
                        self.cursor.execute('''INSERT INTO telebot (url,date,content) VALUES(?, ?, ?)''',
                                            (url, date, content,))
                        text = f'Ссылка: {url}\nОписание: {content}\nДата: {date}\n\n'
                        print('Добавлен в бд')
                        print(text)
                        self.bot.send_message(self.bot_chat_id, text=content)
                        time.sleep(3)
                        # Сохраняем изменения
                        self.conn.commit()
                    else:
                        text = f'Не найдено слово "{slovo}" в посте: {url}'
                else:
                    text = f'Существет в бд: {url}'
                    print(text)
                self.textEdit_p.append(f'{self.date_time()}\n{text}\n')


    def read_post(self):
        self.write_file()
        with open(self.file_name_text_parser) as datas:
            for data in datas:
                index = json.loads(data)
                url = index['url']
                print(url)
                date = index['date'].split(('T', 1)[0])[0]
                print(date)
                content = index['content']
                print(content)
                text = f'Ссылка: {url}\nОписание: {content}\nДата: {date}\n\n'
                self.textEdit_p.append(text)


    def base_del(self):
        if os.path.isfile(self.file_name):
            self.btn_clear.clicked.connect(self.base_clear)
            os.remove(self.file_name)
            print("success")
        else:
            print("File doesn't exists!")

    def base_del_text_parser(self):
        if os.path.isfile(self.file_name_text_parser):
            self.btn_clear.clicked.connect(self.base_clear)
            os.remove(self.file_name_text_parser)
            print("success")
        else:
            print("File doesn't exists!")

    def base_clear(self):
        self.chng_count_post.clear()
        self.chng_url.clear()
        self.chng_telegram_token.clear()
        self.chng_сhat_id.clear()
        self.lineEdit_zamen_text_1.clear()
        self.lineEdit_zamen_text_1_1.clear()
        self.lineEdit_zamen_text_2.clear()
        self.lineEdit_zamen_text_2_2.clear()
        self.lineEdit_period.clear()

    def base_past(self):
        self.text_input()
        with open(self.file_name, 'r', encoding='utf-8') as f:
            nums = f.read().splitlines()
            self.chng_count_post.setText(nums[0].replace('Кол постов: ', ''))
            self.chng_url.setText(nums[1].replace('Cсылка на канал: ', ''))
            self.chng_telegram_token.setText(nums[2].replace('Токен: ', ''))
            self.chng_сhat_id.setText(nums[3].replace('ChatID: ', ''))
            self.lineEdit_zamen_text_1.setText(nums[4].replace('Слово1-1: ', ''))
            self.lineEdit_zamen_text_1_1.setText(nums[5].replace('Слово1-2: ', ''))
            self.lineEdit_zamen_text_2.setText(nums[6].replace('Слово2-1: ', ''))
            self.lineEdit_zamen_text_2_2.setText(nums[7].replace('Слово2-2: ', ''))
            self.lineEdit_period.setText(nums[8].replace('Интервал: ', ''))
            self.lineEdit_find_text.setText(nums[9].replace('Поиск по слову: ', ''))

    def base_save(self):

        self.text_input()
        # self.cursor.execute('SELECT * FROM save_info WHERE (token=? AND chat_id=?)', (self.chng_telegram_token.text(), self.chng_сhat_id.text()))
        # entry = self.cursor.fetchone()
        # print(self.lineEdit_find_text.text())
        # if entry is None:
        #     self.cursor.execute('''INSERT INTO save_info (count_post, url, token, chat_id, zamena_1, zamena_1_1, zamena_2, zamena_2_2, periods, find_text) VALUES (?,?,?,?,?,?,?,?,?,?)''', (self.chng_count_post.text(),self.chng_url.text(),self.chng_telegram_token.text(),self.chng_сhat_id.text(),self.lineEdit_zamen_text_1.text(),self.lineEdit_zamen_text_1_1.text(),self.lineEdit_zamen_text_2.text(),self.lineEdit_zamen_text_2_2.text(),self.lineEdit_period.text(),self.lineEdit_find_text.text(),))
        #     print('New entry added')
        # else:
        #     print ('Entry found')
        # #
        count_post = str(self.chng_count_post.text()) #Кол постов
        url = str(self.chng_url.text()) #ссылка на канал
        token = str(self.chng_telegram_token.text()) #токен
        chat_id = str(self.chng_сhat_id.text()) #сhat_id
        zamena_1 = str(self.lineEdit_zamen_text_1.text()) #Отправка уведомлений замена текста 1
        zamena_1_1 = str(self.lineEdit_zamen_text_1_1.text()) #Отправка уведомлений замена текста 1 -> 1
        zamena_2 = str(self.lineEdit_zamen_text_2.text()) #Отправка уведомлений замена текста 1
        zamena_2_2 = str(self.lineEdit_zamen_text_2_2.text()) #Отправка уведомлений замена текста 1 -> 1
        periods = str(self.lineEdit_period.text()) #периодичность
        find_text = str(self.lineEdit_find_text.text()) #поиск по слову


        with open(self.file_name, 'w', encoding='utf-8') as file:
            file.write('Кол постов: ' + count_post +
                       '\nCсылка на канал: ' + url +
                       '\nТокен: ' + token +
                       '\nChatID: ' + chat_id +
                       '\nСлово1-1: ' + zamena_1 +
                       '\nСлово1-2: ' + zamena_1_1 +
                       '\nСлово2-1: ' + zamena_2 +
                       '\nСлово2-2: ' + zamena_2_2 +
                       '\nИнтервал: ' + periods +
                       '\nПоиск по слову: ' + find_text )
        file.close()
        self.good_write()

    #замена в песочнице
    def replace_file(self):
        a = self.lineEdit_pesoch_text_1.text() # заменяемый текст
        b = self.lineEdit_pesoch_text_2.text() # заменить на текст
        c = self.textEdit_p.toPlainText()
        self.textEdit_p.clear()
        text = c.replace(a,b)
        self.textEdit_p.append(f'{self.date_time()}\n{text}')

    #очистка пеочницы
    def clear_tab(self):
        self.textEdit_p.clear()
        self.lineEdit_pesoch_text_1.clear()
        self.lineEdit_pesoch_text_2.clear()


    #парсинг телеграм
    def write_file(self):
        self.textEdit_p.clear()
        cmd_str = "snscrape --max-results "+str(self.chng_count_post.text())+" --jsonl telegram-channel "+str(self.chng_url.text()).replace('https://t.me/','')+"  > "+str(self.file_name_text_parser)
        subprocess.run(cmd_str, shell=True)


    #успешно
    def good_write(self):
        good = QMessageBox()
        good.setWindowTitle('Успешно')
        good.setText('Данные успешно сохранены')
        # good.setIcon(QMessageBox.Accepted)
        good.exec_()
        # self.close()

    #ошибка
    def error_not_text(self):
        good = QMessageBox()
        good.setWindowTitle('Ошибка')
        good.setText('Посты не обнаружены. Проблема связана с некорректным указаниям группы, либо группа закрыта')
        # good.setIcon(QMessageBox.Accepted)
        good.exec_()
        # self.close()

    # ошибка
    def error_write(self):
        error = QMessageBox()
        error.setWindowTitle('Ошибка!!!')
        error.setText('Заполнены не все обязательные поля')
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Close)
        error.exec_()



    def stop_telegram(self):
        self.btn_stop_telegram.setEnabled(False)
        self.btn_start_telegram.setEnabled(True)
        print("False")
        self.stop_theardss = False
        self.base_del_text_parser()

    def start_telegram(self):
        self.btn_stop_telegram.setEnabled(True)
        self.btn_start_telegram.setEnabled(False)
        self.stop_theardss = True
        self.text_input()
        self.write_file()  # просметреть все посты
        self.time_a = int(self.lineEdit_period.text())
        t1 = threading.Thread(target=self.test)
        t1.start()

    def test(self):
        while self.stop_theardss:
            try:
                self.connection()
            except:
                print('Ошибка')
                self.app.exec_()
            self.func_start_telegram()
            try:
                time.sleep(self.time_a * 60)
            except:
                time.sleep(60)


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    app.exec_()


if __name__ == "__main__":
    application()

