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

service = Service(r'') # will be moved to config.ini later
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)

TOP_CHAMPION_ROW = "/html/body/main/div[6]/div[1]/div[2]"


    
def click_top_champion_row(): 
    div_element = driver.find_element(By.XPATH, TOP_CHAMPION_ROW)
    actions.click(on_element=div_element)
    actions.perform()

def click_accept_privacy_policy_button():
    try:
        accept_privacy_policy_button = '//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, accept_privacy_policy_button)))
        actions.click(on_element=driver.find_element(By.XPATH, accept_privacy_policy_button))
        actions.perform()
    finally:
        print("Privacy policy button check complete")

def click_first_top_champion_column(): # can be extended by accepting the row as parameter
    first_top_champion_column = TOP_CHAMPION_ROW + "/div[2]/div/div[1]"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, first_top_champion_column)))
    actions.click(on_element=driver.find_element(By.XPATH, first_top_champion_column))
    actions.perform()


def extract_champion_name(url):
    # Splitting by '/' breaks the URL into parts between each '/'
    parts = url.split('/')
    # Assuming the champion's name is always after 'vs' in URL
    for index, part in enumerate(parts):
        if part == 'vs':
            # Return the next part after 'vs' which should be the champion's name
            return parts[index + 1]
    return None  # Return None if 'vs' is not found or no name after 'vs'



if __name__ == "__main__":
    
    champion_name = "draven"
    path = "https://lolalytics.com/lol/" + champion_name + "/build/"
    driver.get(path)

    click_accept_privacy_policy_button()
    click_top_champion_row() #to bring the attention there and the champs should start loading
    click_first_top_champion_column() #we click on the first champion so we'll be able to go to the right by pressing the right key

    #and now here below the ugly magic happens which is still not complete so don't judge dem creators
    found_champs = [] #for keeping track which champs have been visited for scrolling
    champion_role = "bottom"
    partner_champion_role = "top"
    partner_relation = "enemy"

    global_last_champ="";
    #first run the champ reading once
    for index in range(300):
        column_counter = str(index+1)
        #TODO remove partner naming from here, unncecessary
        partner_image_a_element_xpath = TOP_CHAMPION_ROW + "/div[2]/div/div[" + column_counter + "]/a"
        partner_win_rate_xpath =  TOP_CHAMPION_ROW + "/div[2]/div/div[" + column_counter + "]/div[1]/span"
        partner_pick_rate_xpath =  TOP_CHAMPION_ROW + "/div[2]/div/div[" + column_counter + "]/div[4]"
        partner_number_of_games_xpath =  TOP_CHAMPION_ROW + "/div[2]/div/div[" + column_counter + "]/div[5]"

        try:
            partner_image_element = driver.find_element(By.XPATH, partner_image_a_element_xpath)
            partner_href = partner_image_element.get_attribute('href');
            partner_champ_name = extract_champion_name(partner_href)    

            #can be shortened to one line, calling .text directly
            partner_win_rate = driver.find_element(By.XPATH, partner_win_rate_xpath).text
            partner_pick_rate = driver.find_element(By.XPATH, partner_pick_rate_xpath).text
            partner_number_of_games = driver.find_element(By.XPATH, partner_number_of_games_xpath).text

            print(partner_champ_name)
            #found_champs.append(partner_champ_name)

            #add champs to the visited 
            stats = ChampionSynergyStats(
                champion_name=champion_name,
                champion_role=champion_role,
                partner_champion_name=partner_champ_name,
                partner_role=partner_champion_role,
                partner_relation=partner_relation,
                win_rate=partner_win_rate,
                pick_rate=partner_pick_rate,
                number_of_games=partner_number_of_games)

            found_champs.append(stats)

            #found_champs.append({"name": champion_name})
            global_last_champ = partner_champ_name;
        except NoSuchElementException:
            print("last found global champ was " + global_last_champ)
            break
        
    last_name_is_repeated = False; #after moving to the right 10 times if the last name matches the current final name it means no more champs are to be seen
    #keep running the champ reading until 
    while(not last_name_is_repeated):
        for _ in range(10):
            actions.send_keys(Keys.ARROW_RIGHT)
        actions.perform()


        local_last_champ = "";
        for index in range(300):
            column_counter = str(index+1)
            champ_image_a_element_xpath = TOP_CHAMPION_ROW + "/div[2]/div/div[" + column_counter + "]/a"
            try:
                partner_image_element = driver.find_element(By.XPATH, partner_image_a_element_xpath)
                partner_href = partner_image_element.get_attribute('href');
                partner_champ_name = extract_champion_name(partner_href)    

                partner_win_rate = driver.find_element(By.XPATH, partner_win_rate_xpath).text
                partner_pick_rate = partner_pick_rate_div = driver.find_element(By.XPATH, partner_pick_rate_xpath).text
                partner_number_of_games = driver.find_element(By.XPATH, partner_number_of_games_xpath).text

                print(partner_champ_name)
                #found_champs.append(partner_champ_name)

                #add champs to the visited 
                stats = ChampionSynergyStats(
                    champion_name=champion_name,
                    champion_role=champion_role,
                    partner_champion_name=partner_champ_name,
                    partner_role=partner_champion_role,
                    partner_relation=partner_relation,
                    win_rate=partner_win_rate,
                    pick_rate=partner_pick_rate,
                    number_of_games=partner_number_of_games)

                champ_already_in_found_champs = any(champ.partner_champion_name == partner_champ_name for champ in found_champs)
                if not champ_already_in_found_champs:      
                    print(partner_champ_name)
                    #add champs to the visited 
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
            print("global last champ " + global_last_champ)

    print(found_champs)
