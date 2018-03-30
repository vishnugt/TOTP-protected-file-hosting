# flask_web/app.py

import flask_login
import os
import pyotp
import flask

app = flask.Flask(__name__)
app.secret_key = 'thisisnotastring'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = "gt"
    return user


@login_manager.request_loader
def request_loader(request):
    otp  = request.form.get('password')
    if otp == None:
        return
    user = User()
    user.id = "gt"
    user.is_authenticated = True
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template("form.html")
    if flask.request.form['password'] == pyotp.TOTP('thisisasecret').now():
        user = User()
        user.id = "gt"
        flask_login.login_user(user)
        return flask.redirect('/')

    return flask.redirect('/login')

@flask_login.login_required
@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    if not hasattr(flask_login.current_user, "id"):
        return flask.redirect("/login")
    BASE_DIR = '/var/lib/deluge/Downloads'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return flask.abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return flask.send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return flask.render_template('files.html', files=files)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

#@app.route('/')
#def my_form():
#    return render_template('form.html')

#@app.route('/', methods=['POST'])
#def my_form_post():
#    totp = pyotp.TOTP('thisisnotasecret')
#    text = request.form['otp']
#    if text==totp.now():
#        return "authenticated"
#    return "nah!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

