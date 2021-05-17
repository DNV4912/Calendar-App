import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import shortuuid

db = sqlite3.connect('Holidays_db',check_same_thread=False)
cursor = db.cursor()

def create_master(): #creates a table to store every usecase
    try:
        cursor.execute("""
    CREATE TABLE master_table (
        reference_id text NOT NULL,
        holiday_id text NOT NULL)""")

    except  Exception as E:
        print('Error :', E)
    else:
        print('master table created')

def get_unique_id(): #gets a unique ID for each usecase
    query = "SELECT reference_id from master_table"
    recs = cursor.execute(query)
    sql_id_list = []
    new_id = shortuuid.uuid()

    for row in recs:
        sql_id_list.append(row[0])

    while new_id in sql_id_list:
        new_id = shortuuid.uuid()
    
    return new_id
    

def insert_values(list_of_rows,df,unique_id): # stores the unique Id of each usecase along with the IDs of the holidays
    query = "insert into master_table values(?,?)"
    list_of_ids =[]
    for row in list_of_rows:

        temp = [unique_id,df.iloc[row-1]['ID']]
        list_of_ids.append(temp)
    
    
    try:
        cursor.executemany(query, list_of_ids)
    except Exception as E:
        print('Error : ', E)
    else:
        db.commit()
        print('data inserted')

def init():
    db = sqlite3.connect('Holidays_db',check_same_thread=False)
    cursor = db.cursor()
    print("connected to db")
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name= 'master_table' ''')
    #if the count is 1, then table exists
    #update_table(get_table())
    if cursor.fetchone()[0]==1 : 
        print('Master Table exists.')
    else:
        create_master()

if __name__ == "__main__":
    init() 