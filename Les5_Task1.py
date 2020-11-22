from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru/')

elem = driver.find_element_by_id('mailbox:login-input')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)

elem = driver.find_element_by_id('mailbox:password-input')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)

driver.get('https://e.mail.ru/inbox')
links = set()
while True:
    links_len_1 = len(links)
    time.sleep(3)
    actions = ActionChains(driver)
    mails = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    for mail in mails:
        links.add(mail.get_attribute('href'))
    links_len_2 = len(links)
    if links_len_1 == links_len_2:
        break
    actions.move_to_element(mails[-1])
    actions.perform()
mail_info = []
for link in links:
    mail = {}
    driver.get(link)
    subject = driver.find_element_by_class_name('thread__subject').text
    sender = driver.find_element_by_class_name('letter-contact').text
    depart_date = driver.find_element_by_class_name('letter__date').text
    try:
        text = driver.find_element_by_xpath("//div[@class='letter__body']").text
    except:
        text = '0'
    mail['subject'] = subject
    mail['sender'] = sender
    mail['depart_date'] = depart_date
    mail['text'] = text
    mail_info.append(mail)
pprint(mail_info)
driver.quit()

