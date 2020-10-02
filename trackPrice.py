import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import tkinter as tk

possible_price_ids = ['priceblock_ourprice', 'priceblock_saleprice','a-color-price']


def getEmailDetails():

    master = tk.Tk()
    tk.Label(master,
             text="Your email").grid(row=0,
                              padx=20,
                              pady=5)
    tk.Label(master,
             text="Password").grid(row=1,
                                   padx=20,
                                   pady=5)
    tk.Label(master,
             text="Receiver's Email").grid(row=2,
                                   padx=20,
                                   pady=5)

    e1 = tk.Entry(master)
    e2 = tk.Entry(master)
    e3 = tk.Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    values = []

    def cont():
        senderEmail = e1.get()
        password = e2.get()
        receiverEmail = e3.get()

        master.destroy()

        values.append(senderEmail)
        values.append(password)
        values.append(receiverEmail)

    tk.Button(master,
              text='Ok', command=cont).grid(row=3,
                                            column=0,
                                            sticky=tk.W,
                                            pady=5,
                                            padx=20)
    tk.Button(master,
              text='Cancel', command=master.quit).grid(row=3,
                                                       column=1,
                                                       sticky=tk.W,
                                                       pady=5,
                                                       padx=20)

    tk.mainloop()

    return values

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
            print('Price : ' + str(converted_price))
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

    email, password, receiverEmail = getEmailDetails()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, password)

    subject = "The price has been changed!!!"
    deviation = current_price - prev_price; 
    body = 'The price for the item : {} has been changed. It went from {} to {}. The deviation is {} \n Check it here : {}'.format(prod_name, prev_price, current_price, deviation, url)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        email,
        receiverEmail,
        msg.encode('utf-8')
    )

    print("Email has been sent.")

    server.quit()


check_price()
