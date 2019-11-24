from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome("./chromedriver")
driver.get("https://emojipedia.org/messenger")
try:
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//img[@title='Flag: South Africa' and @class=' lazyloaded']"))
    )
    emojigrid = driver.find_element_by_class_name("emoji-grid")
    imgs = emojigrid.find_elements_by_tag_name("img")   
    dictionary = open("dict.txt","w")
    for img in imgs:
        src = img.get_attribute("src")
        splitdesc = src.split("/") 
        descriptor = splitdesc[len(splitdesc)-1]
        splitsrc = src.split("_")
        if "fitzpatrick" in descriptor:
            img_name = splitsrc[len(splitsrc)-2] + ".png"
        else:
            img_name = splitsrc[len(splitsrc)-1]
        img_name = img_name.replace("-fe0f", "")
        img_name = img_name.replace("-", "_")
        messenger_dict = "'{}': '{}', \n".format(img_name, descriptor)
        print(messenger_dict)
        dictionary.write(messenger_dict)        
    driver.close()
    dictionary.close()
finally:
    driver.quit()
