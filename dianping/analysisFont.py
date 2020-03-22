from aip import AipOcr
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont  # 绘制图片
import numpy

APP_ID = '16439681'
API_KEY = '4UsK5tTCwvsgwOKaPVaKBAC4'
SECRET_KEY = 'Oq99Gql84P8zAPhGnShAF9yPY7qLwWuU'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
fontPath = 'PingFangSC-Regular-address.woff'  # woff文件路径
WordList = []


"""解析woff文件"""
def fontConvert(fontPath):
    font = TTFont(fontPath)  # 打开文件
    codeList = font.getGlyphOrder()[2:]
    im = Image.new("RGB", (1800, 1000), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(fontPath, 40)
    count = 15
    arrayList = numpy.array_split(codeList, count)  # 将列表切分成15份，以便于在图片上分行显示
    for t in range(count):
        newList = [i.replace("uni", "\\u") for i in arrayList[t]]
        text = "".join(newList)
        text = text.encode('utf-8').decode('unicode_escape')
        dr.text((0, 50 * t), text, font=font, fill="#000000")
    im.save("s1.jpg")
    Image.open("s1.jpg")  # 将图片保存到本地

    with open('s1.jpg', 'rb') as fp:  # 读取图片
        image = fp.read()

    result = client.basicGeneral(image)  # 调用百度AI进行文字识别
    print('result:', result)
    words_list = result["words_result"]
    for w in words_list:  # 对words进行处理
        w_list = list(w["words"])
        for i in w_list:
            WordList.append(i)
    print('WordList:', WordList)
    Save_Chinese("".join(WordList))  # 汉字保存至txt文件


"""汉字保存为txt文件方便调用"""
def Save_Chinese(word):
    with open('word.txt', 'w') as f:
        f.write(word)


if __name__ == "__main__":
    # 先把woff文件里的汉字转为图片，再利用百度AI获取图片上的文字
    fontConvert(fontPath)