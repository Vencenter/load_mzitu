# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#图片管道
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import re
import urllib
import uuid

class MzituPipeline(ImagesPipeline):
    #重写请求
    def get_media_requests(self, item, info):
        """
          :param item: spider.py中返回的item
          :param info:
          :return:
          """
        # 这里的item['image_url'] 是前面的meizi.py返回的一个列表

        for img_url in item['image_url']:
            #这是每一套图总地址url 是前面的meizi.py返回的是一个字符串
            referer=item['url']
            x=uuid.uuid1()
            urllib.urlretrieve(referer,'F:\scrapy\MZITU\%s.jpg' % x)
            #这里的Request默认callback给file_path meta传递参数给 file_path
            yield Request(img_url,meta={'item':item,'referer':referer})

    # 重写文件路径
    def file_path(self, request, response=None, info=None):
        """
           :param request: 每一个图片下载管道请求
           :param response:
           :param info:
           :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
           :return: 每套图的分类目录 传递到item_completed的results
           """
        #接收来自get_media_requests的item 也就是meizi.py提交过来的 item
        item=request.meta['item']
        #得到每套图的名字（文件夹名）
        file_name=item['name']
        #因为得到的名字可能存在window系统非法的文件字符串 所以这里替换一下
        file_name=strip(file_name)
        #利用图片url的分割得到每张图片的名字
        img_name=request.url.split('/')[-1]
        #这里是结合起来得到的每一张图片的具体存取路径
        file_img_path='full/{}/{}'.format(file_name,img_name)
        #print file_img_path
        return file_img_path

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    #找到 RE 匹配的所有子串，并将其用一个不同的字符串替换。可选参数 count 是模式匹配後替换的最大次数；count 必须是非负整数。
    # 缺省值是 0 表示替换所有的匹配。如果无匹配，字符串将会无改变地返回 re.sub(pattern, repl, string, count=0, flags=0)
    #这里非法字符用空''替换
    path = re.sub(r'[？\\*|“<>:/]','', str(path))
    return path


            # def process_item(self, item, spider):
    #     return item
if __name__=="__main__":
    #没什么意思 测试下strip好不好用
    a = '我是一个？\*|“<>:/错误的字符串'
    print(strip(a))
