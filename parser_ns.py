import time, random, configparser
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

config = configparser.ConfigParser()
config.read("config.ini")

proxy_options = {
    "proxy": {
        config["Proxy"]["type"]: f'{config["Proxy"]["type"]}://{config["Proxy"]["login"]}:{config["Proxy"]["password"]}@{config["Proxy"]["ip"]}:{config["Proxy"]["port"]}'
    }
}

driver = webdriver.Chrome(
    executable_path="chromedriver",
    options=options,
    seleniumwire_options=proxy_options
)

def click_to_button(element):
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(0.5)
    element.click()

def main ():
    try:
        driver.get(url="https://www.nseindia.com/")

        # go to PRE-OPEN MARKET
        login_btn = driver.find_element(By.CLASS_NAME, "loginIconBtn")
        click_to_button(login_btn)
        hover_Market = driver.find_element(By.XPATH, "//a[text()='Market Data']")
        ActionChains(driver).move_to_element(hover_Market).perform()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, "//a[text()='Pre-Open Market']").click()
        
        # scroll to table
        time.sleep(3)
        element_table = driver.find_element(By.CSS_SELECTOR, "#preopen-market div.table-wrap")
        driver.execute_script('arguments[0].scrollIntoView({block: "center"})', element_table)
        
        # parsing
        names = driver.find_elements(By.CSS_SELECTOR, "tr td:nth-child(2)")[:-1]
        costs = driver.find_elements(By.CSS_SELECTOR, "tr td:nth-child(7)")
        with open("pars.csv","w") as file:
            for name, cost in zip(names, costs):
                file.write(name.text + ";" + cost.text + "\n")
        time.sleep(random.randint(6, 9))
        
        # go to HOME
        home_btn = driver.find_element(By.CSS_SELECTOR, "#main_navbar ul li:nth-child(1)")
        click_to_button(home_btn)
        login_btn = driver.find_element(By.CLASS_NAME, "loginIconBtn")
        click_to_button(login_btn)
        time.sleep(random.randint(3, 5))
            
        # scroll to graf
        move_graf = driver.find_element(By.CLASS_NAME, "graph-container")
        ActionChains(driver).move_to_element(move_graf).perform()
        time.sleep(random.randint(2, 4))
            
        # click to NIFTY
        nifty_btn = random.choice(driver.find_elements(By.CSS_SELECTOR, "a[href^='#NIFTY']"))
        click_to_button(nifty_btn)
        time.sleep(random.randint(5, 6))
            
        # click to View All
        text = driver.find_element(By.CSS_SELECTOR, "a.active[href^='#NIFTY']").get_attribute("href")
        text = text.replace("https://www.nseindia.com/#", "")
        text = text.replace("%20", " ")
        view_btn = driver.find_elements(By.CSS_SELECTOR, f'a[href*="?symbol={text}"]')[1]
        driver.execute_script('arguments[0].scrollIntoView({block: "center"})', view_btn)
        click_to_button(view_btn)
        time.sleep(random.randint(3, 6))
        
        # click radio_btn
        radio_btn = driver.find_element(By.CSS_SELECTOR, "#radio_stock div:nth-child(2)")
        click_to_button(radio_btn)
        time.sleep(random.randint(2, 4))
        
        # scroll to table
        scroll_table = driver.find_element(By.CLASS_NAME, "selectbox.head_selectbox.posrel")
        driver.execute_script('arguments[0].scrollIntoView({block: "start"})', scroll_table)
        time.sleep(random.randint(2, 4))

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

if __name__== "__main__":
    main()