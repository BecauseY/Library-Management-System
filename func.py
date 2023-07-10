import pymysql
import time


# 读取配置文件
with open('config.txt', 'r') as f:
    config = eval(f.read())
    f.close()


# 登录
def signin(user_message: dict) -> dict:
    ans = None  # 返回值
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        cursor.execute('''
        SELECT aid
        FROM administrator
        WHERE aid=%s AND password=%s
        ''', (
            user_message['ID'],
            user_message['PASSWORD']
        ))
        temp = cursor.fetchall()  # 从数据库中取出数据
        if len(temp) == 0:
            cursor.execute('''
            SELECT sno, sname, sex, dept, majority, max_book
            FROM student
            WHERE sno=%s AND password=%s
            ''', (
                user_message['ID'],
                user_message['PASSWORD']
            ))
            temp = cursor.fetchall()
        ans = temp
        conn.commit()
    except Exception as e:
        print('Signin error!')
        print(e)
    finally:
        if conn:
            conn.close()
        return convert(ans)  # 返回转换后的数据


# 去掉字符串末尾的0
def remove_blank(val):
    if type(val) is not str:               # 如果不是字符串，直接返回
        return val
    while len(val) != 0 and val[-1] == ' ':  # 如果末尾是空格
        val = val[:-1]                      # 去掉末尾的一个字符
    return val                             # 返回去掉空格后的字符串


# 将元组列表转换为字典
def convert(val: list):
    if len(val) == 0:
        return None
    val = val[0]
    if len(val) == 6:  # 如果是学生
        ans = {
            'class': 'stu',
            'sno': remove_blank(val[0]),
            'sname': remove_blank(val[1]),
            'sex': remove_blank(val[2]),
            'dept': remove_blank(val[3]),
            'majority': remove_blank(val[4]),
            'max_book': val[5]
        }
    else:
        ans = {
            'class': 'admin',
            'aid': remove_blank(val[0])
        }
    return ans


def encrypt(val):
    import hashlib
    h = hashlib.sha256()
    password = val
    h.update(bytes(password, encoding='UTF-8'))
    result = h.hexdigest()
    # 注释下面一行即可加密
    result = val
    return result


# 检查注册信息
def check_user_info(info: dict) -> dict:
    '''
    info = {
            'SID': self.accountInput.text(),
            'PASSWORD': self.passwordInput.text(),
            'REPASSWORD': self.repPasswordInput.text(),
            'SNAME': self.nameInput.text(),
            'DEPARTMENT': self.deptInput.text(),
            'MAJOR': self.majorInput.text(),
            'MAX': self.maxNumInput.text(),
            'PUNISHED': 0
        }
    返回 ans = {
        'res':'fail|seccuss',
        'reason':''
    }
    '''
    ans = {
        'res': 'fail',
        'reason': ''
    }
    if len(info['sno']) > 15:
        ans['reason'] = 'ID长度超过15'
        return ans
    if not info['sno'].isalnum():
        ans['reason'] = 'ID存在非法字符'
        return ans
    if info['password'] != info['repassword']:
        ans['reason'] = '两次输入密码不一致'
        return ans
    if not info['max_book'].isdigit():
        ans['reason'] = '最大数量输入含有非法字符'
        return ans
    if int(info['max_book']) > 10:
        ans['reason'] = '最多只能借阅10本书'
        return ans
    if len(info['dept']) > 20:
        ans['reason'] = '学院名称过长'
        return ans
    if len(info['majority']) > 20:
        ans['reason'] = '专业名称过长'
        return ans
    ans['res'] = 'seccuss'
    return ans


