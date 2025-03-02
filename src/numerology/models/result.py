from pydantic import BaseModel

class ResultInfo(BaseModel):
    name:str
    gender:str
    dob_time:datetime
    lunar_dob_time:datetime
    primary_element:
    da_yun:list
    details:dict