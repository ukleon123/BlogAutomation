import os
import urllib.request
from openai import OpenAI
from PIL import Image


class GptPrompt:
    def __init__(self, 
                 key: str | None, 
                 model: str | None, 
                 img_model: str | None, 
                 img_size: str | None, 
                 img_prompt: str | None, 
                 msg_initial: list | None):
        self._api_key = key
        
        self.model = model
        self.msgs = msg_initial

        self.img_model = img_model
        self.img_size = img_size
        self.img_prompt = img_prompt
        
        self.client = OpenAI(api_key=self._api_key)

    def query(self, new_topic):
        self.msgs.append({'role': 'user', 
                          'content': new_topic})

        completion = self.client.chat.completions.create(
            model = self.model,
            messages = self.msgs
        )
        return completion.choices[0].message.content

    def image_generation(self, keyword, path):
        for idx in range(8):
            image = self.client.images.generate(n=1, 
                                                size=self.img_size,
                                                model=self.img_model,
                                                prompt= keyword[idx][0] + self.img_prompt)
            link = image.data[0].url
        
            original_path =  os.path.join(path, f'{idx + 1}.jpg')
            urllib.request.urlretrieve(link, original_path)
            image = Image.open(original_path)
            image = image.convert(mode='RGBA')
            image.save(os.path.join(path, f'{idx + 1}.png'))
            image.close()
            os.remove(original_path)
           