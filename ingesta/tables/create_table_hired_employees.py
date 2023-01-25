query_create_table_hired_employees="""CREATE TABLE IF NOT EXISTS employmentdepartment.hired_employees (
                                        id INT NOT NULL AUTO_INCREMENT,
                                        name VARCHAR(100) NOT NULL,
                                        datetime VARCHAR(50) NOT NULL,
                                        department_id INT NOT NULL,
                                        job_id INT NOT NULL,
                                        PRIMARY KEY (id));
                                    """ 

