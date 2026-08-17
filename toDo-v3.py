import sys
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QStackedWidget, 
    QVBoxLayout, 
    QLabel, 
    QPushButton,
    QMessageBox,
    QApplication, QCheckBox, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QSlider, QProgressBar, QComboBox, QListWidget, QTableWidget, QTableWidgetItem, QTabWidget, QStackedWidget, QToolBox, QScrollArea, QGroupBox, QFormLayout, QHBoxLayout, QInputDialog
)
import ast
from datetime import datetime
#import all the elements you want to use from PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# Class for task item; global
class taskItem:
    # contructor method
    def __init__(self, title, list, description = '', completed = False, archive = False): #only required input is a title to create a task
        self.title = title
        self.list = list
        self.description = description
        self.completed = completed
        self.archive = archive
        # self.dateCreated = datetime.now()
        # self.dateEdited = datetime.now()
        # self.dateCompleted = None
        # self.dateArchived = None

# screen ONE, tasks
class tasksScreen(QWidget):
    """The layout and logic for the first screen."""
    def __init__(self, controller):
        super().__init__()
    #COMPONENTS DEFINED:
        # new task input and button
        self.newTaskInput = QLineEdit()
        self.newTaskInput.setPlaceholderText("New task")
        self.addTaskButton = QPushButton("Add")
        self.addTaskButton.clicked.connect(lambda: self.addTaskToList(self.newTaskInput.text(), self.comboBox.currentText()))
        self.addTaskButton.setObjectName('addButton')

        # save button
        self.saveButton = QPushButton("Save")
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.writeTaskListToFile)

        # combobox and edit button
        self.comboBox = QComboBox()
        self.comboBox.addItems(['All tasks', 'Create new list'])
        self.comboBox.currentTextChanged.connect(self.createNewList)
        self.editButton = QPushButton("Edit")
        self.editButton.setObjectName("editButton")
        self.editButton.clicked.connect(controller.show_second_screen)
        
    #LAYOUTS DEFINED:       
        # newTaskLayout
        self.newTaskLayout = QHBoxLayout()
        self.newTaskLayout.addWidget(self.newTaskInput)
        self.newTaskLayout.addWidget(self.addTaskButton)
        self.newTaskLayout.setSpacing(8)
        
        # taskLayout
        self.taskLayout = QVBoxLayout()
        self.taskLayout.setSpacing(8)
        self.taskLayout.setObjectName('taskLayout')

        # combobox and edit button layout
        self.horizontalButtonsLayout = QHBoxLayout()
        self.horizontalButtonsLayout.addWidget(self.editButton)
        self.horizontalButtonsLayout.addWidget(self.comboBox)
        self.horizontalButtonsLayout.setSpacing(8)

        # contentLayout
        self.contentLayout = QVBoxLayout(self)
        self.contentLayout.setObjectName('contentLayout')
        # restoring margins and spacing for the main content area, w/out titlebar:
        self.contentLayout.setContentsMargins(20, 20, 20, 20)
        self.contentLayout.setSpacing(20)
        self.contentLayout.addLayout(self.horizontalButtonsLayout)
        self.contentLayout.addLayout(self.newTaskLayout)
        self.contentLayout.addLayout(self.taskLayout)
        self.contentLayout.addWidget(self.saveButton)
        self.contentLayout.addStretch()


    #STYLES DEFINED:
        self.setStyleSheet("""
            #contentLayout {
                min-width: 300px;
            } 

            QLineEdit {
                font-size: 16px;
                padding: 6px;
                border: 1px solid lightgrey;
                border-radius: 8px;
                background-color: white;
            }

            QComboBox{
                font-size: 14px;
                padding: 6px;
                border: 0px solid grey;
                border-radius: 8px;
                background-color: white;
            }

            QComboBox::drop-down{
                background: transparent;
            }
            QComboBox::down-arrow {
                image: url("arrow.svg");
                width: 12px;
                height: 12px;
                padding-right: 12px;
            }

            #addButton {
                font-size: 16px;
                padding: 6px;
                background-color: blue;
                color: white;
                border: 0px solid black;
                border-radius: 8px;
                min-width: 40px;
            }
            #addButton:hover {
                background-color: darkblue;
                color: white;
                border: 2px solid #f3f3f3;
                border-radius: 10px;
            }

            #saveButton {
                font-size: 16px;
                padding: 6px;
                background-color: blue;
                color: white;
                border: 0px solid black;
                border-radius: 8px;
            }
            #saveButton:hover {
                background-color: darkblue;
                color: white;
                border: 2px solid #f3f3f3;
                border-radius: 10px;
            }

            #editButton {
                font-size: 14px;
                padding: 6px;
                background-color: blue;
                color: white;
                border: 0px solid black;
                border-radius: 8px;
                max-width: 40px;
            }
            #editButton:hover {
                background-color: darkblue;
                color: white;
                border: 2px solid #f3f3f3;
                border-radius: 10px;
            }

            QCheckBox {
                border-radius: 5px;
                padding: 6px;
                font-size: 16px;
                }
            
            QCheckBox:hover {
                background-color: lightgrey;
            }
            
            QCheckBox:checked {
                background-color: lightblue;
                color:grey;
                font-style: italic;
                }      
            
            #deleteButton {
                font-size: 12px;
                text-align:center;
                background-color: lightgrey;
                border: 0px solid black;
                border-radius: 8px;
                max-height: 28px;
                max-width: 28px;
            }
            #deleteButton:hover {
                background-color: lightcoral;
                color: white;
                }

            """)


    #INITIALIZATION:
        # Filler task items for demonstration purposes
        try:
            with open("taskList.txt", "r") as self.file:
                self.taskList = []
                # read the file and re-create the taskList variable
                for line in self.file:
                    myList = line.split(',')
                    #### BUG: what if user creates a list with a ',' in it
                    completed = myList[3] == "True"
                    archive = myList[4] == "True"
                    self.taskList.append(taskItem(myList[0],myList[1],myList[2],completed, archive))
        except FileNotFoundError:
            with open("taskList.txt", "w") as self.file:
                self.taskList = []
        listNames = []
        for task in self.taskList:
            if task.list not in listNames:
                listNames.append(task.list)
        index = self.comboBox.count()-1
        for name in listNames:
            self.comboBox.insertItem(index, name)
            #### BUG: if a list is created but no task is added, it will not save
        self.refreshTaskList()

