import pytesseract
from PIL import Image
import requests
import urllib.request
import urllib.request
from bs4 import BeautifulSoup
CLIENT_ID=''
CLIENT_SECRET=''
new_text = ""
def jpgtotxt(path):
    img = Image.open(path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, lang='kor', config=custom_config)    
    new = []
    new_text = ''
    lines = text.split('\n')
    for i in lines:                                                     
        if ' ' != i and '' != i:
            new.append(i)
    for k in new:
        new_text = new_text + k + '\n'
    #print(new_text)
    return new_text

krlink = input("linkを入力 : ")
start = int(input("開始話数 : "))
end = int(input("終了話数 : "))
target = '&'
idx = krlink.find(target)
r = krlink[:idx]
while end + 1 > start:
    a = r.replace("list","detail")
    url = a + "&no=" + str(startno)
    print(url)
    start = start + 1
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    keys = soup.find_all("img", alt="comic content")
    encText = ""
    for div in keys:
        links = div.get("src")
        print(links)
        headers_dic = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        re = requests.get(links, headers=headers_dic)
        with open(r"image.jpg", mode='wb') as fw:
            fw.write(re.content)
        txt = jpgtotxt(r"image.jpg")
        encText = encText + urllib.parse.quote(txt)
        print(encText.encode("utf-8"))
        data = "source=ko&target=ja&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",CLIENT_ID)
        request.add_header("X-Naver-Client-Secret",CLIENT_SECRET)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            text = response_body.decode('utf-8')
            target = '"translatedText":"'
            idx = text.find(target)
            r = text[idx + len(target):]
            target = '"'
            idx = r.find(target)
            g = r[:idx]
            print(g)
        else:
            print("Error Code:" + rescode)
