"""
@Project:SelectModel
@File:mysql.py
@Author:函封封
"""
import time

import pymysql

# mysql操作
class Mysql():
    # 系统数据库
    __SYSTEM_DATABASE = ["information_schema", "mysql", "performance_schema", "sys"]
    # 系统用户
    __SYSTEM_USER = ["mysql.infoschema", "mysql.session", "mysql.sys"]

    def __init__(self,**kwargs):
        """
        DATABASES = {
            "name": "demo",
            "user": "root",
            "password": "123",
            "host": "localhost",
            "port": 3306,
            "charset": "utf8",
        }
        """
        self.mysql_con = pymysql.connect(**kwargs)
        self.mysql_cursor = self.mysql_con.cursor() # 创建游标对象
        self.table_name = None  # 表名
        self.field_list = []  # 表字段
        self.temp_field_list = []  # 临时表字段
        self.condition_sql = None # 修改条件

    def show_databases(self, show_system:bool=False):
        """
        查询所有数据库
        :param show_system: 是否返回系统数据库,默认不返回
        :return list 返回一个列表
        """
        sql = """show databases;"""
        self.mysql_cursor.execute(sql)
        data_list = self.mysql_cursor.fetchall()
        database_list = []
        for db in data_list:
            db_name = db[0]
            if show_system is False and db_name in self.__SYSTEM_DATABASE:
                continue
            database_list.append(db_name)
        return database_list # 返回当前数据库内所有的表

    def show_user(self, show_system:bool=False):
        """
        show_user()方法：查询所有用户
        :param show_system: 是否返回系统用户,默认不返回
        :return list[dict] 返回列表嵌套字典
        """
        sql = """SELECT user, host FROM mysql.user;"""
        self.mysql_cursor.execute(sql)
        data_list = self.mysql_cursor.fetchall()
        user_list = []
        for user in data_list:
            name = user[0]
            host = user[1]
            if show_system is False and name in self.__SYSTEM_USER:
                continue
            user_list.append({"name": name,"host": host})
        return user_list  # 返回当前数据库内所有的表

    def set_user_host(self, username:str, password:str, host_list:list, dbname:str=None):
        """
        设置用户连接权限
        :param username: 用户名
        :param password: 密码
        :param host_list: host 列表
        :param dbname: 数据库名
        :return: True
        """
        self.mysql_cursor.execute(f"select Host from mysql.user where User='{username}' AND Host!='localhost'")
        save_host_list = self.mysql_cursor.fetchall()
        for temp_host in save_host_list: # 删除已存在的
            temp_host = temp_host[0]
            if temp_host in host_list:
                host_list.remove(temp_host)
                continue
            self.mysql_cursor.execute(f"drop user '{username}'@'{temp_host}'")

        for host in host_list:
            self.mysql_cursor.execute(f"create user `{username}`@`{host}` identified by '{password}';")
            if dbname is not None and username != "root":
                self.mysql_cursor.execute(f"grant all privileges on {dbname}.* to `{username}`@`{host}`;")
            else:
                self.mysql_cursor.execute(f"grant all privileges on *.* to `{username}`@`{host}`;")
        self.mysql_cursor.execute("flush privileges;")
        return True

    def show_table(self):
        """
        show_tables()方法：查询当前数据库中所有表
        :return: 返回一个列表
        """
        sql = """show tables;"""
        self.mysql_cursor.execute(sql)
        data_list = self.mysql_cursor.fetchall()
        table_list = [data[0] for data in data_list]
        return table_list # 返回当前数据库内所有的表

    def table(self, table_name:str):
        """
        设置操作表
        :param table_name: 表名
        :return: self
        """
        self.table_name = table_name  # 表名
        sql = f"""desc {table_name};"""
        # sql = f"""SHOW COLUMNS FROM {table_name};"""
        self.mysql_cursor.execute(sql)
        field_list = self.mysql_cursor.fetchall()

        self.field_list = []
        for field in field_list:
            self.field_list.append(field[0])
        return self

    def create_table(self, table_name:str=None, field_dict:dict=None, native_sql:str=None):
        """
        创建表，已存在直接返回，不存在则创建
        :param table_name: 表名
        :param field_dict: dict 表字段
        :param native_sql: 原生sql语句
        :return True
        """
        if native_sql is not None:
            sql = native_sql
        else:
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
        self.mysql_cursor.execute(sql)
        self.mysql_con.commit()
        return True

    def create(self,**kwargs):
        """
        添加一行数据
        :param kwargs: key = value/字段 = 值
        :return 返回受影响的行
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
            row_num = self.mysql_cursor.execute(sql)
            self.mysql_con.commit()
            return row_num
        except Exception as err:
            self.mysql_con.rollback()
            raise err

    def delete(self, native_sql:str=None,**kwargs):
        """
        删除满足条件的数据
        :param native_sql: 原生sql语句
        :param kwargs: key = value/字段 = 值 条件
        :return 返回受影响的行
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
            row_num = self.mysql_cursor.execute(sql)
            self.mysql_con.commit()
            return row_num
        except Exception as err:
            self.mysql_con.rollback()
            raise err

    def update_condition(self, **kwargs):
        self.condition_sql = self.create_condition_sql(**kwargs)
        return self

    def update(self, native_sql:str=None, **kwargs):
        """
        修改数据
        :param id: 要修改行的 id
        :param kwargs: key = value/字段 = 值 条件
        :return 返回受影响的行
        """
        try:
            if native_sql is not None:
                sql = native_sql
            else:
                if not kwargs: raise ValueError(f"**kwargs")
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
            row_num = self.mysql_cursor.execute(sql)
            self.mysql_con.commit()
            return row_num
        except Exception as err:
            self.mysql_con.rollback()
            raise err

    def filter(self, *args, native_sql:str=None, **kwargs):
        """
        查询数据库，返回全部数据
        :param native_sql: 原生sql语句
        :param args: list[field_name] 查询结果字段
        :param kwargs: key = value/字段 = 值 条件
        :return list[dict] 返回全部
        """
        if native_sql is not None:
            result_field = self.extract_sql(native_sql)
            sql = native_sql
        else:
            condition_sql = self.create_condition_sql(**kwargs)

            # 结果字段
            if len(args) != 0:
                select_field = ",".join(args)
                result_field = self.extract_field_list(args)
            else:
                result_field = self.field_list
                select_field = ",".join(result_field)

            if condition_sql:
                sql = f"""
                    select {select_field} from `{self.table_name}` where {condition_sql};
                """
            else:
                sql = f"""
                    select {select_field} from `{self.table_name}`;
                """
        self.mysql_cursor.execute(sql)
        data = self.mysql_cursor.fetchall()
        result = self.result(result_field,data)
        return result


    def get(self, *args, native_sql:str=None, **kwargs):
        """
        查询数据库，返回第一条数据
        :param native_sql: 原生sql语句
        :param args: list[field_name] 查询结果字段
        :param kwargs: key = value/字段 = 值 条件
        :return dict
        """
        if native_sql is not None:
            result_field = self.extract_sql(native_sql)
            sql = native_sql
        else:
            condition_sql = self.create_condition_sql(**kwargs)

            # 结果字段
            if len(args) != 0:
                select_field = ",".join(args)
                result_field = self.extract_field_list(args)
            else:
                result_field = self.field_list
                select_field = ",".join(result_field)

            if condition_sql:
                sql = f"""
                    select {select_field} from `{self.table_name}` where {condition_sql} limit 1;
                """
            else:
                sql = f"""
                    select {select_field} from `{self.table_name}` limit 1;
                """
        self.mysql_cursor.execute(sql)
        data = self.mysql_cursor.fetchone()
        result = self.result(result_field,data)
        return result

    def execute_native_sql(self, native_sql:str):
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
            if not sql: continue # 跳过空值

            data = {
                "name": f"结果{idx}",
                "abstract": {
                    "name": sql,
                    "info": "OK"
                },
            }
            if sql.find("use") != -1:
                start_time = time.time()
                self.mysql_cursor.execute(sql)
                end_time = time.time()
                data["abstract"] = {
                    "name": sql,
                    "info": "OK",
                    "select_time": end_time-start_time,
                }
            elif sql.find("select") != -1 or sql.find("show") != -1:
                start_time = time.time()
                self.mysql_cursor.execute(sql)
                end_time = time.time()
                tmp_data = self.mysql_cursor.fetchall()
                result_field = self.extract_sql(sql)
                tmp_data = self.result(result_field, tmp_data)
                data["result"] = tmp_data
                data["abstract"] = {
                    "name": sql,
                    "info": "OK",
                    "select_time": end_time - start_time,
                }
            else:
                start_time = time.time()
                tmp_data = self.mysql_cursor.execute(sql)
                self.mysql_con.commit()
                end_time = time.time()
                data["abstract"] = {
                    "name": sql,
                    "info": f"影响行数：{tmp_data}",
                    "select_time": end_time - start_time,
                }
            result.append(data)
            idx += 1
        return result

    def extract_sql(self, native_sql:str):
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

        return self.extract_field_list(temp_field.split(","))

    def extract_field_list(self, field_list:list):
        """
        解析字段列表，获取字段名称
        :param field_list: list 接受字段列表
        :return list 返回字段列表
        """
        result_field = []
        for field in field_list:
            field = field.strip()
            if field == "*":
                result_field.extend(self.field_list)
                continue
            if field.find("as") != -1:
                field = field.split("as")[-1]
                field = field.strip()

            result_field.append(field)
        return result_field

    def create_condition_sql(self, **kwargs):
        """
        组织条件语句
        :param kwargs: key = value/字段 = 值 条件
        :return sql 条件语句
        """
        condition_list = []
        for key, value in kwargs.items():
            if key not in self.field_list:
                raise ValueError(f"{self.table_name} 表中没有 {key} 字段，应为: {' '.join(self.field_list)}")
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
        组织结果数据
        :param result_field: 字段列表
        :param data: 查询结果，为嵌套元组
        :return: list[dict]
        """
        if data is None:
            return data
        if len(data) == 0:
            return []
        elif isinstance(data[0], tuple):
            result = []
            for i in data:
                temp = {}
                for idx, field in enumerate(result_field):
                    temp[field] = i[idx]
                result.append(temp)
        else:
            result = {}
            for k, j in enumerate(result_field):
                result[j] = data[k]
        # 返回查询集
        return result

    def close(self):
        self.mysql_cursor.close()
        self.mysql_con.close()