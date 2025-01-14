# 导入MySQL模型
# 导入数据库配置
from PySQLModel import MySQL

from setting import MYSQL_DATABASES


def init_db():
    """初始化数据库连接"""
    # 数据库配置
    # DATABASES = {
    #     "database": "demo",
    #     "user": "root",
    #     "password": "123",
    #     "host": "localhost",
    #     "port": 3306,
    #     "charset": "utf8",
    # }
    # mysql_obj = MySQL(name="demo",user="root",password="123",host="localhost",port=3306,charset="utf8")
    # 推荐
    return MySQL(**MYSQL_DATABASES)


def show_tables_example(mysql_obj):
    """查看所有表示例"""
    table_list = mysql_obj.show_table()
    print(table_list)
    """
    ['student_tb', 'test_data', 'test_data_copy1', 'test_data_copy2', 'test_data_copy3', 'test_data_copy4']
    """


def create_tables_example(mysql_obj):
    """创建表示例"""
    # 创建表，已存在直接返回，不存在则创建

    # 表名
    table_name = "class_tb"
    # 表字段
    # 原生 sql 语句
    class_table_fields = {
        "id": "int NOT NULL PRIMARY KEY AUTO_INCREMENT",
        "name": "varchar(20)",  # 一个字符串为一个字段
    }
    mysql_obj.create_table(table_name=table_name, field_dict=class_table_fields)

    # 原生创建
    sql = """
    CREATE TABLE `student_1_tb` (
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `name` varchar(20) DEFAULT NULL COMMENT '名称',
        `age` int,
        `gender` enum('男','女'),
        `phone` varchar(11),
        `sid` int not null,
        FOREIGN KEY (sid) REFERENCES class_tb(id)
    )COMMENT '学生表';
    """
    mysql_obj.create_table(native_sql=sql)


def table_operations_example(mysql_obj):
    """表操作示例"""
    # 每次执行查询、添加、删除、修改需指定操作表
    mysql_obj.table("class_tb")

    # 主要用于设置 表名，获取表字段
    # 同一对象只需设置一次即可
    print(mysql_obj.table_name)  # 查看操作表名
    print(mysql_obj.field_list)  # 查看字段列表
    """
    class_tb
    ['id', 'name']
    """

    mysql_obj.select()
    print(mysql_obj.sql)  # 查看执行 sql
    print(mysql_obj.args)  # 查看执行参数
    """
    select id, name from `class_tb`
    []
    """


def insert_data_example(mysql_obj):
    """添加数据示例"""
    row_num = mysql_obj.table("class_tb").create(id=None, name="一班")
    print(row_num)

    name = "张三"
    age = "18"
    gender = 1
    phone = "12345678910"
    sid = 1

    create_id = mysql_obj.table("student_tb").create(name=name, age=age, gender=gender, phone=phone, sid=sid)
    print(create_id)
    """
    1
    """
    # 或
    temp_dict = {
        "name": "张三1",
        "age": "18",
        "gender": 1,
        "phone": "12345678910",
        "sid": 1,
    }
    create_id = mysql_obj.table("student_tb").create(**temp_dict)
    print(create_id)
    """
    1
    """


def delete_data_example(mysql_obj):
    """删除数据示例"""
    delete_row = mysql_obj.table("student_tb").where("id=%s", 5).delete()
    print(delete_row)
    """
    1
    """


def update_data_example(mysql_obj):
    """修改数据示例"""
    update_row = mysql_obj.table("student_tb").where("age=%s", 18).update(age=19)
    print(update_row)
    """
    2
    """


def query_data_example(mysql_obj):
    """查询数据示例"""
    # 查询所有数据
    result = mysql_obj.table("student_tb").select()
    print(result)
    """
    [
        {'id': 1, 'name': '张三', 'age': 19, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 2, 'name': '李四', 'age': 18, 'gender': '女', 'phone': '12345678911', 'sid': 1}, 
        {'id': 3, 'name': '王五', 'age': 20, 'gender': '女', 'phone': '12345678912', 'sid': 2}, 
        {'id': 4, 'name': '赵六', 'age': 23, 'gender': '男', 'phone': '12345678913', 'sid': 1}
    ]
    """

    # 指定字段
    result = mysql_obj.table("student_tb").fields("name", "age").select()
    print(result)
    """
    [
        {'name': '张三', 'age': 19}, 
        {'name': '李四', 'age': 18}, 
        {'name': '王五', 'age': 20}, 
        {'name': '赵六', 'age': 23}
    ]
    """


