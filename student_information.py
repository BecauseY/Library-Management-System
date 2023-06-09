import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QLineEdit, QToolButton, QGroupBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import func


# import database


class StudentInfo(QGroupBox):
    '''
    编辑书本信息的界面
    传入{
        'sno': str,
        'sname': str,
        'dept': str,
        'majority': str,
        'max_book': int
    }
    返回{
        'sno': str,
        'sname': str,
        'password': str,
        'dept': str,
        'majority': str,
        'max_book': int
    }
    '''
    after_close = pyqtSignal(dict)

    def __init__(self, stu_info: dict):
        super().__init__()
        self.stu_info = stu_info

        self.title = QLabel()
        self.title.setText('学生信息')

        self.subTitle = QLabel()
        self.subTitle.setText('编辑学生信息')

        # 学号输入框
        self.SIDInput = QLineEdit()
        self.SIDInput.setFixedSize(400, 40)
        self.SIDInput.setText(self.stu_info['sno'])
        self.SIDInput.initText = '请输入学号'
        self.SIDInput.setEnabled(False)

        # 姓名输入框
        self.nameInput = QLineEdit()
        self.nameInput.setFixedSize(400, 40)
        self.nameInput.setText(self.stu_info['sname'])
        self.nameInput.initText = '请输入姓名'
        self.nameInput.setTextMargins(5, 5, 5, 5)
        self.nameInput.mousePressEvent = lambda x: self.inputClick(self.nameInput)

        # 性别输入框
        self.sexInput = QLineEdit()
        self.sexInput.setFixedSize(400, 40)
        self.sexInput.setText(self.stu_info['sex'])
        self.sexInput.initText = '请输入性别'
        self.sexInput.setTextMargins(5, 5, 5, 5)
        self.sexInput.mousePressEvent = lambda x: self.inputClick(self.sexInput)

        # 密码
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(400, 40)
        self.passwordInput.setText('请输入密码')
        self.passwordInput.initText = '请输入密码'
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(self.passwordInput)

        # 重复密码
        self.repPasswordInput = QLineEdit()
        self.repPasswordInput.setFixedSize(400, 40)
        self.repPasswordInput.setText('请重复输入密码')
        self.repPasswordInput.initText = '请重复输入密码'
        self.repPasswordInput.setTextMargins(5, 5, 5, 5)
        self.repPasswordInput.mousePressEvent = lambda x: self.inputClick(self.repPasswordInput)

        # 最大借书数
        self.maxNumInput = QLineEdit()
        self.maxNumInput.setFixedSize(400, 40)
        self.maxNumInput.setText(str(self.stu_info['max_book']))
        self.maxNumInput.initText = '请输入最大借书数'
        self.maxNumInput.setTextMargins(5, 5, 5, 5)
        self.maxNumInput.mousePressEvent = lambda x: self.inputClick(self.maxNumInput)

        # 学院
        self.deptInput = QLineEdit()
        self.deptInput.setFixedSize(400, 40)
        self.deptInput.setText(self.stu_info['dept'])
        self.deptInput.initText = '请输入所在学院'
        self.deptInput.setTextMargins(5, 5, 5, 5)
        self.deptInput.mousePressEvent = lambda x: self.inputClick(self.deptInput)

        # 专业
        self.majorInput = QLineEdit()
        self.majorInput.setFixedSize(400, 40)
        self.majorInput.setText(self.stu_info['majority'])
        self.majorInput.initText = '请输入所在专业'
        self.majorInput.setTextMargins(5, 5, 5, 5)
        self.majorInput.mousePressEvent = lambda x: self.inputClick(self.majorInput)

        # 提交
        self.submit = QToolButton()
        self.submit.setText('提交')
        self.submit.setFixedSize(400, 40)
        self.submit.clicked.connect(self.submitFunction)

        # 退出
        self.back = QToolButton()
        self.back.setText('退出')
        self.back.setFixedSize(400, 40)
        self.back.clicked.connect(self.close)

        self.btnList = [
            self.SIDInput,
            self.nameInput,
            self.sexInput,
            self.passwordInput,
            self.repPasswordInput,
            self.deptInput,
            self.majorInput,
            self.maxNumInput
        ]

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addWidget(self.title)
        self.bodyLayout.addWidget(self.subTitle)
        for i in self.btnList:
            self.bodyLayout.addWidget(i)
        self.bodyLayout.addWidget(self.submit)
        self.bodyLayout.addWidget(self.back)

        self.setLayout(self.bodyLayout)
        self.initUI()

    def inputClick(self, e):
        for i in range(2, 10):  # 从2开始，因为前两个是标题和副标题
            item = self.bodyLayout.itemAt(i).widget()  # 获取第i个控件
            if item.text() == '':
                item.setText(item.initText)  # 设置初始文本
                if item is self.passwordInput or item is self.repPasswordInput:
                    item.setEchoMode(QLineEdit.Normal)  # 显示密码

        if e.text() == e.initText:
            e.setText('')
        if e is self.passwordInput or e is self.repPasswordInput:
            e.setEchoMode(QLineEdit.Password)  # 隐藏密码

    def submitFunction(self):
        if not self.maxNumInput.text().isalnum():
            print('最大数量输入错误')
            return
        if self.passwordInput.text() != self.passwordInput.initText:
            if self.passwordInput.text() != self.repPasswordInput.text():
                msgBox = QMessageBox(QMessageBox.Warning, "错误!", '两次输入密码不一致!', QMessageBox.NoButton, self)
                msgBox.addButton("确认", QMessageBox.AcceptRole)
                msgBox.exec_()
                return
            self.stu_info['password'] = func.encrypt(self.passwordInput.text())
        self.stu_info['sname'] = self.nameInput.text()
        self.stu_info['sex'] = self.sexInput.text()
        self.stu_info['dept'] = self.deptInput.text()
        self.stu_info['majority'] = self.majorInput.text()
        self.stu_info['max_book'] = int(self.maxNumInput.text())
        self.close()
        self.after_close.emit(self.stu_info)

    def initUI(self):
        self.setFixedSize(422, 500)
        self.setWindowTitle('编辑学生信息')
        self.setWindowIcon(QIcon('icon/person.png'))
        self.setMyStyle()

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        QLineEdit{
            border:0px;
            border-bottom: 1px solid rgba(229, 229, 229, 1);
            color: grey;
        }
        QToolButton{
            border: 0px;
            background-color:rgba(52, 118, 176, 1);
            color: white;
            font-size: 25px;
            font-family: 微软雅黑;
        }
        QGroupBox{
            border: 1px solid rgba(229, 229, 229, 1);
            border-radius: 5px;
        }
        ''')
        self.title.setStyleSheet('''
        *{
            color: rgba(113, 118, 121, 1);
            font-size: 30px;
            font-family: 微软雅黑;
        }
        ''')
        self.subTitle.setStyleSheet('''
        *{
            color: rgba(184, 184, 184, 1);
        }
        ''')


if __name__ == '__main__':
    stu_msg = temp = {
        'sno': '201602',
        'sname': '小王',
        'sex': '男',
        'dept': '数学与信息科学学院',
        'majority': 'SE',
        'max_book': 5
    }
    app = QApplication(sys.argv)
    ex = StudentInfo(stu_msg)
    ex.show()
    sys.exit(app.exec_())
