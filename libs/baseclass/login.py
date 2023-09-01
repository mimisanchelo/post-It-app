from kivymd.uix.screen import MDScreen
from kivymd.toast.kivytoast import toast
from passlib.hash import bcrypt_sha256


currentUser = None

class LoginScreen(MDScreen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def login_val(self, email, password, data):
        if not email and not password:
            return toast('Empty fields')
        elif not email:
            return toast('Email is not valid')
        elif not password:
            return toast('Password is not valid')
        val = data.select_by_email(email=email)
        if val is None:
            return toast('Wrong data')
        elif not bcrypt_sha256.verify(password, val[4]):
            return toast('Wrong password')
        else:
            print('logged in!')
            return val
