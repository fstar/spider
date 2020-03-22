import requests
from lxml import etree
import time
from tools import saveData
from PIL import Image, ImageFont


class Data:
    dataId = None
    name = None
    url = None
    address = None
    avgPrice = None


def getMaxPage(html):
    t = etree.HTML(html)
    pageText = t.xpath("/html/body/div[@class='section Fix J-shop-search']/div[@class='content-wrap']/div[@class='shop-wrap']/div[@class='page']/a/text()")
    maxPage = 0
    for i in pageText:
        try:
            if int(i) > maxPage:
                maxPage = int(i)
        except Exception:
            continue
    return maxPage


def getAttr(t, xpath):
    attr = t.xpath(xpath)
    if len(attr) > 0:
        if "http://www.dianping.com/business" in attr:
            attr.remove("http://www.dianping.com/business")
        if "" in attr:
            attr.remove("")
        if None in attr:
            attr.remove(None)
        attr = ";".join(attr)
        return attr


def analysis(html):
    t = etree.HTML(html)
    result = []
    liList = t.xpath('//div[@id="shop-all-list"]/ul/li')
    for li in liList:
        data = Data()
        data.dataId = li.xpath(".//div[@class='tit']/a/@data-shopid")[-1]
        data.name = getAttr(li, ".//div[@class='tit']/a/@title")
        data.url = getAttr(li, ".//div[@class='tit']/a/@href")
        data.address = getAttr(li, ".//span[@class='addr']//text()")
        data.avgPrice = getAttr(li, ".//div[@class='comment']/a[@class='mean-price']/b/text()")
        print(data.name)
        result.append(data.__dict__)
    return result


def main():
    keyword = "医疗美容"
    url = "http://www.dianping.com/search/keyword/1/0_{}/p{}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Cookie": "lxsdk_cuid=169d23412f4c8-01e4f18c813a24-12306d51-1aeaa0-169d23412f4c8; _lxsdk=169d23412f4c8-01e4f18c813a24-12306d51-1aeaa0-169d23412f4c8; _hc.v=9bba824a-a9a4-a138-1ed5-1e7f751dea22.1554009822; s_ViewType=10; ua=%E5%B0%8F%E7%A5%9E%E5%90%8C%E5%AD%A6; ctu=a8178f513639cf7d1221f37980f0c301c60f7e1854f33498c47ca710db510f9d; cy=1; cye=shanghai; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; dplet=1c5fb94b1bcb4eff1cd9607b73078399; dper=d1341f45003199e534f9e7267d5e83c6356e56d56f548b56813bb4f5eed1a7b696c7a286338e0a7b3d90392d7e1b17fdd3181ab9abe384e8922c134157883aef25531e97029dd5a0efb461f778d0972409314d8c05cb87a7810515f46a32520d; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=170ffed1f1e-ae4-7fd-a41%7C%7C79"
    }
    response = requests.get(url.format(keyword, 1), headers=headers)
    html = response.text
    maxPage = getMaxPage(html)
    result = []
    for i in range(1, maxPage):
        response = requests.get(url.format(keyword, i), headers=headers)
        html = response.text
        result.extend(analysis(html))
        time.sleep(1)
    saveData.save(result, f"../result/dianping_{int(time.time())}.xlsx", keyword)


if __name__ == "__main__":
    main()