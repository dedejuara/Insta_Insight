import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import uuid
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import gradio as gr

def scrap_instagram(usernames):
    data = []
    usernames = [usernames]

    API_URL = "https://api-inference.huggingface.co/models/timm/mobilenetv3_large_100.ra_in1k"
    API_URL_Capt = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer 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"}

    scraping_folder = 'Scraping_Instagram'
    if not os.path.exists(scraping_folder):
        os.mkdir(scraping_folder)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(options=options)
    driver.get('https://www.instagram.com/')
    time.sleep(1)
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys('coba4824') 
    time.sleep(1)

    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    username_field.send_keys('zazaza123')

    time.sleep(1)

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))
    login_button.click()
    time.sleep(7)

    for user in usernames:
        user_folder = os.path.join(scraping_folder, user)
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)

        driver.get(f"https://www.instagram.com/{user}/")
        time.sleep(5)

        for _ in range(5):
            driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL, Keys.END)
            time.sleep(10)

        raw_html = driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')
        soup_html = BeautifulSoup(raw_html, "html.parser")

        containers = soup_html.findAll('span', attrs={'class': 'xnz67gz x14yjl9h xudhj91 x18nykt9 xww2gxu x9f619 x1lliihq x2lah0s x6ikm8r x10wlt62 x1n2onr6 xzfakq x7imw91 x1j8hi7x x5aw536 x194ut8o x1vzenxt xd7ygy7 xt298gk xynf4tj xdspwft x1r9ni5o x1d52zm6 xoiy6we x15xhmf9 x1qj619r x15tem40 x1xrz1ek x1s928wv x1n449xj x2q1x1w x1j6awrg x162n7g1 x1m1drc7'})
#         containers2 = soup_html.findAll('div', attrs={'class': 'x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1'})
        containers2 = soup_html.findAll('article', attrs={'class': 'x1iyjqo2'})
        name = soup_html.findAll('span', attrs={'class': 'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj'})
        if name:
            acc = name[0].get_text()
        time.sleep(5)
        
        srcs = []
        for container1 in containers:
            img_tag = container1.find('img')
            if img_tag:
                src = img_tag['src']
                srcs.append(src)
                
        filtered_urls = [url for url in srcs if 'scontent.cdninstagram.com' not in url]
        response = requests.get(filtered_urls[0])
        uid_image = str(uuid.uuid4())
        content_type = response.headers['Content-Type']
        if 'image' in content_type:
            extension = content_type.split('/')[1]
            file_name = f"{uid_image}.{extension}"
            file_path = os.path.join(user_folder, file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
            dataset = {
                'id': uid_image,
                'file_path': f"{file_path}",
                'username': user,
                'account_name': acc
            }
            data.append(dataset)
            time.sleep(5)

        feed = []            
        for container in containers2:
            img_tags = container.findAll('img')
            for img_tag in img_tags:
                src2 = img_tag['src']
                feed.append(src2) 

        for img in feed:
            response = requests.get(img)
            uid_image = str(uuid.uuid4())
            content_type = response.headers['Content-Type']
            if 'image' in content_type:
                extension = content_type.split('/')[1]
                file_name = f"{uid_image}.{extension}"
                file_path = os.path.join(user_folder, file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                dataset = {
                    'id': uid_image,
                    'file_path': f"{file_path}",
                    'username': user,
                    'account_name': acc
                }
                data.append(dataset)
                time.sleep(5)

    driver.quit() 
    dataset = pd.DataFrame(data)
    time.sleep(5)
    data_insight = []
    base_options = python.BaseOptions(model_asset_path='detector.tflite')
    options = vision.FaceDetectorOptions(base_options=base_options)
    detector = vision.FaceDetector.create_from_options(options)
    def image_class(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    def image_capt(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL_Capt, headers=headers, data=data)
        return response.json()
    image_to_proccess = dataset['file_path']
    for img in image_to_proccess:
        image = mp.Image.create_from_file(img)
        detection_result = detector.detect(image)
        try:
            first_detection = detection_result.detections[0]
            first_score = first_detection.categories[0].score
            if first_score:
                detection = 1
        except:
            detection = 0
        try:
            output = image_class(img)
            time.sleep(15)
            output2 = image_capt(img)
            time.sleep(15)
        except:
            output = None
            output = None
        try:
            top1_labels = [item['label'].split(':')[0].strip() for item in output[:1] if 'label' in item]
            top2_labels = [item['label'].split(':')[0].strip() for item in output[1:2] if 'label' in item]
            top3_labels = [item['label'].split(':')[0].strip() for item in output[2:3] if 'label' in item]
            caption = output2[0]['generated_text']
        except:
            top1_labels = 'None'
            top2_labels = 'None'
            top3_labels = 'None'
            caption = 'None'
        datas = {
            'face_detec':detection,
            'class1':top1_labels[0],
            'class2':top2_labels[0],
            'class3':top3_labels[0],
            'caption':caption
        }
        data_insight.append(datas)
    dataset['is_Face'] = [item['face_detec'] for item in data_insight]
    dataset['theme_photo_1'] = [item['class1'] for item in data_insight]
    dataset['theme_photo_2'] = [item['class2'] for item in data_insight]
    dataset['theme_photo_3'] = [item['class3'] for item in data_insight]
    dataset['image_caption'] = [item['caption'] for item in data_insight]

    uid_dataset = str(uuid.uuid4())
    dataset.to_csv(f'Dataset_Scrap_Instagram_{uid_dataset}.csv', index=False)
    return dataset

with gr.Blocks(theme = "soft", title="Insta Insight") as instainsight:
    gr.HTML(
    """<img src="https://botika.online/assets/uploads/2019/04/logo-primary-1.png" alt="Logo" style="width:126px;height:38px;"> """
    )
    gr.Markdown(
        """
        # Insta Insight
        Face Detection, Classificaton, and Captioning Instagram Media
        """)
    with gr.Row():
        with gr.Column():
            username = gr.Textbox("",placeholder="Input Username Instagram", label="Target User")
            get_data = gr.Button("Get Insight")
            result = gr.components.Dataframe(type="pandas")
            get_data.click(fn=scrap_instagram, inputs=username, outputs=result)
if __name__ == "__main__":
    instainsight.launch()