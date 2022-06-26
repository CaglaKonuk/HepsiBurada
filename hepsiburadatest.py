from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from decimal import Decimal

##WebDriver Options
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-web-security")
options.add_argument("--disable-site-isolation-trials")

##Create Driver
browser = webdriver.Chrome(options=options)
browser.maximize_window()

browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

##Get Page
browser.get('https://www.hepsiburada.com')
wait = WebDriverWait(browser, 20000)

#Make Login visible
a = ActionChains(browser)
m= wait.until(EC.element_to_be_clickable((By.ID,"myAccount")))
a.move_to_element(m).perform()

#LOGIN
loginlink = wait.until(EC.element_to_be_clickable((By.ID, "login")))

loginlink.click()

username = wait.until(EC.element_to_be_clickable((By.ID, "txtUserName")))
username.send_keys("joxaciy527@serosin.com")

loginbutton = wait.until(EC.element_to_be_clickable((By.ID, "btnLogin")))
loginbutton.click()


password = wait.until(EC.element_to_be_clickable((By.ID, "txtPassword")))
password.send_keys("Test.123")

submitbutton = wait.until(EC.element_to_be_clickable((By.ID, "btnEmailSelect")))
submitbutton.click()

##End Of LOGIN


##Search of Cep Telefonu
typetextfirst = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type=text]")))
typetextfirst.click()
typetextfirst.send_keys("cep telefonu")
searchButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "SearchBoxOld-buttonContainer")))
searchButton.click()


##Filter price range
actionToPriceRange = ActionChains(browser)
rangeElement= wait.until(EC.element_to_be_clickable((By.ID,"fiyat")))
actionToPriceRange.move_to_element(rangeElement).perform()

minPrice = browser.find_element(By.CSS_SELECTOR,"input[placeholder='En az']")
maxPrice = browser.find_element(By.CSS_SELECTOR,"input[placeholder='En çok']")

minPrice.send_keys("3000")
maxPrice.send_keys("5000")

filterButton = browser.find_element(By.CSS_SELECTOR,"#fiyat > div > div > div > div.facetCommon-facetInputContainer.rangeFilterInput-inputRoot > button")
filterButton.click()

##Select Last item
item = wait.until(EC.element_to_be_clickable((By.ID, "i20")))
browser.execute_script('document.getElementById("i20").scrollIntoView();')


browser.execute_script("window.location = $('.productListContent-item > div > a').last()[0].href;")

browser.execute_script("$('.other-sellers > div > a').click();")

sellers = browser.find_elements(By.XPATH,"//table[@id='merchant-list']/tbody/tr/td[position()=2]/div/a[position()=1]")

prev = ""
lowest = ""
index= -1
i = 0


for seller in sellers:
    
    print(i)
    print(seller.text)
    if prev != "":
        if lowest.replace(',','',1).isdigit() & seller.text.replace(',','',1).isdigit():
            if Decimal(lowest.replace(',','.',1)) > Decimal(seller.text.replace(',','.',1)):
                lowest = seller.text
                index = i
          
        else:
            lowest = seller.text
            index = i
       
    else:
        lowest = seller.text
        index=0  
    prev = seller.text
    i += 1

print(lowest)
print(index)




lowSellerAddtoBasket = browser.find_element(By.XPATH,"//table[@id='merchant-list']/tbody/tr[" + str(index+3) + "]/td[4]/form/button")
lowSellerAddtoBasket.click()
close = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Onarım paketi istemiyorum")))
close.click()
success = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"checkoutui-ProductOnBasketHeader-22Wrk")))
print(success.text)
assert success.text =="Ürün sepetinizde", f"Expected text is Ürün Sepetinizde, got: {success.text}"
if success.text =="Ürün sepetinizde":
    print("Test passed")
else:
    print("Test failed")

browser.close()





