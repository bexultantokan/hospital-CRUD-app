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
def refreshing():
	with engine.connect().execution_options(autocommit=True) as con:
		query = '''
		DROP TABLE Specialize;
		DROP TABLE Record;
		DROP TABLE PublicServant;
		DROP TABLE Doctor;
		DROP TABLE Users;
		DROP TABLE Discover;
		DROP TABLE Country;
		DROP TABLE Disease;
		DROP TABLE DiseaseType;

		CREATE TABLE DiseaseType (
  id            INTEGER,
  description   VARCHAR(140),
  PRIMARY KEY(id)
);


INSERT Into DiseaseType values (1, 'Infectious diseases');
INSERT Into DiseaseType values (2, 'Contagious diseases');
INSERT Into DiseaseType values (3, 'Food borne illness');
INSERT Into DiseaseType values (4, 'Communicable diseases');
INSERT Into DiseaseType values (5, 'Non-communicable diseases');
INSERT Into DiseaseType values (6, 'Airborne diseases');
INSERT Into DiseaseType values (7, 'Lifestyle diseases');
INSERT Into DiseaseType values (8, 'Mental disorders');
INSERT Into DiseaseType values (9, 'virology');
INSERT Into DiseaseType values (10, 'Water prone disease');


CREATE TABLE Country (
  cname         VARCHAR(50),
  population    BIGINT,
  PRIMARY KEY(cname)
);

INSERT Into Country values ('China', 1412000000);
INSERT Into Country values ('UK',  68729078);
INSERT Into Country values ('France', 65614511);
INSERT Into Country values ('USA', 332403650);
INSERT Into Country values ('Kazakhstan', 19306643 );
INSERT Into Country values ('Egypt', 106889622);
INSERT Into Country values ('Zambia', 20017675);
INSERT Into Country values ('Algeria', 45717620);
INSERT Into Country values ('Switzerland', 8804099);
INSERT Into Country values ('Germany', 84130000);



CREATE TABLE Disease (
  disease_code  VARCHAR(50),
  pathogen      VARCHAR(20),
  description   VARCHAR(140),
  id            INTEGER,
  PRIMARY KEY(disease_code),
  FOREIGN KEY(id) REFERENCES DiseaseType(id)
  	ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT Into Disease values ('Z86', 'virus', 'covid-19', 1);
INSERT Into Disease values ('L01', 'bacteria', 'impetigo', 2);
INSERT Into Disease values ('A02', 'bacteria', 'salmonella', 3);
INSERT Into Disease values ('Z71', 'virus', 'HIV', 4);
INSERT Into Disease values ('G30', 'N/A', 'tuberculosis', 5);
INSERT Into Disease values ('B44', 'fungi', 'pneumonia', 6);
INSERT Into Disease values ('E66', 'N/A', 'obesity', 7);
INSERT Into Disease values ('F95', 'bacteria', 'tourette’s syndrome', 8);
INSERT Into Disease values ('B52', 'protozoa', 'malaria', 4);
INSERT Into Disease values ('B65', 'worms', 'schistosomiasis', 10);

CREATE TABLE Discover (
  cname         VARCHAR(50),
  disease_code  VARCHAR(50),
  first_enc_dat DATE,
  PRIMARY KEY(cname, disease_code),
  FOREIGN KEY(cname)        REFERENCES Country(cname)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(disease_code) REFERENCES Disease(disease_code)
    ON UPDATE CASCADE ON DELETE CASCADE
);

Insert into Discover Values ('China','Z86','2019-12-15');
Insert into Discover Values ('UK','L01','1864-01-15'); 
Insert into Discover Values ('USA','A02','1885-01-15');
Insert into Discover Values ('France','Z71','1983-01-15'); 
Insert into Discover Values ('Germany','G30','1882-03-24');
Insert into Discover Values ('Germany','B44','1875-01-01');
Insert into Discover Values ('Switzerland','E66','1948-01-01'); 
Insert into Discover Values ('France','F95','1825-01-01');
Insert into Discover Values ('Algeria','B52','1880-01-01'); 
Insert into Discover Values ('Egypt','B65','1851-01-01'); 

CREATE TABLE Users (
  email         VARCHAR(60),
  name          VARCHAR(30),
  surname       VARCHAR(40),
  salary        INTEGER,
  phone         VARCHAR(20),
  cname         VARCHAR(50),
  PRIMARY KEY(email),
  FOREIGN KEY(cname) REFERENCES Country(cname)
  	ON DELETE CASCADE ON UPDATE CASCADE
);

Insert into Users Values ('alexandr.petrov@gmail.com','Alexandr','Petrov',12000,'87013399667','Egypt'); 
Insert into Users Values ('harry.neville@gmail.com','Harry','Neville',70000,'87013456667','UK'); 
Insert into Users Values ('hanna.montana@gmail.com','Hanna','Montana',35000,'87016543667','USA'); 
Insert into Users Values ('gulsim.magnus@gmail.com','Gulsim','Magnus',175000,'87013394567','Algeria'); 
Insert into Users Values ('alibek.kaiyrbay@gmail.com','Alibek','Kaiyrbay',1250000,'87076409667','Kazakhstan'); 
Insert into Users Values ('mark.zuckerberg@gmail.com','Mark','Zuckerberg',100000,'87018375629','USA'); 
Insert into Users Values ('harry.drinkwater@gmail.com','Harry','Drinkwater',50000,'87012938290','Switzerland'); 
Insert into Users Values ('alexey.kostolev@gmail.com','Alexey','Kostolev',200000,'87019382765','USA'); 
Insert into Users Values ('william.shakespeare@gmail.com','William','Shakespeare',19000,'87777777777','UK'); 
Insert into Users Values ('michael.york@gmail.com','Michael','York',342000,'87019899943','China'); 

CREATE TABLE PublicServant (
  email         VARCHAR(60),
  department   VARCHAR(50),
  PRIMARY KEY(email),
  FOREIGN KEY(email) REFERENCES Users(email)
  	ON UPDATE CASCADE ON DELETE CASCADE
);

Insert into PublicServant Values ('alexandr.petrov@gmail.com','Dept1'); 
Insert into PublicServant Values ('harry.neville@gmail.com','Dept2'); 
Insert into PublicServant Values ('hanna.montana@gmail.com','Dept3'); 
Insert into PublicServant Values ('gulsim.magnus@gmail.com','Dept1'); 
Insert into PublicServant Values ('alibek.kaiyrbay@gmail.com','Dept2'); 
Insert into PublicServant Values ('mark.zuckerberg@gmail.com','Dept3'); 
Insert into PublicServant Values ('harry.drinkwater@gmail.com','Dept1'); 
Insert into PublicServant Values ('alexey.kostolev@gmail.com','Dept2'); 
Insert into PublicServant Values ('william.shakespeare@gmail.com','Dept3'); 
Insert into PublicServant Values ('michael.york@gmail.com','Dept1'); 

CREATE TABLE Doctor (
  email         VARCHAR(60),
  degree        VARCHAR(20),
  PRIMARY KEY(email),
  FOREIGN KEY(email) REFERENCES Users(email)
  	ON UPDATE CASCADE ON DELETE CASCADE
);

Insert into Doctor Values ('alexandr.petrov@gmail.com','professional'); 
Insert into Doctor Values ('harry.neville@gmail.com','clinical'); 
Insert into Doctor Values ('hanna.montana@gmail.com','research'); 
Insert into Doctor Values ('gulsim.magnus@gmail.com','professional'); 
Insert into Doctor Values ('alibek.kaiyrbay@gmail.com','clinical'); 
Insert into Doctor Values ('mark.zuckerberg@gmail.com','research'); 
Insert into Doctor Values ('harry.drinkwater@gmail.com','professional'); 
Insert into Doctor Values ('alexey.kostolev@gmail.com','clinical'); 
Insert into Doctor Values ('william.shakespeare@gmail.com','research'); 
Insert into Doctor Values ('michael.york@gmail.com','professional'); 

CREATE TABLE Specialize (
  id    INTEGER,
  email VARCHAR(60),
  PRIMARY KEY(id, email),
  FOREIGN KEY(id)    REFERENCES DiseaseType(id)
  	ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(email) REFERENCES Doctor(email)
  	ON UPDATE CASCADE ON DELETE CASCADE
);	
Insert into Specialize Values (9,'alexandr.petrov@gmail.com'); 
Insert into Specialize Values (3,'alexandr.petrov@gmail.com'); 
Insert into Specialize Values (1,'alexandr.petrov@gmail.com'); 
Insert into Specialize Values (1,'harry.neville@gmail.com'); 
Insert into Specialize Values (2,'harry.neville@gmail.com'); 
Insert into Specialize Values (9,'harry.neville@gmail.com'); 
Insert into Specialize Values (3,'hanna.montana@gmail.com'); 
Insert into Specialize Values (9,'hanna.montana@gmail.com'); 
Insert into Specialize Values (4,'gulsim.magnus@gmail.com'); 
Insert into Specialize Values (5,'alibek.kaiyrbay@gmail.com'); 
Insert into Specialize Values (6,'mark.zuckerberg@gmail.com'); 
Insert into Specialize Values (9,'mark.zuckerberg@gmail.com'); 
Insert into Specialize Values (7,'harry.drinkwater@gmail.com'); 
Insert into Specialize Values (8,'alexey.kostolev@gmail.com');
Insert into Specialize Values (9,'alexey.kostolev@gmail.com'); 
Insert into Specialize Values (9,'william.shakespeare@gmail.com'); 
Insert into Specialize Values (10,'michael.york@gmail.com'); 
Insert into Specialize Values (9,'michael.york@gmail.com'); 

CREATE TABLE Record (
  email          VARCHAR(60),
  cname          VARCHAR(50),
  disease_code   VARCHAR(50),
  total_deaths   INTEGER,
  total_patients INTEGER,
  PRIMARY KEY(email, cname, disease_code),
  FOREIGN KEY(disease_code) REFERENCES Disease(disease_code)
  	ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(cname)        REFERENCES Country(cname)
  	ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(email)        REFERENCES PublicServant(email)
  	ON UPDATE CASCADE ON DELETE CASCADE
);

insert into Record Values ('alexandr.petrov@gmail.com', 'Egypt', 'Z86', 100, 134000);
insert into Record Values ('alexandr.petrov@gmail.com', 'China', 'Z86', 1000, 120000);
insert into Record Values ('alexandr.petrov@gmail.com', 'France', 'Z86', 100, 12000);
insert into Record Values ('alexandr.petrov@gmail.com', 'Germany', 'Z86', 1200, 160000);
insert into Record Values ('harry.neville@gmail.com', 'China', 'Z86', 1000, 120000);
insert into Record Values ('harry.neville@gmail.com', 'France', 'Z86', 100, 12000);
insert into Record Values ('harry.neville@gmail.com', 'Germany', 'Z86', 1200, 16000);
insert into Record Values ('hanna.montana@gmail.com', 'Algeria', 'F95', 120, 122000);
insert into Record Values ('harry.drinkwater@gmail.com', 'USA', 'L01', 10, 9000);
insert into Record Values ('alexey.kostolev@gmail.com', 'Egypt', 'A02', 1038, 9002380);
insert into Record Values ('michael.york@gmail.com', 'Switzerland', 'G30', 10338, 932380);

ALTER TABLE disease OWNER TO postgres;
	'''
		con.execute(query)