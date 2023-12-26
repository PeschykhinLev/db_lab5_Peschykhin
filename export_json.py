import psycopg2
import json

username = 'levpescihin'
password = 'kpi2023'
database = 'Lab_3'
host = 'localhost'
port = '5432'

def export_tables_to_json(tables, cur, json_file_path):
    all_data = {}
    for table_name in tables:
        cur.execute(f"SELECT * FROM {table_name};")
        rows = cur.fetchall()
        columns = [i[0] for i in cur.description]

        all_data[table_name] = [dict(zip(columns, row)) for row in rows]

    with open(json_file_path, 'w') as jsonfile:
        json.dump(all_data, jsonfile, indent=4)

with psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port) as conn:
    with conn.cursor() as cur:
        tables = ['Meal', 'Category', 'Meal_Category', 'Nutritional_Information', 'Daily_Values_on_the_Nutrition', 'Serving_Size_Table']
        export_tables_to_json(tables, cur, 'exported_data.json')