# Methods
    def addTaskToList(self, task, list):
        self.createTask(task, list)
        self.newTaskInput.setText('')
    def createTask(self, task, list):
        newInstance = taskItem(task, list)
        self.taskList.append(newInstance)
        self.refreshTaskList()
    def deleteTask(self, task):
        self.taskList.remove(task)
        self.refreshTaskList()
    def writeTaskListToFile(self):
        with open("taskList.txt", "w") as self.file:
            count = 0
            for item in self.taskList:
                self.file.write(
                    str(self.taskList[count].title) + ',' +
                    str(self.taskList[count].list) + ',' +
                    str(self.taskList[count].description) + ',' +
                    str(self.taskList[count].completed) + ',' +
                    str(self.taskList[count].archive) + '\n'
                )
                count += 1
    def toggleCheckbox(self, task, checked):
        task.completed = checked
    def getComboBoxItems(self):
        return [
        self.comboBox.itemText(i)
        for i in range(self.comboBox.count())]
    def createNewList(self):
        if self.comboBox.currentText() == 'Create new list':
            text, ok = QInputDialog.getText(self, 'Task Title', 'Task title:')
            if ok and text:
                index = self.comboBox.count() -1
                self.comboBox.insertItem(index, text)
                self.comboBox.setCurrentText(self.comboBox.setCurrentIndex(index))
                self.refreshTaskList()
        #### BUG: else block creates pop-ups for all list items.
            else:
                self.comboBox.setCurrentText(self.comboBox.setCurrentIndex(0))
                self.refreshTaskList()
        else:
            self.refreshTaskList()
    def refreshTaskList(self):
        # Clear old widgets; got this snippet from https://gist.github.com/JokerMartini/7fe4f204b6a7912be3ac
        for i in reversed(range(self.taskLayout.count())):
            item = self.taskLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    # If the item is a layout, clear its widgets
                    layout = item.layout()
                    if layout is not None:
                        while layout.count():
                            child_item = layout.takeAt(0)
                            if child_item.widget():
                                child_item.widget().setParent(None)
        # Rebuild the list
        if self.comboBox.currentText() == 'All tasks':
            for task in self.taskList:
                # row layout
                rowLayout = QHBoxLayout()
                self.taskLayout.setSpacing(12)
                taskButton = QCheckBox(task.title)
                taskButton.setChecked(task.completed)
                taskButton.toggled.connect(lambda checked, t=task: self.toggleCheckbox(t, checked))
                rowLayout.addWidget(taskButton)
                deleteButton = QPushButton("✕")
                deleteButton.clicked.connect(lambda checked=False, t=task: self.deleteTask(t))
                deleteButton.setObjectName("deleteButton")
                rowLayout.addWidget(deleteButton)
                self.taskLayout.addLayout(rowLayout)
        else:
            for task in self.taskList:
                if task.list == self.comboBox.currentText():
                    # row layout
                    rowLayout = QHBoxLayout()
                    self.taskLayout.setSpacing(12)
                    taskButton = QCheckBox(task.title)
                    taskButton.setChecked(task.completed)
                    taskButton.toggled.connect(lambda checked, t=task: self.toggleCheckbox(t, checked))
                    rowLayout.addWidget(taskButton)
                    deleteButton = QPushButton("✕")
                    deleteButton.clicked.connect(lambda checked=False, t=task: self.deleteTask(t))
                    deleteButton.setObjectName("deleteButton")
                    rowLayout.addWidget(deleteButton)
                    self.taskLayout.addLayout(rowLayout)

