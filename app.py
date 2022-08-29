from flask import Flask

app = Flask(__name__)

import pyodbc
from decouple import config
from flask import request


class DBConnection:
    mysql = None

    @staticmethod
    def getInstance():
        return DBConnection.mysql

    def __init__(self):
        if DBConnection.mysql is not None:
            """ Raise exception if init is called more than once. """
            raise Exception("This class is a singleton!")
        else:
            app.config['AZURE_SQL_HOST'] = config('SERVER')
            app.config['AZURE_SQL_USERNAME'] = config('USERNAME2')
            app.config['AZURE_SQL_PASSWORD'] = config('PASSWORD')
            app.config['AZURE_SQL_DB'] = config('DATABASE')
            app.config['AZURE_SQL_DRIVER'] = config('DRIVER')

            # print(app.config)

            DBConnection.mysql = pyodbc.connect('DRIVER=' + app.config['AZURE_SQL_DRIVER'] +
                                                  ';SERVER=' + app.config['AZURE_SQL_HOST'] +
                                                  ';DATABASE=' + app.config['AZURE_SQL_DB'] +
                                                  ';UID=' + app.config['AZURE_SQL_USERNAME'] +
                                                  ';PWD=' + app.config['AZURE_SQL_PASSWORD'] +
                                                  ';MARS_Connection=Yes'
                                                  )


@app.route("/", methods=['POST', 'GET'])
def home_view():
    print('Connecting to the database instance, please wait....')
    try:
        if DBConnection.mysql is None:
            mysql_connection = DBConnection()
        else:
            mysql_connection = DBConnection.getInstance()
        print("Test Connection Successful", mysql_connection)
        GSM_data = request.get_json()
        print(GSM_data)

        return "202"

    except Exception as e:
        return "404"

