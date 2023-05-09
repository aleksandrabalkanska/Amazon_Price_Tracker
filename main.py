from unidecode import unidecode
from bs4 import BeautifulSoup
import requests
import smtplib
import os

PRODUCT_URL = input("Enter the URL of the Amazon product you want to track: ")
MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("AMAZON_PRICE_PASSWORD")

# Get the Amazon Price
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Accept-Language": "en-US,en;q=0.5",
}

response = requests.get(url=PRODUCT_URL, headers=headers)
product_webpage = response.text
soup = BeautifulSoup(product_webpage, "html.parser")

product_name = unidecode(soup.find(name="span", id="productTitle").getText().strip())
product_price = float(soup.find(name="span", class_="a-offscreen").getText().strip("$").replace(',', ''))

goal_price = float(input(f"{product_name.title()} current price is ${product_price}."
                   f"\nEnter the price below which the alert should be sent: $"))

email_content = f"The price of {product_name} is now ${product_price}! Buy now at {PRODUCT_URL}"

# Send Email

if product_price <= goal_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Amazon Price Alert!\n\n{email_content}"
        )
