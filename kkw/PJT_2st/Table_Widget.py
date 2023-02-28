import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView

class Table_widget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.edit = QLineEdit()
        self.edit.textChanged.connect(self.filter)
        layout.addWidget(self.edit)

        data = [
            ('France', 'Paris', 'Paris', 'Paris'),
            ('United Kingdom', 'London', 'Paris', 'Paris'),
            ('Italy', 'Rome', 'Paris', 'Paris'),
            ('Korea', 'Rome', 'Paris', 'Paris'),
            ('US', 'Rome', 'Paris', 'Paris'),
            ('Germany', 'Berlin', 'Paris', 'Paris')
        ]

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(6)

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Project', 'Due Date', 'Comment', 'Description'])

        for row in range(6):
            for column in range(4):
                item = QTableWidgetItem(data[row][column])
                self.tableWidget.setItem(row, column, item)

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def filter(self, filter_text):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.tableWidget.setRowHidden(i, match)
                if not match:
                    break
# ----------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    dlg = Table_widget()
    dlg.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()