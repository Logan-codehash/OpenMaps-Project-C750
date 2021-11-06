#inital exploration of the data

import sqlite3
import csv

#naming the output file for the database
sqlite_file = 'Longview_Full_exploration.db'

#connect to database
sql_con = sqlite3.connect(sqlite_file)

#the sql cursor object
sql_cur = sql_con.cursor()

#if table already exists, recreates it. Needed for repeatedly running code to make sure it works
sql_cur.execute('''DROP TABLE IF EXISTS nodes;''')
sql_con.commit()

#creates the table
sql_cur.execute('''
			CREATE TABLE nodes(id INTEGER PRIMARY KEY, user TEXT, uid INTEGER, version TEXT,lat REAL,lon REAL,timestamp DATE,changeset INTEGER) 
		''')
sql_con.commit()

#reads the data from csv into the table
with open('nodes_inital.csv','rb') as temp:
   csv_line = csv.DictReader(temp)
   to_db = [(i['id'],i['user'].decode("utf-8"),i['uid'],i['version'],i['lat'],i['lon'],i['timestamp'],i['changeset']) for i in csv_line]
sql_cur.executemany("INSERT INTO nodes(id,user,uid,version,lat,lon,timestamp,changeset) VALUES(?,?,?,?,?,?,?,?);",to_db)
sql_con.commit()

sql_cur.execute('''DROP TABLE IF EXISTS nodes_tags;''')
sql_con.commit()

sql_cur.execute('''
			CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT) 
		''')
sql_con.commit()

with open('nodes_tags_inital.csv','rb') as temp:
   csv_line = csv.DictReader(temp)
   to_db = [(i['id'],i['key'],i['value'].decode("utf-8"),i['type']) for i in csv_line]
sql_cur.executemany("INSERT INTO nodes_tags(id,key,value,type) VALUES(?,?,?,?);",to_db)
sql_con.commit()

sql_cur.execute('''DROP TABLE IF EXISTS ways;''')
sql_con.commit()

sql_cur.execute('''
			CREATE TABLE ways(id INTEGER PRIMARY KEY, user TEXT,uid INTEGER,version TEXT,timestamp DATE,changeset INTEGER) 
		''')
sql_con.commit()

with open('ways_inital.csv','rb') as temp:
   csv_line = csv.DictReader(temp)
   to_db = [(i['id'],i['user'].decode("utf-8"),i['uid'],i['version'],i['timestamp'],i['changeset']) for i in csv_line]
sql_cur.executemany("INSERT INTO ways(id,user,uid,version,timestamp,changeset) VALUES(?,?,?,?,?,?);",to_db)
sql_con.commit()

sql_cur.execute('''DROP TABLE IF EXISTS ways_tags;''')
sql_con.commit()

sql_cur.execute('''
			CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT, type TEXT) 
		''')
sql_con.commit()

with open('ways_tags_inital.csv','rb') as temp:
   csv_line = csv.DictReader(temp)
   to_db = [(i['id'],i['key'],i['value'].decode("utf-8"),i['type']) for i in csv_line]
sql_cur.executemany("INSERT INTO ways_tags(id,key,value,type) VALUES(?,?,?,?);",to_db)
sql_con.commit()

sql_cur.execute('''DROP TABLE IF EXISTS ways_nodes;''')
sql_con.commit()

sql_cur.execute('''
			CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER) 
		''')
sql_con.commit()

with open('ways_nodes_inital.csv','rb') as temp:
   csv_line = csv.DictReader(temp)
   to_db = [(i['id'],i['node_id'],i['position']) for i in csv_line]
sql_cur.executemany("INSERT INTO ways_nodes(id,node_id,position) VALUES(?,?,?);",to_db)
sql_con.commit()

#print out finished so that I have a visual notice when process is done
print ('finished')
sql_con.close()


