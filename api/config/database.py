from config.credentials import CredentialsDatabase
from sqlalchemy import create_engine,  MetaData


#DATABASE 
config_db=CredentialsDatabase()
USER=config_db.user
PASSWORD=config_db.password
HOST=config_db.host
PORT=config_db.port
DB_NAME=config_db.database

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")


meta_data = MetaData()


