
import os
import copy

from moviepy.editor import ImageSequenceClip
from PIL import Image, ImageDraw, ImageOps, ImageFont
class VideoMaker:
    def __init__(self):
        self.init_path()
        self.load_font()
        self.video_images = []
        self.masked_images = []

    def load_font(self, title_size = 100, subheading_size = 35):
        title_font_path = os.path.join(self.font_path, 'SCDream9.otf')
        subheading_font_path = os.path.join(self.font_path, 'SCDream6.otf')
        self.title_font = ImageFont.truetype(font=title_font_path, size=title_size)
        self.subheading_font = ImageFont.truetype(font=subheading_font_path, size=subheading_size)

    def init_path(self):
        self.font_path = os.path.join(os.getcwd(), 'fonts')
        self.working_dir = os.path.join(os.getcwd(), 'images')
        self.gif_image_path = os.path.join(self.working_dir, 'gif_images')
        self.result_file_path = os.path.join(self.working_dir, 'result')
        self.foreground_file_path = os.path.join(self.working_dir, 'foreground')
        self.background_health_image_path = os.path.join(self.working_dir, 'background', 'health')
        self.background_finance_image_path = os.path.join(self.working_dir, 'background', 'finance')

    def center_crop(self, image, original_size, crop_size):
        width, height = original_size
        crop_width, crop_height = crop_size

        left = (width - crop_width) / 2
        top = (height - crop_height) / 2
        right = (width + crop_width) / 2
        bottom = (height + crop_height) / 2

        return image.crop((left, top, right, bottom))
    
    def add_title_health(self, img_title):
        image = Image.new(mode='RGBA', size = (1024, 1024), color = 0x00)
        image = ImageDraw.Draw(image)
        image.text(xy = (512, 512), text = img_title, align='centered', anchor='mm', fill = (0xFF, 0xFF, 0xFF), font = self.title_font)
        return image._image
    
    def add_title_else(self, img_title):
        image = Image.new(mode='RGBA', size = (1024, 1024), color = 0x00)
        image = ImageDraw.Draw(image)
        image.text(xy = (512, 512), text = img_title, align='centered', anchor='mm', fill = (0, 0, 0), font = self.title_font)
        return image._image
    
    def add_subheading(self, image, title):
        image = ImageDraw.Draw(image)
        bbox = image.textbbox((0,0), title, font=self.subheading_font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        image.rectangle(xy = (355 - text_width // 2, 645 - text_height, 365 + text_width // 2, 655), fill = (0xFF, 0xFF, 0xFF))
        image.text(xy = (360, 650), text = title, anchor='mb', fill = (0, 0, 0), font = self.subheading_font)
        return image._image
        

    def edit_image(self, mode, title, img_title, subHeading):
        if mode == 'health':
            self.background_image_path = os.path.join(self.background_health_image_path, 'background.jpg')
            background_image = Image.open(self.background_image_path).convert('RGBA')
            self.add_title_health(img_title).save(os.path.join(self.foreground_file_path, '0.png'))            
            files = sorted(os.listdir(self.foreground_file_path))
        else :
            self.background_image_path = os.path.join(self.background_finance_image_path, 'background.jpg')
            background_image = Image.open(self.background_image_path).convert('RGBA')
            self.add_title_else(img_title).save(os.path.join(self.foreground_file_path, '0.png'))
            files = sorted(os.listdir(self.foreground_file_path))
        
        for idx, file in enumerate(files):
            result_image = background_image.copy()
            if idx > 8: break
            foreground_image_path = os.path.join(self.foreground_file_path, file)
            if os.path.isfile(foreground_image_path):
                foreground_image = Image.open(foreground_image_path).convert('RGBA')

                result_image_path = os.path.join(self.result_file_path, f'{idx + 1}. {title.strip('?!.,')}.png')
                if idx != 0:
                    foreground_image_rounded = self.make_masked_image(foreground_image)
                    foreground_image_rounded = self.add_subheading(foreground_image_rounded, subHeading[idx - 1][0])
                else : 
                    foreground_image_rounded = foreground_image.resize((720, 720), Image.LANCZOS)
                self.masked_images.append(foreground_image_rounded)
                foreground_image_rounded = ImageOps.expand(foreground_image_rounded, border=40, fill = (0, 0, 0, 0))
                
                result_image.alpha_composite(foreground_image_rounded)
                if idx + 1 < 7: 
                    result_image.save(result_image_path)
                foreground_image.crop().close()
                result_image.close()
            
    def extract_gif(self, title):
        background_image = Image.open(self.background_image_path).convert('RGBA')
        # 18 degree rotation clockwise, fade in(10 frame, 0% to 100%), fade out(9 frame, 100% to 10%, 100% to 10%)total 67 frame
        for idx_1, image in enumerate(self.masked_images):
            gif_images = []
            for idx in range(11):
                result_image = background_image.copy()
                image_rotated = image.rotate(-18 * (10 - idx), expand = True)
                
                _, _, _, A = image_rotated.split()
                A = Image.eval(A, lambda x : int(idx * 25.5) if x == 255 else 0)
                image_rotated.putalpha(A)

                image_resized = self.center_crop(image_rotated, 
                                                 image_rotated.size,
                                                 (800, 800))
                

                result_image = Image.alpha_composite(result_image, image_resized)
                gif_images.append(result_image.convert('RGB'))

            for _ in range(61):
                result_image = background_image.copy()
                expanded_image = ImageOps.expand(image, border=40, fill = (0, 0, 0, 0))
                result_image.alpha_composite(expanded_image)
                gif_images.append(result_image.convert('RGB'))

            for idx in range(0, 9):
                result_image = background_image.copy()    
                width, height = image.size
                image_resized = image.resize((width - 72 * idx, height - 72 * idx), Image.LANCZOS)
                image_rotated = image_resized.rotate(18 * idx, expand = True)

                _, _, _, A = image_rotated.split()
                A = Image.eval(A, lambda x : 255 - int(idx * 25.5) if x == 255 else 0)
                image_rotated.putalpha(A)

                width, height = image_rotated.size
                if width > 800: # crop
                    image_resized = self.center_crop(image_rotated, 
                                                     image_rotated.size,
                                                     (800, 800))
                else: #padding
                    image_resized = ImageOps.expand(image_rotated, 
                                                    (800 - width) // 2, 
                                                    (0, 0, 0, 0))
                result_image = Image.alpha_composite(result_image, image_resized)
                gif_images.append(result_image.convert('RGB'))
            if idx_1 + 1 > 6:
                gif_images[0].save(os.path.join(self.result_file_path, f'{idx_1 + 1}. {title.strip('?!.,')}.gif'), 
                                append_images=gif_images[1:], 
                                save_all=True, 
                                optimize=True, 
                                duration=25,
                                loop=0)
            for idx, image in enumerate(gif_images):
                count = idx_1 * 67 + idx
                image.save(os.path.join(self.gif_image_path, f'{count + 1000}.jpg'))   
        
    def extract_mp4(self, title):
        gif_image_paths = os.listdir(self.gif_image_path)

        for idx, path in enumerate(sorted(gif_image_paths)):
            gif_image_paths[idx] = os.path.join(self.gif_image_path, path)
        clip = ImageSequenceClip(gif_image_paths, fps=33)

        clip.write_videofile(os.path.join(self.result_file_path, f'10. {title}.mp4'))

        #clean directory
        for path in gif_image_paths:
            os.remove(path)

    def round_rect_mask(self):
        mask = Image.new("L", (720, 720), 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((0, 660, 720, 720), fill = 255)
        draw.rounded_rectangle((0, 0, 720, 720), radius=60, fill = 255)
        return mask
    
    def make_masked_image(self, image):
        image_resized = image.resize((720, 720), Image.LANCZOS)
        image_resized.putalpha(self.round_rect_mask())
        return image_resized