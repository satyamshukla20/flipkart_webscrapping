import json
import requests
from bs4 import BeautifulSoup
import boto3

def get_title(soup):
    try:
        title=soup.find("span",attrs={"class":'B_NuCI'})
        title_value=title.text
        title_string=title_value.strip()
        title_string=title_string.replace(",", " ")
    except AttributeError:
        title_string=""
    return title_string
    

def get_price(soup):

    try:
        price = soup.find("div", attrs={'class':'_30jeq3 _16Jk6d'}).text.strip()[1:]
        price = price.replace(",", "")
    except AttributeError:
        price = ""
    return price

def get_orignal_price(soup:BeautifulSoup):
    try:
        _price = soup.find("div", attrs={'class':'_3I9_wc _2p6lqe'}).text.strip()[1:]
        _price = _price.replace(",", "")
    except AttributeError:
        _price=""
    return _price

def get_rating(soup):

    try:
        rating = soup.find("div", attrs={'class':'_3LWZlK'}).text.strip()
    
    except AttributeError:
        rating = ""	

    return rating

def get_review_count(soup):
    try:
        review_count=soup.select_one("span._2_R_DZ > span > span:nth-child(3)").text.strip().split()[0]
        review_count = review_count.replace(",", "")
    except AttributeError:
        review_count = ""	

    return review_count
    
def get_camera(soup):
    try:
        camera = soup.select_one("div._2LE14f > div > a:nth-child(1) > div > div._2aWUii > svg > text").text.strip()
    except AttributeError:
        camera = ""	

    return camera
    
def get_battery(soup):
    try:
        battery = soup.select_one("div._2LE14f > div > a:nth-child(2) > div > div._2aWUii > svg > text").text.strip()
    except AttributeError:
        battery = ""	

    return battery

def get_display(soup):
    try:
        display = soup.select_one("div._2LE14f > div > a:nth-child(3) > div > div._2aWUii > svg > text").text.strip()
    except AttributeError:
        display = ""	

    return display
    
def get_design(soup):
    try:
        design = soup.select_one("div._2LE14f > div > a:nth-child(4) > div > div._2aWUii > svg > text").text.strip()
    except AttributeError:
        design = ""	

    return design


def lambda_handler(event, context):
    URL="https://www.flipkart.com/search?q=smartphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    webpage=requests.get(URL)
    soup = BeautifulSoup(webpage.content,'html.parser')
    links=soup.find_all("a",attrs={'class':'_1fQZEK'})
    
    links_list=[]
    for link in links:
        links_list.append(link.get('href'))

    lst  = []
    lst.append("name,price,original_price,rating,reviews,camera,battery,display,design")
    
    for link in links_list:
        new_webpage=requests.get("https://www.flipkart.com"+link)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        title = get_title(new_soup)
        if title == "":
            continue
        price=get_price(new_soup)
        original_price=get_orignal_price(new_soup)
        rating=get_rating(new_soup)
        reviews=get_review_count(new_soup)
        camera=get_camera(new_soup)
        battery=get_battery(new_soup)
        display=get_display(new_soup)
        design=get_design(new_soup)
        lst.append(title+","+price+","+original_price+","+rating+","+reviews+","+camera+","+battery+","+display+","+design)
        

    s3 = boto3.client('s3')
    file_name = 'flipkart_smartphone_data.csv'
    bucket_name = 'flipkartsmartphonebucket'
    
    
    data_fin='\n'.join(lst)
    s3.put_object(
        Body=data_fin,
        Bucket=bucket_name,
        Key=file_name
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    