# screen TWO, lists
class listsScreen(QWidget):
    """The layout and logic for the second screen."""
    def __init__(self, controller):
        super().__init__()
        # saving the controller so the getComboBoxItems method will work later
        self.controller = controller
    #COMPONENTS DEFINED:
        # QLabel
        self.listLabel = QLabel("Your lists")
        # save back buttons
        self.saveButton = QPushButton("Save")
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.saveListUpdates)
        self.backButton = QPushButton("Back")
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(controller.show_first_screen)


    #LAYOUTS DEFINED:
        # listLayout
        self.listLayout = QVBoxLayout()
        self.listLayout.setSpacing(8)
        self.listLayout.setObjectName('listLayout')
        
        # layout
        self.horizontalButtonsLayout = QHBoxLayout()
        self.horizontalButtonsLayout.addWidget(self.backButton)
        self.horizontalButtonsLayout.addWidget(self.saveButton)

        # contentLayout
        self.contentLayout = QVBoxLayout(self)
        self.contentLayout.setObjectName("contentLayout")
        # restoring margins and spacing for the main content area, w/out titlebar:
        self.contentLayout.setContentsMargins(20, 20, 20, 20)
        self.contentLayout.setSpacing(20)
        self.contentLayout.addWidget(self.listLabel)
        self.contentLayout.addLayout(self.listLayout)
        self.contentLayout.addLayout(self.horizontalButtonsLayout)
        self.contentLayout.addStretch()

    #STYLES DEFINED:
        self.setStyleSheet("""
        #contentLayout {
            min-width: 300px;
        }  
    
        QLineEdit {
            font-size: 16px;
            padding: 6px;
            border: 1px solid lightgrey;
            border-radius: 8px;
            background-color: white;
        }

        QLabel {
            font-size: 16px;
        }

        #addButton {
            font-size: 16px;
            padding: 6px;
            background-color: blue;
            color: white;
            border: 0px solid black;
            border-radius: 8px;
            min-width: 40px;
        }
        #addButton:hover {
            background-color: darkblue;
            color: white;
            border: 2px solid #f3f3f3;
            border-radius: 10px;
        }
    
        #saveButton {
            font-size: 16px;
            padding: 6px;
            background-color: blue;
            color: white;
            border: 0px solid black;
            border-radius: 8px;
        }
        #saveButton:hover {
            background-color: darkblue;
            color: white;
            border: 2px solid #f3f3f3;
            border-radius: 10px;
        }

        #backButton {
            font-size: 16px;
            padding: 6px;
            background-color: lightgrey;
            color: black;
            border: 0px solid black;
            border-radius: 8px;
        }

        #backButton:hover {
            background-color: grey;
            color: white;
            border: 1px solid white;
            border-radius: 10px;
        }     
        
        #deleteButton {
            font-size: 12px;
            text-align:center;
            background-color: lightgrey;
            border: 0px solid black;
            border-radius: 8px;
            max-height: 28px;
            min-width: 28px;
        }
        #deleteButton:hover {
            background-color: lightcoral;
            color: white;
            }
    
        """)

    #INITIALIZATION:
        self.refreshListNames()

