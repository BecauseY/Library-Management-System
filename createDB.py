import time
import pymysql

Config = {
    "host": 'localhost',
    "user": 'root',
    "pwd": '1234'
}


def create_database():
    try:
        conn = pymysql.connect(host=Config['host'], user=Config['user'], password=Config['pwd'])
        cursor = conn.cursor()
        conn.autocommit(True)
        cursor.execute("CREATE DATABASE library3")
        conn.autocommit(False)
        cursor.execute("use library3")

        # 创建学生表
        cursor.execute("""CREATE TABLE `student`(
            `sno` varchar(15),
            `password` varchar(70),
            `sname` varchar(10),
            `sex` varchar(2),
            `dept` varchar(20),
            `majority` varchar(20),
            `max_book` int,
            primary key(`sno`))
        """)
        cursor.execute("""CREATE TABLE `administrator`(
            `aid` varchar(15) ,
            `password` varchar(70),
            primary key(`aid`)
        );
        """)
        cursor.execute("""CREATE TABLE `book`(
            `bno` char(15) PRIMARY KEY,
            `bname` text,
            `author` text,
            `date` char(17),
            `press` char(20),
            `position` char(10),
            `sum` int,
            `rest` int,
            `count` int default 0
        );
        """)




        cursor.execute("""CREATE TABLE `borrowing_book`(
            `bno` char(15),
            `sno` char(15),
            `borrow_date` char(17),
            `deadline` char(17),
            `punish_money` int,
            PRIMARY KEY(bno, sno) 
        );
        """)

        cursor.execute("""CREATE trigger `bcount` after insert 
                    on `borrowing_book` for each row
                    update book set count = count + 1, rest = rest - 1 where bno = new.bno;
                """)

        cursor.execute("""CREATE TABLE `log`(
            `bno` char(15),
            `sno` char(15),
            `borrow_date` char(17),
            `return_date` char(17),
            `punish_money` int
        );
        """)
        cursor.execute(""" CREATE TABLE `classification`(
            `bno` char(15),
            `class` varchar(15),
            PRIMARY KEY(bno, class)
        );
        """)
        cursor.execute("""
        INSERT
        INTO administrator
        VALUES('admin', '123456')
        """)

        # 显示所有书信息
        cursor.execute("""
        CREATE VIEW allbook as
                SELECT bno, bname, author, date, press, position, sum, rest
                FROM book
              """)
        # 显示所有学生信息
        cursor.execute("""
            CREATE VIEW allstudent as
                SELECT sno, sname, sex, dept, majority, max_book
                FROM  student
                    """)



        conn.commit()
    except Exception as e:
        print('Init fall')
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_database()
