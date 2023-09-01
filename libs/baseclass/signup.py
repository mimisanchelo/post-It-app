from kivymd.uix.screen import MDScreen
from passlib.hash import bcrypt_sha256
from kivymd.toast.kivytoast import toast


class SignUpScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

    def sign_up(self, email, name, password, username, img, val, data, user_obj):
        if val is None:
            hashed = bcrypt_sha256.hash(password)
            user_obj.add_email(email)
            user_obj.add_img_profile(img)
            user_obj.add_name(name)
            user_obj.add_password(hashed)
            user_obj.add_username(username)
            toast('Registered successfully !!')
            return data.add_entry(user_obj)
        else:
            return toast('Already exists !!')

    def contact_val(self, email, username, name, data):
        if email == '' or username == '' or name == '':
            return toast('Fields should be filled')
        elif data.select_by_email(email=email) != None:
            return toast('Current email is already taken')
        else:
            return True

    def password_val(self, password, password_re):
        if password != password_re:
            return toast('passwords should be similar')
        elif password == '' or password_re == '':
            return toast('Password fields should be filled')
        else:
            return True

    def img_val(self, profile_img):
        if profile_img == '' or profile_img[0:4] != 'http':
            return toast('Provide the correct link to the image')
        else:
            return True
