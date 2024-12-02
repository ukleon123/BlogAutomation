import time
import random
import pickle

from typing import List

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome, ChromeOptions, ChromeService, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class BlogWriter():
    def __init__(self):

        self.edit_url = ""

        # Chrome 옵션 설정
        driver_option = ChromeOptions()
        driver_service = ChromeService(ChromeDriverManager().install())
        # driver_option.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 감지 방지
        # driver_option.add_experimental_option("excludeSwitches", ["enable-automation"])  # '자동화됨' 메시지 제거
        # driver_option.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 비활성화
        # driver_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # User-Agent 변경

        #driver_option.add_argument("headless")
        self.driver = Chrome(service = driver_service, options=driver_option)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # navigator.webdriver 제거
        self.actions = ActionChains(self.driver)

    def save_cookie(self):
        with open("cookies.pkl", "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookie(self):
        with open("cookies.pkl", 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        self.driver.refresh()
    
    def humanlike_type(self, text : str):
        for key in text:
            self.actions.send_keys(key)
            self.actions.perform()
            time.sleep(random.random() / 5)

    def open_editor(self):
        self.driver.get(self.edit_url)
        self.load_cookie()
        self.driver.get(self.edit_url + '/postwrite')
        # close help pop up
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'se-popup-button-cancel'))
            )
        except:
            pass
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'se-help-panel-close-button'))
        ).click()

    def choose_template(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'se-toolbar-item-template'))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.se-tab-button[value="my"]'))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'se-doc-template'))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'se-sidebar-close-button'))
        ).click()


    def write_title(self, title : str):
        xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[1]/div[1]/div/div/p/span'
        title_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        self.actions.double_click(title_element)
        self.actions.perform()
        self.humanlike_type(title)
    
    def write_thesis(self, thesis : str):
        xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[2]/div/div[2]/div/div/div[1]/p'
        thesis_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        self.actions.move_to_element(thesis_element)
        self.actions.click(thesis_element)
        self.actions.perform()
        self.humanlike_type(thesis)

    def write_introduction(self, content):
        for i in range(1, 3):
            xpath = f'/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[5]/div/div/div/div/p[{i}]'
            introduction_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            self.actions.move_to_element(introduction_element)
            self.actions.click(introduction_element)
            self.actions.double_click(introduction_element)
            self.actions.perform()
            self.humanlike_type(content[i - 1])
    
    def write_paragraphs(self, keyword, content : List[List]):
        # 8paragraph
        idx = 7
        for i in range(0, 29, 4):
            subheading_xpath = f'/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[{idx + i}]/div/div/div/div/p'
            paragraph_xpath = f'/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[{idx + i + 2}]/div/div/div/div/p'
            subheading = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, subheading_xpath))
            )
            paragraph = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, paragraph_xpath))
            )

            self.actions.move_to_element(subheading)
            self.actions.click(subheading)
            self.actions.double_click(subheading)
            self.actions.perform()
            self.humanlike_type(content[i // 4][0])

            self.actions.move_to_element(paragraph)
            self.actions.click(paragraph)
            self.actions.double_click(paragraph)
            self.actions.perform()
            if (i // 4) % 2: 
                self.humanlike_type( content[i // 4][1])
            else:
                self.humanlike_type(content[i // 4][1] + f"{keyword}{content[i // 4][0]}")
    
    def write_final(self, content : List[str]):
        paragraph_xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[39]/div/div/div/div/p'
        end_sentence = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[42]/div/div/div/div/p[1]'
        paragraph = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, paragraph_xpath))
        )
        finale = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, end_sentence))
        )
        
        self.actions.move_to_element(paragraph)
        self.actions.click(paragraph)
        self.actions.double_click(paragraph)
        self.actions.perform()

        self.humanlike_type(content[0])

        self.actions.move_to_element(finale)
        self.actions.click(finale)
        self.actions.double_click(finale)
        self.actions.perform()
        
        self.humanlike_type(content[1])
    
    def save_post(self):
        save_btn_xpath = '/html/body/div[1]/div/div[1]/div/div[2]/button[1]'
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, save_btn_xpath))
        )

        self.actions.move_to_element(save_btn)
        self.actions.click(save_btn)
        self.actions.perform()
            
