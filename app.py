from flask import Flask
from selenium import webdriver
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

def flipkart():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER PATH"),chrome_options=chrome_options)


    search="watch"
    # Open the desired webpage
    driver.get(f"https://www.flipkart.com/search?q={search}")

    # Extract the HTML content of the webpage
    html_content = driver.page_source

    with open('flipkart_product_html.html', 'w', encoding='utf-8') as file:
                file.write(html_content)

    encoded_content = html_content.encode('unicode_escape').decode('utf-8')

    # Print the encoded content
    soup = BeautifulSoup(encoded_content,'html.parser')

    cards = soup.find_all('div',{'class':'_13oc-S'})

    data=[]
    json_data = {}
    json_data['status']='error'
    json_data['data'] = data

    for card in cards:
        name = card.find('div',{'class':'_4rR01T'}) 
        if name:                 #vertical cards
            json_data['status']='success'
            dic = {}
            name=name.get_text()
            price = card.find('div',{'class':"_30jeq3 _1_WHN1"})
            if price:
                price_text=price.get_text()
                price = price_text.split( r'\u20b9')[1]

            list_elements = card.find_all('li', class_='rgWa7D')
            if list_elements:
                list_texts = [element.get_text(strip=True) for element in list_elements]

            link = card.find('a', class_='_1fQZEK')
            if link:
                link = link.get('href')

            image = card.find('img', class_='_396cs4')
            if image:
                image=image.get('src')

            dic["Product_Name"] = name
            dic["Product_Description"]=list_texts
            dic["Product_Price"]=price
            dic["Product_link"]="https://www.flipkart.com"+link
            dic["Product_Image"]=image
            data.append(dic)

            

        else:                                          #horizontal cards
            card_units = card.find_all('div',{'class':'_1xHGtK _373qXS'})
            for card in card_units:
                    json_data['status']='success'
                    dic = {}
                    heading = card.find('div',{'class':'_2WkVRV'})
                    if heading:
                        heading=heading.get_text()
                    else:
                        heading=''

                    prod_name = card.find('a',{'class':'IRpwTa'})
                    if prod_name:
                        prod_name=prod_name.get('title')
                    else:
                        prod_name=''

                    name = heading+ "- "+prod_name
                    
                    list_texts =[]

                    price = card.find('div',{'class':'_30jeq3'})
                    if price:
                        price=price.get_text()
                        price = price.split( r'\u20b9')[1]

                    link = card.find('a',{'class':'_2UzuFa'})
                    if link:
                        link=link.get('href')

                    image= card.find('img',{'class':'_2r_T1I'})
                    if image:
                        image=image.get('src')
                    
                    dic["Product_Name"] = name
                    dic["Product_Description"]=list_texts
                    dic["Product_Price"]=price
                    dic["Product_link"]="https://www.flipkart.com"+link
                    dic["Product_Image"]=image
                    # print(f"Product_Name: {name}")
                    # print(f"Product_Description: {list_texts}")
                    # print(f"Product_Price: {price}")
                    # print("Product_link:","https://www.flipkart.com"+link)
                    # print("Product_Image:",image)
                    # print()
                    data.append(dic)


    json_data = json.dumps(json_data)
    return json_data

@app.route("/")
def hello_world():
    result = flipkart()
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
