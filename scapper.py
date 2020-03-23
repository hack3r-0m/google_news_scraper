from bs4 import BeautifulSoup
import sys
from requests import get, ConnectionError
import csv

class Main():

    def __init__(self):
        self.useragent = { 'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Iron/11.0.700.2 Chrome/11.0.700.2 Safari/534.24'
                        }
        self.special_words = [ 'corona',
                                'virus',
                                'Coronavirus'
                                'COVID-19',
                                'slowdown',
                                'surge',
                                'quarantine',
                                'deaths',
                                'cases',
                                'lockdown',
                                'IPO',
                                'acquisitions'
        ]

    def build_connection(self):
    
        google_news_url = 'https://news.google.com/?hl=en'
        response = get(google_news_url, headers=self.useragent)

        if response.status_code != 200:
            raise ConnectionError("Expected status code 200, but got {}".format(response.status_code))

        return response

    def build_scrapper(self, response):

        raw_soup = BeautifulSoup(response.text, "lxml")

        main_news = []
        all_news = []
        hrefs = []

        for news in raw_soup.find_all('h3'):
            main_news.append(news.text)


        for news in raw_soup.find_all(attrs= {  'class': 'SbNwzf',
                                                'class': 'ipQwMb ekueJc gEATFF RD0gLb',
                                            }):
            all_news.append(news.text)

        for tags in raw_soup.find_all(attrs= {
                                    'class':'VDXfz'
                                }):

            completer = "https://news.google.com/" + tags['href'][2:]
            hrefs.append(completer)

        return main_news, all_news, hrefs

    def news_mapper(self, main_news, all_news, hrefs):

        count=0

        with open('output.csv', 'a+', newline='', encoding="utf-8") as board: # newline attribute for omitting blank lines in csv file
            
            writer = csv.writer(board)
            writer.writerow(['HEADLINES','SUB NEWS','LINKS'])

            for news in all_news:

                if news in main_news:

                    writer.writerow([news])
                    writer.writerow(['','',hrefs[count]])

                else:

                    writer.writerow(['',news,''])

                count += 1

        return None

 
    def custom_words(self, all_news):

        for word in self.special_words:
            for news in all_news:
                for news_word in news.split(" "):

                    if word.lower() == news_word.lower():

                        with open('output_custom_words.csv', 'a+', newline='', encoding="utf-8") as board:
                            writer = csv.writer(board)
                            writer.writerow([word,news])
                            board.close()

        return None

if __name__ == '__main__':
    instance = Main()
    connection = instance.build_connection()
    main_news, all_news, hrefs = instance.build_scrapper(connection)
    output = instance.news_mapper(main_news, all_news, hrefs) # returns None
    custom_words_output = instance.custom_words(all_news) # returns None


    print("Process completed! check the output CSV file")
    sys.exit()
