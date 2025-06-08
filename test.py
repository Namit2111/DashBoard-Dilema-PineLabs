from utils import db_utils  

# List all tables
print(db_utils.get_all_schemas())

# # Show schema of 'settlement_data'
# print(db_utils.get_table_schema('settlement_data'))

# # Preview top 5 rows of 'refund_data'
# print(db_utils.preview_table('refund_data'))

# # Row count
# print(db_utils.get_table_row_count('support_data'))

# # Custom SQL query
# df = db_utils.run_query("SELECT DISTINCT merchant_display_name FROM settlement_data LIMIT 10")
# print(df)
