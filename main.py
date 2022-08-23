import requests
from bs4 import BeautifulSoup
import json

url ="https://store.steampowered.com/search/?category1=998&specials=1&filter=topsellers?query&start=0&count={}&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1%27"
def steamPage(url):
    response=requests.get(url)
    data=dict(response.json())
    return data["results_html"]
def api(sourceCode,array):
    soup=BeautifulSoup(sourceCode,"html.parser")
    links= soup.find_all("a")
    for i in links: 
        title=i.find("span",{"class":"title"}).text.strip()
        price=i.find("div",{"class":"search_price"}).text.strip().split("TL")[1]+"TL"
        para = i.find("div",{"class":"col search_price_discount_combined responsive_secondrow"})
        discount =para.span.text
        oldPrice=para.strike.text.strip()
        liste={"title":title,"oldPrice":oldPrice,"discount":discount,"price":price}
        array.append(liste)
def repeter():
    array1=[]
    for i in range(0,150,50):
        sourceCode=steamPage(url=url.format(i))
        api(sourceCode=sourceCode,array=array1)
    lastApi={"steamDiscounts":array1}
    f=open("steamapi.json","w")
    json_obj=lastApi
    sorted_obj = dict(json_obj) 
    sorted_obj['steamDiscounts'] = sorted(json_obj['steamDiscounts'], key=lambda x : x['discount'], reverse=True)
    json.dump(sorted_obj,f,indent=2)
    
repeter()