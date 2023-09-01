from kivymd.uix.boxlayout import MDBoxLayout


class ShowPost(MDBoxLayout):
    def __init__(self, post_title='', post_subtitle='', post_body='', post_img='', post_by='', **kwargs):
        super(ShowPost, self).__init__()
        self.ids.post_title.text = post_title
        self.ids.post_subtitle.text = post_subtitle
        self.ids.post_body.text = post_body
        self.ids.post_img.source = post_img
        self.ids.post_by.text = post_by

