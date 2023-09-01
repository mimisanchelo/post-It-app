def clear_inputs(self):
    self.root.get_screen('login').ids.email.text = ''
    self.root.get_screen('login').ids.password.text = ''

    self.root.get_screen('signup').ids.email.text = ''
    self.root.get_screen('signup').ids.password.text = ''

    self.root.get_screen('settings').ids.prof_img_edit.text = ''


def clear_create_post_inputs(self):
    self.root.get_screen('main').ids.blog_title.text = ''
    self.root.get_screen('main').ids.blog_subtitle.text = ''
    self.root.get_screen('main').ids.blog_img.text = ''
    self.root.get_screen('main').ids.blog_body.text = ''
    self.root.get_screen('main').ids.post_it_btn.text = 'Post It'
    self.root.get_screen('main').ids.slide.index = 0
