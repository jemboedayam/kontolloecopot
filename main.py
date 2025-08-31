#method one 

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# import time
# import keyboard
# import pyautogui


# driver = uc.Chrome(version_main=138)

# main_link = "https://oceanofpdf.com/page/157340/?s"
# driver.get(main_link)


# pdf_download_xpath = '//*[@id="genesis-content"]/article/div[1]/form[1]'

# driver.maximize_window()

# iter_count = 0


# with open('./iter_index.txt','r') as f:
#     last_iter = int(f.read())


# def skip_to_page(page_number):
#     for i in range(page_number):
#         driver.execute("window.scrollTo(0, document.documentElement.scrollHeight - 500);")
#         time.sleep(1)
#         next_page = driver.find_element(By.XPATH, '//*[@id="genesis-content"]/div[2]/ul/li[1]/a')
#         next_page.click()
#         iter_count+=7
#         time.sleep(1)


# if last_iter - 7 > iter_count:
#     skip_to_page(last_iter // 7)
    

# print(f"iter_count = {iter_count}")
# print(f"last_iter = {last_iter}")
# while True:
#     for i in range(2, 8):
#         article_xpath = f'//*[@id="genesis-content"]/article[{i}]'
#         if last_iter < iter_count:
#             try:
#                 # locate the button inside each article
#                 element = driver.find_element(By.XPATH, article_xpath)
#                 element.click()

#                 download_page = driver.find_element(By.XPATH,f'//*[@id="genesis-content"]/article[{i}]/header/a') 
#                 download_page_link = download_page.get_attribute("href")

#                 print(download_page_link)
#                 driver.get(download_page_link)
#                 # input()
                

#                 time.sleep(2)

#                 driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight - 500);")
#                 # input()
#                 time.sleep(2)
                
#                 download_element = driver.find_element(By.XPATH, f"{pdf_download_xpath}//input[@type='image']")
                
#                 # 647 299
#                 pyautogui.keyDown('ctrl')
#                 pyautogui.click(647,299,button='left')
#                 pyautogui.keyUp('ctrl')
                
#                 iter_count+=1
#                 with open('./iter_index.txt','w') as f:
#                     f.write(iter_count)
#                 # input()
#                 # driver.get("")
#             except Exception as e:
#                 print(f"Error at article {i}: {e}")
#                 print(f"Skipping article")
#                 iter_count+=1

#             driver.get(main_link)

#         else:
#             iter_count+=1
#             continue

#     try:
#         # go to next page (descending)
#         skip_to_page(1)
#     except Exception as e:

#         print(f"Next page error: {e}")
#         break


#method 2
import os
import ssl
import certifi


# Force Python's SSL to use certifi's CA bundle
os.environ["SSL_CERT_FILE"] = certifi.where()
ssl._create_default_https_context = ssl.create_default_context

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import pyautogui
from gdrive_api import upload_basic
import os

until_page = 50000

def start_driver():
    driver = uc.Chrome(version_main=138)
    driver.maximize_window()
    return driver

# --- Start driver ---
driver = start_driver()

with open('./page_number.txt', 'r') as f:
    last_pos = f.read().strip()
    if not last_pos.isdigit():
        last_pos = "157340"  # fallback default
last_pos = int(last_pos)

while True:
    if last_pos < until_page:
        print("done")
        break
    main_link = f"https://oceanofpdf.com/page/{last_pos}/?s"
    driver.get(main_link)
    print(f"[INFO] Current main link: {main_link}")

    for i in range(2, 8):
        article_xpath = f'//*[@id="genesis-content"]/article[{i}]'
        try:
            # locate the article and click
            element = driver.find_element(By.XPATH, article_xpath)
            element.click()

            # get the inner download link
            download_page = driver.find_element(By.XPATH, f'//*[@id="genesis-content"]/article[{i}]/header/a')
            download_page_link = download_page.get_attribute("href")

            print(f"[INFO] Download page link: {download_page_link}")
            driver.get(download_page_link)

            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight - 500);")
            time.sleep(2)

            # find the form element (ensures page is ready)
            pdf_download_xpath = '//*[@id="genesis-content"]/article/div[1]/form[1]'
            driver.find_element(By.XPATH, pdf_download_xpath)


            width, height = pyautogui.size()	
            scale_x = 1920 / width
            scale_y = 1080 / height

            absolute_posx = scale_x * 647
            absolute_posy = scale_y * 299

            # simulate Ctrl+Click at fixed screen coordinates
            pyautogui.keyDown('ctrl')
            pyautogui.click(absolute_posx, absolute_posy, button='left')
            pyautogui.keyUp('ctrl')

            print(f"[INFO] Clicked absolute position for article {i}")
            time.sleep(20)

            search_dir = "C:\\Users\\Jonathan Andrew\\Downloads"

            def get_latest_pdf(search_dir):
                files = [
                    os.path.join(search_dir, f)
                    for f in os.listdir(search_dir)
                    if os.path.isfile(os.path.join(search_dir, f)) and f.lower().endswith(".pdf")
                ]
                files.sort(key=lambda x: os.path.getmtime(x))
                return files[-1] if files else None

            latest_pdf = get_latest_pdf(search_dir)

            if latest_pdf:
                print("PDF terbaru:", latest_pdf)
                upload_basic(pdf_path=latest_pdf)
                os.remove(latest_pdf)
                print("done uploading")
            else:
                print("Tidak ada PDF ditemukan di folder:", search_dir)

        except Exception as e:
            print(f"[ERROR] At article {i}: {e}")
            print(f"[INFO] Skipping article {i}")

        driver.get(main_link)

    # --- Move to next page ---
    last_pos -= 1
    with open('./page_number.txt', 'w') as f:
        f.write(str(last_pos))

    time.sleep(10)
    try:
        # Restart driver to avoid memory leaks/session issues
        driver.quit()
        driver = start_driver()
        main_link = f"https://oceanofpdf.com/page/{last_pos}/?s"
        driver.get(main_link)
    except Exception as e:
        print(f"[FATAL] Could not restart driver: {e}")
        break
