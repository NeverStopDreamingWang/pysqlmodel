# 导入Mysql模型
from SqlModel import MySQL
# from SqlModel.mysql import MySQL

# 导入数据库配置
from setting import MYSQL_DATABASES

"""——————连接数据库——————"""
# 数据库配置
# DATABASES = {
#     "name": "demo",
#     "user": "root",
#     "password": "123",
#     "host": "localhost",
#     "port": 3306,
#     "charset": "utf8",
# }
# mysql_obj = Mysql(name="demo",user="root",password="123",host="localhost",port=3306,charset="utf8")
# 推荐
mysql_obj = Mysql(**MYSQL_DATABASES)

"""——————查看所有数据库——————"""
# database_list = mysql_obj.show_databases()
# print(database_list)
"""
['demo', 'pymysqlmodel_demo']
"""

"""——————查看所有用户——————"""
# user_list = mysql_obj.show_user()
# print(user_list)
"""
[{'name': 'root', 'host': 'localhost'}]
"""

"""——————设置用户登录权限——————"""
# mysql_obj.set_user_host(username="root", password="admin", host_list=["%","127.0.0.1"])
# mysql_obj.set_user_host(username="test_data", password="admin", host_list=["%","127.0.0.1"], dbname="test_data")
# user_list = mysql_obj.show_user()
# print(user_list)
"""
[
    {'name': 'root', 'host': '%'}, 
    {'name': 'test_data', 'host': '192.168.1.123'}, 
    {'name': 'test_data', 'host': '192.168.1.456'}, 
    {'name': 'root', 'host': 'localhost'}, 
    {'name': 'test_data', 'host': 'localhost'}
]
"""

"""——————查看所有表——————"""
# table_list = mysql_obj.show_table()
# print(table_list)
"""
['student_tb', 'test_data', 'test_data_copy1', 'test_data_copy2', 'test_data_copy3', 'test_data_copy4']
"""

"""——————创建表——————"""
# 创建表，已存在直接返回，不存在则创建

# 表名
# table_name = "class_tb"
# # 表字段
# # 原生 sql 语句
# class_table_fields = {
#     "id": "int NOT NULL PRIMARY KEY AUTO_INCREMENT",
#     "name": "varchar(20)",  # 一个字符串为一个字段
# }
# mysql_obj.create_table(table_name=table_name, field_dict=class_table_fields)
#
#
# # 原生创建
# sql = """
# CREATE TABLE `student_1_tb` (
#     `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
#     `name` varchar(20) DEFAULT NULL COMMENT '名称',
#     `age` int,
#     `gender` enum('男','女'),
#     `phone` varchar(11),
#     `sid` int not null,
#     FOREIGN KEY (sid) REFERENCES class_tb(id)
# )COMMENT '学生表';
# """
# mysql_obj.create_table(native_sql=sql)

"""——————指定操作表——————"""
# 每次执行查询、添加、删除、修改需指定操作表
# mysql_obj.table("class_tb")

# 主要用于设置 表名，获取表字段
# 同一对象只需设置一次即可
# print(mysql_obj.table_name) # 查看操作表名
# print(mysql_obj.field_list) # 查看字段列表
"""
class_tb
['id', 'name']
"""

"""——————添加数据——————"""
# 添加数据

# mysql_obj.table("class_tb").create(id=None, name="一班")


# name = "张三"
# age = "18"
# gender = 1
# phone = "12345678910"
# sid = 1
# 
# create_row = mysql_obj.table("student_tb").create(name=name,age=age,gender=gender,phone=phone, sid=sid)
# print(create_row)
"""
1
"""
# # 或
# temp_dict = {
#     "name": "张三1",
#     "age": "18",
#     "gender": 1,
#     "phone": "12345678910",
#     "sid": 1,
# }
# create_row = mysql_obj.table("student_tb").create(**temp_dict)
# print(create_row)
"""
1
"""

"""——————删除数据——————"""
# delete_row = mysql_obj.table("student_tb").where("id=%s", 5).delete()
# print(delete_row)
"""
1
"""

"""——————修改数据——————"""
# # update 修改结果
# update_row = mysql_obj.table("student_tb").where("age=%s",18).update(age=19)
# print(update_row)
"""
2
"""

"""——————查询数据——————"""
# 查询所有数据
# result = mysql_obj.table("student_tb").select()
# print(result)
"""
[
    {'id': 1, 'name': '张三', 'age': 19, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
    {'id': 2, 'name': '李四', 'age': 18, 'gender': '女', 'phone': '12345678911', 'sid': 1}, 
    {'id': 3, 'name': '王五', 'age': 20, 'gender': '女', 'phone': '12345678912', 'sid': 2}, 
    {'id': 4, 'name': '赵六', 'age': 23, 'gender': '男', 'phone': '12345678913', 'sid': 1}
]
"""

# 指定字段
# result = mysql_obj.table("student_tb").select("name","age")
# print(result)
"""
[
    {'name': '张三', 'age': 19}, 
    {'name': '李四', 'age': 18}, 
    {'name': '王五', 'age': 20}, 
    {'name': '赵六', 'age': 23}
]
"""

