import json
from bs4 import BeautifulSoup
import requests
import os
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def addStocks(currentInput):
    url = 'https://markets.businessinsider.com/stocks/' + currentInput + '-stock'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    trackedStockList = [] 

    for name in soup.find_all('span', attrs={'class': 'price-section__label'}):
        print(str(name.text).strip())
        companyName = str(name.text).strip()

    for cPrice in soup.find_all('span', attrs={'class': 'price-section__current-value'}):
        print(str(cPrice.text).strip())
        currentPrice = str(cPrice.text).strip()

    for aPrice in soup.find_all('span', attrs={'class': 'price-section__absolute-value'}):
        print(str(aPrice.text).strip())
        absolutePrice = str(aPrice.text).strip()

    for rValue in soup.find_all('span', attrs={'class': 'price-section__relative-value'}):
        print(str(rValue.text).strip())
        relativeValue = str(rValue.text).strip()

    trackedStockDict = {
        'shortName': currentInput,
        'companyName': companyName,
        'currentPrice': currentPrice,
        'absolutePrice': absolutePrice,
        'relativeValue': relativeValue
    }

    trackedStockList.append(trackedStockDict)

    updatedJsonData = []

    if not os.path.exists('stocks.json'):
        with open('stocks.json', 'w+') as json_file:
            json.dump(trackedStockList, json_file)
    else:
        with open('stocks.json', 'r') as json_file:
            jsonData = json.load(json_file)
            with open('stocks.json', 'w+') as json_file2:
                updatedJsonData.append(trackedStockList[0])
                for i in range(len(jsonData)):
                    #newData = [x for x in trackedStockList[0]['companyName'] if x not in jsonData[i]['companyName']]
                    if trackedStockList[0]['companyName'] not in jsonData[i]['companyName']:
                        
                        jsonShortName = jsonData[i]['shortName']
                        jsonCompanyName = jsonData[i]['companyName']

                        fromJsonUrl = 'https://markets.businessinsider.com/stocks/' + jsonShortName + '-stock'
                        r = requests.get(fromJsonUrl)
                        soup = BeautifulSoup(r.text, 'lxml')

                        for cPrice in soup.find_all('span', attrs={'class': 'price-section__current-value'}):
                            currentPriceJson = str(cPrice.text).strip()

                        for aPrice in soup.find_all('span', attrs={'class': 'price-section__absolute-value'}):
                            absolutePriceJson = str(aPrice.text).strip()

                        for rValue in soup.find_all('span', attrs={'class': 'price-section__relative-value'}):
                            relativeValueJson = str(rValue.text).strip()

                        updatedJsonDict = {
                            'shortName': jsonShortName,
                            'companyName': jsonCompanyName,
                            'currentPrice': currentPriceJson,
                            'absolutePrice': absolutePriceJson,
                            'relativeValue': relativeValueJson
                        }
                        if updatedJsonDict not in updatedJsonData:
                            updatedJsonData.append(updatedJsonDict)
                        
                    else:
                        jsonShortName = jsonData[i]['shortName']
                        jsonCompanyName = jsonData[i]['companyName']

                        fromJsonUrl = 'https://markets.businessinsider.com/stocks/' + jsonShortName + '-stock'
                        r = requests.get(fromJsonUrl)
                        soup = BeautifulSoup(r.text, 'lxml')

                        for cPrice in soup.find_all('span', attrs={'class': 'price-section__current-value'}):
                            currentPriceJson = str(cPrice.text).strip()

                        for aPrice in soup.find_all('span', attrs={'class': 'price-section__absolute-value'}):
                            absolutePriceJson = str(aPrice.text).strip()

                        for rValue in soup.find_all('span', attrs={'class': 'price-section__relative-value'}):
                            relativeValueJson = str(rValue.text).strip()

                        updatedJsonDict = {
                            'shortName': jsonShortName,
                            'companyName': jsonCompanyName,
                            'currentPrice': currentPriceJson,
                            'absolutePrice': absolutePriceJson,
                            'relativeValue': relativeValueJson
                        }
                        if updatedJsonDict not in updatedJsonData:
                            updatedJsonData.append(updatedJsonDict)
                json.dump(updatedJsonData, json_file2)

