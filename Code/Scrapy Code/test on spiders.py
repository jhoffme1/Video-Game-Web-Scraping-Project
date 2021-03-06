from scrapy import Spider, Request
from videogames.items import VideogamesItem 


class VideoGamesSpider(Spider):
        name = 'videogames_spider'
        allowed_domains = ['www.metacritic.com']
        start_urls = ['https://www.metacritic.com/browse/games/score/metascore/all/ps4']
                                    
        def parse(self, response):
            last_page_num = int(response.xpath('//li[@class="page last_page"]/a/text()').extract_first())
            page_urls = [f'https://www.metacritic.com/browse/games/score/metascore/all/ps4?sort=desc&page={i}' for i in range(last_page_num)]

            for url in page_urls[:2]:
                yield Request(url=url, callback=self.parse_list_pages)

        def parse_list_pages(self, response):
            begin = 'https://www.metacritic.com'
            game_pages = response.xpath('//ol[@class="list_products list_product_condensed"]//div[@class="basic_stat product_title"]/a/@href').extract()
            result_urls = [begin + page for page in game_pages]

            for url in result_urls:
                yield Request(url, self.parse_inner_page)


        def parse_inner_page(self, response ):
            ## Individual Product Listing Page
            title= response.xpath('//div[@class= "product_title"]/a/h1/text()').extract()
            seperate_reviews = response.xpath('//div[@class= "metascore_wrap highlight_metascore"]/a/div/span/text()').extract()
            developer= response.xpath('//li[@class= "summary_detail developer"]/span/text()').extract()[1].strip()
            genre= response.xpath('//li[@class= "summary_detail product_genre"]/span/text()').extract()[1].strip()
            user_score= response.xpath('//div[@class= "userscore_wrap feature_userscore"]/div/text()').extract()[4]
            release_date= response.xpath('//li[@class= "summary_detail release_data"]/span/text()').extract()[1]

            # item = VideogamesItem()
            # item['title'] = title
            # item['seperate_reviews'] = seperate_reviews
            # item['developer'] = developer
            # item['genre'] = genre       
            # item['user_score'] = user_score
            # item['release_date'] = release_date

            yield item

        def critic_inner_page(self, response):
            review_grade
            review_critic
            review_body

            review_critic= response.xpath('//div[@class= "review_critic"]/div//text()').extract()
            review_grade= review_grade= response.xpath('//div[@class= "review_grade"]/div//text()').extract()