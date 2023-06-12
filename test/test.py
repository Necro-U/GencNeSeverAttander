from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By


# dsp = Display(visible=False,size=(800,600))
# dsp.start()

driver = webdriver.Chrome()

driver.get("https://gencnesever.com/sporsever/decathlon-200tl-hediye-ceki-374")
sleep(3)
elem = driver.find_element(By.XPATH,"//*[@id='recaptcha-anchor']/div[1]")
elem.click()
sleep(2)
print(elem.get_attribute("src"))
