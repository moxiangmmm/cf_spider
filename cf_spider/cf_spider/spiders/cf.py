# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re
import time
from ..read_company import read_company1, read_company2
from ..item_dump import Item_dump

# url去重
# 保存数据库
# 设置日志


class CfSpider(scrapy.Spider):
    name = 'cf'
    allowed_domains = ['jzsc.mohurd.gov.cn']
    cf_href = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/{}?_={}"
    company_list = read_company2('/home/python/Desktop/company/sx_company.csv')

    def start_requests(self):
        search_url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
        for company in self.company_list:
            print(company)
            i = Item_dump(company,'cf_dump')
            ret = i.item_dump()
            if not ret:
                item = {"company":company, "type":None}
                data = {
                    "qy_type":"",
                    "apt_scope":"",
                    "apt_code":"",
                    "qy_name":"",
                    "qy_code":"",
                    "apt_certno":"",
                    "qy_fr_name":"",
                    "qy_gljg":"",
                    "qy_reg_addr":"",
                    "qy_region":"",
                    "complexname": company
                }
                yield scrapy.FormRequest(
                    search_url,
                    formdata=data,
                    callback=self.parse,
                    meta={"item":item}
                )

    def parse(self, response):
        item = deepcopy(response.meta["item"])
        tr_list = response.xpath("//tbody[@class='cursorDefault']//tr")
        for tr in tr_list:
            detail_href = tr.xpath('.//td[@data-header="企业名称"]/a/@href').extract_first()
            if detail_href:
                company_id = re.findall(r'/dataservice/query/comp/compDetail/(\d+)', detail_href)[0]
                print(company_id)
                nd = int(time.time())*1000
                cf_href = self.cf_href.format(company_id,nd)
                yield scrapy.Request(
                    cf_href,
                    meta={"item":deepcopy(item)},
                    callback=self.cf_parse
                )
            else:
                item["资质信息"] = []
                print(item)
                yield item


    def cf_parse(self, response):
        # http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/001607220057212582?_=1518077185819
        item = deepcopy(response.meta["item"])
        tr_list = response.xpath("//tbody[@class='cursorDefault']//tr")
        cf_list = []
        for tr in tr_list:
            cf_one = []

            cf_type = tr.xpath(".//td[@data-header='资质类别']/text()").extract_first()
            cf_type = cf_type.strip() if cf_type is not None else ""

            cf_id = tr.xpath(".//td[@data-header='资质证书号']/text()").extract_first()
            cf_id = cf_id.strip() if cf_id is not None else ""

            cf_name = tr.xpath(".//td[@data-header='资质名称']/text()").extract_first()
            cf_name = cf_name.strip() if cf_name is not None else ""

            b_data = tr.xpath(".//td[@data-header='发证日期']/text()").extract_first()
            cf_date = b_data.strip() if b_data is not None else ""

            s_data = tr.xpath(".//td[@data-header='证书有效期']/text()").extract_first()
            cf_time = s_data.strip() if s_data is not None else ""

            gov = tr.xpath(".//td[@data-header='发证机关']/text()").extract_first()
            cf_org = gov.strip() if gov is not None else ""
            cf_one.append(cf_type)
            cf_one.append(cf_id)
            cf_one.append(cf_name)
            cf_one.append(cf_date)
            cf_one.append(cf_time)
            cf_one.append(cf_org)
            cf_list.append(cf_one)

        item["资质信息"] = cf_list
        print(item)
        yield item
