import boto3
import os

#locals
from functions.functions import *
from conf.db_config import *


#tables
from tables.create_table_departments import query_create_table_departments 
from tables.create_table_hired_employees import query_create_table_hired_employees
from tables.create_table_jobs import query_create_table_jobs

# PATH
dir_sep = os.path.sep
dir_project = os.getcwd() 
PATH_BIN=dir_project+dir_sep+"bin"
PATH_DOWNLOAD=dir_project+dir_sep+"download"
PATH_LOG=dir_project+dir_sep+"log"
PATH_DATASET=dir_project+dir_sep+"datasets"
# LOG
proccess_date=str(datetime.today().strftime('%Y%m%d%H%M%S'))
proccess_name="log_Data_Ingestion_Employee_AWS_MYSQL.txt"
log_file=PATH_LOG+dir_sep+proccess_name+"_"+proccess_date

#DATABASE 
config_db=ConfigDatabase()
USER=config_db.user
PASSWORD=config_db.password
HOST=config_db.host
PORT=config_db.port
DB_NAME=config_db.database


# AWS 
BUCKET_NAME="company-data-employees"
s3_resource = boto3.resource('s3')
s3_bucket = s3_resource.Bucket(BUCKET_NAME)
s3_client=boto3.client('s3')


# CREATE DATAFRAMES FROM FILES IN S3 
logger(log_file ,msg=f"---------- READING FILES IN S3 - CREATE DATAFRAMES ---------- ",status= 0)

# ************* Jobs Data *************
##read data
df_jobs=s3_read_data(log_file,"jobs")

##set column names
columns_job=["id","jobs"]
df_jobs.columns=columns_job

##drop duplicates - fill Nan values with 0
df_jobs=df_jobs.drop_duplicates()
df_jobs=df_jobs.fillna(0)




# ************* Jobs Departments *************
##read data
df_departments=s3_read_data(log_file,"departments")

##set column names
columns_departments=["id","departments"]
df_departments.columns=columns_departments

##drop duplicates - fill Nan values with 0
df_departments=df_departments.drop_duplicates()
df_departments=df_departments.fillna(0)
print(df_departments)


# ************* Hired Employees *************
##read data
df_hired_employees=s3_read_data(log_file,"hired_employees")

##set column names
columns_hired_employees=["id","name","datetime","department_id","job_id"]
df_hired_employees.columns=columns_hired_employees

##drop duplicates - fill Nan values with 0
df_hired_employees=df_hired_employees.drop_duplicates()
df_hired_employees=df_hired_employees.fillna(0)
print(df_hired_employees)



# EXTABLISH CONNECTION WITH MYSQL
logger(log_file ,msg=f"---------- DATABASE CONNECTION ---------- ",status= 0)
conn=db_connection(log_file,HOST,USER,PASSWORD,PORT)
cursor = conn.cursor()

# CREATE DATABASE
# logger(log_file ,msg=f"---------- DATABASE CREATION ---------- ",status= 0)
# # try:
#    logger(log_file ,msg=f"Creating database {DB_NAME}",status= 0)
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}") 
conn.commit()
#    logger(log_file ,msg=f"Database {DB_NAME} created OK",status= 0)
# except:
#    logger(log_file ,msg=f"An error occured during the creation of database",status= 0)


# CREATE TABLES
logger(log_file ,msg=f"---------- TABLES CREATION ---------- ",status= 0)

##tables name to create
create_tables=[(query_create_table_departments,"departments"), 
              (query_create_table_jobs,"jobs"),
              (query_create_table_hired_employees,"hired_employees")]

for create_table in create_tables:
      try:
         logger(log_file ,msg=f"Creating table {create_table[1]}",status= 0)
         cursor.execute(create_table[0]) 
         conn.commit()
         cursor.execute(create_table[0])
         logger(log_file ,msg=f"Table {create_table[1]} created OK",status= 0)
      except:
         logger(log_file ,msg=f"An error occured during the creation of the table {create_table[1]}",status= 2)

# INSERT THE DATA
logger(log_file ,msg=f"---------- DATA INGESTION ---------- ",status= 0)



## table jobs
# try:
#    logger(log_file ,msg=f"Starts data insertion proccess for table jobs",status= 0)
values_df_jobs=df_jobs.values.tolist()
sql_str="INSERT INTO employmentdepartment.jobs (id, job ) VALUES (%s, %s)"
cursor.executemany(sql_str, values_df_jobs)
conn.commit()
#    logger(log_file ,msg=f"Data insertion done successfully",status= 0)
# except:
#    logger(log_file ,msg=f"An error occured during the insertion of register in the jobs",status= 2)


## table departments
try:
   logger(log_file ,msg=f"Starts data insertion proccess for table departments",status= 0)
   values_df_departments=df_departments.values.tolist()
   sql_str="INSERT INTO employmentdepartment.departments (id, department ) VALUES (%s, %s)"
   cursor.executemany(sql_str, values_df_departments)
   conn.commit()
   logger(log_file ,msg=f"Data insertion done successfully",status= 0)
except:
   logger(log_file ,msg=f"An error occured during the insertion of register in the table departments",status= 2)

# table hired_employees
# try:
#    logger(log_file ,msg=f"Starts data insertion proccess for table hired_employees",status= 0)
values_df_hired_employees=df_hired_employees.values.tolist()
sql_str="INSERT INTO employmentdepartment.hired_employees (id, name, datetime, department_id, job_id ) VALUES (%s, %s, %s,  %s, %s)"
cursor.executemany(sql_str, values_df_hired_employees)
conn.commit()
#    logger(log_file ,msg=f"Data insertion done successfully",status= 0)
# except:
#    logger(log_file ,msg=f"An error occured during the insertion of register in the table hired_employees",status= 2)



 