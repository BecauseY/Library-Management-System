import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox)
from PyQt5 import QtGui
import login
import func
import signup
import student
import administrator


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.login_win()
        self.setGeometry(200, 200, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setMyStyle()
        # 创建登录菜单

    def login_win(self):
        self.login = login.Login()
        self.login.setParent(self)
        self.login.move(390, 120)
        self.login.loginButton.clicked.connect(self.login_button_function)
        self.login.signup.clicked.connect(self.signup_button_function)
    # 登录按钮按下

    def login_button_function(self):
        user_mes = {
            'ID': self.login.accountInput.text(),
            'PASSWORD': func.encrypt(self.login.passwordInput.text())
        }
        self.user = func.signin(user_mes)
        if self.user is not None:
            self.login.setVisible(False)
            self.display()
        else:
            print('登录失败!')

# 显示注册界面
    def signup_button_function(self):
        self.login.setVisible(False)
        self.signup_win()

# 创建注册菜单
    def signup_win(self):
        self.signup = signup.Signup()
        self.signup.setParent(self)
        self.signup.setVisible(True)
        self.signup.move(425, 110)
        self.signup.back.clicked.connect(self.back)
        self.signup.submit.clicked.connect(self.signup_function)

# 后退按钮
    def back(self):
        self.signup.setVisible(False)
        self.login.setVisible(True)

# 注册按钮按下
    def signup_function(self):
        self.user = self.signup.getInfo()
        res = func.check_user_info(self.user)
        if res['res'] == 'fail':
            self.errorBox(res['reason'])
            return
        self.user['max_book'] = int(self.user['max_book'])
        self.user['password'] = func.encrypt(self.user['password'])

        ans = func.signup(self.user)
        self.user['class'] = 'stu'
        self.user.pop('password')
        if ans:
            self.signup.setVisible(False)
            print('成功')
            self.display()
        else:
            self.errorBox('注册失败')

    def display(self):
        # 显示学生信息
        if self.user['class'] == 'stu':
            self.body = student.StudentPage(self.user)
            self.body.setParent(self)
            self.body.setVisible(True)
            self.body.out.clicked.connect(self.logout)
        else:
            self.body = administrator.AdministratorPage(self.user)
            self.body.setParent(self)
            self.body.setVisible(True)
            self.body.out.clicked.connect(self.logout)


    def logout(self):
        self.body.close()
        self.login.setVisible(True)

    def errorBox(self, mes: str):
        msgBox = QMessageBox(
            QMessageBox.Warning,
            "警告!",
            mes,
            QMessageBox.NoButton,
            self
        )
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.exec_()

    def setMyStyle(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("image/bg.jpg").scaled(1280, 720)))
        self.setPalette(window_pale)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setWindowTitle("图书馆管理系统")
    mainwindow.show()
    sys.exit(app.exec_())

