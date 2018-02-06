import scrapy
import urllib

class MetScraper(scrapy.Spider):
    name = "metCrawler"
    def start_requests(self):
        urls=[]
        for i in range(1,43):
            urls.append("https://www.metmuseum.org/art/metpublications/titles-with-full-text-online?searchtype=F&rpp=12&pg="+str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        titles = ((response.css("a#publicationImageLink::attr(href)")).extract())
        if not titles:
            print("You are currently on the page for")
            onclick = response.css("a#m_download_pdf_link::attr(onclick)").extract()
            onclick = onclick[0]
            parsed = onclick.split("('",1)[1]
            parsed = parsed[:-3]
            name = response.css("title::text").extract()
            name = name[0].split(" |",1)[0]
            print(name)
            urllib.urlretrieve(parsed,"/Volumes/QINGNIAO/1/Met Books/"+name+".pdf")
        else:
            numTitles = len(titles)
            for i in range(0,numTitles):
                nextpage = response.urljoin(titles[i])
                yield scrapy.Request(nextpage, callback=self.parse)
