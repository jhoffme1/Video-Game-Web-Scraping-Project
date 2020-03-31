from scrapy import Spider, Request
from videogames.items import VideogamesItem 


class VideoGamesSpider(Spider):
        # i = 0

        name = 'videogames_spider'
        allowed_domains = ['www.metacritic.com']
        start_urls = ['https://www.metacritic.com/browse/games/score/metascore/all/ps4']
                                    
        def parse(self, response):
            last_page_num = int(response.xpath('//li[@class="page last_page"]/a/text()').extract_first())
            page_urls = [f'https://www.metacritic.com/browse/games/score/metascore/all/ps4?sort=desc&page={i}' for i in range(last_page_num)]

            for url in page_urls[:18]:
                yield Request(url=url, callback=self.parse_list_pages)

        def parse_list_pages(self, response):
            begin = 'https://www.metacritic.com'
            game_pages = response.xpath('//ol[@class="list_products list_product_condensed"]//div[@class="basic_stat product_title"]/a/@href').extract()
            result_urls = [begin + page for page in game_pages]
            for url in result_urls:
                yield Request(url, self.parse_inner_page)


        def parse_inner_page(self, response ):
            ## Individual Product Listing Page
            title= response.xpath('//div[@class= "product_title"]/a/h1/text()').extract_first()
            seperate_reviews = response.xpath('//div[@class= "metascore_wrap highlight_metascore"]/a/div/span/text()').extract_first()
            developer= response.xpath('//li[@class= "summary_detail developer"]/span/text()').extract()[1].strip()
            genre= response.xpath('//li[@class= "summary_detail product_genre"]/span/text()').extract()[1].strip()
            user_score= response.xpath('//div[@class= "userscore_wrap feature_userscore"]/div/text()').extract()[4]
            release_date= response.xpath('//li[@class= "summary_detail release_data"]/span/text()').extract()[1]
            meta = {'title':title, 'seperate_reviews':seperate_reviews, 'developer': developer, 'genre': genre, 'user_score': user_score, 'release_date': release_date}
            prefix = 'https://www.metacritic.com'
            suffix = response.xpath('//p[@class= "see_all"]/a/@href').extract_first()

            if suffix:
                next_url = prefix + suffix
                
                yield Request(next_url, self.parse_critic_review, meta = meta)

            else:
                # game_pages = response.xpath('//ol[@class="list_products list_product_condensed"]//div[@class="basic_stat product_title"]/a/@href').extract()
                review_critics= sum([i.split(',') for i in response.xpath('//div[@class= "review_critic"]/div/a/text()').extract()[:-4]], [])   
                review_grades= sum([i.split(',') for i in response.xpath('//div[@class= "review_grade"]/div/text()').extract()[:-4]], [])

                for critic, grade in zip(review_critics, review_grades):

                    item = VideogamesItem()
                    # item['id'] = i
                    item['title'] = meta['title']
                    item['seperate_reviews'] = meta['seperate_reviews']
                    item['developer'] = meta['developer']
                    item['genre'] = meta['genre']       
                    item['user_score'] = meta['user_score']
                    item['release_date'] = meta['release_date']
                    item['review_critic'] = critic
                    item['review_grade'] = grade
                    # item['review_date']= review_date

                    yield item                     
        
        def parse_critic_review(self, response):

            review_critics= sum([i.split(',') for i in response.xpath('//div[@class= "source"]/a/text()').extract()[:-4]], [])   
            review_grades= sum([i.split(',') for i in response.xpath('//div[@class= "review_grade"]/div/text()').extract()[:-4]], [])

            for critic, grade in zip(review_critics, review_grades):
            # review_date= response.xpath('//div[@class= "date"]/text()').extract_first()      
            # critics= response.xpath('//div[@class= "')

            # Find the number of critics

            # names = critics[0:num_critics*2:2]

            # dates = critics[1:num_critics*2:2]

            # grades = review_grade[0:num_critics]
            
            # Make it into a list of tuples

            #individual critic review page

            # For each review, create and yield the item
            # review = list(zip(names, dates, grades))

        
                item = VideogamesItem()
                # item['id'] = i
                item['title'] = response.meta['title']
                item['seperate_reviews'] = response.meta['seperate_reviews']
                item['developer'] = response.meta['developer']
                item['genre'] = response.meta['genre']       
                item['user_score'] = response.meta['user_score']
                item['release_date'] = response.meta['release_date']
                item['review_critic'] = critic
                item['review_grade'] = grade
                # item['review_date']= review_date

                yield item 

            




            # review_critic= response.xpath('//div[@class= "review_critic"]/div//text()').extract()
            # review_grade= response.xpath('//div[@class= "review_grade"]/div//text()').extract()  
            # review_critic = '[' + review_critic + ']'

            

       




        
                

        