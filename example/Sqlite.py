from src.PySQLModel import SQLite

from setting import SQLITE_DATABASE

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
# sqlite3_obj = SQLite(name="demo",user="root",password="123",host="localhost",port=3306,charset="utf8")
# 推荐
sqlite3_obj = SQLite(**SQLITE_DATABASE)

"""——————查看所有表——————"""
# table_list = sqlite3_obj.show_table()
# print(table_list)
"""
['student_tb']
"""

"""——————创建表——————"""
# 创建表，已存在直接返回，不存在则创建

# 表名
table_name = "student_tb"
# 表字段
# 原生 sql 语句
# student_table_fields = {
#     "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
#     "name": "VARCHAR(20)",  # 一个字符串为一个字段
#     "age": "INTEGER",
#     "gender": "VARCHAR (1)",
#     "phone": "varchar(11)",
#     "sid": "int not null",
# }
# 
# sqlite3_obj.create_table(table_name,student_table_fields)

"""——————指定操作表——————"""
# 每次执行查询、添加、删除、修改需指定操作表
sqlite3_obj.table("student_tb")

# 主要用于设置 表名，获取表字段
# 同一对象只需设置一次即可
# print(sqlite3_obj.table_name) # 查看操作表名
# print(sqlite3_obj.field_list) # 查看字段列表
"""
class_tb
['id', 'name']
"""

# sqlite3_obj.select()
# print(sqlite3_obj.sql)  # 查看执行 sql
# print(sqlite3_obj.args)  # 查看执行参数
"""
select id, name, age, gender, phone from `student_tb`
[]
"""

"""——————添加数据——————"""
# # 添加数据
# name = "张三1"
# age = "18"
# gender = "男"
# phone = "12345678910"
# sid = 1
# 
# temp_dict = {
#     "name": "张三2",
#     "age": "20",
#     "gender": "女",
#     "phone": "12345678910",
#     "sid": 1,
# }
# create_id = sqlite3_obj.table("student_tb").create(name=name,age=age,gender=gender,phone=phone, sid=sid)
# print(create_id)

# # 或这样
# create_id = sqlite3_obj.create(**temp_dict)
# print(create_id)

"""——————删除数据——————"""
# delete_row = sqlite3_obj.table("student_tb").where("id=?", 5).delete()
# print(delete_row)
"""
1
"""

"""——————修改数据——————"""
# update 修改结果
# update_row = sqlite3_obj.table("student_tb").where("age=?", 18).update(age=19)
# print(update_row)

"""——————查询全部数据——————"""
# result = sqlite3_obj.table("student_tb").select()
# print(result)
"""
[
    {'id': 1, 'name': '张三2', 'age': 20, 'gender': '2', 'phone': '12345678910'}, 
    {'id': 2, 'name': '张三2', 'age': 20, 'gender': '2', 'phone': '12345678910'}
]
"""

# # 指定字段
# result = sqlite3_obj.table("student_tb").fields("id", "age").select()
# print(result)

"""
[
    {'id': 1, 'age': 20}, 
    {'id': 2, 'age': 20}
]
"""

# 排序
# result = sqlite3_obj.table("student_tb").where("sid=?", 1).order_by("-age", "id").select()
# print(sqlite3_obj.sql)
# print(result)
"""
select id, name, age, gender, phone, sid from `student_tb` where sid=? order by `age` desc, `id` asc
[
    {'id': 2, 'name': '张三1', 'age': 20, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
    {'id': 1, 'name': '张三1', 'age': 19, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
    {'id': 3, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
    {'id': 4, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910', 'sid': 1}
]

"""

# 分页
# page = 1
# pagesize = 3
# sqlite3_obj.table("student_tb").where("sid=?", 1).order_by("-age", "id")
# total, page_number = sqlite3_obj.page(page=page, pagesize=pagesize)
# result = sqlite3_obj.select()
# print(sqlite3_obj.sql)
# print(f"总数：{total}, 页数:{page_number}")
# print(result)
"""
select id, name, age, gender, phone, sid from `student_tb` where sid=? order by `age` desc, `id` asc LIMIT 3 offset 0
总数：4, 页数:2
[
    {'id': 2, 'name': '张三1', 'age': 20, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
    {'id': 1, 'name': '张三1', 'age': 19, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
    {'id': 3, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910', 'sid': 1}
]
"""

# 聚合查询 as 解析
# result = sqlite3_obj.table("student_tb").fields("gender", "avg(age) as age").where("id>0 group by gender").select()
# print(result)
"""
[
    {'gender': '女', 'age': 22.0}, 
    {'gender': '男', 'age': 18.0}
]
"""

"""——————find 查询单条数据——————"""
# result = sqlite3_obj.table("student_tb").find()
# print(result)
"""
{
    'id': 1, 
    'name': '张三1', 
    'age': 18, 
    'gender': '男', 
    'phone': '12345678910'
}
"""

# # 指定字段
# result = sqlite3_obj.table("student_tb").fields("id", "age").where("gender=?", "女").find()
# print(result)
"""
{
    'id': 9, 
    'age': 18
}
"""

"""——————调用 sqlite 执行——————"""
# result_field = ["name","age"]
# 
# sqlite3_obj.table("student_tb")
# # sql 语句不限
# sql = f"""
#     select {",".join(result_field)}  from {sqlite3_obj.table_name} where name like '张%'
# """
# 
# # 调用实例属性 获取游标对象 执行sql语句
# sqlite3_obj.cursor.execute(sql)
# data = sqlite3_obj.cursor.fetchone() # 获取单跳查询结果
# list_data = sqlite3_obj.cursor.fetchall() # 获取查询结果集
# print(data)
# print(list_data)

"""
('张三1', 19)
[('张三1', 19), ('张三1', 19), ('张三1', 19), ('张三1', 19), ('张三1', 19)]
"""

print("`' as as`\"".strip(" `'\""))