MY_ADDRESS = ''
PASSWORD = ''
 
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, 'r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails
 
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def stocksEmail():
    if not os.path.exists('stocks.json'):
        print('there is no data to update contacts with, please enter some data first by pressing 1 on first question')
    else: 
        newData = []
        with open('stocks.json', 'r') as json_file:
            jsonData = json.load(json_file)
            for i in range(len(jsonData)):
                jsonShortName = jsonData[i]['shortName']
                jsonCompanyName = jsonData[i]['companyName']

                fromJsonUrl = 'https://markets.businessinsider.com/stocks/' + jsonShortName + '-stock'
                r = requests.get(fromJsonUrl)
                soup = BeautifulSoup(r.text, 'lxml')

                for cPrice in soup.find_all('span', attrs={'class': 'price-section__current-value'}):
                    currentPriceJson = str(cPrice.text).strip()

                for aPrice in soup.find_all('span', attrs={'class': 'price-section__absolute-value'}):
                    absolutePriceJson = str(aPrice.text).strip()

                for rValue in soup.find_all('span', attrs={'class': 'price-section__relative-value'}):
                    relativeValueJson = str(rValue.text).strip()

                updatedJsonDict = {
                    'shortName': jsonShortName,
                    'companyName': jsonCompanyName,
                    'currentPrice': currentPriceJson,
                    'absolutePrice': absolutePriceJson,
                    'relativeValue': relativeValueJson
                }
                if updatedJsonDict not in newData:
                    newData.append(updatedJsonDict)
            prevChangedData = [x for x in newData if x not in jsonData]
            messageData = []
            if len(prevChangedData) != 0:
                for j in range(len(prevChangedData)):
                    coName = prevChangedData[j]['companyName']
                    reVal = prevChangedData[j]['relativeValue']
                    if prevChangedData[j]['relativeValue'][0] == '-':
                        anString = '%s stock just decreased its relative value by %s' % (coName, reVal)
                    elif prevChangedData[j]['relativeValue'][0] == '+':
                        anString = '%s stock just increased its relative value by %s' % (coName, reVal)
                    """ messageDict = {
                        'companyName': prevChangedData[j]['companyName'],
                        'relativeValue': prevChangedData[j]['relativeValue'],
                        '+Or-': if prevChangedData[j]['relativeValue'][0] == '-' 'negatively' else 'positively'
                    } """
                    messageData.append(anString)

                names, emails = get_contacts('contacts.txt') # read contacts
                message_template = read_template('stocksMail.txt')

                s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
                s.starttls()
                s.login(MY_ADDRESS, PASSWORD)

                for name, email in zip(names, emails):
                    msg = MIMEMultipart()       # create a message

                    # add in the actual person name to the message template
                    message = message_template.substitute(PERSON_NAME=name.title(), STOCK_UPDATE = messageData)

                    # setup the parameters of the message
                    msg['From']=MY_ADDRESS
                    msg['To']=email
                    msg['Subject']="Stock updates!!"

                    # add in the message body
                    msg.attach(MIMEText(message, 'plain'))

                    # send the message via the server set up earlier.
                    s.send_message(msg)
                    
                    del msg
                s.quit()




dataOrEmail = input('Add stocks data or send updates via email? Press "1" to add data or "2" to track the added data and send updates via email: ')
if dataOrEmail == '1':
    market = input('Type in a market (aapl, etc): ')
    page_url = 'https://markets.businessinsider.com/stocks/' + market + '-stock'
    req = requests.get(page_url)
    if req.status_code == 200:
        try:
            addStocks(market)
        except KeyboardInterrupt:
            print('process ended')
    else: 
        print('Market not found, try again')
elif dataOrEmail == '2':
    try: 
        while True:
            stocksEmail()
    except KeyboardInterrupt:
        print('process ended')
