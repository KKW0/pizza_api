import json
import sys

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt


tick = QtGui.QImage("tick.png")


class TodoModel(QtCore.QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.todos[index.row()]
            return text

        if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.todos)


class QtableView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Todo List")
        self.resize(400, 400)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.todoView = QtWidgets.QListView(self.centralwidget)
        self.verticalLayout.addWidget(self.todoView)

        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setText("Add")
        self.buttonLayout.addWidget(self.addButton)

        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setText("Delete")
        self.buttonLayout.addWidget(self.deleteButton)

        self.completeButton = QtWidgets.QPushButton(self.centralwidget)
        self.completeButton.setText("Complete")
        self.buttonLayout.addWidget(self.completeButton)

        self.verticalLayout.addLayout(self.buttonLayout)

        self.todoEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.todoEdit)

        self.model = TodoModel()
        self.load()
        self.todoView.setModel(self.model)
        self.addButton.clicked.connect(self.add)
        self.deleteButton.clicked.connect(self.delete)
        self.completeButton.clicked.connect(self.complete)

    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def load(self):
        try:
            with open("data.json", "r") as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open("data.json", "w") as f:
            data = json.dump(self.model.todos, f)


app = QtWidgets.QApplication(sys.argv)
window = QtableView()
window.show()
app.exec_()

