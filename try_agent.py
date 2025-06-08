from agent.agents import custom_agent
from agent.prompt import intent_prompt, required_tables_prompt
from agent.schema import IntentSchema, RequiredTablesSchema
from utils.db_utils import get_all_schemas


intent_agent = custom_agent(
    system_prompt=intent_prompt,
    user_query="what was the highest amount that was refunded",
    response_model=IntentSchema,
)

required_tables_agent = custom_agent(
    system_prompt=required_tables_prompt.replace("{put_all_table_schemas_here}", str(get_all_schemas())),
    user_query="what was the highest amount that was refunded",
    response_model=RequiredTablesSchema,
)



# print(intent_agent)
print(required_tables_agent)