# 聚合查询 as 解析
# result = mysql_obj.table("student_tb").where("id>0 group by gender").select("gender", "avg(age) as age")
# print(result)
"""
[
    {'gender': '男', 'age': Decimal('45.0000')}, 
    {'gender': '女', 'age': Decimal('13.5000')}
]
"""

"""——————find 查询单条数据——————"""
# result = mysql_obj.table("student_tb").find()
# print(result)
"""
{
    'id': 1, 
    'name': '张三', 
    'age': 18, 
    'gender': '男', 
    'phone': '12345678910', 
    'sid': 1
}
"""

# 指定字段
# result = mysql_obj.table("student_tb").where("gender=%s", "女").find("name","phone")
# print(result)
"""
{
    'name': '李四', 
    'phone': '12345678911'
}
"""

"""——————执行原生 sql——————"""
# # 可同时执行多条语句
# # sql 语句要以 ; 号分隔
# 
# sql = f"""
#      select id,name,age  from student_tb where age > 18;
#      select id,name,phone from student_tb;
# """
# mysql_obj.table("student_tb")
# # 改方法可以执行多条 sql 语句
# result = mysql_obj.execute_native_sql(sql)
# # print(result)
# for i in result:
#     print(i)
"""
[
    {
        'name': '结果1', # 结果名称
        'abstract': {
            'name': 'select id,name,age  from student_tb where age > 18', # 摘要
            'info': 'OK', # 信息
            'select_time': 0.0010004043579101562 # 执行时间
        }, 
        'result': [ # 结果
            {'id': 1, 'name': '张三', 'age': 19}, 
            {'id': 3, 'name': '王五', 'age': 20}, 
            {'id': 4, 'name': '赵六', 'age': 23}
        ]
    }, 
    {
        'name': '结果2', 
        'abstract': {
            'name': 'select id,name,phone from student_tb',
            'info': 'OK', 
            'select_time': 0.0
        }, 
        'result': [
            {'id': 1, 'name': '张三', 'phone': '12345678910'}, 
            {'id': 2, 'name': '李四', 'phone': '12345678911'}, 
            {'id': 3, 'name': '王五', 'phone': '12345678912'}, 
            {'id': 4, 'name': '赵六', 'phone': '12345678913'}
        ]
    }

]
"""

sql = f"""
    use demo;
    select id,name,phone from student_tb;
    update student_tb set age=19 where id=2
"""
# # 改方法可以执行多条 sql 语句
# result = mysql_obj.execute_native_sql(sql)
# # print(result)
# for query_set in result:
#     print("名称", query_set["name"])
#     print("摘要", query_set["abstract"]["name"], query_set["abstract"]["info"])
#     print("信息", query_set["abstract"]["info"])
#     print("查询时间", query_set["abstract"]["select_time"])
#     if query_set.get("result"):
#         print("查询结果", query_set["result"] if len(query_set["result"]) < 11 else query_set["result"][:10])
#     print("\n")
"""
名称 结果1
摘要 use demo OK
信息 OK
查询时间 0.0


名称 结果2
摘要 select id,name,phone from student_tb OK
信息 OK
查询时间 0.7977244853973389
查询结果 [{'id': 1, 'name': '张三', 'phone': '12345678910'}, {'id': 2, 'name': '李四', 'phone': '12345678911'}, {'id': 3, 'name': '王五', 'phone': '12345678912'}, {'id': 4, 'name': '赵六', 'phone': '12345678913'}, {'id': 5, 'name': 'Jackson', 'phone': '7693577033'}, {'id': 6, 'name': 'Man', 'phone': '16514536481'}, {'id': 7, 'name': 'Fu', 'phone': '16836949674'}, {'id': 8, 'name': 'Chow', 'phone': '14741232401'}, {'id': 9, 'name': 'Wong', 'phone': '76984392374'}, {'id': 10, 'name': '卢', 'phone': '76949204670'}]


名称 结果3
摘要 update student_tb set age=18 where id=2 Affected rows：0
信息 影响行数：1
查询时间 0.0010013580322265625


# 注意事项
#
# 单表查询
# 例：
# 第一种：手动指定操作表
# mysql_obj.table("mysql.user") # 指定操作表，获取表字段，否则返回查询的数据异常
# result = mysql_obj.execute_native_sql("select * from mysql.user;")
# print(result)
# 第二种：sql 语句中指定查询字段
# result = mysql_obj.execute_native_sql("select User,Host from mysql.user;")
# print(result)

# 多表查询、或其他查询
# 请勿使用 select *，请在 sql 中指定查询结果字段
# 例：
# sql = "select s.name as sname,c.name as cname from student_tb as s, class_tb as c where s.sid = c.id"
# result = mysql_obj.execute_native_sql(sql)
# print(result)


"""

"""——————调用 pymysql 执行——————"""
# result_field = ["name","age"]
#
# # sql 语句不限
# sql = f"""
#     select {",".join(result_field)}  from {mysql_obj.table_name} where name like '张%';
# """
#
# # 调用实例属性 获取游标对象 执行sql语句
# mysql_obj.mysql_cursor.execute(sql)
# list_data = mysql_obj.mysql_cursor.fetchall()
# print(list_data)
# # 调用方法 组织数据
# student_list = mysql_obj.result(result_field,list_data)
# print(student_list)

"""
(('张三', 18),)
[{'name': '张三', 'age': 18}]
"""