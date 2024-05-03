import pymysql

Config = {
    "host": '127.0.0.1',
    "user": 'root',
    "pwd": '123456',
    'db': 'library'
}


def create_database():
    try:
        conn = pymysql.connect(host=Config['host'], user=Config['user'], password=Config['pwd'])
        print("成功连接到数据库")
        cursor = conn.cursor()
        conn.autocommit(True)
        cursor.execute("CREATE DATABASE `{}`".format(Config['db']))
        conn.autocommit(False)
        cursor.execute("use `{}`".format(Config['db']))
        print("成功创建数据库：{}".format(Config['db']))

        print("开始创建数据表")
        # 创建学生信息表
        cursor.execute("""CREATE TABLE `student`(
            `sno` varchar(15),
            `password` varchar(70),
            `sname` varchar(10),
            `dept` varchar(20),
            `majority` varchar(20),
            `max_book` int,
            primary key(`sno`))
        """)
        # 创建管理员表
        cursor.execute("""CREATE TABLE `administrator`(
            `aid` varchar(15) ,
            `password` varchar(70),
            primary key(`aid`)
        );
        """)
        # 创建书籍信息表
        cursor.execute("""CREATE TABLE `book`(
            `bno` char(15) PRIMARY KEY,
            `bname` text,
            `author` text,
            `date` char(17),
            `press` char(20),
            `position` char(10),
            `sum` int,
            `rest` int
        );
        """)
        # 创建借书表
        cursor.execute("""CREATE TABLE `borrowing_book`(
            `bno` char(15),
            `sno` char(15),
            `borrow_date` char(17),
            `deadline` char(17),
            `punish_money` int,
            PRIMARY KEY(bno, sno) 
        );
        """)
        # 创建日志表
        cursor.execute("""CREATE TABLE `log`(
            `bno` char(15),
            `sno` char(15),
            `borrow_date` char(17),
            `return_date` char(17),
            `punish_money` int
        );
        """)
        # 创建书籍分类表
        cursor.execute(""" CREATE TABLE `classification`(
            `bno` char(15),
            `class` varchar(15),
            PRIMARY KEY(bno, class)
        );
        """)

        # 导入默认管理员账号密码：admin/123456，导入数据库的是加密之后的信息
        cursor.execute("""
        INSERT
        INTO administrator
        VALUES('admin', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92')
        """)
        conn.commit()
        print("成功创建所有数据表")
    except Exception as e:
        print('数据库建立失败，报错信息如下：')
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_database()
