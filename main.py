import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
import os

smtp_server = "smtp.mail.yahoo.com"
password = os.environ.get("password")
sender = os.environ.get("sender")

url = "https://www.amazon.com/Duo-Evo-Plus-esterilizadora-vaporizador/dp/B07W55DDFB/ref=sr_1_4?qid=1597660904"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")

price = soup.select_one(selector=".a-size-base.a-color-price").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)

MAX_PRICE = 170
if price_as_float < MAX_PRICE:
    product_title = soup.select_one(selector="#productTitle").getText()
    message = f"Subject:Amazon Price Alert\n\n{product_title.strip()} " \
              f"is now ${price_as_float}\n{url}".encode("utf8")
    with smtplib.SMTP(smtp_server) as connection:
        connection.starttls()
        connection.login(user=sender, password=password)
        connection.sendmail(from_addr=sender, to_addrs=sender, msg=message)
