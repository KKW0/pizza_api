from PySide2.QtWidgets import QMainWindow, QTableView, QComboBox, QStyledItemDelegate
from PySide2 import QtWidgets, QtCore, QtGui


class WrapDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data(QtCore.Qt.DisplayRole)
        document = QtGui.QTextDocument()
        document.setHtml(text)
        document.setTextWidth(option.rect.width())
        option.text = ""
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)

    def sizeHint(self, option, index):
        text = index.data(QtCore.Qt.DisplayRole)
        document = QtGui.QTextDocument()
        document.setHtml(text)
        document.setTextWidth(option.rect.width())
        return QtCore.QSize(document.idealWidth(), document.size().height())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)

        self.table_view = QTableView(self)
        self.table_view.move(10, 50)
        self.table_view.resize(300, 200)

        self.combo_box = QComboBox(self.table_view.horizontalHeader())
        self.combo_box.setGeometry(0, 0, 100, 30)
        self.combo_box.addItems(['All', 'Option 1', 'Option 2'])
        self.combo_box.currentIndexChanged.connect(self.filter_list)

        self.combo_box2 = QComboBox(self)
        self.combo_box2.move(340, 10)
        self.combo_box2.resize(100, 30)
        self.combo_box2.addItems(['All', 'Option A', 'Option B'])
        self.combo_box2.currentIndexChanged.connect(self.filter_list_col2)

        self.model = QtGui.QStandardItemModel()
        self.model.appendRow([QtGui.QStandardItem('Option 1'), QtGui.QStandardItem('Option A')])
        self.model.appendRow([QtGui.QStandardItem('Option 1'), QtGui.QStandardItem('Option B')])
        self.model.appendRow([QtGui.QStandardItem('Option 2'), QtGui.QStandardItem('Option A')])
        self.model.appendRow([QtGui.QStandardItem('Option 1'), QtGui.QStandardItem('Option A')])

        self.model.setHorizontalHeaderLabels(['Column 1', 'Column 2'])
        self.table_view.setModel(self.model)
        # self.table_view.verticalHeader().hide()
        self.table_view.setAlternatingRowColors(True)
        self.setCentralWidget(self.table_view)

        delegate = WrapDelegate(self.combo_box)
        self.table_view.horizontalHeader().setItemDelegateForColumn(0, delegate)

    def filter_list(self, index):
        option = self.combo_box.currentText()
        option2 = self.combo_box2.currentText()

        proxy_model = QtCore.QSortFilterProxyModel()
        proxy_model.setSourceModel(self.model)

        if option != 'All':
            proxy_model.setFilterRegExp('^{}$'.format(option))
            proxy_model.setFilterKeyColumn(0)
            self.combo_box2.setDisabled(False)
        else:
            self.combo_box2.setCurrentIndex(0)
            option2 = 'All'
            self.combo_box2.setDisabled(True)

        if option2 != 'All':
            proxy_model2 = QtCore.QSortFilterProxyModel()
            proxy_model2.setSourceModel(proxy_model)
            proxy_model2.setFilterRegExp('^{}$'.format(option2))
            proxy_model2.setFilterKeyColumn(1)
            self.table_view.setModel(proxy_model2)
        else:
            self.table_view.setModel(proxy_model)

    def filter_list_col2(self, index):
        self.filter_list(None)


if __name__ == '__main__':
    app = QtCore.QCoreApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()