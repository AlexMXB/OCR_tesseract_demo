from PIL import Image,ImageFilter,ImageOps
from urllib import urlopen,urlretrieve
import subprocess
from bs4 import BeautifulSoup
import requests

def cleanImage(imagepath):
    image = Image.open(imagepath)
    image = image.point(lambda x: 0 if x<143 else 255 )
    borderImage = ImageOps.expand(image,border=20,fill = 'white')
    borderImage.save(imagepath)

html = urlopen("http://pythonscraping.com/humans-only")
bsObj = BeautifulSoup(html)
imagelocation = bsObj.find("img",{"title":"Image CAPTCHA"})["src"]
print(imagelocation)
formbuildID = bsObj.find("input",{"name":"form_build_id"})["value"]
print(formbuildID)
captchaSID = bsObj.find("input",{"name":"captcha_sid"})["value"]
print(captchaSID)
captchaToken = bsObj.find("input",{"name":"captcha_token"})["value"]
print(captchaToken)
captchaUrl = "http://pythonscraping.com"+imagelocation
urlretrieve(captchaUrl,"captcha.jpg")
cleanImage("captcha.jpg")

p = subprocess.Popen(["tesseract","captcha.jpg","captcha"],stdout= subprocess.PIPE,stderr=subprocess.PIPE)
p.wait()
f = open("captcha.txt","r")
print("flag")
captchaResponse = f.read().replace(" ","").replace("\n","")

print(captchaResponse)

if len(captchaResponse) == 5:#test case
    params = {"captcha_token":captchaToken, "captcha_sid":captchaSID,
              "form_id":"comment_node_page_form","form_build_id":formbuildID,
              "captcha_response":captchaResponse,"name":"Ryan Mitchell",
              "subject":"I come to seek the Grail",
              "comment_body[und][0][value]":
                                        "...and I am definitely not a bot"}
    r =requests.post("http://www.pythonscraping.com/comment/reply/10",data=params)

    responseObj = BeautifulSoup(r.text)
    if responseObj.find("div",{"class":"messages"}) is not None:
        print(responseObj.find("div",{"class":"messages"}).get_text())

else:
    print("error reading captcha")

