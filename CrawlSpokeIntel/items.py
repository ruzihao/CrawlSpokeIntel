# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlspokeintelItem(Item):
    # define the fields for your item here like:
    # name = Field()

    # company
    name = Field()
    short_description = Field()

    # summary
    website = Field()
    blog = Field()
    summary = Field()
    status = Field()
    founded_on = Field()
    yearly_revenue = Field() 
    industry = Field()
    people = Field()
    alias = Field()
    tags = Field()
    # social_presence = Field()
    location = Field()
    contact_info_tel = Field()
    contact_info_email = Field()

    # offices
    branch = Field()
    address_line = Field()
    city = Field()
    state = Field()
    postal_code = Field()
    country = Field()

    # latest news
    # latest_news = Field()

    # milestones
    # milestones = Field()

    # links
    # links = Field()

    # people
    members = Field()

    # press releases
    # press_releases = Field()

    # funding
    funding_history = Field()
    funding_investors = Field()

    # investments/acquisitions
    investments = Field()


def main():
    print CrawlspokeintelItem.__dict__
    return


if __name__ == '__main__':
    main()