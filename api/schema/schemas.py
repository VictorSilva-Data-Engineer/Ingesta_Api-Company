from pydantic import BaseModel,Field


# ------- Department Schema ---------
class DepartmentSchema(BaseModel):   
    id: int = Field(
        ...,
        gt=0
    )
    department: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


# ------- Job Schema ---------
class JobSchema(BaseModel):
    
    id: int = Field(
        ...,
        gt=0
    )
    job: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


# ------- Hired Employee Schema ---------
class HiredEmployeeSchema(BaseModel):
    
    id: int = Field(
        ...,
        gt=0
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    datetime: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    
    department_id: int = Field(
        ...,
        gt=0
    )
    
    job_id: int = Field(
        ...,
        gt=0
    )