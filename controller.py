import os
import json

from gpt_prompt import GptPrompt
from response_parser import ResponseParser
from blog_writer import BlogWriter
from video_maker import VideoMaker

class Controller:
    def __init__(self):
        self.cwd = os.getcwd()
        configs = self._load_config(self.cwd)

        gpt_config = configs['gpt']
        blog_config = configs['blog']
        self.prompter = GptPrompt(gpt_config['key'],
                                  gpt_config['model'],
                                  gpt_config['img_model'],
                                  gpt_config['img_size'],
                                  gpt_config['img_prompt'],
                                  gpt_config['prompt'])
        self.parser = ResponseParser()
        self.blog = BlogWriter()
        self.videomaker = VideoMaker()

        self.parsed = []
        self.keyword = configs['keyword']
        self.img_title = configs['img_title']
        self.mode = blog_config['mode']
        self.prompt = f'“{self.keyword}”'

    def _load_config(self, cwd):
        config_path = os.path.join(cwd, 'config.json')
        config_file = open(config_path, encoding='utf-8')
        return json.load(config_file)

    def get_response(self):
        res = False
        while not res:
            resp = self.prompter.query(self.prompt)
            self.parser.load_response(resp)
            res = self.parser.parse_response(self.keyword)
            if res:
                self.parsed = res

    def get_images(self, path):
        self.prompter.image_generation(self.parsed[1], path)
        self.videomaker.edit_image(self.mode, self.keyword, self.img_title, self.parsed[1])
        self.videomaker.extract_gif(self.keyword)
        self.videomaker.extract_mp4(self.keyword)

    def init_blog(self):
        self.blog.open_editor()
        self.blog.choose_template()

    def write_blog(self):
        self.blog.write_title(self.keyword)
        self.blog.write_thesis(self.keyword)
        self.blog.write_introduction(self.parsed[0])
        self.blog.write_paragraphs(self.keyword, self.parsed[1])
        self.blog.write_final(self.parsed[2])
        self.blog.save_post()