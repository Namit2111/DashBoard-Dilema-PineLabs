from agent.agents import custom_agent
from agent.prompt import intent_prompt, required_tables_prompt, required_columns_prompt, query_gen_agent_prompt
from agent.schema import IntentSchema, RequiredTablesSchema, RequiredColumnsSchema, SQLQuerySchema
from utils.db_utils import get_all_schemas, get_table_schema,execute_query
from agent.schema import SQLQuerySchema  
import json


# intent_agent = custom_agent(
#     system_prompt=intent_prompt,
#     user_query="what was the highest amount that was refunded",
#     response_model=IntentSchema,
# )

required_tables_agent = custom_agent(
    system_prompt=required_tables_prompt.replace("{put_all_table_schemas_here}", str(get_all_schemas())),
    user_query="what was the highest amount that was refunded",
    response_model=RequiredTablesSchema,
)

table_schemas = {}
for table in required_tables_agent.tables:
    table_schemas[table] = get_table_schema(table)

required_columns_agent = custom_agent(
    system_prompt=required_columns_prompt.replace("{insert_filtered_table_schemas_here}", str(table_schemas)),
    user_query="what was the highest amount that was refunded",
    response_model=RequiredColumnsSchema,
)

required_columns_json = json.dumps([t.dict() for t in required_columns_agent.tables], indent=2)

query_gen_agent = custom_agent(
    system_prompt=query_gen_agent_prompt.replace("{insert_table_names_here}", str(required_tables_agent.tables)).replace("{insert_json_of_required_columns_schema}", str(required_columns_json)),
    user_query="what was the highest amount that was refunded",
    response_model=SQLQuerySchema,
)

result = execute_query(query_gen_agent.query)

# print(intent_agent)


print(result)