# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import logging

logger = logging.getLogger("CarAutohomeImagePipeline")


class CarAutohomePipeline(object):
    def process_item(self, item, spider):
        return item


# 重写ImagePipeline
class CarAutohomeImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """
        这个方法是在发送下载请求之前调用
        其实这个方法本身就是去发送下载请求的
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        for url in item["image_urls"]:
            # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
            yield Request(url, meta={"item": item})

    def file_path(self, request, response=None, info=None):
        """
        分类保存
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :return: 每套图的分类目录
        strip:清洗Windows系统的文件夹非法字符，避免无法创建目录
        """

        # 接收上面meta传递过来的图片名称
        item = request.meta["item"]
        folder = item["category"]

        # 清洗掉Windows系统非法文件夹名字的字符串,不经过这么一个步骤，会有乱码或无法下载
        folder_strip = re.sub(r"[？\\*|“<>:/]", "", str(folder))

        # 提取url后面的名称作为图片名
        image_guid = request.url.split("/")[-1]
        filename = u'{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def item_completed(self, results, item, info):
        """
        文件下载完成之后，返回一个列表 results
        列表中是一个元组，第一个值是布尔值，请求成功会失败，第二个值的下载到的资源
        """
        if not results[0][0]:
            # 如果下载失败，就抛出异常，并丢弃这个item
            # 被丢弃的item将不会被之后的pipeline组件所处理
            raise DropItem('下载失败')
        # 打印日志
        logger.debug('下载图片成功')
        return item