# 注册
def signup(user_message: dict) -> bool:
    '''
    传入以下格式的字典
    user_message{
        'SID': str,
        'PASSWORD': str,
        'SNAME': str,
        'SEX': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    '''
    res = True
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM student
            WHERE sno=%s
            ''', (user_message['sno']))
        if len(cursor.fetchall()) != 0:
            raise Exception('用户已存在!')
        cursor.execute('''
        INSERT
        INTO student
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        ''', (
            user_message['sno'],
            user_message['password'],
            user_message['sname'],
            user_message['sex'],
            user_message['dept'],
            user_message['majority'],
            user_message['max_book']
        ))
        conn.commit()
    except Exception as e:
        print('Signup error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 更新学生信息
def update_student(user_message: dict) -> bool:
    '''
    传入字典格式如下
    user_message{
        'sno': str,
        'password': str,
        'sname': str,
        'sex': str,  # '男' or '女'
        'dept': str,
        'majority': str,
        'max_book': int
    }
    返回bool
    '''
    try:
        res = True
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE student
            SET sname=%s, sex=%s, dept=%s, majority=%s, max_book=%s
            WHERE sno=%s
            ''', (
            user_message['sname'],
            user_message['sex'],
            user_message['dept'],
            user_message['majority'],
            user_message['max_book'],
            user_message['sno']
        ))
        if 'password' in user_message:
            cursor.execute('''
            UPDATE student
            SET password=%s
            WHERE sno=%s
            ''', (
                user_message['password'],
                user_message['sno']
            ))
        conn.commit()
    except Exception as e:
        print('Update error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取学生信息
def get_student_info(sno: str) -> dict:
    '''
    传入sno
    返回stu_info{
        'class': stu,
        'sno': str,
        'sname': str,
        'sex': str,  # '男' or '女'
        'dept': str,
        'majority': str,
        'max_book': int
    }
    '''
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sno, sname, sex, dept, majority, max_book
            FROM student
            WHERE sno=%s
            ''', (sno))
        ans = cursor.fetchall()
    except Exception as e:
        print(e)
        print('get student info error')
    finally:
        if conn:
            conn.close()
        return convert(ans)


# 查找学生
def search_student(info: str) -> list:
    '''
    传入sno或学生姓名进行查找
    返回[[sno, sname, sex, dept, majority, max_book],...]
    '''
    try:
        res = []
        val = info.split()
        val = [(i, '%' + i + '%') for i in val]
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        # 显示所有学生信息
        if info == 'ID/姓名' or info == '':
            cursor.execute('''
            SELECT *
            FROM allstudent
            ''')
            res += cursor.fetchall()
        else:
            # 按条件查找
            for i in val:
                cursor.execute('''
                SELECT *
                FROM allstudent
                WHERE sno=%s OR sname LIKE %s
                ''', i)
                res += cursor.fetchall()
        res = list(set(res))
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        res = temp
    except Exception as e:
        print('Search student error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


# 删除学生信息
def delete_student(sno: str) -> bool:
    '''
    传入sno
    删除student表内记录,
    找出book表内所借的书强制还书
    删除log表内的记录
    '''
    try:
        res = True
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        # 先强制把书还掉
        cursor.execute('''
            SELECT bno
            FROM borrowing_book
            WHERE sno=%s
        ''', (sno))
        BID_list = cursor.fetchall()
        for bno in BID_list:
            return_book(bno, sno)
        # 再删除学生信息
        cursor.execute('''
            DELETE
            FROM student
            WHERE sno=%s''', (sno))

        cursor.execute('''
            DELETE
            FROM log
            WHERE sno=%s
            ''', (sno))
        conn.commit()
    except Exception as e:
        print('delete book error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取学生的借书信息
def get_borrowing_books(ID: str, bno: bool = False) -> list:
    '''
    当BID为False以sno的方式查找否则以BID查找
    返回此学生在借的书籍列表信息
    [[sno, bno, bname, borrow_date, deadline, punish_money, rest],[...],....]
    '''
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        if ID == '' or ID == 'ID/姓名':
            cursor.execute('''
                SELECT sno, book.bno, bname, borrow_date, deadline, punish_money, rest
                FROM borrowing_book, book
                WHERE book.bno=borrowing_book.bno
            ''')
        elif bno:
            cursor.execute('''
                SELECT sno, book.bno, bname, borrow_date, deadline, punish_money, rest
                FROM borrowing_book, book
                WHERE book.bno=%s AND book.bno=borrowing_book.bno
            ''', (ID,))
        else:
            cursor.execute('''
                SELECT sno, book.bno, bname, borrow_date, deadline, punish_money, rest
                FROM borrowing_book, book
                WHERE sno=%s AND book.bno=borrowing_book.bno
            ''', (ID,))
        res = cursor.fetchall()
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        res = temp
    except Exception as e:
        print('get borrowing books error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


# 还书
def return_book(bno: str, sno: str) -> bool:
    '''
    传入BID, sno，删除borrowing_book表内的记录在log表内新建记录
    返回bool型
    '''
    try:
        res = True
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        # 先把借书日期，书本剩余数量，罚金等信息找出
        cursor.execute('''
        SELECT borrow_date, rest, punish_money
        FROM book, borrowing_book
        WHERE sno=%s AND borrowing_book.bno=%s AND borrowing_book.bno=book.bno
        ''', (sno, bno))
        book_mes = cursor.fetchall()
        rest = book_mes[0][1]
        borrow_date = book_mes[0][0]
        punish_money = book_mes[0][2]
        return_date = time.strftime("%Y-%m-%d-%H:%M")

        # book表内NUM加一，删除borrowing_book表内的记录，把记录插入log表
        cursor.execute('''
        UPDATE book
        SET rest=%s
        WHERE bno=%s''', (str(rest + 1), bno))

        cursor.execute('''
        DELETE
        FROM borrowing_book
        WHERE sno=%s AND bno=%s''', (sno, bno))

        cursor.execute('''
        INSERT
        INTO log
        VALUES(%s, %s, %s, %s, %s)
        ''', (bno, sno, borrow_date, return_date, str(punish_money)))
        conn.commit()
    except Exception as e:
        print('Return error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 交罚金
def pay(bno: str, sno: str, punish_money: int) -> bool:
    '''
    传入BID, sno, PUNISH把当前数的DEADLINE往后延长两个月
    返回bool型
    '''
    try:
        res = True
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()

        # book表内NUM加一，删除borrowing_book表内的记录，把记录插入log表
        cursor.execute('''
            UPDATE borrowing_book
            SET deadline=%s, punish_money=%d
            WHERE bno=%s AND sno=%s
            ''', (postpone(time.strftime('%Y-%m-%d-%H:%M')), punish_money, bno, sno))
        conn.commit()
    except Exception as e:
        print('Pay error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取历史记录
def get_log(ID: str, bno: bool = False) -> list:
    '''
    传入sno
    返回[[sno, bno, bname, borrow_date, return_date, punish_money],...]
    '''
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        if ID == '' or ID == 'ID/姓名':
            cursor.execute('''
                SELECT sno, book.bno, bname, borrow_date, return_date, punish_money
                FROM log, book
                WHERE book.bno=log.bno
                ORDER BY return_date
            ''')
        elif bno:
            cursor.execute('''
                SELECT sno, book.bno, bname, borrow_date, return_date, punish_money
                FROM log, book
                WHERE log.bno=%s AND book.bno=log.bno
                ORDER BY return_date
            ''', (ID,))
        else:
            cursor.execute('''
                SELECT sno, book.bno, bname, borrow_date, return_date, punish_money
                FROM log, book
                WHERE sno=%s AND book.bno=log.bno
                ORDER BY return_date
            ''', (ID,))
        res = cursor.fetchall()
    except Exception as e:
        print('get log error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        return temp


# 加入新书
def new_book(book_info: dict) -> bool:
    '''
    传入以下格式的字典
    book_msg{
        'bno': str,
        'bname': str,
        'author': str,
        'date': str,
        'press': str,
        'position': str,
        'sum': int,
        'class': str
    }
    返回bool
    '''
    res = True
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM book
            WHERE bno=%s
            ''', (book_info['bno']))
        if len(cursor.fetchall()) != 0:
            raise Exception('书ID已存在!')
        # 插入新书
        cursor.execute('''
        INSERT
        INTO book
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            book_info['bno'],
            book_info['bname'],
            book_info['author'],
            book_info['date'],
            book_info['press'],
            book_info['position'],
            str(book_info['sum']),
            str(book_info['sum']),
            book_info['count']
        ))

        # 处理书本分类
        classifications = book_info['class']
        classifications = classifications.split()
        classifications = list(set(classifications))
        classifications = [(book_info['bno'], i) for i in classifications]
        # 插入分类
        cursor.executemany('''
        INSERT
        INTO classification
        VALUES(%s, %s)
        ''', classifications)

        conn.commit()
    except Exception as e:
        print('add book error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取新书详细信息
def get_book_info(bno: str) -> dict:
    '''
    传入BID
    返回book_msg{
        'bno': str,
        'bname': str,
        'author': str,
        'date': str,
        'press': str,
        'position': str,
        'sum': int,
        'rest': int,
        'class': str
    }
    '''
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        # 获取book表内的书本信息
        cursor.execute('''
            SELECT *
            FROM book
            WHERE bno=%s
            ''', (bno))
        res = cursor.fetchall()
        if len(res) == 0:
            raise Exception('查无此书')

        # 获取分类
        cursor.execute('''
        SELECT class
        FROM classification
        WHERE bno=%s
        ''', (bno))
        classification = ''
        for i in cursor.fetchall():
            classification += (remove_blank(i[0]) + ' ')
        # 把列表转换为字典
        res = list(res[0])
        res.append(classification)
        key_list = ['bno', 'bname', 'author', 'date', 'press', 'position', 'sum', 'rest', 'class', 'count']
        ans = {}
        for (i, key) in zip(res, key_list):
            ans[key] = i
            if type(i) is str:
                ans[key] = remove_blank(i)
        res = ans
    except Exception as e:
        print('get book info error!')
        print(e)
        res = None
    finally:
        if conn:
            conn.close()
        return res


# 更新书籍信息
def update_book(book_info: dict) -> bool:
    '''
    传入以下格式的字典
    book_msg{
        'bno': str,
        'bname': str,
        'author': str,
        'date': str,
        'press': str,
        'position': str,
        'sum': int,
        'rest': int,
        'class': str
    }
    返回bool
    '''
    try:
        res = True
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        # 更新book表
        cursor.execute('''
            UPDATE book
            SET bname=%s, author=%s, date=%s, press=%s, position=%s, sum=%s, rest=%s
            WHERE bno=%s
            ''', (
            book_info['bname'],
            book_info['author'],
            book_info['date'],
            book_info['press'],
            book_info['position'],
            str(book_info['sum']),
            str(book_info['rest']),
            book_info['bno']
        ))

        # 更新classification表
        cursor.execute('''
        DELETE
        FROM classification
        WHERE bno=%s''', (book_info['bno']))
        # 处理书本分类
        classifications = book_info['class']
        classifications = classifications.split()
        classifications = list(set(classifications))
        classifications = [(book_info['bno'], i) for i in classifications]
        # 插入分类
        cursor.executemany('''
        INSERT
        INTO classification
        VALUES(%s, %s)
        ''', classifications)

        conn.commit()
    except Exception as e:
        print('Update book error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 删除书籍
def delete_book(bno: str) -> bool:
    '''
    传入BID
    返回bool
    会删除book，borrowing_book，log, classification 表内所有对应的记录
    '''
    try:
        res = True
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        cursor.execute('''
            DELETE
            FROM book
            WHERE bno=%s''', (bno))

        cursor.execute('''
            DELETE
            FROM borrowing_book
            WHERE bno=%s''', (bno))

        cursor.execute('''
            DELETE
            FROM log
            WHERE bno=%s''', (bno))

        cursor.execute('''
            DELETE
            FROM classification
            WHERE bno=%s
            ''', (bno))
        conn.commit()
    except Exception as e:
        print('delete book error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 把book元组转换为list
def tuple_to_list(val: list):  # val是一个tuple的列表
    '''
    传入tuple列表把里面的tuple都转换为list同时去掉字符串里的空格
    '''
    ans = []
    for tuple_ in val:
        temp = []
        for item in tuple_:
            temp.append(item)
            if type(temp[-1]) is str:
                temp[-1] = remove_blank(temp[-1])
        ans.append(temp)
    return ans


# 搜索书籍
def search_book(info: str, restrict: str, sno: str = '') -> list:
    '''
    传入搜索信息，并指明BID或AUTHOR或PRESS或BNAME或CLASSIFYICATION进行查找，如果传入sno则匹配这个学生的借书状态
    返回[[bno, bname, author, date, press, position, sum, rest, class, STATE],...]
    '''
    try:
        res = []
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()

        # 显示所有书信息
        if info == 'ID/书名/作者/出版社' or info == '':
            cursor.execute('''
            SELECT *
            FROM allbook
            ''')
            res = tuple_to_list(cursor.fetchall())
        elif restrict != 'bno' and restrict != 'class':
            # AUTHOR或PRESS或BNAME
            cursor.execute(f'''
            SELECT *
            FROM allbook
            WHERE {restrict} LIKE %s
            ''', ('%' + info + '%'))
            res = tuple_to_list(cursor.fetchall())
        elif restrict == 'bno':
            # bno
            cursor.execute('''
            SELECT *
            FROM allbook
            WHERE bno = %s
            ''', (info))
            res = tuple_to_list(cursor.fetchall())
        elif restrict == 'class':
            # 通过分类搜书
            cursor.execute('''
            SELECT bno
            FROM classification
            WHERE class = %s
            ''', (info))
            for bno in cursor.fetchall():
                cursor.execute('''
                SELECT bno, bname, author, date, press, position, sum, rest
                FROM book
                WHERE bno = %s
                ''', (bno[0]))
                res.append(tuple_to_list(cursor.fetchall())[0])
        # 把分类搜出来
        for book_info in res:
            CLASSIFICATIONS = ''
            bno = book_info[0]
            cursor.execute('''
            SELECT class
            FROM classification
            WHERE bno = %s
            ''', (bno))
            for classification in cursor.fetchall():
                CLASSIFICATIONS += (remove_blank(classification[0]) + ' ')
            book_info.append(CLASSIFICATIONS)

        # 匹配学生信息判断每一本书是否可借
        if sno != '':
            # 获得学生最大借书数
            cursor.execute('''
            SELECT max_book
            FROM student
            WHERE sno=%s
            ''', (sno))
            max_num = cursor.fetchall()[0][0]
            # 获取已经借阅的书的列表
            borrowing_book = get_borrowing_books(sno)
            # 判断是否有罚金
            punish = False
            for i in borrowing_book:
                if i[4] < time.strftime("%Y-%m-%d-%H:%M"):
                    punish = True
                    break
            for book in res:  # 遍历每一本书
                # 有罚金没交
                if punish:
                    book.append('未交罚金')  # 未交罚金
                    continue
                # 如果已经借的书达到上限就不再可借
                if len(borrowing_book) >= max_num:  # 借书达上限
                    book.append('借书达上限')
                    continue
                    # book[-3]为分类
                    # book[-2]为剩余数量
                    # book[-1]为状态
                    # book[0]为bno

                if book[-2] == 0:  # 剩余为0
                    book.append('没有剩余')
                    continue
                # 判断是否有此书
                for borrow in borrowing_book:
                    if book[0] == borrow[1]:
                        book.append('已借此书')
                        break
                if book[-1] != '已借此书':
                    book.append('借书')
    except Exception as e:
        print('Search error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


# 将日期延后两个月
def postpone(start: str):
    temp = start.split('-')
    temp[0] = int(temp[0])
    temp[1] = int(temp[1])
    temp[2] = int(temp[2])
    temp[1] += 2
    if temp[1] > 12:
        temp[1] -= 12
        temp[0] += 1
    ans = '{:d}-{:0>2d}-{:0>2d}-{}'.format(temp[0], temp[1], temp[2], temp[3])
    return ans


# 借书
def borrow_book(bno: str, sno: str) -> bool:
    '''
    传入BID和sno
    返回bool
    book的NUM减一
    在borrowing_book表内新建记录
    '''
    try:
        res = True
        conn = pymysql.connect(host=config['host'], user=config['user'], password=config['pwd'], database=config['db'])
        cursor = conn.cursor()
        # 先把借书日期，书本剩余数量，罚金等信息找出
        cursor.execute('''
        SELECT rest
        FROM book
        WHERE bno=%s
        ''', (bno))
        book_mes = cursor.fetchall()
        # print(book_mes)
        rest = book_mes[0][0]   # book_mes[0][0]
        borrow_date = time.strftime("%Y-%m-%d-%H:%M")
        deadline = postpone(borrow_date)

        # book表内NUM减一，新建borrowing_book表内的记录
        cursor.execute('''
        UPDATE book
        SET rest=%s
        WHERE bno=%s''', (str(rest), bno))
        conn.commit()

        cursor.execute('''
        INSERT
        INTO borrowing_book
        VALUES(%s, %s, %s, %s, 0)
        ''', (bno, sno, borrow_date, deadline))
        conn.commit()

    except Exception as e:
        print('borrow error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 两个日期之间间隔的天数
def days_between(start: str, end: str):
    start = start.split('-')
    end = end.split('-')
    start[0] = int(start[0])
    start[1] = int(start[1])
    start[2] = int(start[2])

    end[0] = int(end[0])
    end[1] = int(end[1])
    end[2] = int(end[2])

    s = start[0] * 365 + start[1] * 30 + start[2]
    e = end[0] * 365 + end[1] * 30 + end[2]
    return e - s
