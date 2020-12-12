import sqlite3


class Database:
    def __init__(self, db: str):
        try:
            self.conn = sqlite3.connect(db)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)
            self.__del__

    def fetch_all(self, table: str):
        try:
            query = self.cursor.execute("SELECT * FROM `?`", table)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(e)
            return False

    def fetch_single(self, table: str, column_name: str, column_value):
        sql_formatted_value = "'{value}'".format(value=column_value)
        placeholder = ":{column_name}".format(column_name=column_name)
        # let's build our query
        sql_prepared = "SELECT * FROM `%s` WHERE `%s`=%s" % (
            table, column_name, placeholder)

        try:
            self.cursor.execute(sql_prepared,
                                [column_value, ])
            row = self.cursor.fetchone()
            return row
        except sqlite3.Error as e:
            print(e)
            return False

    def insert_single(self, table: str, data: dict):
        columns = ""
        placeholders = ""
        values = []
        data_length = len(data)

        for index, (key, value) in enumerate(data.items()):
            # we need to dynamically build some strings based on the data
            # let's generate some placeholders to execute prepared statements
            columns += "`{column_name}`".format(column_name=key)
            placeholders += ":{column_name}".format(column_name=key)
            # let's fill the insert values into a list to use with execute
            values.append(value)

            # only add a comma if there is another item to assess
            if index < (data_length - 1):
                columns += ', '
                placeholders += ', '

        sql_prepared = "INSERT INTO `%s` (%s) VALUES (%s)" % (
            table, columns, placeholders)
        print(sql_prepared)

        try:
            self.cursor.execute(sql_prepared, values)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            return False

    def update_single(self, table: str, data: dict, id: int):
        update_params = ""
        values = []
        data_length = len(data)

        for index, (key, value) in enumerate(data.items()):
            # we need to dynamically build some strings based on the data
            # let's generate some placeholders to execute prepared statements
            update_params += "`{column_name}`=".format(column_name=key)
            update_params += ":{column_name}".format(column_name=key)
            # let's fill the insert values into a list to use with execute
            values.append(value)

            # only add a comma if there is another item to assess
            if index < (data_length - 1):
                update_params += ', '

        # append the id as the last param
        values.append(id)

        sql_prepared = "UPDATE `%s` SET %s WHERE `id`=%s" % (
            table, update_params, ':id')

        try:
            self.cursor.execute(sql_prepared, values)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False

    def delete_single(self, table: str, id: int):
        try:
            self.cursor.execute(
                "DELETE FROM {table} WHERE `id`=?".format(table=table), [id, ])
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            return False

    def delete_all(self, table: str):
        try:
            self.cursor.execute("DELETE FROM {table}".format(table=table))
        except sqlite3.Error as e:
            print(e)
            return False

    def __del__(self):
        self.conn.close()
