from PySQLModel import SQLite
from setting import SQLITE_DATABASE


def init_db():
    """初始化数据库连接"""
    # 数据库配置
    # DATABASES = {
    #     "database": "./demo.db"
    # }
    return SQLite(**SQLITE_DATABASE)


def show_tables_example(sqlite_obj):
    """查看所有表示例"""
    table_list = sqlite_obj.show_table()
    print(table_list)
    """
    ['student_tb']
    """


def create_tables_example(sqlite_obj):
    """创建表示例"""
    # 创建表，已存在直接返回，不存在则创建
    table_name = "student_tb"
    student_table_fields = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "VARCHAR(20)",  # 一个字符串为一个字段
        "age": "INTEGER",
        "gender": "VARCHAR (1)",
        "phone": "varchar(11)",
        "sid": "int not null",
    }
    sqlite_obj.create_table(table_name, student_table_fields)


def table_operations_example(sqlite_obj):
    """表操作示例"""
    # 每次执行查询、添加、删除、修改需指定操作表
    sqlite_obj.table("student_tb")

    # 主要用于设置 表名，获取表字段
    # 同一对象只需设置一次即可
    print(sqlite_obj.table_name)  # 查看操作表名
    print(sqlite_obj.field_list)  # 查看字段列表
    """
    student_tb
    ['id', 'name', 'age', 'gender', 'phone', 'sid']
    """

    sqlite_obj.select()
    print(sqlite_obj.sql)  # 查看执行 sql
    print(sqlite_obj.args)  # 查看执行参数
    """
    select id, name, age, gender, phone, sid from `student_tb`
    []
    """


def insert_data_example(sqlite_obj):
    """添加数据示例"""
    # 添加数据
    name = "张三1"
    age = "18"
    gender = "男"
    phone = "12345678910"
    sid = 1

    create_id = sqlite_obj.table("student_tb").create(
        name=name, age=age, gender=gender, phone=phone, sid=sid
    )
    print(create_id)

    # 或使用字典方式
    temp_dict = {
        "name": "张三2",
        "age": "20",
        "gender": "女",
        "phone": "12345678910",
        "sid": 1,
    }
    create_id = sqlite_obj.create(**temp_dict)
    print(create_id)


def delete_data_example(sqlite_obj):
    """删除数据示例"""
    delete_row = sqlite_obj.table("student_tb").where("id=?", 5).delete()
    print(delete_row)
    """
    1
    """


def update_data_example(sqlite_obj):
    """修改数据示例"""
    update_row = sqlite_obj.table("student_tb").where("age=?", 18).update(age=19)
    print(update_row)


def query_data_example(sqlite_obj):
    """查询数据示例"""
    # 查询所有数据
    result = sqlite_obj.table("student_tb").select()
    print(result)
    """
    [
        {'id': 1, 'name': '张三2', 'age': 20, 'gender': '2', 'phone': '12345678910'}, 
        {'id': 2, 'name': '张三2', 'age': 20, 'gender': '2', 'phone': '12345678910'}
    ]
    """

    # 指定字段
    result = sqlite_obj.table("student_tb").fields("id", "age").select()
    print(result)
    """
    [
        {'id': 1, 'age': 20}, 
        {'id': 2, 'age': 20}
    ]
    """


def order_by_example(sqlite_obj):
    """排序示例"""
    result = sqlite_obj.table("student_tb").where("sid=?", 1).order_by("-age", "id").select()
    print(sqlite_obj.sql)
    print(result)
    """
    select id, name, age, gender, phone, sid from `student_tb` where sid=? order by `age` desc, `id` asc
    [
        {'id': 2, 'name': '张三1', 'age': 20, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 1, 'name': '张三1', 'age': 19, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 3, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 4, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910', 'sid': 1}
    ]
    """


def pagination_example(sqlite_obj):
    """分页示例"""
    page = 1
    pagesize = 3
    sqlite_obj.table("student_tb").where("sid=?", 1).order_by("-age", "id")
    total, page_number = sqlite_obj.page(page=page, pagesize=pagesize)
    result = sqlite_obj.select()
    print(sqlite_obj.sql)
    print(f"总数：{total}, 页数:{page_number}")
    print(result)
    """
    select id, name, age, gender, phone, sid from `student_tb` where sid=? order by `age` desc, `id` asc LIMIT 3 offset 0
    总数：4, 页数:2
    [
        {'id': 2, 'name': '张三1', 'age': 20, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 1, 'name': '张三1', 'age': 19, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 3, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '12345678910', 'sid': 1}
    ]
    """


def aggregation_example(sqlite_obj):
    """聚合查询示例"""
    result = sqlite_obj.table("student_tb").fields("gender", "avg(age) as age").where("id>0 group by gender").select()
    print(result)
    """
    [
        {'gender': '女', 'age': 22.0}, 
        {'gender': '男', 'age': 18.0}
    ]
    """


def find_example(sqlite_obj):
    """查询单条数据示例"""
    result = sqlite_obj.table("student_tb").find()
    print(result)
    """
    {
        'id': 1, 
        'name': '张三1', 
        'age': 18, 
        'gender': '男', 
        'phone': '12345678910'
    }
    """

    # 指定字段
    result = sqlite_obj.table("student_tb").fields("id", "age").where("gender=?", "女").find()
    print(result)
    """
    {
        'id': 9, 
        'age': 18
    }
    """


def raw_sql_example(sqlite_obj):
    """原生SQL执行示例"""
    result_field = ["name", "age"]

    sqlite_obj.table("student_tb")
    # sql 语句不限
    sql = f"""
        select {",".join(result_field)} from {sqlite_obj.table_name} where name like '张%'
    """

    # 调用实例属性 获取游标对象 执行sql语句
    sqlite_obj.cursor.execute(sql)
    data = sqlite_obj.cursor.fetchone()  # 获取单条查询结果
    list_data = sqlite_obj.cursor.fetchall()  # 获取查询结果集
    print(data)
    print(list_data)
    """
    ('张三1', 19)
    [('张三1', 19), ('张三1', 19), ('张三1', 19), ('张三1', 19), ('张三1', 19)]
    """


def transaction_example(sqlite_obj):
    """事务使用示例"""
    try:
        with sqlite_obj.atomic():
            # 在事务中执行多个操作
            sqlite_obj.table("student_tb").create(
                name="李四",
                age=19,
                gender="男",
                phone="12345678911",
                sid=1
            )

            # 再插入一条数据
            sqlite_obj.table("student_tb").create(
                name="王五",
                age=20,
                gender="女",
                phone="12345678912",
                sid=1
            )

            # 如果这里发生异常，之前的操作都会回滚
            # raise Exception("测试回滚")

        print("事务执行成功")
    except Exception as e:
        print(f"事务执行失败: {e}")


def main():
    """主函数"""
    sqlite_obj = init_db()
    try:
        # 这里可以调用各个示例函数
        show_tables_example(sqlite_obj)
        create_tables_example(sqlite_obj)
        table_operations_example(sqlite_obj)
        # insert_data_example(sqlite_obj)
        # delete_data_example(sqlite_obj)
        # update_data_example(sqlite_obj)
        # query_data_example(sqlite_obj)
        # order_by_example(sqlite_obj)
        # pagination_example(sqlite_obj)
        # aggregation_example(sqlite_obj)
        # find_example(sqlite_obj)
        # raw_sql_example(sqlite_obj)
        transaction_example(sqlite_obj)
    finally:
        sqlite_obj.close()


if __name__ == "__main__":
    main()
