# -*- coding: utf-8 -*-
import scrapy

from mzitu.items import MzituItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
###这里千万要把parser函数删了 不然无法调用parser_item函数 因为CrawlSpider已经默认使用parser函数来爬取第一个链接
#该程序的目的就是找到所有的符合规律的url链接跟进获取图片
class MeiziSpider(CrawlSpider):
    name = "meizi"
    allowed_domains = ["mzitu.com"]
    start_urls = ['http://www.mzitu.com/']
    #定义一个全局的列表
    img_urls=[]
    #定义抓取规则 找到如下规则内的所有url allow是允许的  deny是不允许的 从start_url页，从start_urls链接的源代码开始找 然后再跟进继续使用该规则
    rules = (
        Rule(LinkExtractor(allow=('http://www.mzitu.com/\d{6}',),deny=('http://www.mzitu.com/\s',)),\
             callback='parser_item',follow=True),
           )

    def parser_item(self,response):
        item=MzituItem()
        #得到没套图的名字 extract_first(default=”N/A”)取xpath返回值的第一个元素。如果xpath没有取到值，则返回N/A
        #这里我用字符串分割的方法
        name=response.selector.xpath('/html/body/div[2]/div[1]/div[1]/text()[3]').extract()
        item['name']=name[0][3:-1]
        item['url']=response.url
        all_page=response.selector.xpath('/html/body/div[2]/div[1]/div[4]/a[5]/span/text()').extract()
        for page in range(1,int(all_page[0])+1):
            #得到每张照片的地址
            url=response.url+'/'+str(page)
            yield scrapy.Request(url=url,callback=self.img_url)
        #上面的循环所有页面执行完 定义的图片url列表也在下面的 img_url函数里添加好了 所以放入容器
        item['image_url']=self.img_urls
        yield item
    def img_url(self,response):
        urls=response.selector.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@src').extract()
        #有的页面不只一张图 所以加个循环 得到当前页面所有的
        print "--------------------------------------------------\n"
        for img_url in urls:
            #x=uuid.uuid1()
            f =open("data.txt","a+")
            f.write(img_url+"\n")
            f.close()
            print img_url+"    ===>>download"
            self.img_urls.append(img_url)



