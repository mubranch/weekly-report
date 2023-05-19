from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import os
import time
import bs4 as bs
import time
import functions

class LoopScraper:
    def __init__(self, username = None, password = None) -> None:
        url = os.getenv("URL")
        self.url = self._add_usr_and_pw(url, username=username, password=password)
        self.browser = webdriver.Edge()
    
    def get_source(self):
        self.browser.get(self.url) # Load page
        browser = self.browser # alias for self.browser
        
        main_window = browser.current_window_handle
        
        SIGNINBUTTON = (By.XPATH, "/html/body/div/div/div/div/div/div/div[2]/main/div[1]/div[1]/button[1]")
        EMAILFIELD = (By.ID, "i0116")
        NEXTBUTTON = (By.ID, "idSIButton9")
        
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(SIGNINBUTTON)).click()
        
        browser.switch_to.window(browser.window_handles[1]) # Switch to login window
        
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(os.getenv("USERNAME"))
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click() # Perform 2FA authentication
        
        time.sleep(5)
        
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        
        browser.switch_to.window(main_window) # Switch back to main window
            
        time.sleep(10)
        
        return self.browser.page_source
    
    def _add_usr_and_pw(self, url: str, username: str = os.getenv("USERNAME"), password: str = os.getenv("PASSWORD")):
        url = url.replace("https://", f"https://{username}:{password}@")
        return url
    
class Entry: 
    def __init__(self, title, description, links):
        self.title = title
        self.description = description
        self.links = links

    def __repr__(self) -> str:
        return f"Title: {self.title}\nDescription: {self.description}\nLinks: {self.links}"
    
class EntryMaker:
    def __init__(self, source):
        self.source = source
        
    def make_entries(self):
        items = []

        soup = bs.BeautifulSoup(self.source, features="html.parser")
        canvas = bs.BeautifulSoup(soup.find_all("div", {"aria-label": "Canvas"}).__repr__(), features="html.parser")
        
        item_index = 1
        for child in canvas.findChildren(recursive=False)[2:]: # first two children are irrelevant
            row = bs.BeautifulSoup(child.__repr__(), features="html.parser") # convert to soup
            l = row.find_all("span", {"role": "link"}) # find all links in row
            
            links = {}
            
            link_index = 1
            
            for link in l: #handles multiple links
                '''formats links to be more readable and adds them to link dict'''
                l_soup = bs.BeautifulSoup(link.__repr__(), features="html.parser")
                start = l_soup.__repr__().find("title") + 7
                end = l_soup.__repr__().find("Command +")
                links[f"Link {link_index}: "] = (l_soup.__repr__()[start:end])
                link_index += 1
            
            items.append(Entry(title=f"Activity {item_index}", description=functions.format_child(child.text), links=links))
            item_index += 1
            
        return items