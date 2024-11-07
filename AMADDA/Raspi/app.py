import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

from ui_main import Ui_MainWindow
import resources_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.profile4_button.setEnabled(False)
        self.ui.profile4_button.hide()
        self.ui.profile4_name.hide()
        #self.ui.profile3_button.setEnabled(False)
        #self.ui.profile3_button.hide()
        #self.ui.profile3_name.hide()
        #self.ui.profile2_button.setEnabled(False)
        #self.ui.profile2_button.hide()
        #self.ui.profile2_name.hide()


    def button_clicked1(self):
        a = 1
        #self.ui.label_4.setStyleSheet("color: rgb(0,255,0)")

    def slot1(self):
        self.ui.background.setStyleSheet("background-color:red;")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()