# Methods
    def deleteList(self, deleteItem):
        areYouSure = QMessageBox.question(None, 'Delete List?', 'Are you sure you want to delete ' + str(deleteItem) + '?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if areYouSure == QMessageBox.StandardButton.Yes:
            # basically just refreshListNames() but skip over the item, then update the list based on the display.
            # Clear old widgets; got this snippet from https://gist.github.com/JokerMartini/7fe4f204b6a7912be3ac
            for i in reversed(range(self.listLayout.count())):
                item = self.listLayout.itemAt(i)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
                    else:
                        # If the item is a layout, clear its widgets
                        layout = item.layout()
                        if layout is not None:
                            while layout.count():
                                child_item = layout.takeAt(0)
                                if child_item.widget():
                                    child_item.widget().setParent(None)
            # Rebuild the list
            for item in self.controller.tasksScreen.getComboBoxItems():
                if item != 'All tasks' and item != 'Create new list' and item != deleteItem:
                    # row layout
                    rowLayout = QHBoxLayout()
                    self.listLayout.setSpacing(12)
                    listButton = QLineEdit(item)
                    deleteButton = QPushButton("✕")
                    deleteButton.clicked.connect(lambda checked=False, t=item: self.deleteList(t))
                    deleteButton.setObjectName("deleteButton")
                    #layout
                    rowLayout.addWidget(listButton)
                    rowLayout.addWidget(deleteButton)
                    self.listLayout.addLayout(rowLayout)
            # update list of lists with the current data
            self.controller.tasksScreen.comboBox.clear()
            newList = []
            for i in range(self.listLayout.count()):
                item = self.listLayout.itemAt(i)
                rowLayout = item.layout()
                if rowLayout is None:
                    continue
                listItem = rowLayout.itemAt(0)
                if listItem is None:
                    continue
                listButton = listItem.widget()
                if listButton is not None:
                    newList.append(listButton.text())
            newList.insert(0, 'All tasks')
            newList.insert(len(newList), 'Create new list')
            self.controller.tasksScreen.comboBox.addItems(newList)
            # delete any task items that's taskItem.list is not in the new list
            # looping over a copy of taskList so that any deleted items dont mess with the looping index
            for task in self.controller.tasksScreen.taskList.copy():
                if task.list not in newList:
                    self.controller.tasksScreen.taskList.remove(task)
            # update file to match
            self.controller.tasksScreen.writeTaskListToFile()
            self.controller.tasksScreen.refreshTaskList()
    def saveListUpdates(self):
        # update list of lists with the current data
        # build current list
        currentList = []
        for i in range(self.controller.tasksScreen.comboBox.count()):
            listName = self.controller.tasksScreen.comboBox.itemText(i)
            currentList.append(listName)
        # build the new list (based on screen display/changes)
        newList = []
        for i in range(self.listLayout.count()):
            item = self.listLayout.itemAt(i)
            rowLayout = item.layout()
            if rowLayout is None:
                continue
            listItem = rowLayout.itemAt(0)
            if listItem is None:
                continue
            listButton = listItem.widget()
            if listButton is not None:
                newList.append(listButton.text())
        newList.insert(0, 'All tasks')
        newList.insert(len(newList), 'Create new list')
        # compare the lists
        index = 0
        for name in currentList:
            if name != newList[index]:
                for task in self.controller.tasksScreen.taskList:
                #### BUG: Does not write to file
                    if task.list == name:
                        task.list = newList[index]
            index += 1
        self.controller.tasksScreen.comboBox.clear()
        self.controller.tasksScreen.comboBox.addItems(newList)
        # update file to match
        self.controller.tasksScreen.writeTaskListToFile()
    def refreshListNames(self):
        # Clear old widgets; got this snippet from https://gist.github.com/JokerMartini/7fe4f204b6a7912be3ac
        for i in reversed(range(self.listLayout.count())):
            item = self.listLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    # If the item is a layout, clear its widgets
                    layout = item.layout()
                    if layout is not None:
                        while layout.count():
                            child_item = layout.takeAt(0)
                            if child_item.widget():
                                child_item.widget().setParent(None)
        # Rebuild the list
        for item in self.controller.tasksScreen.getComboBoxItems():
            if item != 'All tasks' and item != 'Create new list':
                # row layout
                rowLayout = QHBoxLayout()
                self.listLayout.setSpacing(12)
                listButton = QLineEdit(item)
                deleteButton = QPushButton("✕")
                deleteButton.clicked.connect(lambda checked=False, t=item: self.deleteList(t))
                deleteButton.setObjectName("deleteButton")
                #layout
                rowLayout.addWidget(listButton)
                rowLayout.addWidget(deleteButton)
                self.listLayout.addLayout(rowLayout)

# main window
class MainWindow(QMainWindow):
    """The central manager handling screen navigation."""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("To-Do List")
        self.setWindowIcon(QIcon("resume.ico"))

        #title bar label and buttons
        title = QLabel("To-Do List")
        minButton = QPushButton("−")
        minButton.clicked.connect(self.showMinimized)
        closeButton = QPushButton("✕")
        closeButton.clicked.connect(self.closeButton)

        # content layout
        content = QWidget()
        content.setObjectName('mainContent')
        self.contentLayout = QVBoxLayout(content)
        # restoring margins and spacing for the main content area, w/out titlebar:

        # titleBar layout
        titleBar = QWidget()
        titleBarLayout = QHBoxLayout(titleBar)
        titleBar.setObjectName("titleBar")
        titleBar.setFixedHeight(40)
        titleBarLayout.addWidget(title)
        titleBarLayout.addWidget(minButton)
        titleBarLayout.addWidget(closeButton)

        # main window container layout
        container = QWidget()
        self.setCentralWidget(container)
        layoutVertical = QVBoxLayout(container)
        layoutVertical.setContentsMargins(0, 0, 0, 0)
        layoutVertical.setSpacing(0)
        layoutVertical.addWidget(titleBar)
        layoutVertical.addWidget(content)

        
        # stack
        self.stacked_widget = QStackedWidget()
        self.contentLayout.addWidget(self.stacked_widget)

        # screens
        self.tasksScreen = tasksScreen(self)
        self.listsScreen = listsScreen(self)

        # add screens to stack
        self.stacked_widget.addWidget(self.tasksScreen)  # Index 0
        self.stacked_widget.addWidget(self.listsScreen)  # Index 1
        
        # Set the default starting screen
        self.stacked_widget.setCurrentWidget(self.tasksScreen)

        self.setStyleSheet("""
            #mainContent {
                min-width: 300px;
                margin:10px;
            } 
            #titleBar {
                background-color: transparent;
                padding:0px;
                }

            #titleBar QLabel {
                font-size: 14px;
                background-color: transparent;}
            
            #titleBar QPushButton {
                background-color: transparent;
                border: 1px solid black;
                border-radius: 0px;
                color: black;
                border: none;
                font-size: 12px;
                padding: 6px;
                max-width: 20px;
                }

            #titleBar QPushButton:hover {
                background-color: lightgrey;
                color: black;}
            #titleBar QPushButton:pressed {
                background-color: grey;
                border: 1px solid black;
                color: black;
                }

            """)


    #title bar functions
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(
                self.pos()
                + event.globalPosition().toPoint()
                - self.dragPos
            )
            self.dragPos = event.globalPosition().toPoint()
    def closeButton(self):
            self.close()

    # screen functions
    def show_first_screen(self):
        """Switches the view to the first page layout."""
        self.stacked_widget.setCurrentIndex(0)
    def show_second_screen(self):
        """Switches the view to the second page layout."""
        self.stacked_widget.setCurrentIndex(1)
        #refresh, so any changes made but not saved will not appear
        self.listsScreen.refreshListNames()


# run app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
