from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pathlib
import time

option = webdriver.ChromeOptions()
option.add_argument("--start-maximized")
option.add_argument("--ignore-certificate-errors")
option.add_extension("/Users/sanozan7/Desktop/TUFTS/year3/comp116/final/Adblock-Plus_v1.13.4.crx")

browser = webdriver.Chrome(executable_path='/Users/sanozan7/Desktop/TUFTS/year5/Fall/Corpora/project/chromedriver', chrome_options=option)

browser.get("http://www.google.com/")
window_before = browser.window_handles[1] 
browser.switch_to_window(window_before)
actions = ActionChains(browser)


# crane
#prof_id = "121940"

#proctor
prof_id = "271353"

dialog_clicked = False

browser.get('http://www.ratemyprofessors.com/ShowRatings.jsp?tid='+ prof_id)

# click away the dialog box
if not dialog_clicked:
	browser.find_element_by_css_selector('.btn').click()
	dialog_clicked = True
	print("found dialog box")

# load all of the content
while True:
	try: browser.find_element_by_id('loadMore').click()
	except: break

#find the reviews
reviews = browser.find_elements_by_tag_name("p")
#reviews = browser.find_elements_by_tag_name("tr")


#print or save all of the reviews to their own files for later analysis 
c = 0
for r in reviews:
	if (r.text != "" and r.text !="No Comments"):
		print("review # "+str(c))
		print(r.text)
		print()
		c+= 1