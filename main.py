import time
from bigQuery import send_to_bq
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

#cons
website = ["https://www.bbc.com/"]
news = ['a', 'class', 'block-link__overlay-link']
options = Options()
options.add_argument('--headless')

#Open Browser
driver = webdriver.Firefox(options=options)
driver.get(website[0])
time.sleep(3)

#get anchors
anchors = driver.find_elements(By.XPATH, "//" + news[0] + "[@" + news[1] + "='" + news[2] + "']")

#get links
hrefs = []
for anchor in anchors:
    hrefs.append(anchor.get_attribute('href'))

#get infos
titles = []
titleInfo = ['title']

authors = []
authorInfo = ['p', 'class', 'ssrcss-ugte5s-Contributor', 'strong']
authorInfo2 = ['a', 'class', 'author-unit__text']

dates = []
dateInfo = ['time', 'datetime']

texts = []
textInfo = ['div', 'data-component', 'text-block']

#append titles
for href in hrefs:
    #open news link
    driver.get(href)

    #append titles
    title = driver.find_element(By.TAG_NAME, titleInfo[0]).get_attribute('innerHTML')
    titles.append(title)

    #append authors
    try:
        try:
            author = driver.find_element(By.CLASS_NAME, authorInfo[2]).find_element(By.TAG_NAME, authorInfo[3]).get_attribute('innerText')
        except:
            author = driver.find_element(By.CLASS_NAME, authorInfo2[2]).get_attribute('innerText')
    except:
        author = 'No Author'
    authors.append(author)

    #append times
    try:
        auxDate = driver.find_element(By.TAG_NAME, dateInfo[0]).get_attribute(dateInfo[1])
        date = re.match(r'\d{4}-\d{2}-\d{2}',auxDate).group()
    except:
        auxDate = re.sub(r'[^\d]', '', href) #excluir o que não é dígito
        if len(auxDate) == 8:
            date = auxDate[0] + auxDate[1] + auxDate[2] + auxDate[3] + '-' + auxDate[4] + auxDate[5] + '-' + auxDate[6] + auxDate[7]

    dates.append(date)

    #append text
    try:
        textResult = ''
        textsArray = driver.find_elements(By.XPATH, "//" + textInfo[0] + "[@" + textInfo[1] + "='" + textInfo[2] + "']")
        for i in textsArray:
            textTemp = i.find_element(By.TAG_NAME, 'p').get_attribute('innerText')
            textResult = textResult + textTemp + ' '
        if len(textResult) > 1:
            texts.append(textResult)
        else:
            firstArticle = driver.find_element(By.CSS_SELECTOR, '.article__body-content')
            textResult = ''
            textsArray = firstArticle.find_elements(By.CSS_SELECTOR, '.body-text-card__text')
            for i in textsArray:
                textTemp = i.get_attribute('innerText')
                textResult = textResult + textTemp + ' '
            if len(textResult) > 1:
                texts.append(textResult)
    except:
        textResult = ''
        textsArray = driver.find_elements(By.CSS_SELECTOR, 'div[aria-live="polite"] p')
        for i in textsArray:
            textTemp = i.get_attribute('innerText')
            textResult = textResult + textTemp + ' '
        if len(textResult) > 1:
            texts.append(textResult)
        else:
            texts.append('FAIL TO FETCH')

i = 0
while i < len(hrefs):
    href = hrefs[i]
    title = titles[i]
    author = authors[i]
    date = dates[i]
    text = texts[i]

    send_to_bq(href, title, author, date, text)
    i += 1


driver.quit()

