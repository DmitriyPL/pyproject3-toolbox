from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import User, Order, Meal, Category, db

admin = Admin()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Order, db.session))

