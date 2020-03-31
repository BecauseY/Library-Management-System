import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QLineEdit, QToolButton, QGroupBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

KEY_LIST = ['bno', 'bname', 'author',
            'date', 'press', 'position', 'sum', 'class']


class BookInfo(QGroupBox):
    '''
    编辑书本信息的界面
    返回book_msg{
        'bno': str,
        'bname': str,
        'author': str,
        'date': str,
        'press': str,
        'position': str,
        'sum': int,
        'class': str
    }
    '''
    after_close = pyqtSignal(dict)

    def __init__(self, book_msg: dict = None):
        super().__init__()
        if book_msg is not None:
            self.book_msg = book_msg
        else:
            self.book_msg = {
                'bno': '请输入书号',
                'bname': '请输入书名',
                'author': '请输入作者',
                'date': '请输入出版日期',
                'press': '请输入出版社',
                'position': '请输入存放位置',
                'sum': '请输入数量',
                'class': '请输入分类, 以空格区分'
            }

        self.title = QLabel()
        self.title.setText('书本信息')

        self.subTitle = QLabel()
        self.subTitle.setText('编辑书籍信息')

        # 书号输入框
        self.bnoInput = QLineEdit()
        self.bnoInput.setFixedSize(400, 40)
        self.bnoInput.setText(self.book_msg['bno'])
        self.bnoInput.initText = '请输入书号'
        self.bnoInput.mousepressEvent = lambda x: self.inputClick(self.bnoInput)
        # bno不允许修改
        if self.bnoInput.text() != self.bnoInput.initText:
            self.bnoInput.setEnabled(False)

        # 书名输入框
        self.bnameInput = QLineEdit()
        self.bnameInput.setFixedSize(400, 40)
        self.bnameInput.setText(self.book_msg['bname'])
        self.bnameInput.initText = '请输入书名'
        self.bnameInput.mousepressEvent = lambda x: self.inputClick(self.bnameInput)

        # 总书数
        self.NumInput = QLineEdit()
        self.NumInput.setFixedSize(400, 40)
        self.NumInput.setText(str(self.book_msg['sum']))
        self.NumInput.initText = '请输入数量'
        self.NumInput.mousepressEvent = lambda x: self.inputClick(self.NumInput)

        # 作者
        self.authorInput = QLineEdit()
        self.authorInput.setFixedSize(400, 40)
        self.authorInput.setText(self.book_msg['author'])
        self.authorInput.initText = '请输入作者'
        self.authorInput.mousepressEvent = lambda x: self.inputClick(self.authorInput)

        # 出版社
        self.pressInput = QLineEdit()
        self.pressInput.setFixedSize(400, 40)
        self.pressInput.setText(self.book_msg['press'])
        self.pressInput.initText = '请输入出版社'
        self.pressInput.mousepressEvent = lambda x: self.inputClick(self.pressInput)

        # 出版日期
        self.DATEInput = QLineEdit()
        self.DATEInput.setFixedSize(400, 40)
        self.DATEInput.setText(self.book_msg['date'])
        self.DATEInput.initText = '请输入出版日期'
        self.DATEInput.mousepressEvent = lambda x: self.inputClick(self.DATEInput)

        # 位置
        self.positionInput = QLineEdit()
        self.positionInput.setFixedSize(400, 40)
        self.positionInput.setText(self.book_msg['position'])
        self.positionInput.initText = '请输入存放位置'
        self.positionInput.mousepressEvent = lambda x: self.inputClick(self.positionInput)

        # 分类
        self.classInput = QLineEdit()
        self.classInput.setFixedSize(400, 40)
        self.classInput.setText(self.book_msg['class'])
        self.classInput.initText = '请输入分类, 以空格区分'
        self.classInput.mousepressEvent = lambda x: self.inputClick(self.classInput)

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
            self.bnoInput,
            self.bnameInput,
            self.authorInput,
            self.DATEInput,
            self.pressInput,
            self.positionInput,
            self.NumInput,
            self.classInput
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
        for item in self.btnList:
            if item.text() == '':
                item.setText(item.initText)
        if e.text() == e.initText:
            e.setText('')

    def submitFunction(self):
        for btn, key in zip(self.btnList, KEY_LIST):
            if btn.text() == btn.initText:
                self.book_msg[key] = ''
            else:
                self.book_msg[key] = btn.text()

        if not self.book_msg['bno'].isalnum():
            self.errorBox('书编号存在非法字符')
            return
        if len(self.book_msg['bno']) > 15:
            self.errorBox('书编号长度大于15')
            return
        if len(self.book_msg['bname']) == 0:
            self.errorBox('书名不能为空')
            return
        if len(self.book_msg['author']) == 0:
            self.errorBox('作者不能为空')
            return
        if len(self.book_msg['date']) > 12:
            self.errorBox('日期编号过长')
            return
        if len(self.book_msg['press']) > 12:
            self.errorBox('出版社名称长度不能超过20')
            return
        po = self.book_msg['position']
        if not (len(po) == 3 and po[0].isalpha and po[1:].isdigit()):
            self.errorBox('位置编号不合法')
            return
        if self.book_msg['sum'].isdigit():
            self.book_msg['sum'] = int(self.book_msg['sum'])
        else:
            self.errorBox('图书数量有非法字符')
            return
        self.close()
        self.after_close.emit(self.book_msg)

    def initUI(self):
        self.setFixedSize(422, 550)
        self.setWindowTitle('编辑书本')
        self.setWindowIcon(QIcon('icon/book.png'))
        self.setMyStyle()

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
    book_msg = {
        'bno': '4',
        'bname': 'Java',
        'author': 'kak',
        'date': '2009-05',
        'press': '电子出版社',
        'position': 'C05',
        'sum': 5,
        'class': 'aasd asd asd ad '
    }
    app = QApplication(sys.argv)
    ex = BookInfo(book_msg)
    ex.show()
    sys.exit(app.exec_())
