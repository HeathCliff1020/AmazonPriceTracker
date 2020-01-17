import requests
from bs4 import BeautifulSoup
import smtplib
import json
import csv


possible_price_ids = ['priceblock_ourprice', 'priceblock_saleprice']


def check_price():

    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'};

    fields = ['url', 'price']
       
    data = csv.DictReader( open('urls.csv', 'r') )

    with open('temp.csv', 'w') as file:

        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
    
        for line in data :
            
            prev_price = int(eval(line['price'].strip()))
            page_url = line['url']
                
            page_data = requests.get(page_url, headers = headers);

            soup = BeautifulSoup(page_data.content,'html.parser')

            prod_name = soup.find(id='productTitle').text.strip()

            for ids in possible_price_ids:
                prod_price = soup.find(id=ids)
                if type(prod_price) != type(None):
                    prod_price = prod_price.text.replace(',', '')
                    break
                elif ids == possible_price_ids[-1]:
                    prod_price = '$-1'
                    

            converted_price = int(eval(prod_price[1:].strip()))
            
            #print('Product : ' + prod_name)
            #print('Price : ' + prod_price)
            #print()
                  
            if (converted_price != prev_price):
                line['price'] = str(converted_price)
                sendMail(prev_price,converted_price, prod_name, page_url)

            writer.writerow({'url': line['url'], 'price': line['price']})

    with open("temp.csv") as f:
        with open("urls.csv", "w") as f1:
            for line in f:
                f1.write(line)

    
def sendMail(prev_price, current_price, prod_name, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('mukeshbisht1020@gmail.com', 'xvzomrfgidvwxxto')

    subject = "The price has been changed!!!"
    deviation = current_price - prev_price; 
    body = 'The price for the item : {} has been changed. It went from {} to {}. The deviation is {} \n Check it here : {}'.format(prod_name, prev_price, current_price, deviation, url)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'mukeshbisht1020@gmail.com',
        'heathcliff1020@gmail.com',
         msg.encode('utf-8')
        )

    print("Email has been sent.")

    server.quit()


check_price()
