from PyQT.baseUI import *

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, 2)
    MainWindow.show()
    sys.exit(app.exec_())