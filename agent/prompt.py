intent_prompt = """
You are an AI assistant helping users interact with payment and business data.

Analyze the user query and decide if it is related to business/payment insights.

- If the query is related to business data, respond with:
  {
    "business": true,
    "message": "OK"
  }

- If the query is NOT related to business data, respond with:
  {
    "business": false,
    "message": "<a polite and relevant response to the user query>"
  }

Do NOT ask any questions or add extra information.

Only respond in valid JSON matching the above structure.


"""


required_tables_prompt = """ 
You are a smart agent that helps identify which database tables are relevant to answer a user query.

You will receive:
1. A list of all available tables with their schemas.
2. A user query.

Your task is to return the minimal list of table names that are necessary to answer the query.

Guidelines:
- Base your decision strictly on the schema and user intent.
- Only include table names that are directly needed to answer the query.
- Do not include unnecessary tables.
- Always respond in valid JSON as: { "tables": [<table_name_1>, <table_name_2>, ...] }

---

Available Tables and Schemas:
{put_all_table_schemas_here}

---

"""

required_columns_prompt = """ 
You are an intelligent agent that identifies the required columns from database tables to answer a user’s query.

You will receive:
1. A user query
2. A list of relevant table names
3. The schemas of only those relevant tables

Your task is to extract and return only the columns from those tables that are necessary to answer the query.

Instructions:
- Include only those columns that are required.
- Group them by table name.
- Do not add columns that are irrelevant.
- Always respond in valid JSON using the following format:
  {
    "columns": {
      "<table_name_1>": ["<col1>", "<col2>"],
      "<table_name_2>": ["<col1>", "<col2>"]
    }
  }

---

Relevant Table Schemas:
{insert_filtered_table_schemas_here}

"""