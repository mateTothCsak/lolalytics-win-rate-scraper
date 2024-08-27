from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException;
from configs import CHROMEDRIVER_PATH
import json

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)


# Collects all meta champions by position from lolalytics so we only scrape later the relevant
# champs for each lane
if __name__ == "__main__":
    champions_by_roles = {
        "top": [],
        "jungle": [],
        "middle": [],
        "bottom": [],
        "support": []
    }

    for role in champions_by_roles.keys():
        path = 'https://lolalytics.com/lol/tierlist/?lane=' + role
        driver.get(path)
        champion_div_index = 3 # Xpath of first champ is /html/body/main/div[6]/div[3]/div[3]/a
        is_all_champions_scraped = False
        while not is_all_champions_scraped:
            try:
                champ_name = driver.find_element(By.XPATH, '/html/body/main/div[6]/div[' + str(champion_div_index) + ']/div[3]/a').text
                print(champ_name)
                champions_by_roles.get(role).append(champ_name)
                champion_div_index += 1
                actions.send_keys(Keys.ARROW_DOWN) # scroll down because champs are loaded dynamically
                actions.perform()
            except NoSuchElementException:
                is_all_champions_scraped = True

    print(champions_by_roles)

    driver.close()

    with open('output/champions_by_roles.json', 'w') as file:
        json.dump(champions_by_roles, file)
