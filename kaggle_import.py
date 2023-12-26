import psycopg2
import csv
import re

username = 'levpescihin'
password = 'kpi2023'
database = 'Lab_3'
host = 'localhost'
port = '5432'

INPUT_CSV_FILE = '/Users/levpescihin/Desktop/KPI/3 курс/БД/ЛАБ 5/menu.csv'

query_0 = ('ALTER TABLE serving_size_table DROP COLUMN IF EXISTS beverage_fl_oz_cup;'
           'ALTER TABLE serving_size_table ADD beverage_fl_oz_cup FLOAT;'
           'ALTER TABLE serving_size_table DROP COLUMN IF EXISTS beverage_ml;'
           'ALTER TABLE serving_size_table ADD beverage_ml FLOAT;'
           'ALTER TABLE serving_size_table ALTER COLUMN ounces TYPE FLOAT;'
           'ALTER TABLE serving_size_table ALTER COLUMN ounces DROP NOT NULL;'
           'ALTER TABLE serving_size_table ALTER COLUMN grams TYPE FLOAT;'
           'ALTER TABLE serving_size_table ALTER COLUMN grams DROP NOT NULL')

query_1 = ('ALTER TABLE nutritional_information '
           'ALTER COLUMN calories TYPE FLOAT, '
           'ALTER COLUMN calories_from_fat TYPE FLOAT, '
           'ALTER COLUMN total_fat TYPE FLOAT, '
           'ALTER COLUMN saturated_fat TYPE FLOAT, '
           'ALTER COLUMN cholesterol TYPE FLOAT, '
           'ALTER COLUMN sodium TYPE FLOAT, '
           'ALTER COLUMN carbohydrates TYPE FLOAT, '
           'ALTER COLUMN dietary_fiber TYPE FLOAT, '
           'ALTER COLUMN sugars TYPE FLOAT, '
           'ALTER COLUMN protein TYPE FLOAT;')


def filling_meals(file, cur):
    reader = csv.DictReader(file)
    i = 1
    for row in reader:
        cur.execute('INSERT INTO meal (item_id, item_name) VALUES (%s, %s)', (i, row['Item'],))
        i+=1

def filling_serving_portion(file, cur):
    reader = csv.DictReader(file)
    i=1
    for row in reader:
        ounces, grams, beverage_fl_oz_cup, beverage_ml = None, None, None, None

        serving_size = row['Serving Size']
        grams_match = re.search(r'\((\d+)\s*g\)', serving_size)
        ounces_match = re.search(r'(\d+(\.\d+)?)', serving_size)

        if 'cookie' in serving_size:
            grams = grams_match.group(1)
        if 'cup' in serving_size:
            beverage_fl_oz_cup = re.search(r'^(\d+)', serving_size).group(1)
        if 'carton' in serving_size:
            beverage_ml = re.search(r'(\d+)\s*ml', serving_size).group(1)
        if 'oz' in serving_size and 'cup' not in serving_size:
            ounces = re.search(r'(\d+(\.\d+)?)', serving_size).group(1)
            if grams_match:
                grams = grams_match.group(1)

        cur.execute('INSERT INTO serving_size_table (ounces, grams, beverage_fl_oz_cup, beverage_ml, item_id) VALUES (%s, %s, %s, %s, %s)',
                    (ounces, grams, beverage_fl_oz_cup, beverage_ml, i))
        i+=1

def filling_category(file, cur):
    reader = csv.DictReader(file)
    category_set = set()
    i = 1
    for row in reader:
        if row['Category'] not in category_set:
            category_set.add(row['Category'] )
            cur.execute('INSERT INTO category (category_id, category_name) VALUES (%s, %s)', (i ,row['Category'],))
            i += 1

def filling_meal_category(file, cur):
    reader = csv.DictReader(file)
    i = 1
    for row in reader:
        cur.execute('SELECT category_id FROM category WHERE category_name = %s', (row['Category'],))
        category_id_check = cur.fetchone()
        cur.execute('INSERT INTO meal_category(item_id, category_id) VALUES (%s, %s)', (i, category_id_check))
        i += 1

def filling_nutritional_information(file, cur):
    reader = csv.DictReader(file)
    i = 1
    cur.execute(query_1)
    for row in reader:
        cur.execute('INSERT INTO nutritional_information(calories, calories_from_fat, total_fat, saturated_fat, cholesterol, sodium, carbohydrates, dietary_fiber, sugars, protein, item_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (row['Calories'], row['Calories from Fat'], row['Total Fat'], row['Saturated Fat'], row['Cholesterol'], row['Sodium'], row['Carbohydrates'], row['Dietary Fiber'], row['Sugars'], row['Protein'], i))
        i += 1

def filling_daily_nutritional_information(file, cur):
    reader = csv.DictReader(file)
    i = 1
    for row in reader:
        cur.execute('INSERT INTO daily_values_on_the_nutrition(total_fat_daily_percentage, saturated_fat_daily_percentage, cholesterol_daily_percentage, sodium_daily_percentage, carbohydrates_daily_percentage, dietary_fiber_daily_percentage, vitamin_a_daily_percentage, vitamin_c_daily_percentage, calcium_daily_percentage, iron_daily_percentage, item_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (row['Total Fat (% Daily Value)'], row['Saturated Fat (% Daily Value)'], row['Cholesterol (% Daily Value)'], row['Sodium (% Daily Value)'], row['Carbohydrates (% Daily Value)'],
        row['Dietary Fiber (% Daily Value)'], row['Vitamin A (% Daily Value)'], row['Vitamin C (% Daily Value)'], row['Calcium (% Daily Value)'], row['Iron (% Daily Value)'], i))
        i += 1

with psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port) as conn:
    with conn.cursor() as cur:
        cur.execute(query_0)
        cur.execute(query_1)
        conn.commit()

        filling_meals(open(INPUT_CSV_FILE, 'r'), cur)
        filling_serving_portion(open(INPUT_CSV_FILE, 'r'), cur)
        filling_category(open(INPUT_CSV_FILE, 'r'), cur)
        filling_meal_category(open(INPUT_CSV_FILE, 'r'), cur)
        filling_nutritional_information(open(INPUT_CSV_FILE, 'r'), cur)
        filling_daily_nutritional_information(open(INPUT_CSV_FILE, 'r'), cur)

        conn.commit()



