from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard


class CommentCard(MDCard):
    def __init__(self, link_to_user='', profile_img='', comment_body='', comment_time_send='', **kwargs):
        super(CommentCard, self).__init__()
        self.ids.link_to_user.text = link_to_user
        self.ids.profile_img.source = profile_img
        self.ids.comment_body.text = comment_body
        self.ids.comment_time_send.text = comment_time_send


