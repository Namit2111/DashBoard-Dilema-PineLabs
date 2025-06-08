from pydantic import BaseModel
from typing import List

class IntentSchema(BaseModel):
    business: bool
    message: str



class RequiredTablesSchema(BaseModel):
    tables: List[str]