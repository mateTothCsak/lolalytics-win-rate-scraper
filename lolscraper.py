from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from champion_synergy_stats import ChampionSynergyStats
from configs import CHROMEDRIVER_PATH

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)

CHAMPION_ROLE_ROWS_XPATH = {
    "top": "/html/body/main/div[6]/div[1]/div[2]",
    "jungle": "/html/body/main/div[6]/div[1]/div[3]",
    "mid": "/html/body/main/div[6]/div[1]/div[4]",
    "bottom": "/html/body/main/div[6]/div[1]/div[5]",
    "support": "/html/body/main/div[6]/div[1]/div[6]",
}

def click_accept_privacy_policy_button():
    try:
        accept_privacy_policy_button = '//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, accept_privacy_policy_button)))
        actions.click(on_element=driver.find_element(By.XPATH, accept_privacy_policy_button))
        actions.perform()
    finally:
        print("Privacy policy button check complete")


def click_champion_row(role): 
    div_element = driver.find_element(By.XPATH, CHAMPION_ROLE_ROWS_XPATH.get(role))
    actions.click(on_element=div_element)
    actions.perform()


def click_first_champion_column(role):
    first_top_champion_column = CHAMPION_ROLE_ROWS_XPATH.get(role) + "/div[2]/div/div[1]"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, first_top_champion_column)))
    actions.click(on_element=driver.find_element(By.XPATH, first_top_champion_column))
    actions.perform()

# assuming the url path is in this format: /lol/draven/vs/senna/build/?vslane=support
# we grab the name from the part after 'vs'
def extract_champion_name(url):
    parts = url.split('/')
    for index, part in enumerate(parts):
        if part == 'vs':
            return parts[index + 1]
    return None

def build_xpaths(column_counter, role):
    base_xpath = CHAMPION_ROLE_ROWS_XPATH.get(role) + "/div[2]/div/div[" + str(column_counter) + "]"
    return {
        'image': base_xpath + "/a",
        'win_rate': base_xpath + "/div[1]/span",
        'pick_rate': base_xpath + "/div[4]",
        'number_of_games': base_xpath + "/div[5]"
    }

def get_scraped_synergy_stats(column_counter, role):
    xpaths = build_xpaths(column_counter, role)
    try:
        partner_image_element = driver.find_element(By.XPATH, xpaths['image'])
        partner_href = partner_image_element.get_attribute('href')
        partner_champ_name = extract_champion_name(partner_href)
        partner_win_rate = driver.find_element(By.XPATH, xpaths['win_rate']).text
        partner_pick_rate = driver.find_element(By.XPATH, xpaths['pick_rate']).text
        partner_number_of_games = driver.find_element(By.XPATH, xpaths['number_of_games']).text
        return partner_champ_name, partner_win_rate, partner_pick_rate, partner_number_of_games
    except NoSuchElementException:
        raise

def collect_champ_stats(champion_name, champion_role, partner_role, partner_relation):
    found_champs = [] #for keeping track which champs have been visited for scrolling
    global_last_champ="";
    last_name_is_repeated = False; #after moving to the right 10 times if the last name matches the current final name it means no more champs are to be seen
    
    while(not last_name_is_repeated):
        local_last_champ = "";
        for index in range(300): #TODO nice would be to replace this random 300 number with a proper solution
            column_counter = str(index+1)
            try:
                partner_champ_name, partner_win_rate, partner_pick_rate, partner_number_of_games = get_scraped_synergy_stats(column_counter, partner_role)
                print(partner_champ_name)
                champ_already_in_found_champs = any(champ.partner_champion_name == partner_champ_name for champ in found_champs)
                if not champ_already_in_found_champs:
                    stats = ChampionSynergyStats(
                        champion_name=champion_name,
                        champion_role=champion_role,
                        partner_champion_name=partner_champ_name,
                        partner_role=partner_role,
                        partner_relation=partner_relation,
                        win_rate=partner_win_rate,
                        pick_rate=partner_pick_rate,
                        number_of_games=partner_number_of_games)
                    #add champs to the visited 
                    print("adding partner champ to found champs: " + partner_champ_name)
                    found_champs.append(stats)
                    #extract champ details
                local_last_champ = partner_champ_name;
            except NoSuchElementException:
                print("last found local champ was " + local_last_champ)
                break
        if local_last_champ == global_last_champ:
            last_name_is_repeated = True
            break
        else:
            global_last_champ = local_last_champ
            print("moving to the right, global last champ " + global_last_champ)
            actions.send_keys(Keys.ARROW_RIGHT * 10) # TODO add WebdriverWait on top to avoid potential race conditions
            actions.perform()
    return found_champs

def process_champion_for_position(champion_name, champion_role, partner_role, partner_relation):
        click_champion_row(partner_role) #to bring the attention there and the champs should start loading
        click_first_champion_column(partner_role) #we click on the first champion so we'll be able to go to the right by pressing the right key
        return collect_champ_stats(champion_name, champion_role, partner_role, partner_relation)

def process_champion(champion_name, champion_role, partner_relation):
    roles = ["top", "jungle", "mid", "bottom", "support"]
    champion_stats = []
    for role in roles:
        champion_stats += process_champion_for_position(champion_name, champion_role, role, partner_relation)
    return champion_stats

    

if __name__ == "__main__":
    champion_name = "draven"
    champion_role = "bottom"
    partner_relation = "enemy"
    path = "https://lolalytics.com/lol/" + champion_name + "/build/"
    driver.get(path)

    click_accept_privacy_policy_button()
    result = process_champion(champion_name, champion_role, partner_relation)

    print(result)
    print(len(result))

    driver.close()