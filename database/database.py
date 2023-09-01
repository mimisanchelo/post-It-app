import datetime as dt
import sqlite3


class User():
    def add_email(self, email):
        self.email = email

    def add_password(self, password):
        self.password = password

    def add_username(self, username):
        self.username = username

    def add_name(self, name):
        self.name = name

    def add_img_profile(self, img):
        self.img_profile = img


class Database():
    def __init__(self):
        self.conn = sqlite3.connect('database/postIt.db')
        self.c = self.conn.cursor()

    def add_entry(self, user_obj):
        with self.conn:
            self.c.execute(f'INSERT into users values(NULL, "{user_obj.name}", "{user_obj.username}", "{user_obj.email}", "{user_obj.password}", "{user_obj.img_profile}", NULL)')
        self.conn.commit()

    def select_by_email(self, user_obj=None, email=None):
        if user_obj is not None:
            with self.conn:
                self.c.execute(f'SELECT * from users where email="{user_obj.email}"')
                return self.c.fetchone()
        else:
            with self.conn:
                self.c.execute(f'SELECT * from users where email="{email}"')
                return self.c.fetchone()

    def fetch_posts(self):
        with self.conn:
            self.c.execute('select * from blog_posts order by id DESC')
            return self.c.fetchall()

    def fetch_author_posts(self, user_id):
        with self.conn:
            self.c.execute(f'Select * from blog_posts where author_id="{user_id}" order by id DESC')

            return self.c.fetchall()

    def insert_created_post(self, user_id, user_name, blog_title, subtitle, body, img_url):
        d_today = dt.date.today().strftime('%B %d, %Y')
        with self.conn:
            self.c.execute(
                f'insert into blog_posts values(NULL, "{user_id}", "{user_name}", "{blog_title}", "{subtitle}", "{d_today}", "{body}", "{img_url}")')
            self.conn.commit()

    def open_post(self, title, username, subtitle):
        with self.conn:
            self.c.execute(f'select * from blog_posts where title="{title}" and author_name="{username}" and subtitle="{subtitle}"')
            return self.c.fetchone()

    def update_profile(self, user_id, user_name, user_username, user_description):
        with self.conn:
            self.c.execute(f'update users Set name="{user_name}", username="{user_username}", description="{user_description}" WHERE id="{user_id}"')
            self.conn.commit()

    def update_profile_img(self, user_id, img):
        with self.conn:
            self.c.execute(f'update users Set user_img="{img}" WHERE id="{user_id}"')
            self.conn.commit()

    def fetch_user(self, user_id):
        with self.conn:
            self.c.execute(f'Select * from users where id="{user_id}"')
            return self.c.fetchone()

    def get_user_profile(self, username):
        with self.conn:
            self.c.execute(f'SELECT * FROM users WHERE username="{username}"')
            return self.c.fetchone()


    def insert_comment(self, author_id, user_id, comment_text):
        d_today = dt.date.today().strftime('%d %b, %Y')
        time_now = dt.datetime.now().strftime('%H:%M')
        print(time_now, d_today)
        with self.conn:
            self.c.execute(f'insert into comments values(NULL, "{author_id}", "{user_id}", "{comment_text}", "{time_now}", "{d_today}")')
            self.conn.commit()

    def fetch_all_comments(self, post_id):
        with self.conn:
            self.c.execute(f'select * from comments where post_id="{post_id}" order by id DESC')
            return self.c.fetchall()

    def update_chosen_post(self, title, subtitle, body, img, post_id):
        with self.conn:
            self.c.execute(f'update blog_posts Set title="{title}", subtitle="{subtitle}", body="{body}", img_url="{img}" WHERE id="{post_id}"')
            self.conn.commit()
