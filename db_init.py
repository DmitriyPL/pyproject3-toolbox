import os

import xlrd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import Category, Meal

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

file_data = xlrd.open_workbook('Data.xlsx')

sheet_meals = file_data.sheet_by_name("meals")
sheet_categories = file_data.sheet_by_name("categories")

for row_num in range(1, sheet_categories.nrows):
    row = sheet_categories.row(row_num)
    category = Category(title=row[1].value)
    db.session.add(category)

db.session.commit()

# По скольку БД уже начала индексировать данные в таблице, id не откатить до 1-5.
# Что бы не пересоздавать таблицы и бд небольшой вспомогательный словарь

cat = {1: "Суши",
       2: "Стритфуд",
       3: "Пицца",
       4: "Паста",
       5: "Новинки",
       }

for row_num in range(1, sheet_meals.nrows):
    row = sheet_meals.row(row_num)
    meal = Meal(
                title=row[1].value,
                price=row[2].value,
                description=row[3].value,
                picture=row[4].value
                )
    db.session.add(meal)

    category = db.session.query(Category).filter(Category.title == cat[int(row[5].value)]).first()
    meal.categories.append(category)

db.session.commit()
