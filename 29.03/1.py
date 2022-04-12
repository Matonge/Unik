import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, \
 QSystemTrayIcon, QStyle, QAction, qApp, QMenu
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from calendar import Calendar
from delayed_alarms import Delayed_Alarms
import ctypes
import PyQt5.QtGui

class Alarm(QMainWindow):
    tray_icon = None
    def __init__(self):
        super().__init__()
        self.initUI()
        self.alarms_list = []


    def initUI(self):

        loadUi('Budilnik.ui', self)
        self.setWindowTitle('Будильник')
        self.setWindowIcon(QIcon('clock.png'))
        self.setStyleSheet("background-color: #FFFFFF")
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Установка полей выбора повтора сигнала
        self.comboBox.addItem("Никогда")
        self.comboBox.addItem("Каждый понедельник")
        self.comboBox.addItem("Каждый вторник")
        self.comboBox.addItem("Каждую среду")
        self.comboBox.addItem("Каждый четверг")
        self.comboBox.addItem("Каждую пятницу")
        self.comboBox.addItem("Каждую субботу")
        self.comboBox.addItem("Каждое воскресенье")

        # self.sound = QSound('C:\Users\AAA\Desktop\Мелодии для будильника\ 1595432.wav')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.current_time)
        self.timer.singleShot(1000, self.current_time)

        #создание меню в трее
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('clock.png'))

        show_action = QAction("Show", self)  # показать
        hide_action = QAction("Hide", self)  # скрыть
        quit_action = QAction("Quit", self)  # выйти

        #привязка пункта меню к действию
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu(self)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        tray_menu.addAction(hide_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        show_calendar = QAction("Показать календарь", self) #Отображение окна с календарём
        show_calendar.triggered.connect(self.set_calendar)
        self.menu_3.addAction(show_calendar)

        show_alarms = QAction("Все установленные будильники", self) #Отображение окна с установленными будильниками
        show_alarms.triggered.connect(self.set_alarms)
        self.menu_2.addAction(show_alarms)

        self.pushButton_2.clicked.connect(self.add_alarms)

    def closeEvent(self, event):
        if self.checkBox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Фоновый режим",
                "Приложение скрыто в фоновый режим",
                QSystemTrayIcon.Information,
                3000
            )

    def set_calendar(self):
        self.window_2 = Calendar()
        self.window_2.show()

    def set_alarms(self):
        self.delay_alarms = Delayed_Alarms(self)
        self.delay_alarms.show()

    def current_time(self):
        time = QtCore.QTime.currentTime()  # Установка актуального времени
        self.timeEdit.setTime(time)


        date = QtCore.QDate.currentDate()  # Установка актуальной даты
        self.dateEdit.setDate(date)

    def add_alarms(self):
        time = self.timeEdit.text()
        date = self.dateEdit.text()
        self.alarms_list.append(time)
        self.alarms_list.append(date)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('clock.png'))
    ex = Alarm()
    ex.show()
    sys.exit(app.exec())