import sys
from PyQt5.QtWidgets import QApplication
import main_widget
import createDB, main_widget


def main():
    # createDB.create_database()
    app = QApplication(sys.argv)
    mainwin = main_widget.MainWindow()
    mainwin.setWindowTitle("图书馆管理系统")
    mainwin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
