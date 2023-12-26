import csv
import psycopg2

username = 'levpescihin'
password = 'kpi2023'
database = 'Lab_3'
host = 'localhost'
port = '5432'

def export_table_to_csv(table_name, cur, csv_file_path):
    cur.execute(f"SELECT * FROM {table_name};")
    rows = cur.fetchall()
    column_names = [i[0] for i in cur.description]

    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
        csvwriter.writerows(rows)

tables = ['Meal', 'Category', 'Meal_Category', 'Nutritional_Information', 'Daily_Values_on_the_Nutrition', 'Serving_Size_Table']

with psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port) as conn:
    with conn.cursor() as cur:
        for table in tables:
            export_table_to_csv(table, cur, f'csv_files/{table}.csv')