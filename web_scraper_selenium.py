from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
import urllib.request
import csv

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


try:
    driver.get("https://www.imdb.com/search/title/?genres=animation&keywords=anime")
    next_button = driver.find_element(By.CLASS_NAME, "ipc-see-more")
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(next_button).click().pause(1).perform()
    animes = driver.find_elements(By.CLASS_NAME, "ipc-title-link-wrapper")
    links = []
    for anime in animes:
        link = anime.get_attribute("href")
        links.append(link)

    data = []
    i = 0
    for link in links:
        driver.get(link)
        # title = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span').text
        title = driver.find_element(By.CSS_SELECTOR, "#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-afa4bed1-0.iMxoKo > section > div:nth-child(5) > section > section > div.sc-37902d12-3.jCzyxv > div.sc-d6bd91ba-0.heSxMd > h1").text
        print(title)
        try:
            pass
            episodes = driver.find_element(By.CLASS_NAME, "sc-2fa14b14-3").text
        except:
            pass
            episodes = "N/A"
        rating = driver.find_element(By.CLASS_NAME, "sc-eb51e184-1").text
        short_description = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p').text
        poster_image_link = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a').get_attribute("href")
        tag_elements = driver.find_elements(By.CLASS_NAME, "ipc-chip__text")
        tags = []
        for tag in tag_elements:
            tags.append(tag.text)
        driver.get(poster_image_link)
        img_url = driver.find_element(By.TAG_NAME, "img").get_attribute("src")
        urllib.request.urlretrieve(img_url, f"{i}.jpg")
        datum = {
            "title": title,
            "episodes": episodes,
            "rating": rating,
            "short_description": short_description,
            "tags": tags,
            "image": f"{i}.jpg"
        }
        print(title)
        data.append(datum)
        i += 1

    keys = data[0].keys()
    with open("anime_data.csv", "w", newline="") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        for anime in data:
            w.writerow(anime)

finally:
    # Close the browser
    driver.quit()
