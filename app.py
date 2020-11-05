from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db
from admin import admin
from forms import *


app = Flask(__name__)
app.config.from_object(Config)

admin.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)


from views import *


if __name__ == '__main__':
    app.run()
