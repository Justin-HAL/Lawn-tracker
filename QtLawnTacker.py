import tkinter as tk
from tkinter import filedialog
import pandas as pd

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys



class MyWindow(QMainWindow):
   
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(50, 50, 500, 500)
        self.MAX_row = 0
        self.current_row = 0
        self.df = pd.DataFrame()
        self.File_read = False

        self.Central_widget = QWidget()
        self.setCentralWidget(self.Central_widget)
        self.initUI()

    def initUI(self):
        mainLayout = QtWidgets.QVBoxLayout()

        topLayout = QtWidgets.QHBoxLayout()
        middlelayout = QtWidgets.QGridLayout()
        bottomlayout = QtWidgets.QHBoxLayout()
#add to top layout
        self.open_file_button = QtWidgets.QPushButton(self)

        self.open_file_button.clicked.connect(self.open_file)
        self.open_file_button.setText('Load schedule')
        self.open_file_button.adjustSize()
        topLayout.addWidget(self.open_file_button)

        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setText('save data')
        self.save_button.clicked.connect(self.save_data_to_file)
        topLayout.addWidget(self.save_button)

        mainLayout.addLayout(topLayout)
        self.Central_widget.setLayout(mainLayout)

#data in middle layout:
        #data titles
        middlelayout.addWidget(QtWidgets.QLabel('Address:'), 0,0)
        middlelayout.addWidget(QtWidgets.QLabel('Name:'), 1,0)
        middlelayout.addWidget(QtWidgets.QLabel('Start Time'), 2,0)
        middlelayout.addWidget(QtWidgets.QLabel('End Time:'), 3,0)
        
        #data labels to write to:
        self.data_address = QtWidgets.QLabel('')
        self.data_address.adjustSize()

        self.data_name = QtWidgets.QLabel('')
        self.data_name.adjustSize()

        self.data_start_box = QtWidgets.QLineEdit()
        self.data_end_box = QtWidgets.QLineEdit()
        middlelayout.addWidget(self.data_address, 0,1)
        middlelayout.addWidget(self.data_name,1,1)
        middlelayout.addWidget(self.data_start_box, 2,1)
        middlelayout.addWidget(self.data_end_box,3,1)
        mainLayout.addLayout(middlelayout)

#bottem layout
        self.button_prev = QtWidgets.QPushButton("Prevous")
        self.button_prev.clicked.connect(self.prev_house)

        self.button_save = QtWidgets.QPushButton("Save times")
        self.button_save.clicked.connect(self.save_to_data_frame)

        self.button_next = QtWidgets.QPushButton("Next")
        self.button_next.clicked.connect(self.next_house)

        bottomlayout.addWidget(self.button_prev)
        bottomlayout.addWidget(self.button_save)
        bottomlayout.addWidget(self.button_next)
        mainLayout.addLayout(bottomlayout)
    def open_file(self):
    # Open file dialog and get the selected file path
        file_path = filedialog.askopenfilename()
        if file_path:
            #with open(file_path, 'r') as file
            self.df = pd.read_csv(file_path)
            self.current_row = 0
            self.MAX_row = len(self.df.index)
            self.File_read = True
            self.display()
    
    def display(self):
        if self.File_read:
            self.data_address.setText(self.df.iat[self.current_row,0])
            self.data_name.setText(self.df.iat[self.current_row,1])
            self.data_start_box.setText(str(self.df.iat[self.current_row,2]))
            self.data_end_box.setText(str(self.df.iat[self.current_row,3]))

    def save_to_data_frame(self):
        if self.File_read:
            start_time = int(self.data_start_box.text())
            end_time =  int(self.data_end_box.text())
            self.df.iat[self.current_row,2] = start_time
            self.df.iat[self.current_row,3] = end_time

    def next_house(self):
        if self.current_row < self.MAX_row -1:
            self.current_row += 1
            self.display()

    def prev_house(self):
        if self.current_row  > 0:
            self.current_row -= 1
            self.display()

    def save_data_to_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save DataFrame", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.df.to_csv(file_path, index=False)
            print(f"DataFrame saved to {file_path}")


def window():
    app = QApplication(sys.argv)
    win = MyWindow()


    win.update()
    win.show()
    sys.exit(app.exec_())

window()