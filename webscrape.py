# https://www.newegg.com/Server-Memory/SubCategory/ID-541?cm_sp=CAT_Memory_3-_-VisNav-_-Server-Memory --> URL of the page being scraped 

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 

my_url = 'https://www.newegg.com/Server-Memory/SubCategory/ID-541?cm_sp=CAT_Memory_3-_-VisNav-_-Server-Memory'

# Opening up connection, grabbing page

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# Parsing the web data

page_soup = soup(page_html, 'html.parser')

# Grabs each product
containers = page_soup.findAll("div", {"class":"item-container"})

# Creates products.csv with header categories

filename = "products.csv"
f = open(filename, "w")

headers = "Brand, Product_Name, Shipping, Price\n"
f.write(headers)

# Grabbing the Brand Name, Product Name, Shipping Price, & Current Listed Price of Product and writes into a .csv file

for container in containers:
	try:
		brand = container.div.div.a.img["title"]
		print("\nBrand: " + brand)
	except (AttributeError, TypeError) as e:
		print("No Brand Name")
		brand = ''

	try:
		title_cotainer = container.findAll("a", {"class": "item-title"})
		product_name = title_cotainer[0].text
		print("Product Name: " + product_name)
	except (AttributeError, TypeError) as e:
		print("No Product Name")
		product_name = ''

	try:
		shipping_container = container.findAll("li",{"class": "price-ship"})
		shipping_price = shipping_container[0].text.strip()
		print("Shipping : " + shipping_price)
	except (AttributeError, TypeError) as e:
		print("No Shipping Found")
		shipping_price = ''

	try:
		price_container = container.findAll("li",{"class": "price-current"})
		price_current_dollar = price_container[0].strong.text.strip()
		price_current_cent = price_container[0].sup.text.strip()
		price_current = price_current_dollar + price_current_cent
		print("Current Price: $" + price_current)
	except (AttributeError, TypeError) as e:
		print("No Price Found")
		price_current = ''

	print("\n")

	f.write(brand + "," + product_name.replace(",", "|") + "," + shipping_price + price_current + "\n")

f.close()