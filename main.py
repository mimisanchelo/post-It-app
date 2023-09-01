from kivy.core.window import Window
from kivymd.app import MDApp

import helper
from screenManager import ScreenManagement
from libs.baseclass.login import LoginScreen
from libs.baseclass.signup import SignUpScreen

from kivymd.toast.kivytoast import toast
from libs.components.create_post import CreatePost
from libs.components.postItem import PostItem
from libs.components.showPost import ShowPost
from libs.components.commentCard import CommentCard


from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton

from database.database import *

Window.size = (414, 600)

class PostItApp(MDApp):
    light_black = 57/255, 62/255, 70/255, 255/255
    orange = 214/255, 90/255, 49/255, 255/255
    foggy = 238/255, 238/255, 238/255, 255/255
    dark = 34/255, 40/255, 49/255, 255/255

    user_obj = User()
    data = Database()
    currentUser = None
    currentOpenPost = None

    def build(self):
        self.theme_cls.material_style = "M3"
        return ScreenManagement()

    def currentScreen(self, screen, direction):
        self.root.current = screen
        self.root.transition.direction = direction
        self.root.get_screen('main').ids.nav_bot.switch_tab('screen 1')
        self.root.get_screen('main').ids.scroll_view.scroll_y = 1
        self.root.get_screen('profile').ids.scroll_view.scroll_y = 1
        self.root.get_screen('post_page').ids.post_place.scroll_y = 1
        self.on_start()

    # ------------ POST ACTIVITIES ------------

    def type_comment(self, text):
        if text == '':
            return
        self.data.insert_comment(self.currentUser[0], self.currentOpenPost[0], text)

        self.fetch_comments_all()

    def fetch_comments_all(self):
        self.root.get_screen('comment_page').ids.comment_list.clear_widgets()
        for comment in self.data.fetch_all_comments(self.currentOpenPost[0]):
            commentator = self.data.fetch_user(comment[1])
            self.root.get_screen('comment_page').ids.comment_list.add_widget(
                CommentCard(
                    link_to_user=f'{commentator[2]}',
                    profile_img=f'{commentator[5]}',
                    comment_body=f'{comment[3]}',
                    comment_time_send=f'{comment[4]}'
                ))
        self.root.get_screen('comment_page').ids.prof_img.source = self.currentUser[5]
        self.currentScreen('comment_page', 'up')

    def post_open(self, title, username, subtitle):
        self.root.get_screen('post_page').ids.post_place.clear_widgets()

        # feed or profile
        if self.root.current == 'main':
            post_data = self.data.open_post(title, username, subtitle)
        else:
            username = self.root.get_screen('profile').ids.profile_toolbar.title
            post_data = self.data.open_post(title, username, subtitle)

        self.currentOpenPost = post_data

        # open screen with correct data
        self.root.get_screen('post_page').ids.post_place.add_widget(
            ShowPost(
                post_title=f'{post_data[3]}',
                post_subtitle=f'{post_data[4]}',
                post_body=f'{post_data[6]}',
                post_img=f'{post_data[-1]}',
                post_by=f'posted by {post_data[2].title()}',
                ))
        self.currentScreen('post_page', 'up')

    # ------------ TO LOAD PAGE ------------
    def on_start(self):
        self.load_feed()
        self.load_profile()

    def load_feed(self):
        if self.root.current == 'main':
            self.root.get_screen('main').ids.post_list.clear_widgets()

            for d in self.data.fetch_posts():
                self.root.get_screen('main').ids.post_list.add_widget(PostItem(post_id=f'{d[0]}',
                                                                               post_t=f'{d[3]}',
                                                                               post_s=f'{d[4]}',
                                                                               post_i=f'{d[-1]}',
                                                                               post_d=f'{d[5]}',
                                                                               post_by=f'{d[2]}',

                                                                               ))
            self.root.get_screen('main').ids.nav_user_data.title = self.currentUser[2]
            self.root.get_screen('main').ids.nav_user_data.text = self.currentUser[3]
            self.root.get_screen('main').ids.nav_user_data.source = self.currentUser[5]


    def load_profile(self):
        if self.root.current == 'profile':
            ##################################

            #############################
            self.root.get_screen('profile').ids.post_list.clear_widgets()
            total_users_post = []
            for post in self.data.fetch_author_posts(self.currentUser[0]):
                total_users_post.append(post)
                self.root.get_screen('profile').ids.post_list.add_widget(
                    PostItem(post_t=f'{post[3]}',
                             post_s=f'{post[4]}',
                             post_d=f'{post[5]}',
                             post_i=f'{post[-1]}',
                             edit_post='pencil'
                             ))

            self.root.get_screen('profile').ids.total_user_posts.text = str(len(total_users_post))
            self.root.get_screen('profile').ids.profile_toolbar.title = self.currentUser[2]
            self.root.get_screen('profile').ids.profile_img.source = self.currentUser[5]

            if self.currentUser[-1] == None:
                self.root.get_screen('profile').ids.profile_description.text = ''
            else:
                self.root.get_screen('profile').ids.profile_description.text = self.currentUser[-1]

    def load_user_settings(self):
        if self.root.current == 'settings':
            self.root.get_screen('settings').ids.prof_username.text = self.currentUser[2]
            self.root.get_screen('settings').ids.prof_name.text = self.currentUser[1]
            self.root.get_screen('settings').ids.prof_img_edit.source = self.currentUser[5]
            if self.currentUser[-1] == None:
                self.root.get_screen('settings').ids.prof_description.text = ''
            else:
                self.root.get_screen('settings').ids.prof_description.text = self.currentUser[-1]

    def load_create_post(self):
        self.root.get_screen('profile').ids.create_post.add_widget(CreatePost())

    # on username click tp to profile page of that user
    def get_profile_user(self, username):
        self.root.get_screen('profile').ids.post_list.clear_widgets()

        user = self.data.get_user_profile(username)
        # check if user is yourself
        if user == self.currentUser:

            #delete follow btn
            self.root.get_screen('profile').ids.profile_desc_box.remove_widget(
                self.root.get_screen('profile').ids.follow_btn)
            self.currentScreen('profile', 'left')
            #################################
            # self.root.get_screen('profile').ids.profile_desc_box.remove_widget(self.root.get_screen('profile').ids.follow_btn)
            ##########################
        else:
            # get total n for post by user
            total_users_post = []
            for post in self.data.fetch_author_posts(user[0]):
                total_users_post.append(post)
                self.root.get_screen('profile').ids.post_list.add_widget(PostItem(post_t=f'{post[3]}',
                                                                                  post_s=f'{post[4]}',
                                                                                  post_d=f'{post[5]}',
                                                                                  post_i=f'{post[-1]}'))

            self.root.get_screen('profile').ids.total_user_posts.text = str(len(total_users_post))
            self.root.get_screen('profile').ids.profile_toolbar.title = user[2]
            self.root.get_screen('profile').ids.profile_img.source = user[5]


            if user[-1] == None:
                self.root.get_screen('profile').ids.profile_description.text = ''
            else:
                self.root.get_screen('profile').ids.profile_description.text = user[-1]

    # ------------ TO CREATE POST AND EDIT POST ------------
    def create_post(self, title, subtitle, body, img_url):
        if title == '' or body == '':
            toast('Field needs to be filled to post')

        if self.root.get_screen('main').ids.post_it_btn.text == 'Post It':
            self.data.insert_created_post(self.currentUser[0], self.currentUser[2], title, subtitle, body, img_url)

            toast('added to base')
            helper.clear_create_post_inputs(self)
            self.root.get_screen('main').ids.nav_bot.switch_tab('screen 1')
            self.root.get_screen('main').ids.slide.index = 0
            self.load_feed()
            self.load_profile()
        else:
            self.load_post_to_edit(title, subtitle)
            self.edit_post(title, subtitle, body, img_url)
            helper.clear_create_post_inputs(self)

    def edit_post(self, title, subtitle, body, img_url):
        self.data.update_chosen_post(title, subtitle, body, img_url, self.currentOpenPost[0])
        self.root.get_screen('main').ids.slide.index = 0
        self.load_profile()
        self.currentScreen('profile', 'left')

    def load_post_to_edit(self, title, subtitle):
        if self.root.current == 'main':
            return
        else:
            # find post in db
            post_data = self.data.open_post(title, self.currentUser[2], subtitle)
            self.currentOpenPost = post_data

            # open editor
            self.currentScreen('main', 'left')
            self.root.get_screen('main').ids.nav_bot.switch_tab('screen 2')

            # fill textfields
            self.root.get_screen('main').ids.blog_title.text = post_data[3]
            self.root.get_screen('main').ids.blog_subtitle.text = post_data[4]
            self.root.get_screen('main').ids.blog_img.text = post_data[-1]
            self.root.get_screen('main').ids.blog_body.text = post_data[6]
            self.root.get_screen('main').ids.post_it_btn.text = 'Edit It'

    def to_body_post(self, title, img):
        if title == '' or img == '':
            return toast('Field should be filled')
        self.root.get_screen('main').ids.slide.load_next(mode='next')

    # ------------ SETTINGS PAGE ------------
    def settings_update_profile_data(self, name, username, description):
        self.data.update_profile(self.currentUser[0], name, username, description)
        self.currentUser = self.data.fetch_user(self.currentUser[0])
        self.currentScreen('profile', 'left')

    def settings_update_profile_img(self, img):
        self.data.update_profile_img(self.currentUser[0], img)
        self.root.get_screen('settings').ids.prof_img_edit.source = img
        if img != None:
            self.root.get_screen('settings').ids.input_edit_img.text = ''


    # ------------ SIGNUP PAGE ------------
    def sign_up_validation(self, email, name, password, username, img):
        val = self.data.select_by_email(email=email)
        if SignUpScreen.img_val(SignUpScreen(), img):
            SignUpScreen.sign_up(SignUpScreen(), email, name, password, username, img, val, self.data, self.user_obj)
            self.root.get_screen('signup').ids.slide.load_next(mode='next')
            self.root.get_screen('signup').ids.photo.text_color = self.orange
            self.root.get_screen('signup').ids.num3.text_color = self.orange
            helper.clear_inputs(self)
            self.root.current = 'login'

    def sign_up_validation1(self, email, username, name):
        if SignUpScreen.contact_val(SignUpScreen(), email, username, name, self.data):
            self.root.get_screen('signup').ids.slide.load_next(mode='next')
            self.root.get_screen('signup').ids.contact.text_color = self.orange
            self.root.get_screen('signup').ids.progress1.value = 100
            self.root.get_screen('signup').ids.num1.text_color = self.orange

    def sign_up_validation2(self, password, password_re):
        if SignUpScreen.password_val(SignUpScreen(), password, password_re):
            self.root.get_screen('signup').ids.slide.load_next(mode='next')
            self.root.get_screen('signup').ids.passwordLabel.text_color = self.orange
            self.root.get_screen('signup').ids.progress2.value = 100
            self.root.get_screen('signup').ids.num2.text_color = self.orange

    def prev1(self):
        self.root.get_screen('signup').ids.slide.load_previous()
        self.root.get_screen('signup').ids.contact.text_color = 0, 0, 0, 1
        self.root.get_screen('signup').ids.progress1.value = 0
        self.root.get_screen('signup').ids.num1.text_color = 0, 0, 0, 1

    def prev2(self):
        self.root.get_screen('signup').ids.slide.load_previous()
        self.root.get_screen('signup').ids.passwordLabel.text_color = 0, 0, 0, 1
        self.root.get_screen('signup').ids.progress2.value = 0
        self.root.get_screen('signup').ids.num2.text_color = 0, 0, 0, 1

    # ------------ LOGIN PAGE ------------
    def login_validation(self, email, password):
        self.currentUser = LoginScreen.login_val(LoginScreen(), email, password, self.data)
        helper.clear_inputs(self)
        if self.currentUser != None:
            self.root.current = 'main'
            print(self.currentUser)
            self.on_start()

    # ------------ LOGOUT ------------
    def logout(self):
        self.root.current = 'welcome'
        self.currentUser = None
        toast('You logged out. see you soon')


if __name__ == "__main__":
    PostItApp().run()

