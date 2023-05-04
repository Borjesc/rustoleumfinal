import undetected_chromedriver as uc
import multiprocessing
import requests
import time
import selenium
import ssl
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def scrapelowes(item_num):
    # t0 = time.time()
    try:
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = uc.Chrome(options=options)
        driver.get('https://www.lowes.com/')

        # Search Lowes website
        driver.find_element(By.ID, 'search-query').send_keys(item_num, Keys.ENTER)
        time.sleep(1)

        # Find and retrive data
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        pricecont = str(soup.find('span', attrs={'class': 'item-price-dollar'}))
        centcont = str(soup.find('span', attrs={'class': 'PriceUIstyles__Cent-sc-14j12uk-0 hyTYGg item-price-cent'}))

        # get cents
        cent_sub = centcont[centcont.find(">"):centcont.find(">") + 6]
        cent = cent_sub[1:cent_sub.find('<')]

        # get dollar
        price_sub = pricecont[pricecont.find(">"):pricecont.find(">") + 6]
        dollar = price_sub[1:price_sub.find('<')]
        driver.quit()
        return dollar + cent
        
    except Exception as k:
        driver.quit()
        return "Item Not Carried"
    # print('done with lowes')


def scrapedepot(item_num):
    time.sleep(1)
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options)
    driver.get('https://www.homedepot.com')

    # Search Home Depot website
    try:
        driver.find_element(By.ID, 'headerSearch').send_keys(item_num, Keys.ENTER)
        driver.find_element(By.CLASS_NAME, 'product-image__wrapper--dmvgq').click()
        # <button type="button" class="super-sku__inline-tile border-radius--medium">1</button>
        
        time.sleep(5)
        driver.find_element(By.XPATH, "/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[8]/div/div[3]/div[2]/div[1]/button").click()
        time.sleep(8)
        
        # print("clicked")
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        # print("hi")
        pricecont2 = str(soup.find('span', attrs={'class': 'price-detailed__unit-price'}))
        # print(pricecont2)
        if pricecont2.count('<') == 4:
            realprice = pricecont2[pricecont2.find('span>'):pricecont2.find('>') + 15]
            # print(realprice)
        driver.quit()
        return(realprice[5:realprice.find('<')])
                
    except Exception as j:
        driver.quit()
        return("Item not carried")



def scrapeace(item_num):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options)
    driver.get('https://www.acehardware.com/')

    # Search Lowes website
    try:
        driver.find_element(By.NAME, 'query').send_keys(item_num, Keys.ENTER)
        time.sleep(5)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        pricecontainer = str(soup.find('span', attrs={'class': 'custom-price mz-price hide-price'}))
        realprice=pricecontainer[pricecontainer.find("$"):-1]
        finalprice=realprice[0:realprice.find("<")]
        return finalprice

    except Exception as l:
        driver.quit()
        return "Item not carried"
    


# def addtofile(x,y,z,itemnum):
#     df = pd.read_excel('classwork4.xlsx', header=None)
#     first_cell_value = df.iloc[1, 0]
#     if pd.notna(first_cell_value): 
#         data = {'Lowes':x,'Home Depot':y,'Ace':z}
#         df=pd.DataFrame(data,[pd.Index([itemnum])])
#         df.to_excel("/Users/carlosborjes/Desktop/Grading OOP/classwork4.xlsx", startrow=0, startcol=0)
#     else:
#         new_row = {'Lowes': x, 'Home Depot': y, 'Ace': z}
#         df = df.append(new_row, ignore_index=True)
#         df.to_excel('classwork4.xlsx', index=False)


if __name__ == "__main__":  
    # item_num="327874"
    # t0 = time.time()
    # item_num = "7792830"

    #home depot item_num
    item_num='7792830'
    # x=scrapedepot(item_num)
    # y=scrapelowes(item_num)
    # print(y)
    # print(x)
    # z=scrapeace(item_num)
    
    # processes = []
    # lowes = multiprocessing.Process(target=scrapelowes, args=(item_num,))
    # homedepot = multiprocessing.Process(target=scrapedepot, args=(item_num,))
    # ace=multiprocessing.Process(target=scrapeace, args=(item_num,))
    # processes.append(lowes)
    # processes.append(homedepot)
    # processes.append(ace)
    # lowes.start()
    # homedepot.start()
    # ace.start()
    # for p in processes:
    #     p.join()
    # itemlist.append(item_num)
    
    # loweslist=[1,2]
    # homedepotlist=[]
    # acelist=[]
    # addtofile(y,x,z,item_num)
    # data = {'Lowes':loweslist,'Home Depot':x,'Ace':z}
    # df=pd.DataFrame(data,[pd.Index([item_num])])
    # print(df)
    # df.to_excel("/Users/carlosborjes/Desktop/Grading OOP/classwork4.xlsx", startrow=0, startcol=0)
    # t1 = time.time()
    # total = t1 - t0
    # print(total)