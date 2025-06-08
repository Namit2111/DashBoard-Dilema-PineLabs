from agent.agents import custom_agent
from agent.prompt import intent_prompt, required_tables_prompt, required_columns_prompt, query_gen_agent_prompt, insight_prompt
from agent.schema import IntentSchema, RequiredTablesSchema, RequiredColumnsSchema, SQLQuerySchema, InsightResponseSchema
from utils.db_utils import get_all_schemas, get_table_schema,execute_query,summarize_dataframe,get_distinct_column_values
from agent.schema import SQLQuerySchema  
import json


intent_agent = custom_agent(
    system_prompt=intent_prompt,
    user_query="how many transactio n failed ",
    response_model=IntentSchema,
)
# if intent_agent.business: only then proceed to next agent else return the message from intent_agent
required_tables_agent = custom_agent(
    system_prompt=required_tables_prompt.replace("{put_all_table_schemas_here}", str(get_all_schemas())),
    user_query="how many transactio n failed ",
    response_model=RequiredTablesSchema,
)

table_schemas = {}
for table in required_tables_agent.tables:
    table_schemas[table] = get_table_schema(table)

required_columns_agent = custom_agent(
    system_prompt=required_columns_prompt.replace("{insert_filtered_table_schemas_here}", str(table_schemas)),
    user_query="how many transactio n failed ",
    response_model=RequiredColumnsSchema,
)
print(required_columns_agent)
required_columns_json = json.dumps([t.dict() for t in required_columns_agent.tables], indent=2)

valid_column_values = {}
for table in required_columns_agent.tables:
    table_name = table.table
    for column in table.columns:
        col_name = column.name
        values = get_distinct_column_values(table_name, col_name)
        # Only include short lists to avoid bloat
        if len(values) <= 20:
            valid_column_values[f"{table_name}.{col_name}"] = values

# Generate the context string for valid column values
actual_values = "\n\n".join(
    [f"Valid values for '{col}': {vals}" for col, vals in valid_column_values.items()]
)


query_gen_agent = custom_agent(
    system_prompt=query_gen_agent_prompt.replace("{insert_table_names_here}", str(required_tables_agent.tables)).replace("{insert_json_of_required_columns_schema}", str(required_columns_json)+ f"\n\nValid values {actual_values}"),
    user_query="how many transactio n failed ",
    response_model=SQLQuerySchema,
)
print(query_gen_agent)
df = execute_query(query_gen_agent.query)

if len(df) > 50:
    sql_result = summarize_dataframe(df)
else:
    sql_result = df.to_markdown(index=False)
print(sql_result)

insight_agent = custom_agent(
    system_prompt=insight_prompt.replace("{sql_result}", sql_result),
    user_query="how many transactio n failed ",
    response_model=InsightResponseSchema,
)

print(insight_agent)


