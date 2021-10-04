from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import requests
from bs4 import BeautifulSoup

URL_SITE = 'https://www.gettyimages.com/photos/patient-lying-down'


def getImages(url, folder): #url and folder name as a string
    #the number that can be changed to go through certain amount of pages
    lenOfPages = 10
    #creates an empty list for us to put list of images in
    finalImages = []
    #creates a new path for the images
    try:
        os.mkdir(os.path.join(os.getcwd(), folder)) #this is creating a new directory INSIDE our current path
    except:
        pass
    
    #changes into the new folder we created
    os.chdir(os.path.join(os.getcwd(), folder))

    '''
    URL_SITE = 'https://www.gettyimages.com/photos/patient-lying-down'

    browser = webdriver.Chrome('/Users/devinheng/Documents/chromedriver/chromedriver')
    browser.get(URL_SITE)
    page = browser.find_element_by_tag_name("html")
    sourceCode = browser.page_source
    browser.close()
    soup = BeautifulSoup(sourceCode, 'lxml')

    images = soup.findAll('img')
    counter = 1
    for image in images:
        print("image number " + str(counter) + "==> " + image['src'])
        counter += 1

    '''
    
    op = webdriver.ChromeOptions()  #this makes the browser not open so you can get the cookies without having to go in
    op.add_argument('headless')
    browser = webdriver.Chrome('/Users/devinheng/Documents/chromedriver/chromedriver')                                                                          
    browser.implicitly_wait(20)
    browser.get(url)

    while(lenOfPages > 0):
        page = browser.find_element_by_tag_name("html")
        sourceCode = browser.page_source
        soup = BeautifulSoup(sourceCode, 'lxml')
        images = soup.findAll('img')
        finalImages.append(images)
        if(lenOfPages == 10):
            browser.find_element_by_xpath('/html/body/div[2]/section/div/main/div/div/div[3]/div[2]/section/a').click()
            lenOfPages -= 1
            time.sleep(10)
            print("this is: " + str(lenOfPages))
            for index in range(0, (len(images)-2)):
                imageName = ("patient" + str(index))
                link = (images[index])['src']
                with open(imageName.replace(' ', '-').replace("'", '').replace('"', '').replace('/', '') + '.jpg', 'wb') as f: #this opens a file with the image name and downloads the image
                    im = requests.get(link)
                    f.write(im.content)
        else:
            #redo the last process and press the next button to get next page of images
            browser.find_element_by_xpath('/html/body/div[2]/section/div/main/div/div/div[3]/div[2]/section/a[2]').click()
            lenOfPages -= 1
            time.sleep(10)
            print("this is: " + str(lenOfPages))
            for index in range(0, (len(images)-2)):
                imageName = ("patient" + str(index))
                link = (images[index])['src']
                with open(imageName.replace(' ', '-').replace("'", '').replace('"', '').replace('/', '') + '.jpg', 'wb') as f: #this opens a file with the image name and downloads the image
                    im = requests.get(link)
                    f.write(im.content)
        browser.close()


if __name__ == "__main__":
    getImages(URL_SITE, 'patientImages') 