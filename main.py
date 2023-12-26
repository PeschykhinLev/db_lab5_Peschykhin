import psycopg2
import matplotlib.pyplot as plt
import random

username = 'levpescihin'
password = 'kpi2023'
database = 'Lab_3'
host = 'localhost'
port = '5432'

query_1 = '''

CREATE View Meal_Protein AS
SELECT Meal.item_name, Nutritional_Information.protein
FROM Meal
JOIN Nutritional_Information ON Meal.item_id = Nutritional_Information.item_id
ORDER BY protein

'''

query_2 = '''
CREATE View Category_Calories AS
SELECT Category.category_name, SUM(Nutritional_Information.Calories) AS Total_Calories
FROM Category
JOIN Meal_Category ON Category.category_id = Meal_Category.category_id
JOIN Nutritional_Information ON Meal_Category.item_id = Nutritional_Information.item_id
WHERE Nutritional_Information.Calories > 100
GROUP BY Category.category_name
ORDER BY Total_Calories;
'''

query_3 = '''
CREATE View Meal_DailyFat_Percentage AS
SELECT Meal.item_name, Nutritional_Information.Calories, Daily_Values_on_the_Nutrition.Total_Fat_Daily_Percentage
FROM Meal
JOIN Meal_Category ON Meal.item_id = Meal_Category.category_id
JOIN Nutritional_Information ON Meal.item_id = Nutritional_Information.item_id
JOIN Daily_Values_on_the_Nutrition ON Meal.item_id = Daily_Values_on_the_Nutrition.item_id
ORDER BY Nutritional_Information.Calories;
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:

    cur = conn.cursor()
    cur.execute("DROP View IF EXISTS Meal_Protein;")
    cur.execute(query_1)
    cur.execute("SELECT * FROM Meal_Protein;")

    meal_name = []
    meal_protein = []

    # for row in cur:
    #     meal_name.append(row[0])
    #     meal_protein.append(row[1])

    rows = cur.fetchall()
    sample_rows = random.sample(rows, min(12, len(rows)))

    for row in sample_rows:
        meal_name.append(row[0])
        meal_protein.append(row[1])

    pie_fig, pie_ax = plt.subplots()
    pie_ax.pie(meal_protein, labels=meal_name, autopct='%1.1f%%')
    pie_ax.set_title('Частка кількості протеїну у кожній страві')

    cur = conn.cursor()
    cur.execute("DROP View IF EXISTS Category_Calories;")
    cur.execute(query_2)
    cur.execute("SELECT * FROM Category_Calories;")

    #plt.savefig('plots/query1_plot.png', bbox_inches='tight')

    сategory_name = []
    total_calories = []

    for row in cur:
        сategory_name.append(row[0])
        total_calories.append(row[1])

    x_range = range(len(сategory_name))
    bar_fig, bar_ax = plt.subplots()

    bar = bar_ax.bar(x_range, total_calories, label='Total')
    bar_ax.bar_label(bar, label_type='center')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(сategory_name, rotation=45, fontsize='small')
    bar_ax.set_xlabel('Категорії')
    bar_ax.set_ylabel('Кількість калорій, сal.')
    bar_ax.set_title("Загальна кількість калорій у категорій страв")

    cur = conn.cursor()
    cur.execute("DROP View IF EXISTS Meal_DailyFat_Percentage;")
    cur.execute(query_3)
    cur.execute("SELECT * FROM Meal_DailyFat_Percentage;")

    #plt.savefig('plots/query2_plot.png', bbox_inches='tight')

    meal_name = []
    calories = []
    total_fat_daily = []

    # for row in cur:
    #     meal_name.append(row[0])
    #     calories.append(row[1])
    #     total_fat_daily.append(row[2])

    rows = cur.fetchall()
    sample_rows = random.sample(rows, min(12, len(rows)))

    for row in sample_rows:
        meal_name.append(row[0])
        calories.append(row[1])
        total_fat_daily.append(row[2])

    graph_fig, graph_ax = plt.subplots()
    graph_ax.scatter(calories, total_fat_daily, color='blue', marker='o')  # Using scatter here

    i = 0
    for cal, fat in zip(calories, total_fat_daily):
        graph_ax.annotate(f'{meal_name[i], fat}', xy=(cal, fat), fontsize=6, color='black', xytext=(3, 2),
                          textcoords='offset points')
        i += 1

    graph_ax.set_xlabel('Калорії')
    graph_ax.set_ylabel('Відсоток від денної норми жиру, %')
    graph_ax.set_title('Залежність кількосіт калорій та денної норми жиру')

    #plt.savefig('plots/query3_plot.png', bbox_inches='tight')

mng = plt.get_current_fig_manager()
mng.resize(1400, 600)
plt.show()