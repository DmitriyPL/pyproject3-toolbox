import random, datetime

from flask import session, redirect, render_template, url_for, request

from app import app, db
from models import Category, Meal, User, Order, meals_relations_association
from forms import OrderedForm, LoginForm, RegistrationForm, ChangePasswordForm


@app.route('/', methods=["GET", "POST"])
def main_view():

    if not session.get("cart"):
        session["cart"] = []

    if not session.get("user"):
        session["is_auth"] = False

    categories = db.session.query(Category).all()
    meals_by_category = get_meals_by_category(categories)
    update_session_param()

    return render_template("main.html", meals_by_category=meals_by_category)


@app.route('/account/')
def account_view():

    if session["is_auth"]:

        orders = get_user_orders_from_bd()

        return render_template("account.html", orders=orders)

    return redirect(url_for('login_view'))


@app.route('/cart/', methods=["GET", "POST"])
def cart_view():

    form = OrderedForm()

    if request.method == "POST":

        session["meal_is_deleted"] = False

        if form.validate_on_submit():

            if session["is_auth"]:

                write_order_in_bd(form)

                return redirect(url_for('ordered_view'))

    meals_in_cart = wrap_meals_in_cart()

    return render_template("cart.html", form=form, meals_in_cart=meals_in_cart)


@app.route('/add_to_cart/<int:meal_id>/')
def add_to_cart_view(meal_id):

    add_meal_to_cart(meal_id)
    update_session_param()

    return redirect(url_for('main_view'))


@app.route('/del_from_cart/<int:meal_id>/')
def del_from_cart_view(meal_id):

    del_meal_from_cart(meal_id)
    update_session_param()

    return redirect(url_for('cart_view'))


@app.route('/ordered/', methods=["GET", "POST"])
def ordered_view():
    return render_template("ordered.html")


@app.route('/login/', methods=["GET", "POST"])
def login_view():

    form = LoginForm()

    if request.method == "POST":

        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if user and user.password_valid(form.password.data):
                session["user"] = {
                    "id": user.id,
                    "email": user.email
                }
                session["is_auth"] = True

                return redirect(url_for('account_view'))
            else:
                form.email.errors.append("Не верное имя или пароль.")

    return render_template("login.html", form=form)


@app.route('/register/', methods=["GET", "POST"])
def register_view():

    if session.get("user"):
        return redirect(url_for('main_view'))

    form = RegistrationForm()

    if request.method == "POST":

        if form.validate_on_submit():

            email = form.email.data

            email_exist = User.query.filter_by(email=email).first()

            if email_exist:
                form.email.errors.append("Такой пользователь уже зарегестрирован.")
            else:
                user = User()
                user.email = email
                user.set_password(form.password.data)

                db.session.add(user)
                db.session.commit()

                session["user"] = {
                    "id": user.id,
                    "email": user.email
                }
                session["is_auth"] = True

                return redirect(url_for('account_view'))

    return render_template("register.html", form=form)


@app.route('/logout/')
def logout_view():

    session.pop("user")
    session["is_auth"] = False

    return redirect(url_for('login_view'))


@app.route('/change_password/', methods=["GET", "POST"])
def change_password_view():

    if not session["is_auth"]:
        return redirect(url_for('main_view'))

    form = ChangePasswordForm()

    if request.method == "POST":

        if form.validate_on_submit():

            user = db.session.query(User).get(session["user"]["id"])

            if user.password_valid(form.password.data):
                form.password.errors.append("Вы используете старый пароль!")
                return render_template("change_password.html", form=form)

            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('account_view'))

    return render_template("change_password.html", form=form)


def get_meals_by_category(categories):

    meals_by_category = {}

    for cat in categories:

        meals = cat.meals

        random.shuffle(meals)

        meals_in_cat = []

        for index in range(3):

            meals_in_cat.append(meals[index])

        meals_by_category[cat.title] = meals_in_cat

    return meals_by_category


def get_amount_current_order():

    amount = 0

    for meal in session["cart"]:
        amount += meal["price"]

    return amount


def get_meals_quantity():

    return len(session["cart"])


def get_meals_unit():

    num = session["meals_quantity"]

    if num % 10 == 1 and num != 11:
        return "блюдо"
    elif num % 10 in [2, 3, 4] and num not in [12, 13, 14]:
        return "блюда"
    else:
        return "блюд"


def add_meal_to_cart(meal_id):

    meal = db.session.query(Meal).get(meal_id)

    session["cart"].append({"id": meal_id, "title": meal.title, "quantity": 1, "price": meal.price})

    session["meal_is_deleted"] = False


def del_meal_from_cart(meal_id):

    for meal in session["cart"]:

        if meal["id"] == meal_id:
            session["cart"].remove(meal)
            session["meal_is_deleted"] = True
            break


def update_session_param():
    session["amount_order"] = get_amount_current_order()
    session["meals_quantity"] = get_meals_quantity()
    session["meals_unit"] = get_meals_unit()


def write_order_in_bd(form):

    order = Order()
    order.email = form.email.data
    order.adress = form.adress.data
    order.phone = form.phone.data
    order.status = "в работе"
    order.amount = session["amount_order"]
    order.time = datetime.datetime.now()

    db.session.add(order)

    for meal in session["cart"]:
        meal = db.session.query(Meal).get(meal["id"])
        order.meals.append(meal)

    user = db.session.query(User).get(session["user"]["id"])
    user.orders.append(order)
    db.session.add(user)

    db.session.commit()


# в сесси храню список добавленных в корзину товаров простыней
# для вывода сворачиваю
def wrap_meals_in_cart():

    meals_in_cart = {}

    for meal in session["cart"]:
        id = meal["id"]
        if meals_in_cart.get(id):
            meals_in_cart[id]["quantity"] += 1
            meals_in_cart[id]["price"] += meal["price"]
        else:
            meals_in_cart[id] = {"title": meal["title"], "quantity": 1, "price": meal["price"]}

    return meals_in_cart

# пришлось писать свертку для аккаунта, хотел сделать универсально и хранить в сессии объекты блюд,
# но их нельзя сериализовать, поэтому в сессии корзина как словарь... а в аккаунт получаю список блюд из бд
def wrap_meals_in_account(meals_from_order):

    meals_in_account = {}

    for meal in meals_from_order:
        id = meal.id
        if meals_in_account.get(id):
            meals_in_account[id]["quantity"] += 1
            meals_in_account[id]["price"] += meal.price
        else:
            meals_in_account[id] = {"title": meal.title, "quantity": 1, "price": meal.price}

    return meals_in_account


def get_user_orders_from_bd():

    orders_list = []

    user = db.session.query(User).get(session["user"]["id"])

    for order in user.orders:

        order_for_print = {}

        order_for_print["time"] = order.time.strftime('%Y-%m-%d в %H:%M:%S')
        order_for_print["amount"] = order.amount
        order_for_print["meals"] = wrap_meals_in_account( get_meals_from_order(order) )

        orders_list.append(order_for_print)

    return orders_list


def get_meals_from_order(order):

    meals_in_order = db.session.query(meals_relations_association).filter_by(order_id=order.id).all()

    meals = []
    for meal in meals_in_order:
        add = db.session.query(Meal).get(meal._asdict()["meal_id"])
        meals.append(add)

    return meals
