# -*- coding: utf-8 -*-

import requests
import re
import base64
from lxml import etree
from fontTools.ttLib import TTFont
from io import BytesIO


data_map = {(0, 1549): 'B', (1588, 0): '男', (868, 0): '王', (825, 367): '大', (265, -118): '专', (0, 1026): 'M', (-110, -150): '女', (1460, 0): '吴', (230, 390): '硕', (156, 262): '赵', (660, 0): '黄', (924, 0): '李', (0, 1325): '1', (0, 134): '8', (0, 144): '经', (0, 125): '2', (1944, 0): '下', (-52, -52): '本', (582, 0): '届', (0, -227): '5', (146, 78): '应', (228, 306): '科', (-244, -426): '7', (770, 0): '中', (928, 0): '生', (-121, 62): '6', (-833, 0): 'E', (299, 0): '陈', (159, -123): '3', (164, 0): '以', (-764, 0): '杨', (-221, 0): 'A', (238, 0): '张', (0, -1023): '4', (784, 0): '无', (0, 410): '0', (128, -74): '9', (-46, -550): '验', (0, 110): '博', (0, 132): '技', (746, 0): '士', (210, 358): '校', (1298, 0): '高', (-74, -366): '刘', (0, -508): '周'}


def hex2word(font_map, t):
    temp_list = []
    for i in t:
        if i in font_map:
            temp_list.append(font_map[i])
        else:
            temp_list.append(i)
    return "".join(temp_list)


def get_font_map(content):
    """
    根据相应内容 得到当前的字体映射关系
    :param content:
    :return:
    """
    font_map = {}
    result = re.search(r"base64,(.*?)\)", content, flags=re.S).group(1)
    b = base64.b64decode(result)
    tf = TTFont(BytesIO(b))
    for index, i in enumerate(tf.getGlyphNames()[1:-1]):
        temp = tf["glyf"][i].coordinates
        x1, y1 = temp[0]
        x2, y2 = temp[1]
        new = (x2-x1, y2-y1)
        key = i.replace("uni", r"\u").lower()
        key = key.encode('utf-8').decode('unicode_escape')
        font_map[key] = data_map[new]
    return font_map


def parse_zt():
    """
    请求网页获取字体
    :return:
    """
    url = "https://jianli.58.com/resumedetail/singles/3_neyQnErXnGdvTGtfTGnvlEt5_ErQ_ErNnGZfnEdQlEmN_eO5nEdslETknemsMGya_75fTvZYnhsunErsnEIkneZX_eO*?psid=110727694205091200207377067&entinfo=3_neyQnErXnGdvTGtfTGnvlEt5_ErQ_ErNnGZfnEdQlEmN_eO5nEdslETknemsMGya_75fTvZYnhsunErsnEIkneZX_eO*_z&sourcepath=pc-jllista-zhineng&f=pc_list_detai&dpid=0b78b70d437a430cb16328eddb7e7883&followparam={%E2%80%9CsearchID%E2%80%9C:%E2%80%9C0e04a566cec54e46968a504533cb2654%E2%80%9C,%E2%80%9CsearchVersion%E2%80%9C:10000,%E2%80%9CsearchAreaID%E2%80%9C:172,%E2%80%9CsearchFirstAreaID%E2%80%9C:172,%E2%80%9CsearchPositionID%E2%80%9C:2079,%E2%80%9CsearchSecondPositionID%E2%80%9C:2079,%E2%80%9Cpage%E2%80%9C:1,%E2%80%9Clocation%E2%80%9C:0,%E2%80%9CresumeType%E2%80%9C:2,%E2%80%9Cplatform%E2%80%9C:%E2%80%9Cpc%E2%80%9C,%E2%80%9CsourcePage%E2%80%9C:%E2%80%9Cpc-jllista-zhineng%E2%80%9C,%E2%80%9CoperatePage%E2%80%9C:%E2%80%9Clist%E2%80%9C}&PGTID=0d303353-000a-c384-ec96-53887258367b&ClickID=5&adtype=3&tdsourcetag=s_pcqq_aiomsg&qq-pf-to=pcqq.temporaryc2c&pts=1564721773288"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': '',  # 已删除cookie部分，验证的时候，请复制自己的cookie
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    font_map = get_font_map(response.text)
    html = etree.HTML(response.text)
    sex = html.xpath("//span[contains(@class, 'sex')]/text()")[0]
    print("性别: ", hex2word(font_map, sex))
    age = html.xpath("//span[contains(@class, 'age')]/text()")[0]
    print("年龄: ", hex2word(font_map, age))
    edu = html.xpath("//span[contains(@class, 'edu')]/text()")[0]
    print("学校: ", hex2word(font_map, edu))
    jy = html.xpath("//div[@class='base-detail']/span[last()]/text()")[0]
    print("工作经验: ", hex2word(font_map, jy))


if __name__ == "__main__":
    parse_zt()

