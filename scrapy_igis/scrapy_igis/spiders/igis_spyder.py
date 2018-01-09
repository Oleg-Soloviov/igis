import sys
import scrapy
import re
import random
sys.path.append('/home/oleg/PycharmProjects/igis/myproject')
from django.utils.text import slugify
from transliterate import translit
from ..settings import MY_START_URLS, logger
from ..items import ScrapyIgisItem, ScrapyIgisIzhItem, PersonIgisItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class IgisSpider(CrawlSpider):
    name = "igis_udm"
    allowed_domains = ['igis.ru']

    def start_requests(self):
        for url in MY_START_URLS:
            request = scrapy.Request(url, callback=self.parse)
            request.meta['place_url'] = url
            yield request

    def parse(self, response):
        urls = response.xpath('//a[contains(@href, "?obj=")]/@href').extract()
        for url in urls:
            request = scrapy.Request(response.urljoin(url), callback=self.parse_item)
            request.meta['place_url'] = response.meta['place_url']
            yield request

    def parse_item(self, response):
        logger.info('Hi, this is an item page! %s', response.url)
        item = ScrapyIgisItem()
        try:
            item['place_url'] = response.meta['place_url']
            logger.debug('place_url: {0}'.format(item['place_url']))
            item['url'] = response.url
            logger.debug('url: {0}'.format(item['url']))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'Сайт:\s*<a target="_blank" href="(.*)">')
            if x:
                x = x[0]
                x = x.strip()
                item['site_address'] = x.rstrip('/')
            logger.debug('site_addrr: {0}, x: {1}'.format(28, x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'E-mail:\s*<a href=".*">([.@\w]*)</a>')
            if x:
                x = x[0]
                item['email'] = x.strip()
            logger.debug('email: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'Телефон:(.*)\s*<br>E-mail')
            if x:
                x = x[0]
                item['phone'] = x.strip()
            logger.debug('phone: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'x=[\d]{2}.[\d]{2,6}')
            if x:
                x = x[0]
                item['x_coord'] = x.strip()
            logger.debug('x_coord: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'y=[\d]{2}.[\d]{2,6}')
            if x:
                x = x[0]
                item['y_coord'] = x.strip()
            logger.debug('y_coord: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'Адрес:(.*)\(<a href="javascript')
            if x:
                x = x[0]
                item['hospital_address'] = x.strip()
            logger.debug('hospital_address: {0}'.format(x))
            x = response.css('#parent-div>div>hr+h2::text').extract_first()
            item['hospital_name'] = x.strip()
            logger.debug('hospital_name: {0}'.format(x))
            x = response.xpath('//img[contains(@src, "/com/img/?size=b&path=medic/clinic/")]/@src').extract_first()
            if x:
                x = 'http://igis.ru' + x
                item['image_urls'] = [x]
            logger.debug('image_urls: {0}'.format(x))
            item['slug'] = slugify(translit(item['hospital_name'], 'ru', reversed=True))
            logger.debug('slug: {0}'.format(item['slug']))
        except Exception as e:
            logger.error('Error: {0}'.format(e))
        return item


class IgisIzhSpider(CrawlSpider):
    name = "igis_iz"
    allowed_domains = ['igis.ru']

    start_urls = [
        'http://igis.ru/online?tip=1',
        'http://igis.ru/online?tip=2',
        'http://igis.ru/online?tip=3',
        'http://igis.ru/online?tip=4'
    ]

    rules = (
        Rule(LinkExtractor(allow=('obj=',)), callback='parse_item'),
    )

    def parse_item(self, response):
        logger.info('Hi, this is an item page! %s', response.url)
        item = ScrapyIgisIzhItem()
        try:
            item['url'] = response.url
            logger.debug('url: {0}'.format(item['url']))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'Сайт:\s*<a target="_blank" href="(.*)">')
            if x:
                x = x[0]
                x = x.strip()
                item['site_address'] = x.rstrip('/')
            logger.debug('site_addrr: {0}, x: {1}'.format(28, x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'E-mail:\s*<a href=".*">([.@\w]*)</a>')
            if x:
                x = x[0]
                item['email'] = x.strip()
            logger.debug('email: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'Телефон:(.*)\s*<br>E-mail')
            if x:
                x = x[0]
                item['phone'] = x.strip()
            logger.debug('phone: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'x=[\d]{2}.[\d]{2,16}')
            if x:
                x = x[0]
                item['x_coord'] = x.strip()
            logger.debug('x_coord: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'y=[\d]{2}.[\d]{2,16}')
            if x:
                x = x[0]
                item['y_coord'] = x.strip()
            logger.debug('y_coord: {0}'.format(x))
            x = response.xpath('//div[@id="parent-div"]//table//table').re(r'Адрес:(.*)\(<a href="javascript')
            if x:
                x = x[0]
                item['hospital_address'] = x.strip()
            logger.debug('hospital_address: {0}'.format(x))
            x = response.css('#parent-div>div>hr+h2::text').extract_first()
            item['hospital_name'] = x.strip()
            logger.debug('hospital_name: {0}'.format(x))
            x = response.xpath('//img[contains(@src, "/com/img/?size=b&path=medic/clinic/")]/@src').extract_first()
            if x:
                x = 'http://igis.ru' + x
                item['image_urls'] = [x]
            logger.debug('image_urls: {0}'.format(x))
            item['slug'] = slugify(translit(item['hospital_name'], 'ru', reversed=True))
            logger.debug('slug: {0}'.format(item['slug']))
        except Exception as e:
            logger.error('Error: {0}'.format(e))
        return item


class IgisPersonSpider(CrawlSpider):
    name = 'person_igis'
    allowed_domains = ['igis.ru']
    start_urls = ['http://igis.ru/online']

    rules = (
        Rule(LinkExtractor(allow=('tip=',))),
        Rule(LinkExtractor(allow=('obj=',)), callback='parse_value'),
    )

    def parse_value(self, response):
        all_links = response.xpath('//a[contains(@href, "javascript:winbox(2,\'/com/online/page_obj_spec.php?")]/@href').extract()
        for link in all_links:
            m = re.search(r"javascript:winbox\(\d{0,4},\'(/com/online/page_obj_spec\.php\?(obj=\d{1,6})&id=(\d{2,12}))\'", link)
            if m:
                randint = random.randrange(1000, 100000)
                url = 'http://igis.ru' + m.group(1) + '&rnd=' + str(randint)
                request = scrapy.Request(url, callback=self.parse_item)
                yield request

    def parse_item(self, response):
        logger.debug('Start new item')
        item = PersonIgisItem()
        try:
            url = response.url
            m = re.search(r"(http://igis.ru/com/online/page_obj_spec.php\?(obj=\d{1,6})&id=(\d{1,12}))", url)
            item['igis_url'] = m.group(1)
            item['igis_person_id'] = m.group(3)
            item['igis_obj'] = m.group(2)
            item['fio'] = response.css('h1::text').extract_first()
            my_tables = response.css('table')
            first_table = my_tables[0]
            my_rows = first_table.xpath('.//tr')
            my_items = {}
            for row in my_rows:
                x = row.css('td::text').extract()
                try:
                    x_key = x[0]
                except Exception:
                    continue
                try:
                    x_item = x[1]
                except Exception:
                    x_item = ''
                my_items[x_key.strip()] = x_item.strip()
            item['update_date'] = my_items.get('Обновление информации', '')
            item['speciality'] = my_items.get('Специальность', '')
            item['room'] = my_items.get('Кабинет №', '')
            item['time_limit'] = my_items.get('Норма времени', '')
            x = my_items.get('Код / Участок', 'Не найден / Не найден')
            kod, sector = x.split('/')
            item['kod'] = kod.strip()
            item['sector'] = sector.strip()
            item['time_filter'] = my_items.get('Фильтр расписания', '')
            item['unit'] = my_items.get('Подразделение', '')
            item['info'] = my_items.get('Информация', '')
            m = re.search(r'Выходные дни:(.*) </div>', response.text)
            if m:
                x = m.group(1)
                item['free_days'] = x.strip()
            m = re.search(r'Изменения в работе\s*</h2>(.*)<br>\s*Выходные дни:', response.text)
            if m:
                x = m.group(1)
                item['not_working_days'] = x.split('<br>')
            return item
        except Exception as e:
            logger.error('Error: {0}'.format(e))
