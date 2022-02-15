import io
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)
from PyQt5.uic import loadUi
from user_load_test_ui import Ui_testRunWindow
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.Qt import Qt
import sys


class Window(QMainWindow, Ui_testRunWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()
        self.filename = ''
        self.selected_files = ''

        # Setup example tree where all elements are checkable, in cascasde fashion
        for i in range(3):
            parent = QtWidgets.QTreeWidgetItem(self.treeWidget)
            parent.setText(0, "dir_{}/".format(i))
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for x in range(5):
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, "test_{}.jmx".format(i * 5 + x))
                child.setCheckState(0, Qt.Unchecked)

        # Connect itemClicked signal to a slot to track the state of the tree
        self.treeWidget.itemClicked.connect(self.vrfs_selected)

    def vrfs_selected(self):
        """
        Prints out the selected items in the tree whenver the tree state is updated
        :return: None
        """
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget, QtWidgets.QTreeWidgetItemIterator.Checked)
        dir_name = ''
        new_files = []
        while iterator.value():
            tree_elem = iterator.value()
            item_text = tree_elem.text(0)
            print(tree_elem.text(0))
            if '/' in item_text:
                dir_name = item_text
            elif '.jmx' in item_text:
                new_files.append(dir_name + item_text)
            iterator += 1
        if new_files:
            self.selected_files = new_files
            print(f'selected_files: {self.selected_files}')

            iterator += 1
        print('*' * 20)

    def connect_signals_slots(self):
        self.actionExit.triggered.connect(self.close)
        """self.actionFind_and_Replace.triggered.connect(self.find_and_replace)
        self.actionAbout.triggered.connect(self.about)"""
        self.action_Open.triggered.connect(self.on_open)

    def on_open(self):
        """
        Try to set text edit content to the contents of the file
        :return: None
        """
        filepath = self.select_file()
        if filepath:
            with io.open(filepath, 'r') as file:
                file_lines = ''.join(file.readlines())
                self.textEdit.setText(file_lines)

    def select_file(self):
        """
        Display open file dialogue and select a file
        :return: the name of the file or empty string
        :rtype: string
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
        return file

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def find_and_replace(self):
        dialog = FindReplaceDialog(self)
        dialog.exec()

    def about(self):
        QMessageBox.about(
            self,
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())