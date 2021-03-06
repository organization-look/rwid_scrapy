from typing import List

import scrapy
from cssselect import Selector


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['127.0.0.1']

    #mulai dari urls ini
    start_urls = ['http://127.0.0.1:5000/']

    def parse(self, response):
        data ={
            "username":"user",
            "password":"user12345",
        }
        return scrapy.FormRequest(
            url='http://127.0.0.1:5000/login',
            formdata=data,
            callback=self.after_login
        )

    def after_login(self,response):
        """
         2 taks disini


         ambil semua data barang yang ada di hasil => akan menuju parsing detail
         ambil semua link next => akan kembali ke self.after_login

        :param response:
        :return:
        """

        #get datail Product
        detail_product: List[Selector] = response.css(".card .card-title a" )
        for detail in detail_product:
           href = detail.attrib.get("href")
           yield response.follow(href,callback=self.parse_detail)

        pagination:List[Selector]=response.css(".pagination a.page-link")
        for paginations in pagination:
            href=paginations.attrib.get("href")
            yield response.follow(href,callback=self.after_login)

        yield {"title" : response.css("title::text").get()}

    def parse_detail(self,response):
        image =response.css(".card-img-top").attrib.get("src")
        title = response.css(".card-title::text").get()
        stock = response.css(".card-stock::text").get()
        description = response.css(".card-text::text").get()

        return {
            'image':image,
            'title': title,
            'stock': stock,
            'description': description,

        }

