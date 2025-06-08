from pydantic import BaseModel,Field
from typing import List
from typing import Dict, List

class IntentSchema(BaseModel):
    business: bool
    message: str



class RequiredTablesSchema(BaseModel):
    tables: List[str]


class ColumnInfo(BaseModel):
    name: str = Field(..., description="Name of the column")
    type: str = Field(..., description="Data type of the column")

class TableColumnSchema(BaseModel):
    table: str = Field(..., description="Table name")
    columns: List[ColumnInfo] = Field(..., description="List of columns with names and types")

class RequiredColumnsSchema(BaseModel):
    tables: List[TableColumnSchema] = Field(..., description="List of tables and their required columns")


class SQLQuerySchema(BaseModel):
    query: str = Field(..., description="The generated SQL query as a string")


class InsightResponseSchema(BaseModel):
    insight: str  