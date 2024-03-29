
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
import json
import time
import os

class mangaRock(webdriver.Chrome,webdriver.chrome.options.Options,webdriver.common.by.By,webdriver.support.ui.WebDriverWait):
    def __init__(self,**kwargs):
        self.user = kwargs.get('username')
        self.password = kwargs.get('password')

        # Get the driver path from kwargs, if none passed use '/Applications/chromedriver' as default
        self.options = webdriver.chrome.options.Options()
        # self.options.add_argument('--headless')

        self.driver = webdriver.Chrome(executable_path=kwargs.get('driverPath','/Applications/chromedriver'),options=self.options)
        # self.driver.minimize_window()

        # The wait for elements config
        self.wait = webdriver.support.ui.WebDriverWait(self.driver,10000000)

    def getFavorites(self,**kwargs):
        
        self.xPath = '//*[@id="all"]/div/div[2]/div[%d]/div[1]/a'

        importWeb = kwargs.get('importFavorites',False)

        if importWeb == True:
            self.importToWeb()
        
        else:
            # login and go to favorites 
            self.logIn()
    
        # wait for sign in button to load
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, '//*[@id="all"]/div/div[2]/div[1]/div[1]/a')))
       
        # Wait a bit for the mangas to arrange in the page
        time.sleep(3)
        # Get the number of favorites
        self.nFavorites = self.driver.find_element_by_xpath('//*[@id="all"]/div/div[1]/div/div[1]/div').text
        self.nFavorites = self.nFavorites.split(' ')
        self.nFavorites = int(self.nFavorites[0])

        print(self.nFavorites)

        # get all the favorites' names and authors
        self.favorites = []
        self.authors = []

        counter = 1

        for manga in range(1,self.nFavorites+1):

            # Get the title
            self.favorites.append(self.driver.find_element_by_xpath(self.xPath %(counter)).text)

            # Try to get the name of the author, if it falies loof for it in the other xpath
            try:
                self.authors.append(self.driver.find_element_by_xpath('//*[@id="all"]/div/div[2]/div[%d]/div[2]/a/span' %(counter)).text)
            except:
                # if it fails  again, just pass
                try:
                    self.authors.append(self.driver.find_element_by_xpath('//*[@id="all"]/div/div[3]/div[%d]/div[2]/a/span' %(counter)).text)
                except:
                    self.authors.append(None)
                    
            
            # Update counter 
            counter+=1

        for manga, author in zip(self.favorites,self.authors):
            print(manga,author)

        # Save in the file
        self.saveFavorites()

    def logIn(self):
        
        # xPaths
        loginBtn = '//*[@id="page-content"]/div/div/div/div[4]/button/span'
        continueBtn = '//*[@id="page-content"]/div/div/div/form/div[2]/button/span'
        enterBtn = '//*[@id="page-content"]/div/div/div/form/div[2]/button/span'

        emailXpath = '//*[@id="page-content"]/div/div/div/form/div[1]/div/div/input'
        passwordXpath = '//*[@id="password"]'

        # Go to the favorite page
        self.driver.get('https://mangarock.com/account/favorite')

        # wait for sign in button to load
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, '//*[@id="header"]/div[2]/div/div[2]/div[1]/button/span')))
        
        # Click in the first login button
        self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div[2]/div[1]/button/span').click()


        # wait for the elements to load
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, loginBtn)))

        # Press the button 
        self.driver.find_element_by_xpath(loginBtn).click()

        # Wait for box to open
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, emailXpath)))

        # Insert the username
        self.driver.find_element_by_xpath(emailXpath).send_keys(self.user)

        # Click continue
        self.driver.find_element_by_xpath(continueBtn).click()

        # Wait for next input box to open
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, passwordXpath)))

        # Type the password
        self.driver.find_element_by_xpath(passwordXpath).send_keys(self.password)

        # Click the login button 
        self.driver.find_element_by_xpath(enterBtn).click()

    def saveFavorites(self):

        # Create the file and open in write mode
        with open('Favorites.json','w') as file:
            
            # Save the json file
            file.write(self.createJson())
    
    def importToWeb(self):
  
        # The log in Code
        
        # xPaths
        loginBtn = '//*[@id="page-content"]/div/div/div/div[4]/button/span'
        continueBtn = '//*[@id="page-content"]/div/div/div/form/div[2]/button/span'
        enterBtn = '//*[@id="page-content"]/div/div/div/form/div[2]/button/span'

        emailXpath = '//*[@id="page-content"]/div/div/div/form/div[1]/div/div/input'
        passwordXpath = '//*[@id="password"]'

        self.driver.get('https://mangarock.com/import_export')
        
        # wait for sign in button to load
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, '//*[@id="header"]/div[2]/div/div[2]/div[1]/button/span')))
        
        # Click in the first login button
        self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div[2]/div[1]/button/span').click()


        # wait for the elements to load
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, loginBtn)))

        # Press the button 
        self.driver.find_element_by_xpath(loginBtn).click()

        # Wait for box to open
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, emailXpath)))

        # Insert the username
        self.driver.find_element_by_xpath(emailXpath).send_keys(self.user)

        # Click continue
        self.driver.find_element_by_xpath(continueBtn).click()

        # Wait for next input box to open
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, passwordXpath)))

        # Type the password
        self.driver.find_element_by_xpath(passwordXpath).send_keys(self.password)

        # Click the login button 
        self.driver.find_element_by_xpath(enterBtn).click()
        

        ####################################################################################################################################
            
        # Wait for the import btn to load then click it
        importXpath = '//*[@id="page-content"]/div/div/div/div/div[1]/div/button/span'
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, importXpath)))
        self.driver.find_element_by_xpath(importXpath).click()

        # Wait for the message of completion to appear
        messageXpath = '//*[@id="page-content"]/div/div/div/div/div[1]/div'
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, messageXpath)))

        # Go to the favorites page
        self.driver.get('https://mangarock.com/account/favorite')

    def createJson(self):

        # Creates a list of dictionaries containing all the data
        favoriteJson = [{"Title":None,"Author":None} for n in range(self.nFavorites)]
        for manga,author,data in zip(self.favorites,self.authors,favoriteJson):
            data["Title"]  = manga
            data["Author"] = author

        # Make it a json string
        favoriteJson = json.dumps(favoriteJson, indent=4)

        return favoriteJson

if __name__ == '__main__':
    manga = mangaRock(username = '',password = '')
     
    manga.getFavorites(importFavorites = False)