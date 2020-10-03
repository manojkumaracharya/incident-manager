#!/usr/bin/env python
# coding: utf-8
# In[140]:testdb

# install package
#pip install mysql-connector-python   

# import libraries
import mysql.connector
import json
import sys
from mysql.connector.constants import ClientFlag
from configparser import ConfigParser

configParser = ConfigParser()    
configFilePath = r'C:\workspace\ssl\Config.txt'  # change this path where Config.txt is saved also check path for ssl files
configParser.read(configFilePath)

# set the GCP DB details in config var
# prerequisite to store ssl files on local
Config = {
    'user': configParser.get('config', 'user'),
    'password': configParser.get('config', 'password'),
    'host': configParser.get('config', 'host'),
    'port' : configParser.get('config', 'port'),
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': configParser.get('config', 'ssl_ca'),
    'ssl_cert': configParser.get('config', 'ssl_cert'),
    'ssl_key': configParser.get('config', 'ssl_key'),
    'database':configParser.get('config', 'database')
}

conn = mysql.connector.connect(**Config) # create a connection object
cursor = conn.cursor() # initialize connection cursor


# In[146]:
inputAction = sys.argv[1]

# additional functions to support insert statements

class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles Numpy types """

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value) 
conn.set_converter_class(NumpyMySQLConverter)

# Create table

def create_table (table_name):
    if table_name == "user_details":
        query = ("CREATE TABLE IF NOT EXISTS user_details ("
               "username VARCHAR(255),"
               "password VARCHAR(255),"
               "userid INT(8) )")
    if table_name == "IN_SUMMARY":
        query = ("CREATE TABLE IF NOT EXISTS IN_SUMMARY ("
               "IN_NO VARCHAR(20),"
               "SUMMARY VARCHAR(255),"
               "OPEN_DATE DATETIME,"
               "PRIORITY INT (4),"
               "STATUS VARCHAR(20),"
               "LAST_UPDATED DATETIME,"
               "UPDATED_BY VARCHAR(255))")
    if table_name == "IN_DETAIL":
        query = ("CREATE TABLE IF NOT EXISTS IN_DETAIL ("
               "IN_NO VARCHAR(20),"
               "SUMMARY VARCHAR(255),"
               "OPEN_DATE DATETIME,"
               "DESCRIPTION VARCHAR (3000),"
               "PRIORITY INT(4),"
               "STATUS VARCHAR(20),"
               "ASSIGNED_TO VARCHAR(255),"
               "LAST_UPDATED DATETIME,"
               "UPDATED_BY VARCHAR(255))")
    if table_name == "slack_ch_details":
        query = ("CREATE TABLE IF NOT EXISTS slack_ch_details ("
               "channel_id VARCHAR(255),"
               "channel_name VARCHAR(255),"
               "channel_create_dt DATETIME )")
    if table_name == "rakshak_in_manager":
        query = ("CREATE TABLE IF NOT EXISTS rakshak_in_manager ("
               "members_id VARCHAR(255),"
               "members_name VARCHAR(255),"
               "members_real_name VARCHAR(255),"
               "members_uname VARCHAR(255),"
               "member_password VARCHAR(255) )")
   
    cursor.execute(query)
    conn.commit()
    
    
def insert_table (table_name):
    if table_name == "user_details":
        query = ("INSERT INTO user_details (username,password,userid) "
          "VALUES ('KUDE,VISHAKHA','hsbc1234', '43678962'),('RANJAN,RAVI','hsbc1234','43678952'),('ACHARYA,MANOJ','hsbc1234','53678952'),('PATEL,MEENAKSHI','hsbc1234', '54678952')")
        cursor.execute(query)
    if table_name == "IN_SUMMARY":
        query = ("INSERT INTO IN_SUMMARY (IN_NO, SUMMARY,OPEN_DATE,PRIORITY,STATUS,LAST_UPDATED,UPDATED_BY) "
         "VALUES (%s,%s,%s,%s,%s,%s,%s)")
        import pandas as pd
        IN_SUMMARY = pd.read_csv('IN_SUMMARY.csv')
        # then we execute with every row in our dataframe
        cursor.executemany(query, list(IN_SUMMARY.to_records(index=False)))
    if table_name == "IN_DETAIL":
        query = ("INSERT INTO IN_DETAIL (IN_NO,SUMMARY, OPEN_DATE,DESCRIPTION,PRIORITY,STATUS,ASSIGNED_TO,LAST_UPDATED,UPDATED_BY) "
         "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        import pandas as pd
        IN_DETAIL = pd.read_csv('IN_DETAIL.csv')
        # then we execute with every row in our dataframe
        cursor.executemany(query, list(IN_DETAIL.to_records(index=False)))
    if table_name == "rakshak_in_manager":
        query = ("INSERT INTO rakshak_in_manager (members_id,members_name, members_real_name,members_uname,member_password) "
         "VALUES (%s,%s,%s,%s,%s)")
        import pandas as pd
        rakshak_in_manager = pd.read_csv('rakshak_in_manager.csv')
        # then we execute with every row in our dataframe
        cursor.executemany(query, list(rakshak_in_manager.to_records(index=False)))
    
        
    conn.commit()
    
def read_data(table_name):
    cursor.execute("select * from " + table_name)
    out = cursor.fetchall()
    for row in out:
        print(row)
        
def json_output(table_name):
    cursor = conn.cursor(dictionary=True) 
    cursor.execute("select * from " + table_name)
    out = cursor.fetchall()
    return out    
    
def update_INstatus(tablename,newstatus,IN_NO ):
    
    # prepare query and data
    query = " UPDATE " + tablename + " SET status = %s WHERE IN_NO = %s "

    data = (newstatus, IN_NO)
    cursor.execute(query, data)
    conn.commit() 
    return "Status Updated"  

if inputAction == "getData" :
    print (json.dumps(json_output("IN_DETAIL"),indent=4,sort_keys=True, default=str)) 
    sys.stdout.flush()

if inputAction == "getUserData" :
    print (json.dumps(json_output("rakshak_in_manager"))) 
    sys.stdout.flush()    
 
if inputAction == "updateStatus" :
    status = sys.argv[2]
    incident = sys.argv[3]
    print (update_INstatus("IN_DETAIL",status,incident)) 
    sys.stdout.flush()

# In[147]:


json_output('IN_SUMMARY')


# In[148]:


json_output('IN_DETAIL')


# In[ ]:




