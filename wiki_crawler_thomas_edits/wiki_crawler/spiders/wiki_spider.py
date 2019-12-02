# -*- coding: utf-8 -*-
import scrapy
import spacy
from bs4 import BeautifulSoup
from lxml import etree
import requests
import json
import logging
from io import StringIO, BytesIO
# from scrapy.crawler import settings
logger = logging.getLogger('scrapy output')


def fix_encoding(text):
    return text.replace('\u00a0','_')

def fix_relation(relation):
    if relation == "founders":
        relation = "founded_by"
    if relation == "original_author(s)":
        relation = "founded_by"
    if relation =='founder(s)':
        relation = 'founded_by'
    if relation == 'type_of_business':
        relation = 'type'
    return relation


class WikiSpider(scrapy.Spider):

    name = 'wiki_entities'
    # start_urls = ['https://en.wikipedia.org/wiki/Summify']
    start_urls = ['https://en.wikipedia.org/wiki/Facebook', 'https://en.wikipedia.org/wiki/Twitter', 'https://en.wikipedia.org/wiki/Snapchat', 
    'https://en.wikipedia.org/wiki/Instagram', 'https://en.wikipedia.org/wiki/Periscope_(app)', 'https://en.wikipedia.org/wiki/Vine_(service)', 
    'https://en.wikipedia.org/wiki/Summify', "https://en.wikipedia.org/wiki/Pinterest", "https://en.wikipedia.org/wiki/Reddit", "https://en.wikipedia.org/wiki/WeChat"]


    allowed_domains=['en.wikipedia.org']


    def parse(self, response):
        type_dict = {
            "businessperson": "person",
            "Public company": "company",
            "software": "company",
            "Privately held company": "company",
            "organisation": "company",
            "Subsidiary": "company",
            "Consolidated city-county": "location",
            "city": "location",
            "City": "location",
            "City (California)": "location",
            "List of cities in British Columbia": "location",
            "language": "programming_language",
            "Thing": "programming_language"
        }

        dont_crawl = ['https://en.wikipedia.org/wiki/United_States_dollar', "https://en.wikipedia.org/wiki/Proprietary_software", "https://en.wikipedia.org/wiki/New_York_Stock_Exchange",
        "https://en.wikipedia.org/wiki/S%26P_500", "https://en.wikipedia.org/wiki/S%26P_100", "https://en.wikipedia.org/wiki/NASDAQ"]
        if response.url not in dont_crawl:
            entity_html = response.xpath('//*[@id="firstHeading"]').getall()[0]
            entity_soup = BeautifulSoup(entity_html, 'lxml')
            entity_name = entity_soup.get_text().strip()

            dbn = entity_name.replace(' ', '_')
            dbn_url = "http://dbpedia.org/page/{}".format(dbn)
            r_dbn = requests.get(dbn_url)
            dbn_soup = BeautifulSoup(r_dbn.text, 'lxml')

            entity_type_list = dbn_soup.find_all('div', {'class': 'page-resource-uri'})[0]
            entity_type = entity_type_list.find_all('a')[0].get_text()

            if type_dict.get(entity_type):
                entity_type = type_dict[entity_type]
            out_d = {}
            out_d["name"] = entity_name
            out_d["url"] = response.url
            out_d["entity_type"] = entity_type

            table = response.xpath('//*[@id="mw-content-text"]/div/table[1]').getall()[0]
            if len(table) < 2000:
                table = response.xpath('//*[@id="mw-content-text"]/div/table[2]').getall()[0]
            table_soup = BeautifulSoup(table, 'lxml')
            for tr in table_soup.find_all('tr'):
                if tr.td and tr.th:
                    relation = fix_encoding(tr.th.get_text().strip().lower().replace(' ', '_'))
                    relation = fix_relation(relation)
                    values = tr.td
                    if values.find_all('li'):
                        value = []
                        for v in values.find_all('li'):
                            value.append(fix_encoding(v.get_text()))
                            if v.a:
                                next_page = v.a['href']
                                yield response.follow(next_page, callback=self.parse)
                        out_d[relation] = value

                    else:
                        v_list = values.find_all('a')
                        if len(v_list) > 1:
                            value = []
                            for v in v_list:
                                value.append(fix_encoding(v.get_text()))
                                if v.a:
                                    next_page = v.a['href']
                                    yield response.follow(next_page, callback=self.parse)
                            out_d[relation] = value
                        else:
                            for a in values.find_all('a'):
                                value = fix_encoding(values.get_text())
                                out_d[relation] = value
                                if values.a:
                                    next_page = values.a['href']
                                    yield response.follow(next_page, callback=self.parse)
            logger.info(json.dumps(out_d,indent=4))

            if len(out_d.keys()) > 2:
                with open('entities.json', 'a') as outfile:
                    outfile.write(json.dumps(out_d) + '\n')
                yield out_d



