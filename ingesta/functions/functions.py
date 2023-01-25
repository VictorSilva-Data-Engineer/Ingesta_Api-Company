from datetime import datetime
import pymysql
import pandas as pd
import boto3 

#FUCTION: write in a log file the messages indicated,
#the are three categories [INFO] infomation, [WRN] warning ,[ERR] error


def logger(log_file,msg,status):
        """recieve:
            -log_file
            -msg: message to write in the log_file
            -status: massage category
           return:
            -write message in the log_file 
        """
       
        if status == 0:
           status_flag= "[INFO]"
        elif status == 1:
           status_flag = "[WRN]"
        elif status == 2:
           status_flag = "[ERR]"
       
        message = str( str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')) +" - "+ str(status_flag)+ " - ") + msg + "\n"
        with open(log_file, "a") as file:
            file.write(message)
        
#FUNCTION: download objects from s3 
def aws_download_data(args,PATH_DOWNLOAD,BUCKET_NAME,file_name):
   """recieve:
        -args:file_log
        -PATH_DOWNLOAD: directory where files are stored
        -BUCKET_NAME: name of the bucket in s3
        -file_name: name of the file to download
      return:
        -the file indicted in the parameter file_name
   """
   try:
      s3_resource = boto3.resource('s3')
      s3_object = s3_resource.Object(BUCKET_NAME, file_name)
      s3_object.download_file(PATH_DOWNLOAD+"/"+file_name)
      logger(args,msg=f"The file {file_name} has been successfully downloaded from origin bucket {BUCKET_NAME}",status= 0)
   except:
      logger(args,msg=f"An error ocurred during the download process of the file {file_name} ",status= 2)


#FUNCTION: read the data in csv format from s3 
def s3_read_data(args,table_name):   
   """recieve:
         -table_name: name of tha file.csv located in s3
         return:
         -read the file.csv
   """
   # try:
   #    logger(args,msg=f"Starts reading file process for the file {table_name}.csv",status= 0)
   s3_bucket_name=f's3://company-data-employees/{table_name}.csv'
   logger(args,msg=f"Reading file OK",status= 0)
   return pd.read_csv(s3_bucket_name, header=0)
   # except:
   #    logger(args,msg=f"An Error has occured during the reading file proccess",status=2)

#FUNCTION: establish connection with MySql
def db_connection(args,HOST,USER,PASSWORD,PORT):
   """recieve:
       -args:file_log
       -HOST 
       -USER
       -PASSWORD
       -PORT
      return:
       -connection with MySql
   """
   try:
      logger(args,msg=f"Initializing connection to MySQL",status= 0)
      conn = pymysql.connect(host=HOST,
                              user=USER,
                              password=str(PASSWORD),
                              port=PORT
                              )
      
      logger(args,msg=f"Connection OK ",status= 0)
      return conn
   except pymysql.MySQLError as e: 
      logger(args,msg=f"An Error occurred trying to connect to MySQL",status=2)
      logger(args,msg=f"{e}",status=2)




       
    
    


