from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import MDIconButton
from kivy.properties import ObjectProperty


class PostItem(RelativeLayout):
    def __init__(self, post_t="", post_s='', post_i='', post_d='', post_by='', edit_post='', **kwargs):
        super(PostItem, self).__init__()
        self.ids.post_title.text = post_t
        self.ids.post_subtitle.text = post_s
        self.ids.post_img.source = post_i
        self.ids.post_date.text = post_d
        self.ids.post_by.text = post_by
        self.ids.edit_post.icon = edit_post

    def disabled_btn(self):
        return True