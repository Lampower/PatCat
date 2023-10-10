import os
import sqlite3
import asyncio

class DataBase:
    
    def __init__(self, name: str) -> None:
        self.database_name = name
        self.open_db()
        
        self.user_table_name = "users"
        self.user_name = "name"
        self.user_id = "id"
        self.count_s = "count"
        self.timer = "timer"
        
        self.__create_table(self.user_table_name)  
        self.__db__.close()
        
        print("DB is initilized")
    def is_open(self) -> bool:
        return False
    def open_db(self):
        self.__db__ = sqlite3.connect(f"{self.database_name}.db")
        self.cur = self.__db__.cursor()

    def close_db(self):
        self.__db__.commit()
        self.__db__.close()

    def execute_query(self, query: str = None, commit: bool = False):
        if query == None:
            return
        self.cur.execute(query)
        if commit == True:
            self.__db__.commit()
        
    def add_new_user(self, name: str, id: int):
        insert_query = f"""INSERT INTO {self.user_table_name} ({self.user_name},{self.user_id}, {self.count_s}, {self.timer}) 
            VALUES ('{name}', {id}, 0, 0)"""
        self.execute_query(insert_query, True)
        print(f"succesfully added {name} ({id}) to db")
            
    def __create_table(self, table_name: str):
        create_tab = f"""CREATE TABLE IF NOT EXISTS {table_name} (
            {self.user_name} TEXT,
            {self.user_id} INT,
            {self.count_s} INT,
            {self.timer} INT
            );
        """   
        self.execute_query(create_tab, True)
        self.test()
    
    
    
    def test(self):
        query = f"SELECT * FROM {self.user_table_name}"
        self.execute_query(query)
        data = self.cur.fetchall()
        print("Users in DB")
        for d in data:
            print(f"  {d}")
    
    def add_count_to_user(self, id: int, amount: int = 1):
        add_query = f"UPDATE {self.user_table_name} SET {self.count_s} = {self.count_s} + {amount} WHERE {self.user_id} = {id}"
        self.execute_query(add_query, True)
        print(f"added {amount} to {id}, total is {self.get_count(id)}")
    
    def delete_user_from_base(self, id: int):
        delete_query = f"DELETE FROM {self.user_table_name} WHERE {self.user_id} = {id}"
        self.execute_query(delete_query, True)
    
    
    def get_time(self, id: int):
        query = f"SELECT {self.user_id}, {self.timer} / 60, {self.timer} % 60 from {self.user_table_name} WHERE {self.user_id} = {id}"
        self.execute_query(query)
        time = list(self.cur.fetchone())
        return time

    def get_count(self, id: int):
        query = f"SELECT {self.count_s} FROM {self.user_table_name} WHERE {self.user_id} = {id}"
        self.execute_query(query)
        data = self.cur.fetchone()[0]
        return data
    
    def get_user(self, id: int):
        query = f"SELECT {self.user_id} FROM {self.user_table_name} WHERE {self.user_id} = {id}"
        self.execute_query(query)
        res = self.cur.fetchone()
        return res
    
    
    
    def change_timer(self, amount: int):
        query = f"UPDATE {self.user_table_name} SET {self.timer} = {self.timer} - {amount} WHERE {self.timer} > 0"
        self.execute_query(query, True)
        # need timer dont know how
    
    def reset_timer_to_max(self, id: int):
        query = f"UPDATE {self.user_table_name} SET {self.timer} = 300 WHERE {self.user_id} = {id}"
        self.execute_query(query, True)
    
    def reset_timer_to_min(self, id: int):
        query = f"UPDATE {self.user_table_name} SET {self.timer} = 0 WHERE {self.user_id} = {id}"
        self.execute_query(query, True)
    # def __gen_query()    
    
    def delete_all_users(self):
        query = f"DELETE FROM {self.user_table_name}"
        self.execute_query(query, True)
    
    def __test_ok(self):
        print("daun")

    async def change_time_periodicaly(self):
        await self.change_timer(1)
        
