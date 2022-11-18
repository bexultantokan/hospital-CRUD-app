import sqlalchemy as db
import pandas as pd

engine = db.create_engine('postgresql://postgres:Bekamsol54_Ayanat@db.dkbrcjbbaermhhltcubj.supabase.co:6543/postgres')


def add_data(table_name, arr):
	with engine.connect().execution_options(autocommit=True) as con:
		con.execute("insert into {table_name} values {arr}".format(table_name=table_name, arr='(\'' + '\' ,\''.join(arr) + '\')'))

def read_data(table_name):
	with engine.connect().execution_options(autocommit=True) as con:
		query = con.execute("select * from {}".format(table_name))
		df = pd.DataFrame(query.fetchall())
		df.columns = query.keys()
		return df

def update_data(table_name, row, data):
	with engine.connect().execution_options(autocommit=True) as con:
		id_name = data.columns[0]
		query = 'update '+ table_name + ' set ' 
		for i in range(1, len(data.columns)):
			query += str(data.columns[i]) + ' =\'' + str(data.iloc[row, i]) + '\','
		query = query[:-1] + ' where ' + str(id_name) + ' = ' + '\''+str(data.iloc[row,0]+'\'')
		con.execute(query)

def delete_data(table_name, row, data):
	with engine.connect().execution_options(autocommit=True) as con:
		id_name = data.columns[0]
		query = 'delete from ' + table_name + ' where ' + str(id_name) + ' = \'' + str(data.iloc[row,0]+'\'')
		con.execute(query)