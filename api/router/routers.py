from fastapi import APIRouter,Response
from fastapi  import status
from typing import List
from fastapi import Body

#local modules
from schema.schemas import DepartmentSchema, JobSchema, HiredEmployeeSchema
from config.database import engine
from model.models import departments_table, jobs_table, hired_employees_table

router = APIRouter()

@router.get("/")
def root():
    return {"message":"Hi, I am FastAPI with a router"}


# ************** Departments ************** 
##GET
@router.get(
            path="/departments",
            tags=["Departments"],
            response_model = List[DepartmentSchema],
            status_code=status.HTTP_200_OK
            )
def get_departments():
    with engine.connect() as conn:
        departments_data= conn.execute(departments_table.select()).fetchall()
        return departments_data


##POST
@router.post(
            path="/departments/new",
            tags=["Departments"],
            status_code=status.HTTP_201_CREATED
            )
def create_user(department_insert: DepartmentSchema = Body(...)):
    try:
        new_department=department_insert.dict()
        with engine.connect() as conn:
            conn.execute(departments_table.insert().values(new_department))
            return Response(status_code=status.HTTP_201_CREATED)
    except:
        return "An error have ocurred during inserting a new departement"

# ************** Jobs ************** 
##GET
@router.get(
            path="/jobs",
            tags=["Jobs"],
            response_model = List[JobSchema],
            status_code=status.HTTP_200_OK
            )
def get_jobs():
    with engine.connect() as conn:
        jobs_data= conn.execute(jobs_table.select()).fetchall()
        return jobs_data
    
##POST
@router.post(
            path="/jobs/new",
            tags=["Jobs"],
            status_code=status.HTTP_201_CREATED
            )
def create_user(job_insert: JobSchema = Body(...)):
    try:
        new_job=job_insert.dict()
        with engine.connect() as conn:
            conn.execute(jobs_table.insert().values(new_job))
            return Response(status_code=status.HTTP_201_CREATED)
    except:
        return "An error have ocurred during inserting a new job"

    
# ************** Hired Employees **************
##GET
@router.get(
            path="/hired_employees",
            tags=["Hired Employees"],
            response_model = List[HiredEmployeeSchema],
            status_code=status.HTTP_200_OK
            )
def get_hired_employees():
    with engine.connect() as conn:
        hired_employees_data= conn.execute(hired_employees_table.select()).fetchall()
        return hired_employees_data

##POST
@router.post(
            path="/hired_employees/new",
            tags=["Hired Employees"],
            status_code=status.HTTP_201_CREATED
            )
def create_user(hired_employee_insert: HiredEmployeeSchema = Body(...)):
    try:
        new_hired_employee=hired_employee_insert.dict()
        with engine.connect() as conn:
            conn.execute(hired_employees_table.insert().values(new_hired_employee))
        return Response(status_code=status.HTTP_201_CREATED)
    except:
        return "An error have ocurred during inserting a new employee"
