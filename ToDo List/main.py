from functools import partial

from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import database

class ToDo(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load('MainWindow.ui', None)
        self.ui.show()
        
        self.ui.add_btn.clicked.connect(self.addNewTaskToDatabase)

        self.readFromDatabase()

        self.warning_mg_box = QMessageBox()
        self.warning_mg_box.setWindowTitle('Warning!')
        self.warning_mg_box.setText("Something went wrong, Please check database")
    
    def readFromDatabase(self):
        try:
            layout = self.ui.gridLayout
            layout_2 = self.ui.gridLayout_2
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)

            for i in reversed(range(layout_2.count())): 
                layout_2.itemAt(i).widget().setParent(None)

            results = database.getAll()
            
            for i in range(len(results)):
                new_checkbox = QCheckBox()
                new_checkbox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
                new_checkbox.clicked.connect(partial(self.doneOrNot, new_checkbox, results[i][0]))
                if results[i][3] == 1:
                    new_checkbox.setChecked(True)
                
                new_task_btn = QPushButton()
                new_task_btn.setText(results[i][1])
                if results[i][6] == 1:
                    new_task_btn.setStyleSheet('background-color: rgb(232, 76, 61); color: rgb(253, 252, 255)')
                else:
                    new_task_btn.setStyleSheet('background-color: rgb(84, 80, 214); color: rgb(253, 252, 255)')
                
                new_task_btn.clicked.connect(partial(self.showTaskDetails,results[i][1], results[i][2], results[i][4], results[i][5]))

                new_delete_btn = QPushButton()
                new_delete_btn.setText('❌')
                new_delete_btn.setStyleSheet('background-color: rgb(84, 80, 214)')
                new_delete_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
                new_delete_btn.clicked.connect(partial(self.deleteTaskFromDatabase, results[i][0]))
                
                if results[i][3] == 0:
                    self.ui.gridLayout_2.addWidget(new_checkbox, i, 0)
                    self.ui.gridLayout_2.addWidget(new_task_btn, i, 1)
                    self.ui.gridLayout_2.addWidget(new_delete_btn, i, 2)
                
                elif results[i][3] == 1:
                    self.ui.gridLayout.addWidget(new_checkbox, i, 0)
                    self.ui.gridLayout.addWidget(new_task_btn, i, 1)
                    self.ui.gridLayout.addWidget(new_delete_btn, i, 2)
        except:
            mg_box = QMessageBox()
            mg_box.setWindowTitle('Warning!')
            mg_box.setText("Can't load the database, please try again")
            mg_box.exec()

    def doneOrNot(self, checkbox ,id):
        try:
            if checkbox.isChecked():
                database.editDone(id, 1)
            else:
                database.editDone(id, 0)
            self.readFromDatabase()
        except:
            self.warning_mg_box.exec()
    
    def deleteTaskFromDatabase(self, id):
        try:
            database.deleteTask(id)
            mg_box = QMessageBox()
            mg_box.setWindowTitle('Delete')
            mg_box.setText('Task Deleted Successfully ✅')
            mg_box.exec()
            self.readFromDatabase()
        except:
            self.warning_mg_box.exec()
    
    def addNewTaskToDatabase(self):
        try:
            title = self.ui.tb_title.text()
            if title == '':
                mg_box = QMessageBox()
                mg_box.setWindowTitle('Warning!')
                mg_box.setText('You need to set a Title for your task!')
                mg_box.exec()
            else: 
                description = self.ui.tb_description.text()
                time = self.ui.tb_time.text()
                date = self.ui.tb_date.text()
                done = 0

                if self.ui.checkbox_priority.isChecked():
                    priority = 1
                else:
                    priority = 0
                
                results = database.getAll()
                id = 1
                generate_id = True
                while generate_id :
                    for i in range(len(results)):
                        if id == results[i][0]:
                            id += 1
                            generate_id = True
                        elif id != results[i][0]:
                            generate_id = False
                
                database.add(id, title, description, done, time, date, priority)

                self.readFromDatabase()
                self.ui.checkbox_priority.setChecked(False)

                self.ui.tb_title.setText('')
                self.ui.tb_description.setText('')
                self.ui.tb_time.setText('')
                self.ui.tb_date.setText('')
        except:
            self.warning_mg_box.exec()

    def showTaskDetails(self, title, description, time, date):
        try:
            mg_box = QMessageBox()
            mg_box.setWindowTitle(f'{title}')
            mg_box.setText(f'Title : {title}\nDescription : {description}\nTime : {time}\nDate : {date}')
            mg_box.exec()
        except:
            self.warning_mg_box.exec()
    
app = QApplication([])
window = ToDo()
app.exec()