from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


orders_relations_association = db.Table(
    'orders_relations',
    db.Column('order_id', db.Integer(), db.ForeignKey('orders.id')),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'))
)

meals_relations_association = db.Table(
    'meals_relations',
    db.Column('order_id', db.Integer(), db.ForeignKey('orders.id')),
    db.Column('meal_id', db.Integer(), db.ForeignKey('meals.id'))
)


categories_relations_association = db.Table(
    'categories_relations',
    db.Column('category_id', db.Integer(), db.ForeignKey('categories.id')),
    db.Column('meal_id', db.Integer(), db.ForeignKey('meals.id'))
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    orders = db.relationship("Order", secondary=orders_relations_association, back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)

    orders = db.relationship("Order", secondary=meals_relations_association, back_populates='meals')
    categories = db.relationship("Category", secondary=categories_relations_association, back_populates='meals')


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)

    meals = db.relationship("Meal", secondary=categories_relations_association, back_populates='categories')


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    adress = db.Column(db.String, nullable=False)

    users = db.relationship("User", secondary=orders_relations_association, back_populates='orders')
    meals = db.relationship("Meal", secondary=meals_relations_association, back_populates='orders')

