import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QToolButton, QPushButton
from PyQt5.QtCore import Qt


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.bodyLayout = QGridLayout()

        # 欢迎登陆图书馆系统标题
        self.titleText = QLabel(self)
        self.titleText.setText('登录我的图书馆')
        self.titleText.setAlignment(Qt.AlignCenter)
        self.titleText.setFixedSize(480, 60)

        account = QLabel()
        account.setText('读者证号(学工号)')

        password = QLabel()
        password.setText('图书馆密码')

        # 学号输入框
        self.accountInput = QLineEdit()
        self.accountInput.setFixedSize(400, 50)
        self.accountInput.setTextMargins(5, 5, 5, 5)
        self.accountInput.mousePressEvent = lambda x: self.inputClick(self.accountInput)
        # self.accountInput.setClearButtonEnabled(True)

        # 密码输入框
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(400, 50)
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(self.passwordInput)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        # self.passwordInput.setClearButtonEnabled(True)

        # 注册按钮
        self.signup = QToolButton()
        self.signup.setText('注册')
        self.signup.setFixedSize(80, 40)

        # 登录按钮
        self.loginButton = QToolButton()
        self.loginButton.setText('登录')
        self.loginButton.setFixedSize(80, 40)

        # 把上面定义的元素加入大框
        self.inputBoxLayout = QVBoxLayout()
        self.inputBoxLayout.addWidget(account)
        self.inputBoxLayout.addWidget(self.accountInput)
        self.inputBoxLayout.addWidget(password)
        self.inputBoxLayout.addWidget(self.passwordInput)

        self.inputBoxLayout2 = QHBoxLayout()
        self.inputBoxLayout2.addWidget(self.signup)
        self.inputBoxLayout2.addWidget(self.loginButton)

        # 下面一个大框
        self.inputBox = QWidget()
        self.inputBox.setObjectName('inputBox')
        self.inputBox.setContentsMargins(30, 30, 30, 30)
        self.inputBox.setFixedSize(480, 250)
        self.inputBox.setLayout(self.inputBoxLayout)

        self.inputBox2 = QWidget()
        self.inputBox2.setObjectName('inputBox2')
        self.inputBox2.setContentsMargins(30, 30, 30, 30)
        self.inputBox2.setFixedSize(480, 150)
        self.inputBox2.setLayout(self.inputBoxLayout2)

        # 把大标题和下面输入框加入self
        self.bodyLayout.addWidget(self.titleText, 0, 0)
        self.bodyLayout.addWidget(self.inputBox, 1, 0)
        self.bodyLayout.addWidget(self.inputBox2, 2, 0)
        self.setLayout(self.bodyLayout)
        self.setFixedSize(480, 450)
        self.setMyStyle()

    def inputClick(self, e):
        if e.text() == '学号' or e.text() == '******':
            e.setText('')

    def setMyStyle(self):
        self.setStyleSheet('''
            QWidget{
                background-color:white;
            }
        ''')
        self.titleText.setStyleSheet('''
            *{
                color: rgba(3, 54, 73);
                width: 200px;
                background-color: #8CC7B5;
                font-size: 20px;
                font-family: 微软雅黑;
            }
        ''')
        self.inputBox.setStyleSheet('''
       
        QLineEdit{
            color: black;
            font-size: 25px;
            font-family: 微软雅黑;
        }
        QLabel{
            font-size: 20px;
            font-family: 微软雅黑;
        }
        QToolButton{
            background-color:#8CC7B5;
            color: black;
            font-size: 20px;
            font-family: 微软雅黑;
        }
        QPushButton{
            color:black;
            font-weight:300;
            border:1;
            background-color:#8CC7B5;
            font-size: 20px;
            font-family: 微软雅黑;
        }
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
