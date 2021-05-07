import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib3
import json
from datetime import datetime
import sqlite3

url = 'https://www.bankbazaar.com/indian-holiday-calendar.html'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()
db = sqlite3.connect('Holidays_db')
cursor = db.cursor()

# extract all the tables in the HTML 
tables = soup.find_all('table')

def parse_html_table(table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
                    
            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                            index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        
        #Resetting the headers
        df_headers = df.iloc[0]
        df=df[1:]
        df.columns =df_headers
        
        return df


def get_table():
    table = parse_html_table(tables[1])

    new = table['Date'].str.split(" ", n = 2, expand = True)
    new['Date'] = new[0] + " "+ new[1].apply(lambda x:str(x)[:3]) + " "+new[2]
    
    table_actual = table
    # table["Date2"] =new['Date']
    # table = table.dropna()
    # table['Date3'] = table['Date2'].apply(lambda x:datetime.strptime(str(x),'%d %b %Y'))
    # table_actual = table[['Date3','Day','Holiday','States']]
    # table_actual = table_actual.rename({'Date3': 'Date'}, axis=1)
    table_actual['id'] = (table_actual['Date'].astype(str) + table_actual['Holiday'].astype(str))
    print(table_actual.info())
    
    return table_actual

def create_table_sql():
    try:
        cursor.execute("""
    CREATE TABLE Holidays_table (
        Date text NOT NULL,
        Day text NOT NULL,
        Holiday text NOT NULL,
        State text NOT NULL,
        ID text NOT NULL)""")

    except  Exception as E:
        print('Error :', E)
    else:
        print('Holidays table created')

def insert_values(table_name,no_of_columns,dataframe):         #Inserts values into the created tables
    
        
    query = "insert into "+ table_name +" values(" 
    for i in range(no_of_columns):
        query =query + "?"
        if i<no_of_columns-1:
            query = query + ","
    query = query + ")"
    df_list = list(dataframe.to_records(index=False))
    
    try:
        cursor.executemany(query, df_list)
    except Exception as E:
        print('Error : ', E)
    else:
        db.commit()
        print('data inserted')

def update_table(df):
    db = sqlite3.connect('Holidays_db')
    cursor = db.cursor()
    query = "SELECT ID from Holidays_table"
    recs = cursor.execute(query)
    sql_id_list = []
    new_ids=[]

    for row in recs:
        sql_id_list.append(row)

    df_id_list = list(df['id'])
    # print("Tjis is the db table",df_id_list)
    new_ids = [value for value in df_id_list if value in sql_id_list] #Find new holidays

    if len(new_ids)!=0: 
        new_df = pd.DataFrame()
        for new_id in new_ids:
            new_df.append(df.loc[df['id']==new_id])
        insert_values('Holidays_table', 5, new_df) # insert the new holidays into the existing table
    
def select_table():
    db = sqlite3.connect('Holidays_db')
    cursor = db.cursor()
    df = pd.read_sql_query("SELECT * FROM Holidays_table", db)
    return df



def init():
    db = sqlite3.connect('Holidays_db')
    cursor = db.cursor()
    print("connected to db")
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name= 'Holidays_table' ''')
    #if the count is 1, then table exists
    #update_table(get_table())
    if cursor.fetchone()[0]==1 : 
        print('Table exists.')
        df = get_table()
        update_table(df)
    else :
        df = get_table()
        create_table_sql()
        insert_values('Holidays_table',5,df)
        update_table(df)
    
    # print(select_table())
    # cursor.execute('SELECT * from Holidays_table')
    # print(cursor.fetchall())

if __name__ == "__main__":
    init()   
    
