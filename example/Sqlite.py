

from SelectModel.sqlite import Sqlite
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
# StudentModel = Mysql(name="demo",user="root",password="123",host="localhost",port=3306,charset="utf8")
# 推荐
StudentModel = Sqlite(**SQLITE_DATABASE)

"""——————查看所有表——————"""
# table_list = StudentModel.show_table()
# print(table_list)
"""
['sqlite_sequence', 'student_tb']
"""

"""——————创建表——————"""
# 创建表，已存在直接返回，不存在则创建

# # 表名
table_name = "student_tb"
# 表字段
# 原生 sql 语句
student_table_fields = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "VARCHAR(20)",  # 一个字符串为一个字段
    "age": "INTEGER",
    "gender": "VARCHAR (1)",
    "phone": "varchar(11)",
}

StudentModel.create_table(table_name,student_table_fields)

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
# is_success = StudentModel.create(name=name,age=age,gender=gender,phone=phone)
#
# # 或这样
# is_success = StudentModel.create(**temp_dict)

"""——————删除数据——————"""
# is_success = StudentModel.delete(age=18)
#
# # 或者 原生 sql
# is_success = StudentModel.delete(native_sql=f"delete from student_tb where age=18")

"""——————查询全部数据——————"""
# result = StudentModel.all()
# print(result)
#
# # 指定字段
# result = StudentModel.all("id","age")
# print(result)

"""
[{'id': 1, 'name': '张三2', 'age': 20, 'gender': '2', 'phone': '12345678910'}, {'id': 2, 'name': '张三2', 'age': 20, 'gender': '2', 'phone': '12345678910'}]
[{'id': 1, 'age': 20}, {'id': 2, 'age': 20}]
"""

"""——————filter 批量条件查询数据——————"""
# result = StudentModel.filter(age=18)
# print(result)
#
# # 指定字段
# result = StudentModel.filter("id","age",gender="男")
# print(result)
#
# # 原生查询
# result = StudentModel.filter(native_sql="select * from student_tb where gender='男'")
# print(result)
#
# # 自动解析 查询结果字段
# # as 查询结果字段重命名
# # 两表联查去除表别名：表别名.字段名
# result = StudentModel.filter(native_sql="select s.id,age as a,gender from student_tb as s where gender='男'")
# print(result)

"""
[{'id': 1, 'name': '张三2', 'age': 18, 'gender': '男', 'phone': '12345678910'}, {'id': 2, 'name': '张三2', 'age': 18, 'gender': '男', 'phone': '12345678910'}]
[{'id': 1, 'age': 18}, {'id': 2, 'age': 18}]
[{'id': 1, 'name': '张三2', 'age': 18, 'gender': '男', 'phone': '12345678910'}, {'id': 2, 'name': '张三2', 'age': 18, 'gender': '男', 'phone': '12345678910'}]
[{'id': 1, 'a': 18, 'gender': '男'}, {'id': 2, 'a': 18, 'gender': '男'}]
"""

"""——————get 单个条件查询数据——————"""
# result = StudentModel.get(age=18)
# print(result)
#
# # 指定字段
# result = StudentModel.get("id","age",gender="男")
# print(result)
#
# # 原生查询
# result = StudentModel.get(native_sql="select * from student_tb where gender='男'")
# print(result)
#
# # 自动解析 查询结果字段
# # as 查询结果字段重命名
# # 两表联查去除表别名：表别名.字段名
# result = StudentModel.get(native_sql="select s.id,age as a,gender from student_tb as s where gender='男'")
# print(result)

"""
{'id': 1, 'name': '张三2', 'age': 18, 'gender': '男', 'phone': '12345678910'}
{'id': 1, 'age': 18}
{'id': 1, 'name': '张三2', 'age': 18, 'gender': '男', 'phone': '12345678910'}
{'id': 1, 'a': 18, 'gender': '男'}
"""

"""——————修改数据——————"""
# # 使用 update 方法之前需要先调用，update_condition
# # update_condition 要修改数据的条件
# # update 修改结果
# is_success = StudentModel.update_condition(id=1).update(age=19)
#
# # 或者 原生 sql
# # 当使用原生 sql 修改时可以直接调用 update 方法
# is_success = StudentModel.update(native_sql=f"update student_tb set gender='女' where id=2")

"""——————聚合查询——————"""
# result = StudentModel.filter("avg(age)",age=18)
# print(result)
#
# result = StudentModel.filter(native_sql="select avg(age) as a from student_tb")
# print(result)

"""
[{'avg(age)': 18.0}]
[{'a': 19.0}]
"""

"""——————调用 sqlite 执行——————"""
# result_field = ["name","age"]
#
# # sql 语句不限
# sql = f"""
#     select {",".join(result_field)}  from {StudentModel.table_name} where name like '张%'
# """
#
# # 调用实例属性 获取游标对象 执行sql语句
# StudentModel.sqlite.execute(sql)
# data = StudentModel.sqlite.fetchone() # 获取单跳查询结果
# list_data = StudentModel.sqlite.fetchall() # 获取查询结果集
# print(data)
# print(list_data)
#
# # 调用方法 组织数据
# student_list = StudentModel.result(result_field,data)
# print(student_list)
#
# student_list = StudentModel.result(result_field,list_data)
# print(student_list)

"""
('张三2', 19)
[('张三2', 18)]
{'name': '张三2', 'age': 19}
[{'name': '张三2', 'age': 18}]
"""

"""——————扩展——————"""
# name = "张三1"
# age = "18"
# gender = "男"
# phone = None
#
# # 关键字传参
# result = StudentModel.filter(name=name,age=age)
# print(result)
#
# temp_dict = {
#     "name": "张三2",
#     "age": "20",
#     "gender": "女",
#     "phone": "12345678910",
# }
# # 接受一个 **kwargs 参数
# result = StudentModel.filter(**temp_dict)
# print(result)
#
# temp = {}
# if name:
#     temp["name"] = name
# if age:
#     temp["age"] = age
# if gender:
#     temp["gender"] = gender
# if phone:
#     temp["phone"] = phone
# # 接受一个 **kwargs 参数
# result = StudentModel.filter(**temp)
# print(result)

"""
[{'id': 1, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910'}]
[{'id': 2, 'name': '张三2', 'age': 20, 'gender': '女', 'phone': '12345678910'}]
[{'id': 1, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910'}]
"""