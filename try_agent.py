from agent.agents import custom_agent
from agent.prompt import intent_prompt, required_tables_prompt, required_columns_prompt
from agent.schema import IntentSchema, RequiredTablesSchema, RequiredColumnsSchema
from utils.db_utils import get_all_schemas, get_table_schema


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

# print(intent_agent)


print(required_columns_agent)