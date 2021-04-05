import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib3
from datetime import datetime

url = 'https://www.bankbazaar.com/indian-holiday-calendar.html'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

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
    
    
    table["Date2"] =new['Date']
    table = table.dropna()
    table['Date3'] = table['Date2'].apply(lambda x:datetime.strptime(str(x),'%d %b %Y'))
    table_actual = table[['Date3','Day','Holiday','States']]
    table_actual = table_actual.rename({'Date3': 'Date'}, axis=1)

    return table_actual