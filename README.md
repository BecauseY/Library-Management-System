# Library-Management-System

## 部署

推荐使用Git

1. 在空文件夹中打开git bash并输入

   ```
   git clone git@github.com:Rouphy/Library-Management-System.git
   ```

   或者fork到自己仓库后再进行以下操作(指令略)

2. 在项目路径下打开控制台并且用pip安装requirements.txt

   ```
   pip install -r requirements.txt
   ```

3. 编辑配置文件config.txt

   其中对应的host，user，pwd以及db分别对应着mysql的主机名，用户名，密码和数据库名

   修改前三个项*冒号*:后面‘*单引号*’里的内容即可

4. 在执行主程序前需要先单独执行createdb.py进行数据库的创建

5. main.py是程序入口（给小白看的）

   调试请从这个文件开始



## 历史版本（开发自用

##### 结构更改：

- [x] -罚款信息
- [x] 更改对应图书信息名：
  - 图书编号ISBN
  - 所属类别
- [x] +读者性别
- [x] +图书借阅次数

##### 对于sql语句：

- 包含触发器
- 包含索引
