import sqlalchemy as db
import pandas as pd

# engine = db.create_engine('mysql+pymysql://root:bekamsol54@localhost:3306/hospital') # for local connection
engine = db.create_engine('postgresql://postgres:Bekamsol54_Ayanat@db.befqayiukinhwzqhxzqu.supabase.co:5432/postgres')


def add_data(table_name, arr):
	with engine.connect().execution_options(autocommit=True) as con:
		con.execute("insert into {table_name} values {arr}".format(table_name=table_name, arr='(\'' + '\' ,\''.join(arr) + '\')'))

def read_data(table_name):
	with engine.connect().execution_options(autocommit=True) as con:
		query = con.execute("select * from {}".format(table_name))
		df = pd.DataFrame(query.fetchall())
		if len(df.columns) > 0:
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
		query = 'delete from ' + table_name + ' where ' + str(id_name) + ' = \'' + str(data.iloc[row,0])+'\''
		con.execute(query)
def query1():
	with engine.connect().execution_options(autocommit=True) as con:
		query ='''
			select disease.disease_code, disease.description 
			from disease 
				inner join discover 
					on disease.disease_code=discover.disease_code 
					and disease.pathogen= 'bacteria'
					and discover.first_enc_dat < '1900-01-01'
		''' 
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df 

def query2():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
		select distinct t.name, t.surname, doctor.degree from
			doctor inner join
				(select users.email, users.name, users.surname from
					users inner join
						(select users.email from users
							where users.email not in
								(select email from diseasetype inner join specialize
									on diseasetype.description='infectious diseases'
									and diseasetype.id=specialize.id)) as u
						on users.email=u.email) as t
			on doctor.email=t.email 
		'''
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query3():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''  
		select distinct t.name, t.surname, doctor.degree from
			doctor inner join
				(select users.email, users.name, users.surname from
				users inner join
					(select specialize.email 
					from specialize
					group by specialize.email having count(*) > 2) as s
				on users.email=s.email) as t
			on doctor.email=t.email
		'''
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query4():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
select t1.cname, avg(t1.salary) as avg_age from
    (select users.cname, users.salary from users inner join
    (select specialize.email from specialize inner join
        (select diseasetype.id from diseasetype where diseasetype.description='virology') as id
        on specialize.id=id.id) as t
    on users.email=t.email) as t1
    group by t1.cname
'''
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query5():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
select publicservant.department, count(publicservant.email) as cnt from publicservant inner join
    (select record.email from record inner join
        (select disease.disease_code from disease where disease.description ='covid-19') as t
        on record.disease_code=t.disease_code
        group by record.email having count(record.cname) > 1) as u
    on publicservant.email=u.email
    group by publicservant.department
'''
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query6():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
			update users 
			set salary = salary * 2
			where users.email in 
					(select email from record inner join
						(select disease.disease_code from disease where disease.description ='covid-19') as t
						on record.disease_code=t.disease_code
						group by record.email having count(record.email) > 3);
		'''
		con.execute(query)
		check = 'select * from users'
		ans = con.execute(check)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query7():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
			delete from users
			where users.name like '%%bek%%' or users.name like '%%gul%%';
		'''
		con.execute(query)
		check = 'select * from users'
		ans = con.execute(check)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query8():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
		ALTER TABLE disease OWNER TO current_user;
		CREATE INDEX pathogen_idx ON disease (pathogen);
		select *
		from pg_indexes
		where tablename = 'disease';
		'''
		
		ans = con.execute(query)
		# check = 'show index from disease'
		# ans = con.execute(check)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query9():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
		select distinct u.email, u.name, publicservant.department from publicservant inner join 
			(select users.email, users.name from users inner join
				(select email from record where total_patients between 100000 and 999999) as t
				on users.email=t.email) as u
			on u.email=publicservant.email
		'''
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query10():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
    select cname as cnt from record
    group by cname
    order by sum(total_patients) desc
    limit 5;
'''
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df

def query11():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
    select t.description, sum(record.total_patients)-sum(record.total_deaths) as sum from record inner join
        (select disease.disease_code, diseasetype.description from disease inner join diseasetype
        on disease.id=diseasetype.id) as t
    on record.disease_code=t.disease_code
    group by t.description
'''
		ans = con.execute(query)
		df = pd.DataFrame(ans.fetchall())
		if len(df.columns) > 0:
			df.columns = ans.keys()
		return df