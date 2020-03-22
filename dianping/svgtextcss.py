"""
   大众点评网的图文混排css
"""
import requests
import re
import time
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import json

from fontTools.ttx import TTFont
from aip import AipOcr

APP_ID = '16439681'
API_KEY = '4UsK5tTCwvsgwOKaPVaKBAC4'
SECRET_KEY = 'Oq99Gql84P8zAPhGnShAF9yPY7qLwWuU'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

fontDict = {}


def findCss(html):
    cssUrl = re.search(r'href="(//s3plus\.meituan\.net/.*?\.css)"', html)
    if cssUrl:
        url = cssUrl.group(1)
        if not url.startswith("https"):
            url = "https:" + url
        return url


def fontConvert(fontFile, fontFamily):
    font = TTFont(fontFile)
    drFont = ImageFont.truetype(fontFile, 60)
    codeList = font.getGlyphOrder()[2:]
    result_dict = {}
    for code in codeList:
        im = Image.new("RGB", (80, 80), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        text = code.replace("uni", "\\u")
        text = text.encode('utf-8').decode('unicode_escape')
        dr.text((10, 10), text, font=drFont, fill="#000000")
        bf = BytesIO()
        im.save(bf, "png")
        im.save("s1.jpg", "png")
        result = client.basicGeneral(bf.getvalue())
        print(code, result)
        result_dict[code] = result
        time.sleep(0.5)

    with open(f"{fontFamily}.json", "w") as f:
        json.dump(result_dict, f)


def downloadCss(url):
    req = requests.get(url)
    html = req.text
    strList = html.split("@font-face")
    for s in strList:
        if s == "":
            continue
        s = s.replace(" ", "")
        fontFamily = re.search(r'font-family:"(.*?)";', s).group(1)
        fontUrl = re.search(r'format\("embedded-opentype"\),url\("(.*?)"\);}', s).group(1)
        if not fontUrl.startswith("https"):
            fontUrl = "https:" + fontUrl
        fontReq = requests.get(fontUrl)
        with open(f"{fontFamily}.woff", "wb") as f:
            f.write(fontReq.content)


def analysis(fontFamily, code):
    if fontDict.get(fontFamily, {}).get(code):
        return fontDict.get(fontFamily, {}).get(code)
    else:
        fontFile = f"{fontFamily}.woff"
        font = TTFont(fontFile)
        drFont = ImageFont.truetype(fontFile, 60)
        print(type(font.get()))


if __name__ == "__main__":
    keyword = "医疗美容"
    url = "http://www.dianping.com/search/keyword/1/0_{}/p{}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Cookie": "lxsdk_cuid=169d23412f4c8-01e4f18c813a24-12306d51-1aeaa0-169d23412f4c8; _lxsdk=169d23412f4c8-01e4f18c813a24-12306d51-1aeaa0-169d23412f4c8; _hc.v=9bba824a-a9a4-a138-1ed5-1e7f751dea22.1554009822; s_ViewType=10; ua=%E5%B0%8F%E7%A5%9E%E5%90%8C%E5%AD%A6; ctu=a8178f513639cf7d1221f37980f0c301c60f7e1854f33498c47ca710db510f9d; cy=1; cye=shanghai; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; dplet=1c5fb94b1bcb4eff1cd9607b73078399; dper=d1341f45003199e534f9e7267d5e83c6356e56d56f548b56813bb4f5eed1a7b696c7a286338e0a7b3d90392d7e1b17fdd3181ab9abe384e8922c134157883aef25531e97029dd5a0efb461f778d0972409314d8c05cb87a7810515f46a32520d; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=170ffed1f1e-ae4-7fd-a41%7C%7C79"
    }
    response = requests.get(url.format(keyword, 1), headers=headers)
    html = response.text
    # url = findCss(html)
    # downloadCss(url)
    analysis("PingFangSC-Regular-address", "aa")
