from app import app


@app.route('/')
def main_view():
    pass


@app.route('/cart/')
def cart_view():
    pass


@app.route('/account/')
def account_view():
    pass


@app.route('/login/')
def login_view():
    pass


@app.route('/register/')
def register_view():
    pass


@app.route('/logout/')
def logout_view():
    pass


@app.route('/ordered/')
def ordered_view():
    pass

