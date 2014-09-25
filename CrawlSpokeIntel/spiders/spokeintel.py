from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from CrawlSpokeIntel.items import CrawlspokeintelItem
from scrapy.http import Request

import re
import config as cf

TC = cf.TABLE_COMPANIES_COLS
TM = cf.TABLE_MEMBERS_COLS
TF = cf.TABLE_FUNDINGS_COLS 
TA = cf.TABLE_ACQUISITIONS_COLS 
TI = cf.TABLE_INVESTORS_COLS

START_PAGE_NUM = 2
START_MORE_MEMBER_NUM = 2
DOMAIN = u'http://www.spokeintel.com'

class SpokeintelSpider(CrawlSpider):
    name = 'spokeintel'
    allowed_domains = ['www.spokeintel.com']
    # start_urls = ['http://www.www.spokeintel.com/']
    # start_urls = ['http://www.spokeintel.com/dir/companies/name/goo/google']
    # start_urls = ['http://www.spokeintel.com/companies/airbnb-4e419a34091eb05bba00002c']
    start_urls = ['http://www.spokeintel.com/companies/google-3e122f809e597c1003565d3f']

    # rules = (
    #     Rule(SgmlLinkExtractor(allow=(r'google\-3e122f809e597c1003565d3f',)), callback='parse_item', follow=False),
    # )

    def __init__(self):
        self.p = None
        self.num_more_pages = None
        self.link_prefix = None

    def parse(self, response):
        ''' Wrapper. '''
        rtn = self.parse_item(response)
        return rtn


    def parse_item(self, response):
        ''' Parser for all. '''
        # initialization
        self.p = START_PAGE_NUM
        hxs = HtmlXPathSelector(response)
        i = CrawlspokeintelItem()
        self.extract_name(hxs, i)
        self.extract_summary(hxs, i)
        self.extract_offices(hxs, i)
        self.extract_members(hxs, i)
        self.extract_investments(hxs, i)
        self.extract_funding(hxs, i)

        # post processing
        i = self.post_processing(i)

        self.num_more_pages, self.link_prefix = self.get_more_members_stats(hxs, i)
        return Request(self.link_prefix+str(self.p), callback=self.parse_more, meta={'item':i})


    def extract_name(self, hxs, item):
        ''' Extract name and short_description. '''
        item[TC['name']] = hxs.select('//*[@id="profile-intro"]/div/div/div[3]/div[3]/h1/text()').extract()
        item[TC['short_des']] = hxs.select('//*[@id="profile-intro"]/div/div/div[3]/div[3]/div/div[2]/text()').extract()


    def extract_summary(self, hxs, item):
        ''' Extract summary. '''
        item[TC['website']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[1]/p/span[1]/a/@href').extract()
        item[TC['blog']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[1]/p/span[2]/a/@href').extract()
        item[TC['summary']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[1]/div[2]/p/text()').extract()
        item[TC['status']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[2]/span').extract()
        item[TC['founded_on']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[3]/span[1]/span/text()').extract()
        item[TC['year_rev']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[4]/span[1]/span/text()').extract()
        item[TC['industry']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[3]/span[2]/span/text()').extract()
        item[TC['people']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[4]/span[2]/span/text()').extract()
        item[TC['alias']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[5]/span[1]/span/text()').extract()
        item[TC['tags']] = hxs.select('//*[@id="summary"]/div/div/div[1]/div/div[5]/span[2]/span//text()').extract()
        item[TC['location']] = hxs.select('//*[@id="summary"]/div/div/div[2]/div/div/p/text()').extract()
        item[TC['tel']] = hxs.select('//*[@id="summary"]/div/div/div[2]/div/div/address/span[2]/text()').extract()
        item[TC['email']] = hxs.select('//*[@id="summary"]/div/div/div[2]/div/div/address/a/text()').extract()


    def extract_offices(self, hxs, item):
        ''' Extract offices location. '''
        item[TC['branch']] = hxs.select('//*[@id="offices"]/div/div/div/div/div/address/strong/text()').extract()
        item[TC['addr']] = hxs.select('//*[@id="offices"]/div/div/div/div/div/address/span[1]/text()').extract()
        item[TC['city']] = hxs.select('//*[@id="offices"]/div/div/div/div/div/address/span[2]/a/text()').extract()
        item[TC['state']] = hxs.select('//*[@id="offices"]/div/div/div/div/div/address/span[3]/a/text()').extract()
        item[TC['ps_code']] = hxs.select('//*[@id="offices"]/div/div/div/div/div/address/span[4]/text()').extract()
        item[TC['country']] = hxs.select('//*[@id="offices"]/div/div/div/div/div/address/div/text()').extract()


    def extract_members(self, hxs, item):
        ''' Extract key members info. '''
        num_members = len(hxs.select('//*[@id="people-all"]/div/div/div/h4/a/span/text()').extract())
        item['members'] = []
        for n in range(num_members):
            mber = {}
            name = hxs.select('//*[@id="people-all"]/div[%d]/div/div/h4/a/span/text()'%(n+1)).extract()
            title = hxs.select('//*[@id="people-all"]/div[%d]/div/div/div[1]//text()'%(n+1)).extract()
            category = hxs.select('//*[@id="people-all"]/div[%d]/div/div/div[2]/text()'%(n+1)).extract()
            since = hxs.select('//*[@id="people-all"]/div[%d]/div/div/div[2]/span/text()'%(n+1)).extract()
            mber[TM['name']] = ''.join(name)
            mber[TM['title']] = ''.join(title)
            mber[TM['cat']] = ''.join(category).strip(', ')
            mber[TM['since']] = ''.join(since)
            item['members'].append(mber)


    def get_more_members_stats(self, hxs, item):
        ''' To extact members by clicking "more" '''
        num_more_pages = int(hxs.select('//*[@id="page_people_all"]/@data-total-pages').extract()[0])
        link = DOMAIN + hxs.select('//*[@id="page_people_all"]/@href').extract()[0]
        link_prefix = ''.join(link.split('=')[0:-1]) + '='
        return (num_more_pages, link_prefix)


    def parse_more(self, response):
        ''' For parse members after clicking "more" '''
        item = response.meta['item']
        hxs = HtmlXPathSelector(response)
        # start parsing
        num_more_members = len(hxs.select('/html/body/div/div[@itemprop="member"]').extract())
        for n in range(START_MORE_MEMBER_NUM, num_more_members+START_MORE_MEMBER_NUM):
            mber = {}
            name = hxs.select('/html/body/div[%d]/div/div/h4/a/span/text()'%(n+1)).extract()
            title = hxs.select('/html/body/div[%d]/div/div/div[1]/text()'%(n+1)).extract()
            category = hxs.select('/html/body/div[%d]/div/div/div[2]/text()'%(n+1)).extract()
            since = hxs.select('/html/body/div[%d]/div/div/div[2]/span/text()'%(n+1)).extract()
            mber[TM['name']] = ''.join(name)
            mber[TM['title']] = ''.join(title)
            mber[TM['cat']] = ''.join(category).strip(', ')
            mber[TM['since']] = ''.join(since)
            item['members'].append(mber) 

        # return Request or item
        if self.p < self.num_more_pages + 1:
            self.p += 1
            return Request(self.link_prefix+str(self.p), callback=self.parse_more, meta={'item':item})
        else:
            return item


    def extract_funding(self, hxs, item):
        ''' Extract funding info. '''
        # Extract funding history
        num_funding = len([x for x in hxs.select('//*[@id="funding-history"]/table//tr/td[1]/text()').extract() if '-' in x])
        item['funding_history'] = []
        for n in range(1, num_funding+1):
            fnd = {}
            date = hxs.select('//*[@id="funding-history"]/table//tr[%d]/td[1]/text()'%n*2).extract()
            series = hxs.select('//*[@id="funding-history"]/table//tr[%d]/td[2]/text()'%n*2).extract()
            amount = hxs.select('//*[@id="funding-history"]/table//tr[%d]/td[3]/text()'%n*2).extract()
            investors = hxs.select('//*[@id="funding-history"]/table//tr[%d]/td[2]/div/a//text()'%(n*2+1)).extract()
            fnd[TF['date']] = ''.join(date).strip('\n')
            fnd[TF['series']] = ''.join(series).strip('\n')
            fnd[TF['amount']] = ''.join(amount).strip('\n')
            fnd[TF['investors']] = [x for x in investors if '(lead)' not in x]
            item['funding_history'].append(fnd)

        # Extract funding investments
        num_investors = len(hxs.select('//*[@id="funding-investors"]/div').extract())
        item['funding_investors'] = []
        for n in range(1, num_investors+1):
            ivt = {}
            name = hxs.select('//*[@id="funding-investors"]/div[%d]/div/div/div[1]/a//text()'%n).extract()
            since = hxs.select('//*[@id="funding-investors"]/div[%d]/div/div/div[last()-1]/text()'%n).extract()
            series = hxs.select('//*[@id="funding-investors"]/div[%d]/div/div/div[last()]/text()'%n).extract()
            ivt[TI['name']] = ''.join(name)
            ivt[TI['since']] = ''.join(since).strip('\n')
            ivt[TI['series']] = ''.join(series).strip('\n')
            item['funding_investors'].append(ivt)

            
    def extract_investments(self, hxs, item):
        ''' Extract investments info. '''
        num_invests = len(hxs.select('//*[@id="investments"]/div/div/div/div/div/div[1]/a/span/text()').extract())
        item['investments'] = []
        for n in range(num_invests):
            inv = {}
            name = hxs.select('//*[@id="investments"]/div/div/div[%d]/div/div/div[1]/a/span/text()'%(n+1)).extract()
            since = hxs.select('//*[@id="investments"]/div/div/div[%d]/div/div/div[2]/text()'%(n+1)).extract()
            status = hxs.select('//*[@id="investments"]/div/div/div[%d]/div/div/div[last()]/span/text()'%(n+1)).extract()
            inv[TA['name']] = ''.join(name)
            inv[TA['since']] = ''.join(since).strip('\n')
            inv[TA['status']] = ''.join(status)
            item['investments'].append(inv)


    def post_processing(self, item):
        ''' Post processing on item. '''
        item['name'] = item['name'][0].strip('\n')
        attr_names = ('short_description',
                      'website',
                      'blog',
                      'summary',
                      'founded_on',
                      'yearly_revenue',
                      'industry',
                      'people',
                      'alias',
                      'contact_info_tel',
                      'contact_info_email',
                      'branch',
                      'city',
                      'state',
                      'postal_code',
                      'country')
        for n in attr_names:
            item[n] = item[n][0] if len(item[n])>0 else ''
        item['status'] = re.sub("<.*?>", " ", item['status'][0]).strip(' \n') # strip html tags
        item['tags'] = ''.join(item['tags']).strip('\n').split(', ')
        item['location'] = item['location'][0].strip('\n')
        item['address_line'] = item['address_line'][0].strip('\n')
        return item
