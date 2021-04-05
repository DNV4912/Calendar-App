from flask import Flask, render_template,jsonify, request,send_file, send_from_directory
import fetching_holidays as fh
import generate_ics as gi
import pandas as pd
import time


app = Flask('testapp')

@app.route('/')
def index():
    table = fh.get_table()
    
    return render_template('index3.html', column_names=table.columns.values, row_data=list(table.values.tolist()),
                            zip=zip)



@app.route('/create', methods=['POST'])
def create():
    
    table = fh.get_table()
    
    list_of_rows = request.get_json()
    gi.generate_file(list_of_rows,table)
    
    
    return send_from_directory('./ics_files/','your_custom.ics')

@app.route('/download', methods=['GET'])
def download():
    return send_from_directory('./ics_files/','your_custom.ics')


    
if __name__ == '__main__':
    app.run(debug=True)