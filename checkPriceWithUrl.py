import requests
from bs4 import BeautifulSoup
import smtplib
import tkinter as tk

possible_price_ids = ['priceblock_ourprice', 'priceblock_saleprice', 'a-color-price']

#sample urls:
#https://www.amazon.in/FreShineBlind-Sleeping-Cotton-Smooth-Travel/dp/B084V1PZ19/ref=sr_1_1_sspa?crid=3V7CE7P6N5U8Y&dchild=1&keywords=eye+cover+for+sleep&qid=1601649636&sprefix=eye+cover+%2Cstripbooks%2C441&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyRkZIU0xXS09QMU4zJmVuY3J5cHRlZElkPUEwOTAwNDUyS0hMOVBaSEg3WVVFJmVuY3J5cHRlZEFkSWQ9QTA1NTY3ODAxNzBXQlQzV01SV1U4JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==

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


def geturl():
    master = tk.Tk()
    tk.Label(master,
             text="Enter Url of the product").grid(row=0,
                                                   padx=20,
                                                   pady=5)

    e1 = tk.Entry(master)

    e1.grid(row=0, column=1)

    values = []

    def cont():
        url = e1.get()

        master.destroy()

        values.append(url)

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


def check_price(page_url):

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'};

    fields = ['url', 'price']

    page_data = requests.get(page_url, headers=headers);

    soup = BeautifulSoup(page_data.content, 'html.parser')

    prod_name = soup.find(id='productTitle').text.strip()

    for ids in possible_price_ids:
        prod_price = soup.find(id=ids)
        if type(prod_price) != type(None):
            prod_price = prod_price.text.replace(',', '')
            break
        elif ids == possible_price_ids[-1]:
            prod_price = '$-1'

    current_price = int(eval(prod_price[1:].strip()))

    print('Price : ' + str(current_price))

    sendMail(current_price, prod_name, page_url)


def sendMail(current_price, prod_name, url):

    email, password, receiverEmail = getEmailDetails()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, password)

    subject = "The price of your product"
    body = 'The price for the item : {} has been checked. The current prices is {}. Check it here : {}'.format(
        prod_name, current_price, url)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        email,
        receiverEmail,
        msg.encode('utf-8')
    )

    print("Email has been sent.")

    server.quit()


page_url = geturl()

check_price(page_url[0])
