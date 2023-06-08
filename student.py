import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QGroupBox,
                             QToolButton, QSplitter, QVBoxLayout, QHBoxLayout,
                             QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView,
                             QLineEdit, QFileDialog, QToolTip, QComboBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
import func


# import func


class StudentPage(QWidget):
    def __init__(self, stu_mes):
        super().__init__()
        self.focus = 0
        self.stu_mes = stu_mes
        self.initUI()

    def initUI(self):
        # 标题栏
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(1250, 50)
        self.setTitleBar()

        # 分割
        self.body = QSplitter(Qt.Vertical, self)
        self.setLeftMunu()
        self.content = None
        self.setContent()

        self.bodyLayout = QGridLayout()
        self.bodyLayout.addWidget(self.titleBar, 0, 0, 1, 7)
        self.bodyLayout.addWidget(self.body, 1, 0, 7, 7)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.bodyLayout)
        self.setFixedSize(1280, 720)
        self.setMyStyle()

    # 设置标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('欢迎使用图书馆管理系统')
        self.title.setFixedHeight(30)

        self.account = QToolButton()
        self.account.setIcon(QIcon('icon/person.png'))
        self.account.setText(self.stu_mes['sno'] + self.stu_mes['sname'] + '，你好！')
        self.account.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.account.setFixedHeight(20)
        self.account.setEnabled(False)

        self.out = QToolButton()
        self.out.setText('退出')
        self.out.setFixedHeight(30)

        titleLayout = QHBoxLayout()
        titleLayout.addWidget(self.account)
        titleLayout.addSpacing(120)
        titleLayout.addWidget(self.title)
        titleLayout.addWidget(self.out)
        self.titleBar.setLayout(titleLayout)

    # 左侧菜单栏
    def setLeftMunu(self):
        # 查询按钮
        self.bookSearch = QToolButton()
        self.bookSearch.setText('图书查询')
        self.bookSearch.setFixedSize(160, 50)
        self.bookSearch.setIcon(QIcon('icon/book.png'))
        self.bookSearch.setIconSize(QSize(30, 30))
        self.bookSearch.clicked.connect(
            lambda: self.switch(0, self.bookSearch))
        self.bookSearch.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 借阅按钮
        self.borrow = QToolButton()
        self.borrow.setText('借阅信息')
        self.borrow.setFixedSize(160, 50)
        self.borrow.setIcon(QIcon('icon/borrowing.png'))
        self.borrow.setIconSize(QSize(30, 30))
        self.borrow.clicked.connect(lambda: self.switch(1, self.borrow))
        self.borrow.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 借阅历史
        self.history = QToolButton()
        self.history.setText('借阅历史')
        self.history.setFixedSize(160, 50)
        self.history.setIcon(QIcon('icon/history.png'))
        self.history.setIconSize(QSize(30, 30))
        self.history.clicked.connect(lambda: self.switch(2, self.history))
        self.history.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 个人信息
        self.detial = QToolButton()
        self.detial.setText('个人信息')
        self.detial.setFixedSize(160, 50)
        self.detial.setIcon(QIcon('icon/detial.png'))
        self.detial.setIconSize(QSize(30, 30))
        self.detial.clicked.connect(lambda: self.switch(3, self.detial))
        self.detial.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.btnList = [self.bookSearch,
                        self.borrow, self.history, self.detial]

        self.layout = QHBoxLayout()
        self.layout.addStretch()
        self.layout.addWidget(self.bookSearch)
        self.layout.addStretch()
        self.layout.addWidget(self.borrow)
        self.layout.addStretch()
        self.layout.addWidget(self.history)
        self.layout.addStretch()
        self.layout.addWidget(self.detial)
        self.layout.addStretch()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.menu = QGroupBox()
        self.menu.setFixedSize(1250, 50)
        self.menu.setLayout(self.layout)
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.body.addWidget(self.menu)

    def switch(self, index, btn):  # 切换页面,index为页面编号
        self.focus = index
        for i in self.btnList:
            i.setStyleSheet('''
            *{
                background: white;
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 0.3);
            }
            ''')

        btn.setStyleSheet('''
        QToolButton{
            background-color: rgba(230, 230, 230, 0.7);
        }
        ''')
        self.setContent()

    # 设置右侧信息页
    def setContent(self):
        if self.content is not None:
            self.content.deleteLater()
        if self.focus == 0:
            self.content = Books(self.stu_mes)
        elif self.focus == 1:
            self.content = BorrowingBooks(self.stu_mes)
        elif self.focus == 2:
            self.content = History(self.stu_mes)
        else:
            self.content = Detial(self.stu_mes)
        self.body.addWidget(self.content)

    def setMyStyle(self):  # 设置样式
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        ''')
        self.titleBar.setStyleSheet('''
        QWidget{
            background-color: rgba(44,44,44,1);
            border:1px solid black;
          
        }
        ''')
        self.menu.setStyleSheet('''
        QWidget{
            border: 0px;
            border-right: 1px solid rgba(227, 227, 227, 1);
        }
        QToolButton{
            color: rgba(51, 90, 129, 1);
            font-family: 微软雅黑;
            font-size: 25px;
            border-right: 1px solid rgba(227, 227, 227, 1);
        }
        QToolButton:hover{
            background-color: rgba(230, 230, 230, 0.3);
        }
        ''')
        self.title.setStyleSheet('''
        *{
            color: white;
            font-family: 微软雅黑;
            font-size: 25px;
            border: 0px;
        }
        ''')
        self.account.setStyleSheet('''
        *{
            color: white;
            font-weight: 微软雅黑;
            font-size: 25px;
            border: 0px;
        }
        ''')
        self.out.setStyleSheet('''
        QToolButton{
            color: white;
            border:0px;
            font-size: 12px;
        }
        QToolButton:hover{
            color: rgba(11, 145, 255, 1);
        }
        ''')


class Books(QGroupBox):
    def __init__(self, stu_mes):
        super().__init__()
        self.stu_mes = stu_mes
        self.book_list = []
        self.body = QVBoxLayout()
        self.table = None
        self.setTitleBar()
        self.setSearchBar()
        self.searchFunction()

        self.setLayout(self.body)
        self.setFixedSize(1280, 600)
        self.setMyStyle()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('书籍信息')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addStretch()
        titleLayout.addWidget(self.title)
        titleLayout.addStretch()
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(1250, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    # 设置搜索框
    def setSearchBar(self):
        self.selectBox = QComboBox()
        self.selectBox.addItems(['书号', '分类', '出版社', '作者', '书名'])
        self.selectBox.setFixedHeight(30)
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索书籍')
        self.searchInput = QLineEdit()
        self.searchInput.setText('')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(400, 40)
        self.searchButton = QToolButton()
        self.searchButton.setFixedSize(100, 40)
        self.searchButton.setText('搜索')
        self.searchButton.clicked.connect(self.searchFunction)
        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.selectBox)
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addStretch()
        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self):
        convert = {'书号': 'bno', '分类': 'class', '出版社': 'press', '作者': 'author', '书名': 'bname', '': 'bname'}
        self.book_list = func.search_book(self.searchInput.text(), convert[self.selectBox.currentText()],
                                          self.stu_mes['sno'])
        if self.book_list == []:
            print('未找到')
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self):
        self.table = QTableWidget(1, 9)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(0, 80)
        # self.table.setColumnWidth(1, 150)
        # self.table.setColumnWidth(2, 125)
        # self.table.setColumnWidth(3, 125)
        # self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(6, 80)

        self.table.setItem(0, 0, QTableWidgetItem('书号'))
        self.table.setItem(0, 1, QTableWidgetItem('书名'))
        self.table.setItem(0, 2, QTableWidgetItem('作者'))
        self.table.setItem(0, 3, QTableWidgetItem('出版日期'))
        self.table.setItem(0, 4, QTableWidgetItem('出版社'))
        self.table.setItem(0, 5, QTableWidgetItem('分类'))
        self.table.setColumnHidden(5, True)
        self.table.setItem(0, 6, QTableWidgetItem('位置'))
        self.table.setItem(0, 7, QTableWidgetItem('总数/剩余'))
        self.table.setItem(0, 8, QTableWidgetItem('操作'))

        for i in range(9):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        # 显示借阅详情
        for i in self.book_list:
            self.insertRow(i)
        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):  # val = [bno, bname, author, date, press, position, sum, rest, class]
        itemBID = QTableWidgetItem(val[0])
        itemBID.setTextAlignment(Qt.AlignCenter)

        itemNAME = QTableWidgetItem('《' + val[1] + '》')
        itemNAME.setTextAlignment(Qt.AlignCenter)

        itemAUTHOR = QTableWidgetItem(val[2])
        itemAUTHOR.setTextAlignment(Qt.AlignCenter)

        itemDATE = QTableWidgetItem(val[3])
        itemDATE.setTextAlignment(Qt.AlignCenter)

        itemPRESS = QTableWidgetItem(val[4])
        itemPRESS.setTextAlignment(Qt.AlignCenter)

        itemPOSITION = QTableWidgetItem(val[5])
        itemPOSITION.setTextAlignment(Qt.AlignCenter)

        itemSUM = QTableWidgetItem(str(val[6]) + '/' + str(val[7]))
        itemSUM.setTextAlignment(Qt.AlignCenter)

        itemCLASSIFICATION = QTableWidgetItem(val[8])
        itemCLASSIFICATION.setTextAlignment(Qt.AlignCenter)

        itemOPERATE = QToolButton(self.table)
        itemOPERATE.setFixedSize(70, 25)

        # val[-3]为总数量
        # val[-2]为剩余数量
        # val[-1]为借阅状态
        # val[0]为为书号

        if val[-1] == '借书':  # 可借
            itemOPERATE.setText('借书')
            itemOPERATE.clicked.connect(lambda: self.borrowBook(val[0]))
            itemOPERATE.setStyleSheet('''
            *{
                color: white;
                font-family: 微软雅黑;
                background: rgba(131, 175, 155, 1);
                border: 0;
           
                font-size:18px;
            }
            ''')
        else:
            itemOPERATE.setText('不可借')  # 不可借
            itemOPERATE.setEnabled(False)
            itemOPERATE.setToolTip(val[-1])  # 设置提示
            QToolTip.setFont(QFont('微软雅黑', 15))
            itemOPERATE.setStyleSheet('''
            QToolButton{
                color: white;
                font-family: 微软雅黑;
                background: rgba(200, 200, 200, 1);
                border: 0;
             
                font-size:18px;
            }
            QToolTip{
                color: black;
                border: 1px solid rgba(200, 200, 200, 1);
            }
            ''')

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemLayout.addWidget(itemOPERATE)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemBID)
        self.table.setItem(1, 1, itemNAME)
        self.table.setItem(1, 2, itemAUTHOR)
        self.table.setItem(1, 3, itemDATE)
        self.table.setItem(1, 4, itemPRESS)
        self.table.setItem(1, 5, itemCLASSIFICATION)
        self.table.setItem(1, 6, itemPOSITION)
        self.table.setItem(1, 7, itemSUM)
        self.table.setCellWidget(1, 8, itemWidget)

    def borrowBook(self, bno: str):
        ans = func.borrow_book(bno, self.stu_mes['sno'])
        # 刷新表格
        if ans:
            self.searchFunction()

    def setMyStyle(self):
        self.setStyleSheet('''
        *{
            background-color: white;
            border:0px;
        }
        ''')
        self.titleBar.setStyleSheet('''
        QWidget {
            border:0;
            background-color: rgba(216, 216, 216, 1);
            color: rgba(113, 118, 121, 1);
        }
        QLabel{
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')
        self.searchTitle.setStyleSheet('''
            QLabel{
                font-size:20px;
                color: black;
                font-family: 微软雅黑;
            }
        ''')
        self.searchInput.setStyleSheet('''
            QLineEdit{
                border: 1px solid rgba(201, 201, 201, 1);
                color: rgba(120, 120, 120, 1)
            }
        ''')
        self.searchButton.setStyleSheet('''
            QToolButton{
        
                background-color:rgba(131, 175, 155, 1);
                color: white;
                font-size: 25px;
                font-family: 微软雅黑;
            }
        ''')
        self.selectBox.setStyleSheet('''
        *{
            border: 0px;
        }
        QComboBox{
            border: 1px solid rgba(201, 201, 201, 1);
        }
        ''')


# 正在借阅的书
class BorrowingBooks(QGroupBox):
    def __init__(self, stu_mes):
        super().__init__()
        self.stu_mes = stu_mes
        self.body = QVBoxLayout()
        self.setTitleBar()
        self.setTable()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('借阅信息')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addStretch()
        titleLayout.addWidget(self.title)
        titleLayout.addStretch()
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(1250, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    def setTable(self, val: dict = None):
        self.table = QTableWidget(1, 6)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 175)
        self.table.setColumnWidth(3, 175)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 150)

        self.table.setItem(0, 0, QTableWidgetItem('书号'))
        self.table.setItem(0, 1, QTableWidgetItem('书名'))
        self.table.setItem(0, 2, QTableWidgetItem('借书日期'))
        self.table.setItem(0, 3, QTableWidgetItem('还书日期'))
        self.table.setItem(0, 4, QTableWidgetItem('罚金'))
        # 隐藏罚金
        self.table.setColumnHidden(4, True)
        self.table.setItem(0, 5, QTableWidgetItem('操作'))

        for i in range(6):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))
        self.body.addWidget(self.table)

        # 显示借阅详情
        self.book_list = func.get_borrowing_books(self.stu_mes['sno'])
        for i in self.book_list:
            self.insertRow(i)
        self.table.setStyleSheet('''
        *{
            font-size:18px;
            color: black;
            background-color: white;
            font-family: 微软雅黑;
        }
        ''')

    # 插入行
    def insertRow(self, val: list):
        itemBID = QTableWidgetItem(val[1])
        itemBID.setTextAlignment(Qt.AlignCenter)
        itemNAME = QTableWidgetItem('《' + val[2] + '》')
        itemNAME.setTextAlignment(Qt.AlignCenter)
        itemBEGIN = QTableWidgetItem(val[3])
        itemBEGIN.setTextAlignment(Qt.AlignCenter)
        itemBACK = QTableWidgetItem(val[4])
        itemBACK.setTextAlignment(Qt.AlignCenter)
        itemPUNISHED = QLabel()
        itemPUNISHED.setText('0')
        itemPUNISHED.setAlignment(Qt.AlignCenter)
        isPunished = func.days_between(
            val[4], time.strftime("%Y-%m-%d-%H:%M"))
        if isPunished <= 0:
            itemPUNISHED.setStyleSheet('''
                *{
                    color: green;
                    font-size:20px;
                    font-family: 微软雅黑;
                }
            ''')
        else:
            itemPUNISHED.setText(str(isPunished))
            itemPUNISHED.setStyleSheet('''
                *{
                    color: red;
                    font-size:20px;
                    font-family: 微软雅黑;
                }
            ''')
        itemOPERATE = QToolButton(self.table)
        itemOPERATE.setFixedSize(70, 25)
        if isPunished <= 0:
            itemOPERATE.setText('还书')
            itemOPERATE.clicked.connect(lambda: self.retrurnBook(val[1]))
            itemOPERATE.setStyleSheet('''
            *{
                color: white;
                font-family: 微软雅黑;
                background: rgba(38, 175, 217, 1);
                border: 0;
            
                font-size:18px;
            }
            ''')
        else:
            itemOPERATE.setText('交罚金')
            itemOPERATE.clicked.connect(
                lambda: self.pay(val[1], isPunished))
            itemOPERATE.setStyleSheet('''
            *{
                color: white;
                font-family: 微软雅黑;
                background: rgba(222, 52, 65, 1);
                border: 0;
           
                font-size:18px;
            }
            ''')

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemLayout.addWidget(itemOPERATE)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemBID)
        self.table.setItem(1, 1, itemNAME)
        self.table.setItem(1, 2, itemBEGIN)
        self.table.setItem(1, 3, itemBACK)
        self.table.setCellWidget(1, 4, itemPUNISHED)
        self.table.setCellWidget(1, 5, itemWidget)

    def retrurnBook(self, bno: str):
        ans = func.return_book(bno, self.stu_mes['sno'])
        # 刷新表格
        if ans:
            self.book_list = func.get_borrowing_books(self.stu_mes['sno'])
            self.table.deleteLater()
            self.setTable()

    def pay(self, bno: str, PUNISH):
        ans = func.pay(bno, self.stu_mes['sno'], PUNISH)
        # 刷新表格
        if ans:
            self.book_list = func.get_borrowing_books(self.stu_mes['sno'])
            self.table.deleteLater()
            self.setTable()

    def initUI(self):
        self.setFixedSize(1280, 600)
        self.setStyleSheet('''
        *{
            background-color: white;
            border:0px;
        }
        ''')
        self.titleBar.setStyleSheet('''
        QWidget {
            border:0;
            background-color: rgba(216, 216, 216, 1);
          
            color: rgba(113, 118, 121, 1);
        }
        QLabel{
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')


class History(QGroupBox):
    def __init__(self, stu_mes):
        super().__init__()
        self.stu_mes = stu_mes
        self.body = QVBoxLayout()
        self.setTitleBar()
        self.setTable()
        self.setOut()
        self.body.addStretch()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('借阅记录')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addStretch()
        titleLayout.addWidget(self.title)
        titleLayout.addStretch()
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(1250, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    # 创建表格
    def setTable(self, val: dict = None):
        self.table = QTableWidget(1, 5)
        self.table.setFixedHeight(400)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 175)
        self.table.setColumnWidth(3, 175)
        self.table.setColumnWidth(4, 100)

        self.table.setItem(0, 0, QTableWidgetItem('书号'))
        self.table.setItem(0, 1, QTableWidgetItem('书名'))
        self.table.setItem(0, 2, QTableWidgetItem('借书日期'))
        self.table.setItem(0, 3, QTableWidgetItem('还书日期'))
        self.table.setItem(0, 4, QTableWidgetItem('罚金'))
        # 隐藏罚金
        self.table.setColumnHidden(4, True)

        for i in range(5):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        self.list = func.get_log(self.stu_mes['sno'])
        for i in self.list:
            self.insertRow(i)
        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        itemBID = QTableWidgetItem(val[1])
        itemBID.setTextAlignment(Qt.AlignCenter)
        itemNAME = QTableWidgetItem('《' + val[2] + '》')
        itemNAME.setTextAlignment(Qt.AlignCenter)
        itemBEGIN = QTableWidgetItem(val[3])
        itemBEGIN.setTextAlignment(Qt.AlignCenter)
        itemBACK = QTableWidgetItem(val[4])
        itemBACK.setTextAlignment(Qt.AlignCenter)
        itemPUNISHED = QLabel()
        itemPUNISHED.setText(str(val[5]))
        itemPUNISHED.setAlignment(Qt.AlignCenter)
        if val[5] == 0:
            itemPUNISHED.setStyleSheet('''
                *{
                    color: green;
                    font-size: 20px;
                }
            ''')
        else:
            itemPUNISHED.setStyleSheet('''
                *{
                    color: red;
                    font-size: 20px;
                }
            ''')

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemBID)
        self.table.setItem(1, 1, itemNAME)
        self.table.setItem(1, 2, itemBEGIN)
        self.table.setItem(1, 3, itemBACK)
        self.table.setCellWidget(1, 4, itemPUNISHED)

    # 导出文件
    def setOut(self):
        self.outButton = QToolButton()
        self.outButton.setText('导出')
        self.outButton.clicked.connect(self.outFunction)
        self.outButton.setFixedSize(100, 50)
        outLayout = QHBoxLayout()
        outLayout.addStretch()
        outLayout.addWidget(self.outButton)
        outWidget = QWidget()
        outWidget.setLayout(outLayout)

        self.body.addWidget(outWidget)

    def outFunction(self):
        import csv
        dirName = QFileDialog.getExistingDirectory(self, '选择文件夹')

        title = ['sno', 'bno', 'bname', 'borrow_date', 'return_date', 'punish_money']
        with open(os.path.join(dirName, self.stu_mes['sno'] + '.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(title)
            for row in self.list:
                writer.writerow(row)

    def initUI(self):
        self.setFixedSize(1280, 600)
        self.setStyleSheet('''
        *{
            background-color: white;
            border:0px;
        }
        ''')
        self.titleBar.setStyleSheet('''
        QWidget {
            border:0;
            background-color: rgba(216, 216, 216, 1);
          
            color: rgba(113, 118, 121, 1);
        }
        QLabel{
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')
        self.table.setStyleSheet('''
            font-size:18px;
            color: black;
            background-color: white;
            font-family: 微软雅黑;
        ''')
        self.outButton.setStyleSheet('''
        QToolButton{
          
            background-color:rgba(131, 175, 155, 1);
            color: white;
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')


class Detial(QWidget):
    def __init__(self, stu_mes):
        super().__init__()
        self.stu_mes = func.get_student_info(stu_mes['sno'])

        # 学号输入框
        account = QLabel()
        account.setText('学号')
        self.accountInput = QLineEdit()
        self.accountInput.setFixedSize(1250, 40)
        self.accountInput.setText(self.stu_mes['sno'])
        self.accountInput.setTextMargins(5, 5, 5, 5)
        self.accountInput.setEnabled(False)
        accountLayout = QHBoxLayout()
        accountLayout.addStretch()
        accountLayout.addWidget(account)
        accountLayout.addWidget(self.accountInput)
        accountLayout.addStretch()

        # 姓名输入框
        name = QLabel()
        name.setText('姓名')
        self.nameInput = QLineEdit()
        self.nameInput.setFixedSize(1250, 40)
        self.nameInput.setText(self.stu_mes['sname'])
        self.nameInput.setTextMargins(5, 5, 5, 5)
        self.nameInput.setEnabled(False)
        nameLayout = QHBoxLayout()
        nameLayout.addStretch()
        nameLayout.addWidget(name)
        nameLayout.addWidget(self.nameInput)
        nameLayout.addStretch()

        # 性别输入框
        sex = QLabel()
        sex.setText('性别')
        self.sexInput = QLineEdit()
        self.sexInput.setFixedSize(1250, 40)
        self.sexInput.setText(self.stu_mes['sex'])
        self.sexInput.setTextMargins(5, 5, 5, 5)
        self.sexInput.setEnabled(False)
        sexLayout = QHBoxLayout()
        sexLayout.addStretch()
        sexLayout.addWidget(sex)
        sexLayout.addWidget(self.sexInput)
        sexLayout.addStretch()

        # 密码
        password = QLabel()
        password.setText('密码')
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(1250, 40)
        self.passwordInput.setText('******')
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.setEnabled(False)
        passwordLayout = QHBoxLayout()
        passwordLayout.addStretch()
        passwordLayout.addWidget(password)
        passwordLayout.addWidget(self.passwordInput)
        passwordLayout.addStretch()

        # 重复密码
        repPassword = QLabel()
        repPassword.setText('重复密码')
        self.repPasswordInput = QLineEdit()
        self.repPasswordInput.setFixedSize(1250, 40)
        self.repPasswordInput.setText('******')
        self.repPasswordInput.setEchoMode(QLineEdit.Password)
        self.repPasswordInput.setTextMargins(5, 5, 5, 5)
        self.repPasswordInput.setEnabled(False)
        repPasswordLayout = QHBoxLayout()
        repPasswordLayout.addStretch()
        repPasswordLayout.addWidget(repPassword)
        repPasswordLayout.addWidget(self.repPasswordInput)
        repPasswordLayout.addStretch()

        # 最大借书数
        maxNum = QLabel()
        maxNum.setText('最大借书数')
        self.maxNumInput = QLineEdit()
        self.maxNumInput.setFixedSize(1250, 40)
        self.maxNumInput.setText(str(self.stu_mes['max_book']))
        self.maxNumInput.setTextMargins(5, 5, 5, 5)
        self.maxNumInput.setEnabled(False)
        maxNumLayout = QHBoxLayout()
        maxNumLayout.addStretch()
        maxNumLayout.addWidget(maxNum)
        maxNumLayout.addWidget(self.maxNumInput)
        maxNumLayout.addStretch()

        # 学院
        dept = QLabel()
        dept.setText('学院')
        self.deptInput = QLineEdit()
        self.deptInput.setFixedSize(1250, 40)
        self.deptInput.setText(self.stu_mes['dept'])
        self.deptInput.setTextMargins(5, 5, 5, 5)
        self.deptInput.setEnabled(False)
        deptLayout = QHBoxLayout()
        deptLayout.addStretch()
        deptLayout.addWidget(dept)
        deptLayout.addWidget(self.deptInput)
        deptLayout.addStretch()

        # 专业
        major = QLabel()
        major.setText('专业')
        self.majorInput = QLineEdit()
        self.majorInput.setFixedSize(1250, 40)
        self.majorInput.setText(self.stu_mes['majority'])
        self.majorInput.setTextMargins(5, 5, 5, 5)
        self.majorInput.setEnabled(False)
        majorLayout = QHBoxLayout()
        majorLayout.addStretch()
        majorLayout.addWidget(major)
        majorLayout.addWidget(self.majorInput)
        majorLayout.addStretch()

        # 保存
        self.save = QToolButton()
        self.save.setText('保存')
        self.save.setFixedSize(100, 40)
        self.save.setEnabled(False)
        self.save.clicked.connect(self.saveFunction)

        # 修改
        self.modify = QToolButton()
        self.modify.setText('修改')
        self.modify.setFixedSize(100, 40)
        self.modify.clicked.connect(self.modifyFunction)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(self.modify)
        btnLayout.addWidget(self.save)
        btnLayout.addStretch()

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addLayout(accountLayout)
        self.bodyLayout.addLayout(nameLayout)
        self.bodyLayout.addLayout(sexLayout)
        self.bodyLayout.addLayout(passwordLayout)
        self.bodyLayout.addLayout(repPasswordLayout)
        self.bodyLayout.addLayout(deptLayout)
        self.bodyLayout.addLayout(majorLayout)
        self.bodyLayout.addLayout(maxNumLayout)
        self.bodyLayout.addLayout(btnLayout)
        self.bodyLayout.addStretch()
        self.setLayout(self.bodyLayout)
        self.initUI()

    def saveFunction(self):  # 保存
        if self.passwordInput.text() != self.repPasswordInput.text():
            print('密码不一致')
            return
        if not self.maxNumInput.text().isalnum():
            print('最大数量输入错误')
            return
        if self.passwordInput.text() != '******':
            self.stu_mes['password'] = func.encrypt(self.passwordInput.text())
        self.stu_mes['sname'] = self.nameInput.text()
        self.stu_mes['sex'] = self.sexInput.text()
        self.stu_mes['dept'] = self.deptInput.text()
        self.stu_mes['majority'] = self.majorInput.text()
        self.stu_mes['max_book'] = int(self.maxNumInput.text())
        if not func.update_student(self.stu_mes):
            print('更新失败')
            return
        self.save.setEnabled(False)
        self.nameInput.setEnabled(False)
        self.sexInput.setEnabled(False)
        self.passwordInput.setEnabled(False)
        self.repPasswordInput.setEnabled(False)
        self.deptInput.setEnabled(False)
        self.majorInput.setEnabled(False)
        self.maxNumInput.setEnabled(False)
        self.setMyStyle()

    def modifyFunction(self):  # 修改按钮
        self.save.setEnabled(True)
        self.nameInput.setEnabled(True)
        self.sexInput.setEnabled(True)
        self.passwordInput.setEnabled(True)
        self.repPasswordInput.setEnabled(True)
        self.deptInput.setEnabled(True)
        self.majorInput.setEnabled(True)
        self.maxNumInput.setEnabled(True)
        self.setStyleSheet('''
            QWidget{
                background-color: white;
            }
            QLabel{
                font-size: 20px;
                font-family: 微软雅黑;
            }
            QLineEdit{
                border: 1px solid rgba(229, 229, 229, 1);
             
                color: black;
            }
            QToolButton{
            
                background-color:rgba(52, 118, 176, 1);
                color: white;
                font-size: 25px;
                font-family: 微软雅黑;
            }
        ''')
        self.save.setStyleSheet('''
        *{
            background-color:rgba(52, 118, 176, 1);
        }
        ''')

    def initUI(self):
        self.setFixedSize(550, 600)
        self.setMyStyle()

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        QLabel{
            font-size: 20px;
            font-family: 微软雅黑;
        }
        QLineEdit{
            border: 1px solid rgba(229, 229, 229, 1);
        
            color: grey;
        }
        QToolButton{
         
            background-color:rgba(52, 118, 176, 1);
            color: white;
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')
        self.save.setStyleSheet('''
        *{
            background-color: gray;
        }
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_message = {
        'sno': '1',
        'sname': '1',
        'sex': '1',
        'dept': '1',
        'majority': '1',
        'max_book': 5
    }
    ex = StudentPage(user_message)
    ex.show()
    sys.exit(app.exec_())
