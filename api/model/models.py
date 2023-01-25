from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.database import engine, meta_data

departments_table = Table( "departments", meta_data,
                            Column("id", Integer, primary_key = True),
                            Column("department",String (100),nullable=False))

jobs_table = Table("jobs", meta_data,
                    Column("id", Integer, primary_key = True),
                    Column("job",String (100),nullable=False))

hired_employees_table = Table("hiredEmployees", meta_data,
                    Column("id", Integer, primary_key = True),
                    Column("name",String (100),nullable=False),
                    Column("datetime",String (100),nullable=False),
                    Column("department_id",Integer,nullable=False),
                    Column("job_id",Integer,nullable=False))

#Execute creation of tables
meta_data.create_all(engine)

