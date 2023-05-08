"""
@Project:SelectModel
@File:sqlite.py
@Author:函封封
"""

import sqlite3

# sqlite操作
class Sqlite():
    def __init__(self,**kwargs):
        """
        DATABASES = {
            "database": "./demo.db"
        }
        """
        self.sqlite_con = sqlite3.connect(**kwargs)
        self.sqlite = self.sqlite_con.cursor() # 创建游标对象
        self.table_name = None  # 表名
        self.field_list = []  # 表字段
        self.condition_sql = None # 修改条件

    def show_table(self):
        """
        show_tables()方法：查询当前数据库中所有表
        :return: 返回一个列表
        """
        sql = f"""select name from sqlite_master where type='table' order by name"""
        self.sqlite.execute(sql)
        data_list = self.sqlite.fetchall()
        table_list = [data[0] for data in data_list]
        return table_list # 返回当前数据库内所有的表

    def create_table(self, table_name:str, field_dict:dict):
        """
        create_table() 创建表，已存在直接返回，不存在则创建
        :param table_name: 表名
        :param field_dict: 表字段列表
        :return: 连接成功：返回 True
        """
        self.table_name = table_name  # 将表名赋值给实例属性

        self.field_list = field_dict.keys() # 获取该表的所有的字段名

        table_list = self.show_table()  # 获取数据库里所有的表
        if self.table_name in table_list:  # 判断该表是否已存在
            return True # 该表已存在！直接返回

        field_list = [f"`{key}` {value}" for key,value in field_dict.items()]
        create_field = ",".join(field_list)  # 将所有的字段与字段类型以 “ , ” 拼接
        sql = f"""
             create table `{self.table_name}`(
                {create_field}
              );
         """
        self.sqlite.execute(sql)
        self.sqlite_con.commit()
        return True

    def create(self,**kwargs):
        """
        create() 添加一行数据
        :param kwargs: 接收一个字典，key = value 字段 = 值
        :return: 添加成功：返回 True 添加失败：返回 Flase
        """
        try:
            value_list = []
            for field in self.field_list:
                value = kwargs.get(field)
                if value == None:
                    value = "NULL"
                else:
                    value = f"{value}" if isinstance(value, int) else f"'{value}'"
                value_list.append(value)
            field_sql = "`,`".join(self.field_list)
            create_sql = ",".join(value_list)

            # id 字段为null ，默认自增
            sql = f"""
                insert into `{self.table_name}`  (`{field_sql}`) values 
                ({create_sql});
            """
            self.sqlite.execute(sql)
        except Exception as err:
            self.sqlite_con.rollback()
            print(f"插入数据错误：{err}")
            return False
        else:
            self.sqlite_con.commit()
            return True

    def delete(self, native_sql=None,**kwargs):
        """
        delete() 删除条件满足的所有数据
        :param native_sql: 原生sql语句
        :param kwargs: 接收一个字典，key == value 条件
        :return: 删除成功：True 删除失败：False
        """
        try:
            if native_sql is not None:
                sql = native_sql
            else:
                condition_sql = self.create_condition_sql(**kwargs)
                # 删除数据
                sql = f"""
                    delete from `{self.table_name}` where {condition_sql};
                """
            self.sqlite.execute(sql)
        except Exception as err:
            self.sqlite_con.rollback()
            print(f"删除数据错误：{err}")
            return False
        else:
            self.sqlite_con.commit()
            return True

    def update(self, native_sql=None, **kwargs):
        """
        update() 修改数据
        :param id: 要修改行的 id
        :param kwargs: 接收一个字典，key == value 条件
        :return: 修改成功：返回 True 删除失败：返回 False
        """
        try:
            if native_sql is not None:
                sql = native_sql
            else:
                value_list = []
                for key, value in kwargs.items():
                    if key in self.field_list:
                        if value == None:
                            value = f"{key}=NULL"
                        elif isinstance(value, int):
                            value = f"{key}={value}"
                        else:
                            value = f"{key}='{value}'"
                        value_list.append(value)
                update_sql = ",".join(value_list)

                sql = f"""
                    update `{self.table_name}` set {update_sql} where {self.condition_sql};
                """
            self.sqlite.execute(sql)
        except Exception as err:
            self.sqlite_con.rollback()
            print("修改数据错误：", err)
            return False
        else:
            self.sqlite_con.commit()
            return True

    def all(self,*args):
        """
        all() 查询所有数据
        :param args: 接收一个列表，查询结果表字段，可聚合查询
        :return: 返回查询到的所有行，列表嵌套字典类型
        """
        result_field = args if len(args) != 0 else self.field_list
        select_field = ",".join(result_field)

        # 根据表名直接查询
        sql = f"""
            select {select_field} from `{self.table_name}`;
        """

        self.sqlite.execute(sql)
        data = self.sqlite.fetchall()

        result = self.result(result_field,data)
        return result # 最终返回查询集

    def filter(self, *args, native_sql=None, **kwargs):
        """
        filter() 查询数据库
        :param native_sql: 接收原生sql语句，用于复杂查询，如 order by,group by,子查询
        :param args: 接收一个列表，查询结果表字段，可聚合查询
        :param kwargs: 接收一个字典，key == value 条件
        :return: 返回查询到的所有行，为列表嵌套字典类型
        """
        if native_sql is not None:
            result_field = self.extract_field(native_sql)
            sql = native_sql
        else:
            condition_sql = self.create_condition_sql(**kwargs)

            # 结果字段
            result_field = args if len(args) != 0 else self.field_list
            select_field = ",".join(result_field)

            sql = f"""
                select {select_field} from `{self.table_name}` where {condition_sql};
            """
        self.sqlite.execute(sql)
        data = self.sqlite.fetchall()
        result = self.result(result_field,data)
        return result


    def get(self, *args, native_sql=None, **kwargs):
        """
        get() 查询数据库
        :param native_sql: 接收原生sql语句，用于复杂查询，如 order by,group by,子查询
        :param args: 接收一个列表，查询结果表字段，可聚合查询
        :param kwargs: 接收一个字典，key == value 条件
        :return: 返回查询到的第一行数据，为字典类型
        """
        if native_sql is not None:
            result_field = self.extract_field(native_sql)
            sql = native_sql
        else:
            condition_sql = self.create_condition_sql(**kwargs)

            # 结果字段
            result_field = args if len(args) != 0 else self.field_list
            select_field = ",".join(result_field)

            sql = f"""
                select {select_field} from `{self.table_name}` where {condition_sql} limit 1;
            """
        self.sqlite.execute(sql)
        data = self.sqlite.fetchone()
        result = self.result(result_field,data)
        return result

    def extract_field(self, native_sql:str):
        """
        extract_field() 原生查询提取查询字段
        :param kwargs: 接受一个字典，key == value 条件
        :return: sql条件语句
        """
        temp_field = str(native_sql).lower()
        temp_field = str(temp_field).split("from")[0]
        temp_field = str(temp_field).strip("select")
        temp_field = str(temp_field).strip()
        if temp_field == "*":
            result_field = self.field_list
        else:
            temp_field_list = temp_field.split(",")
            result_field = []
            for temp_field in temp_field_list:
                if len(temp_field.split("as")) != 1:
                    temp_field = temp_field.split("as")[-1]
                    temp_field = temp_field.strip()
                    temp_field = temp_field.split(".")[-1]
                    temp_field = temp_field.strip()
                elif len(temp_field.split(".")) != 1:
                    temp_field = temp_field.split(".")[-1]
                    temp_field = temp_field.strip()

                result_field.append(temp_field)
        return result_field

    def update_condition(self, **kwargs):
        self.condition_sql = self.create_condition_sql(**kwargs)
        return self


    def create_condition_sql(self, **kwargs):
        """
        create_condition_sql() 组织条件语句
        :param kwargs: 接受一个字典，key == value 条件
        :return: sql条件语句
        """
        condition_list = []
        for key, value in kwargs.items():
            if key in self.field_list:
                if value == None:
                    sql = f"{key} is NULL"
                elif isinstance(value, int):
                    sql = f"{key}={value}"
                else:
                    sql = f"{key}='{value}'"
                condition_list.append(sql)
        condition_sql = " and ".join(condition_list)
        return condition_sql

    def result(self, result_field, data):
        """
        result() 组织结果数据
        :param result_field: 接受一个列表，数据为表字段，组织数据使用
        :param data: sql查询结果，为嵌套元组
        :return: 列表嵌套字典类型
        """
        if data is None:
            return data
        if len(data) == 0:
            return []
        elif isinstance(data[0], tuple):
            result = []
            for i in data:
                temp = {}
                for k, j in enumerate(result_field):
                    temp[j] = i[k]
                result.append(temp)
        else:
            result = {}
            for k, j in enumerate(result_field):
                result[j] = data[k]
        # 返回查询集
        return result
