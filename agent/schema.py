from pydantic import BaseModel
from typing import List
from typing import Dict, List

class IntentSchema(BaseModel):
    business: bool
    message: str



class RequiredTablesSchema(BaseModel):
    tables: List[str]



class RequiredColumnsSchema(BaseModel):
    columns: List[str]

    