def order_by_example(mysql_obj):
    """排序示例"""
    result = mysql_obj.table("student_tb").where("sid=%s", 1).order_by("-age", "id").select()
    print(mysql_obj.sql)
    print(result)
    """
    select id, name, age, gender, phone, sid from `student_tb` where sid=%s order by `age` desc, `id` desc
    [
        {'id': 2, 'name': '李四', 'age': 19, 'gender': '女', 'phone': '12345678911', 'sid': 1}, 
        {'id': 1, 'name': '张三', 'age': 16, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 3, 'name': '王五', 'age': 10, 'gender': '男', 'phone': '12345678912', 'sid': 1}
        {'id': 4, 'name': '赵六', 'age': 10, 'gender': '女', 'phone': '12345678913', 'sid': 1}, 
    ]
    """


def pagination_example(mysql_obj):
    """分页示例"""
    page = 1
    pagesize = 3
    mysql_obj.table("student_tb").where("sid=%s", 1).order_by("-age", "id")
    total, page_number = mysql_obj.page(page=page, pagesize=pagesize)
    result = mysql_obj.select()
    print(mysql_obj.sql)
    print(f"总数：{total}, 页数:{page_number}")
    print(result)
    """
    select id, name, age, gender, phone, sid from `student_tb` where sid=%s order by `age` desc, `id` asc LIMIT 3 offset 0
    4 2
    [
        {'id': 2, 'name': '李四', 'age': 19, 'gender': '女', 'phone': '12345678911', 'sid': 1}, 
        {'id': 1, 'name': '张三', 'age': 16, 'gender': '男', 'phone': '12345678910', 'sid': 1}, 
        {'id': 3, 'name': '王五', 'age': 10, 'gender': '男', 'phone': '12345678912', 'sid': 1}
    ]
    """


def aggregation_example(mysql_obj):
    """聚合查询示例"""
    result = mysql_obj.table("student_tb").fields("gender", "avg(age) as age").where("id>0 group by gender").select()
    print(result)
    """
    [
        {'gender': '男', 'age': Decimal('45.0000')}, 
        {'gender': '女', 'age': Decimal('13.5000')}
    ]
    """


def find_example(mysql_obj):
    """查询单条数据示例"""
    result = mysql_obj.table("student_tb").find()
    print(result)
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
    result = mysql_obj.table("student_tb").fields("name", "phone").where("gender=%s", "女").find()
    print(result)
    """
    {
        'name': '李四', 
        'phone': '12345678911'
    }
    """


def raw_sql_example(mysql_obj):
    """原生SQL执行示例"""
    result_field = ["name", "age"]

    mysql_obj.table("student_tb")
    # sql 语句不限
    sql = f"""
        select {",".join(result_field)}  from {mysql_obj.table_name} where name like '张%';
    """

    # 调用实例属性 获取游标对象 执行sql语句
    mysql_obj.cursor.execute(sql)
    list_data = mysql_obj.cursor.fetchall()
    print(list_data)
    """
    (('张三', 16),)
    """


def transaction_example(mysql_obj):
    """事务使用示例"""
    try:
        with mysql_obj.atomic():
            # 在事务中执行多个操作
            class_id = mysql_obj.table("class_tb").create(id=None, name="二班")

            student_data = {
                "name": "李四",
                "age": 19,
                "gender": "女",
                "phone": "12345678911",
                "sid": class_id
            }
            mysql_obj.table("student_tb").create(**student_data)

            # 如果这里发生异常，之前的操作都会回滚
            # raise Exception("测试回滚")

        print("事务执行成功")
    except Exception as e:
        print(f"事务执行失败: {e}")


def main():
    """主函数"""
    mysql_obj = init_db()
    try:
        # 这里可以调用各个示例函数
        show_tables_example(mysql_obj)
        create_tables_example(mysql_obj)
        table_operations_example(mysql_obj)
        # insert_data_example(mysql_obj)
        # delete_data_example(mysql_obj)
        # update_data_example(mysql_obj)
        # query_data_example(mysql_obj)
        # order_by_example(mysql_obj)
        # pagination_example(mysql_obj)
        # aggregation_example(mysql_obj)
        # find_example(mysql_obj)
        # raw_sql_example(mysql_obj)
        transaction_example(mysql_obj)
    finally:
        mysql_obj.close()


if __name__ == "__main__":
    main()
