from ics import Calendar, Event
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

def validate_master_id(master_id): # Function to check if the user input is valid or not
    db = sqlite3.connect('Holidays_db',check_same_thread=False)
    cursor = db.cursor()
    query = "SELECT reference_id from master_table"
    recs = cursor.execute(query)
    sql_id_list = []

    for row in recs:
        sql_id_list.append(row[0])

    
    if master_id in sql_id_list:
        return True
    else:
        return False



def generate_file(master_id,table):
    db = sqlite3.connect('Holidays_db',check_same_thread=False)
    cursor = db.cursor()
    query = "SELECT holiday_id from master_table WHERE reference_id ='"+master_id+"'"
    recs = cursor.execute(query)
    sql_id_list = []

    for row in recs:
        sql_id_list.append(row[0]) # gets the list of Holiday IDs pertaining to the required use case

    print(sql_id_list)
    new = table['Date'].str.split(" ", n = 2, expand = True)
    new['Date'] = new[0] + " "+ new[1].apply(lambda x:str(x)[:3]) + " "+new[2]
    
    table["Date2"] =new['Date']
    table = table.dropna()
    table['Date3'] = table['Date2'].apply(lambda x:datetime.strptime(str(x),'%d %b %Y')) # to convert the string dates to date time format
    table_actual = table[['Date3','Day','Holiday','State','ID']]
    table_actual = table_actual.rename({'Date3': 'Date'}, axis=1)
    c = Calendar()
    
    

    for event in sql_id_list:
        e = Event()
        if event == 0:
            continue
        
        e.name = table_actual[table_actual['ID']==event]['Holiday'].iloc[0]
        
        e.begin = table_actual[table_actual['ID']==event]['Date'].iloc[0]
        c.events.add(e)

    
    with open('./ics_files/your_custom.ics', 'w') as f:
        f.writelines(c)

