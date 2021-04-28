from flask import Flask, render_template,jsonify, request,send_file, send_from_directory
import fetching_holidays as fh
import master_table as mt
import generate_ics as gi
import pandas as pd
import time

fh.init()
app = Flask('testapp')

@app.route('/')
def index():
    table = fh.select_table()
    
    table = table[['Date','Day','Holiday','State']]
    
    return render_template('index3.html', column_names=table.columns.values, row_data=list(table.values.tolist()),
                            zip=zip)



@app.route('/create', methods=['POST','GET'])
def create():
    
    table = fh.select_table()
    
    mt.init()
    id_user = mt.get_unique_id()
    
    list_of_rows = request.get_json()

    mt.insert_values(list_of_rows,table, id_user)

    #gi.generate_file(list_of_rows,table)
    
    
    return id_user

@app.route('/download', methods=['GET'])
def download():
    #ID = request.form['fname']
    return render_template('search.html')
    # return send_from_directory('./ics_files/','your_custom.ics')

@app.route('/generate_ics', methods=['POST'])
def generate_ics():
    ID = request.form['fname']
    table = fh.select_table()
    if  gi.validate_master_id(ID):
        gi.generate_file(ID,table)
        return send_from_directory('./ics_files/','your_custom.ics')
    else:
        return render_template('error.html')
    
    #return render_template('search.html')
    

    
if __name__ == '__main__':
    app.run(debug=True)