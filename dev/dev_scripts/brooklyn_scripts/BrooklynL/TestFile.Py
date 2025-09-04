import pandas as pd 
from sqlalchemy import create_engine
connection_string = "[REMOVEDSECRET]"
engine = create_engine(connection_string)
table_name = "Projects"
query = f"SELECT * FROM {table_name}"
df = pd.read_sql_query(query, engine)
engine.dispose()