# Create your tasks here
from celery import shared_task

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = None

@shared_task
def play_song(keyword, url=None):
    global driver

    if driver is None:
        driver = webdriver.Chrome('./drivers/chromedriver')

    wait = WebDriverWait(driver, timeout=0)
    visible = EC.visibility_of_element_located

    video_keyword = keyword
    video_url = "" if url is None else url

    if video_url == "":
        driver.get('https://www.youtube.com/results?search_query={}'.format(str(video_keyword)))
        wait.until(visible((By.ID, "video-title")))
        driver.find_element_by_css_selector("#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer").click()

        current_url = driver.current_url
        return current_url
    else:
        driver.get(video_url)
        return video_url