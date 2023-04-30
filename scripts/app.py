import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox
from subprocess import Popen, PIPE, STDOUT
from PyQt5.QtCore import QProcess, QTextCodec
from PyQt5.QtGui import QTextCursor
import os


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Extraction de données - RAJA'
        self.left = 100
        self.top = 60
        self.width = 700
        self.height = 150
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label = QLabel("Sélectionner le dossier de destination des données extraites :", self)
        label.move(20, 20)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 50)
        self.textbox.resize(400, 30)

        browse_button = QPushButton('Parcourir', self)
        browse_button.move(440, 47)
        browse_button.clicked.connect(self.browse_folder)

        execute_button = QPushButton("Lancer l'extraction", self)
        execute_button.move(20, 90)
        execute_button.clicked.connect(self.on_click)


        self.show()

    def browse_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select folder path", options=options)
        if folder_path:
            self.textbox.setText(folder_path)


    def on_click(self):
        path = self.textbox.text()
        print(f"Executing main.py for folder: {path}")
        command = ['python', 'scripts/main.py', path]
        # Popen(command)
        process = Popen(command)
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         self.output.insertPlainText(output.strip() + '\n')
        process.communicate()[0]
        QMessageBox.information(self, "Extraction terminée", "L'extraction des données est terminée.")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

