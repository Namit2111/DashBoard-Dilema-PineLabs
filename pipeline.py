from typing import Union,Callable, Optional
from agent.agents import custom_agent
from agent.prompt import intent_prompt, required_tables_prompt, required_columns_prompt, query_gen_agent_prompt, insight_prompt
from agent.schema import IntentSchema, RequiredTablesSchema, RequiredColumnsSchema, SQLQuerySchema, InsightResponseSchema
from utils.db_utils import get_all_schemas, get_table_schema, execute_query, summarize_dataframe, get_distinct_column_values
import json


def run_nl_to_sql_pipeline(user_query: str,debug: bool = False,progress_callback: Optional[Callable[[str], None]] = None) -> Union[str, InsightResponseSchema]:
    
    if progress_callback:
        progress_callback("Parsing your natural language query...")

    # 1. Intent Agent
    intent_agent = custom_agent(
        system_prompt=intent_prompt,
        user_query=user_query,
        response_model=IntentSchema,
    )

    

    if not intent_agent.business:
        # If not business related, return the agent's message directly
        return {"answer":intent_agent.message}

    if progress_callback:
        progress_callback("Fetching tables...")

    # 2. Required Tables Agent
    all_schemas = get_all_schemas()
    required_tables_agent = custom_agent(
        system_prompt=required_tables_prompt.replace("{put_all_table_schemas_here}", str(all_schemas)),
        user_query=user_query,
        response_model=RequiredTablesSchema,
    )

    if not required_tables_agent.tables:
        return {"answer":"Sorry, no relevant tables found for your query."}

    if progress_callback:
        progress_callback("Fetching schemas for required tables...")

    # 3. Fetch Schemas for Required Tables
    table_schemas = {}
    for table in required_tables_agent.tables:
        table_schemas[table] = get_table_schema(table)

    if progress_callback:
        progress_callback("Fetching required columns...")

    # 4. Required Columns Agent
    required_columns_agent = custom_agent(
        system_prompt=required_columns_prompt.replace("{insert_filtered_table_schemas_here}", str(table_schemas)),
        user_query=user_query,
        response_model=RequiredColumnsSchema,
    )

    if not required_columns_agent.tables:
        return {"answer":"Sorry, no relevant columns found for your query."}

    required_columns_json = json.dumps([t.dict() for t in required_columns_agent.tables], indent=2)

    if progress_callback:
        progress_callback("Gathering valid column values...")

    # 5. Gather valid column values for categorical columns (limited to <= 20 unique)
    valid_column_values = {}
    for table in required_columns_agent.tables:
        table_name = table.table
        for column in table.columns:
            col_name = column.name
            values = get_distinct_column_values(table_name, col_name)
            if len(values) <= 20:
                valid_column_values[f"{table_name}.{col_name}"] = values

    # Format valid values for prompt context
    actual_values = "\n\n".join(
        [f"Valid values for '{col}': {vals}" for col, vals in valid_column_values.items()]
    )

    if progress_callback:
        progress_callback("Generating SQL query...")

    # 6. Query Generation Agent
    query_gen_agent = custom_agent(
        system_prompt=query_gen_agent_prompt
            .replace("{insert_table_names_here}", str(required_tables_agent.tables))
            .replace("{insert_json_of_required_columns_schema}", str(required_columns_json) + f"\n\nValid values {actual_values}"),
        user_query=user_query,
        response_model=SQLQuerySchema,
    )
    
    if not query_gen_agent.query:
        return {"answer":"Sorry, I couldn't generate a SQL query for that."}

    if progress_callback:
        progress_callback("Executing SQL query...")

    # 7. Execute SQL Query
    df = execute_query(query_gen_agent.query)

    # 8. Summarize if large result set
    if len(df) > 50:
        sql_result = summarize_dataframe(df)
    else:
        sql_result = df.to_markdown(index=False)

    if progress_callback:
        progress_callback("Generating insight...")

    # 9. Insight Agent to generate final response
    insight_agent = custom_agent(
        system_prompt=insight_prompt.replace("{sql_result}", sql_result).replace("{sql_query}", query_gen_agent.query),
        user_query=user_query,
        response_model=InsightResponseSchema,
    )

    if debug:
        return {"insight":insight_agent.insight, "tables":required_tables_agent.tables, "columns":json.dumps([t.dict() for t in required_columns_agent.tables], indent=2), "query":query_gen_agent.query}

    return insight_agent.insight


if __name__ == "__main__":
    result = run_nl_to_sql_pipeline("How many transaction failed")
    print(result)
