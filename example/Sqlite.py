from SqlModel.sqlite import SQLite
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
# sqlite3_obj = Sqlite(name="demo",user="root",password="123",host="localhost",port=3306,charset="utf8")
# 推荐
sqlite3_obj = Sqlite(**SQLITE_DATABASE)

"""——————查看所有表——————"""
# table_list = sqlite3_obj.show_table()
# print(table_list)
"""
['sqlite_sequence', 'student_tb']
"""

"""——————创建表——————"""
# 创建表，已存在直接返回，不存在则创建

# # 表名
# table_name = "student_tb"
# 表字段
# 原生 sql 语句
# student_table_fields = {
#     "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
#     "name": "VARCHAR(20)",  # 一个字符串为一个字段
#     "age": "INTEGER",
#     "gender": "VARCHAR (1)",
#     "phone": "varchar(11)",
# }
# 
# sqlite3_obj.create_table(table_name,student_table_fields)

"""——————指定操作表——————"""
# 每次执行查询、添加、删除、修改需指定操作表
# sqlite3_obj.table("student_tb")

# 主要用于设置 表名，获取表字段
# 同一对象只需设置一次即可
# print(sqlite3_obj.table_name) # 查看操作表名
# print(sqlite3_obj.field_list) # 查看字段列表
"""
class_tb
['id', 'name']
"""

"""——————添加数据——————"""
# # 添加数据
# name = "张三1"
# age = "18"
# gender = "男"
# phone = "12345678910"
#
# temp_dict = {
#     "name": "张三2",
#     "age": "20",
#     "gender": "女",
#     "phone": "12345678910",
# }
# create_row = sqlite3_obj.table("student_tb").create(name=name,age=age,gender=gender,phone=phone)
# print(create_row)

# # 或这样
# create_row = sqlite3_obj.create(**temp_dict)
# print(create_row)

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
# result = sqlite3_obj.table("student_tb").select("id","age")
# print(result)

"""
[
    {'id': 1, 'age': 20}, 
    {'id': 2, 'age': 20}
]
"""

# 聚合查询 as 解析
# result = sqlite3_obj.table("student_tb").where("id>0 group by gender").select("gender", "avg(age) as age")
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
# result = sqlite3_obj.table("student_tb").where("gender=?", "女").find("id","age")
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
# # sql 语句不限
# sql = f"""
#     select {",".join(result_field)}  from {sqlite3_obj.table_name} where name like '张%'
# """
#
# # 调用实例属性 获取游标对象 执行sql语句
# sqlite3_obj.sqlite.execute(sql)
# data = sqlite3_obj.sqlite.fetchone() # 获取单跳查询结果
# list_data = sqlite3_obj.sqlite.fetchall() # 获取查询结果集
# print(data)
# print(list_data)
#
# # 调用方法 组织数据
# student_list = sqlite3_obj.result(result_field,data)
# print(student_list)
#
# student_list = sqlite3_obj.result(result_field,list_data)
# print(student_list)

"""
('张三2', 19)
[('张三2', 18)]
{'name': '张三2', 'age': 19}
[{'name': '张三2', 'age': 18}]
"""