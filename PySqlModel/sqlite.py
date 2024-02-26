"""
@Project:PgSqlModel
@File:sqlite.py
@Author:函封封
"""
import time
import sqlite3


# sqlite操作
class SQLite():
    def __init__(self, **kwargs):
        """
        DATABASES = {
            "database": "./demo.db"
        }
        """
        self.sqlite_con = sqlite3.connect(**kwargs)
        self.sqlite = self.sqlite_con.cursor()  # 创建游标对象
        self.table_name = None  # 表名
        self.field_list = []  # 表字段
        self.condition_sql = ""  # 条件语句
        self.args = []

    def show_table(self):
        """
        show_tables()方法：查询当前数据库中所有表
        :return: 返回一个列表
        """
        sql = "select name from sqlite_master where type='table' and name not in ('sqlite_master','sqlite_sequence')"
        self.sqlite.execute(sql)
        data_list = self.sqlite.fetchall()
        table_list = [data[0] for data in data_list]
        return table_list  # 返回当前数据库内所有的表

    def table(self, table_name: str):
        """
        设置操作表
        :param table_name: 表名
        :return: self
        """

        self.table_name = table_name  # 表名
        sql = f"PRAGMA table_info(`{table_name}`);"
        self.sqlite.execute(sql)
        field_list = self.sqlite.fetchall()

        self.field_list = []
        for field in field_list:
            self.field_list.append(field[1])
        return self

    def create_table(self, table_name: str, field_dict: dict):
        """
        create_table() 创建表，已存在直接返回，不存在则创建
        :param table_name: 表名
        :param field_dict: 表字段列表
        :return: 连接成功：返回 True
        """
        self.table_name = table_name  # 将表名赋值给实例属性

        self.field_list = field_dict.keys()  # 获取该表的所有的字段名

        table_list = self.show_table()  # 获取数据库里所有的表
        if self.table_name in table_list:  # 判断该表是否已存在
            return True  # 该表已存在！直接返回

        field_list = [f"`{key}` {value}" for key, value in field_dict.items()]
        create_field = ",".join(field_list)  # 将所有的字段与字段类型以 “ , ” 拼接
        sql = f"""create table `{self.table_name}`(
  {create_field}
  );"""
        self.sqlite.execute(sql)
        self.sqlite_con.commit()
        return True

    def create(self, **kwargs):
        """
        create() 添加一行数据
        :param kwargs: 接收一个字典，key = value 字段 = 值
        :return: 添加成功：返回 True 添加失败：返回 Flase
        """
        try:
            field_sql = "`,`".join(kwargs.keys())
            create_sql = ",".join(["?"] * len(kwargs))

            # id 字段为null ，默认自增
            sql = f"""insert into `{self.table_name}`  (`{field_sql}`) values ({create_sql});"""
            self.sqlite.execute(sql, tuple(kwargs.values()))
            self.sqlite_con.commit()
            return self.sqlite.rowcount
        except Exception as err:
            self.sqlite_con.rollback()
            raise err

    def where(self, sql: str = None, *args):
        """
        条件函数
        :param native_sql: 原生sql语句
        :param kwargs: key = value/字段 = 值 条件
        :return: self
        """
        self.condition_sql = sql
        self.args = tuple(args)
        return self

    def delete(self):
        """
        删除满足条件的数据
        :return: 影响行数
        """
        sql = f"delete from `{self.table_name}` where {self.condition_sql};"

        try:
            self.sqlite.execute(sql, self.args)
            self.sqlite_con.commit()
            return self.sqlite.rowcount
        except Exception as err:
            self.sqlite_con.rollback()
            raise err
        finally:
            self.condition_sql = ""
            self.args = []

    def update(self, **kwargs):
        """
        update() 修改数据
        :param kwargs: 接收一个字典，key == value 条件
        :return: 影响行数
        """
        if not kwargs: raise ValueError(f"**kwargs")

        update_sql = ",".join([f"`{field}`=?" for field in kwargs.keys()])
        sql = f"update `{self.table_name}` set {update_sql} where {self.condition_sql};"
        args = list(kwargs.values())
        args.extend(self.args)

        try:
            self.sqlite.execute(sql, args)
            self.sqlite_con.commit()
            return self.sqlite.rowcount
        except Exception as err:
            self.sqlite_con.rollback()
            raise err
        else:

            return True

    def __extract_field_list(self, *args):
        """
        解析字段列表，获取字段名称
        :param field_list: list 接受字段列表
        :return list 返回字段列表
        """
        result_field = []
        for field in args:
            field = field.strip()
            if field == "*":
                result_field.extend(self.field_list)
            elif field.find(" as ") != -1:
                field = field.split(" as ")[-1]
                field = field.strip()

            result_field.append(field)
        return result_field

    def select(self, *fields):
        """
        查询数据库，返回全部数据
        :param fields: list[field_name] 查询结果字段
        :return: list[dict] 返回查询到的所有行
        """
        # 结果字段
        if len(fields) == 0:
            result_field = self.field_list
            select_field = ",".join(result_field)
        else:
            result_field = self.__extract_field_list(*fields)
            select_field = ",".join(fields)

        if self.condition_sql:
            sql = f"select {select_field} from `{self.table_name}` where {self.condition_sql};"
        else:
            sql = f"select {select_field} from `{self.table_name}`;"

        try:
            self.sqlite.execute(sql)
            data = self.sqlite.fetchall()
            result = self.result(result_field, data)
            return result
        except Exception as err:
            raise err
        finally:
            self.condition_sql = ""
            self.args = []

    def find(self, *fields):
        """
        查询数据库，返回第一条数据
        :param fields: list[field_name] 查询结果字段
        :return dict
        """
        # 结果字段
        if len(fields) == 0:
            result_field = self.field_list
            select_field = ",".join(result_field)
        else:
            result_field = self.__extract_field_list(*fields)
            select_field = ",".join(fields)

        if self.condition_sql:
            sql = f"select {select_field} from `{self.table_name}` where {self.condition_sql};"
        else:
            sql = f"select {select_field} from `{self.table_name}`;"

        try:
            self.sqlite.execute(sql, self.args)
            data = self.sqlite.fetchone()
            result = self.result(result_field, data)
            return result
        except Exception as err:
            raise err
        finally:
            self.condition_sql = ""
            self.args = []

    def execute_native_sql(self, native_sql: str):
        """
        执行原生sql，支持多条语句
        :param native_sql: str 接受原生sql
        :return list[list[dict]] 返回字段列表
        """
        native_sql_list = native_sql.split(";")
        idx = 1
        result = []
        for sql in native_sql_list:
            sql = sql.lower().strip()
            if not sql: continue  # 跳过空值
            data = {
                "name": f"结果{idx}",
                "abstract": {
                    "name": sql,
                    "info": "OK"
                },
            }
            if sql.startswith("use"):
                start_time = time.time()
                self.sqlite.execute(sql)
                end_time = time.time()
                data["abstract"] = {
                    "name": sql,
                    "info": "OK",
                    "select_time": end_time - start_time,
                }
            elif sql.startswith("select"):
                start_time = time.time()
                self.sqlite.execute(sql)
                end_time = time.time()
                tmp_data = self.sqlite.fetchall()
                result_field = self.__extract_sql(sql)
                tmp_data = self.result(result_field, tmp_data)
                data["result"] = tmp_data
                data["abstract"] = {
                    "name": sql,
                    "info": "OK",
                    "select_time": end_time - start_time,
                }
            elif sql.startswith("show"):
                start_time = time.time()
                self.sqlite.execute(sql)
                end_time = time.time()
                tmp_data = self.sqlite.fetchall()
                tmp_data = [i[0] for i in tmp_data]
                data["result"] = tmp_data
                data["abstract"] = {
                    "name": sql,
                    "info": "OK",
                    "select_time": end_time - start_time,
                }
            else:
                start_time = time.time()
                tmp_data = self.sqlite.execute(sql)
                self.sqlite_con.commit()
                end_time = time.time()
                data["abstract"] = {
                    "name": sql,
                    "info": f"影响行数：{tmp_data}",
                    "select_time": end_time - start_time,
                }
            result.append(data)
            idx += 1
        return result

    def __extract_sql(self, native_sql: str):
        """
        解析原生sql，获取字段列表
        :param native_sql: str 接受原生sql
        :return list 返回字段列表
        """
        temp_field = str(native_sql).strip().lower()
        temp_field = temp_field.lstrip("select")
        end_idx = temp_field.find("from")
        if end_idx == -1:
            raise ValueError(f"{native_sql} 中不存在 from")

        temp_field = temp_field[:end_idx]
        temp_field = temp_field.strip()

        return self.__extract_field_list(temp_field.split(","))

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