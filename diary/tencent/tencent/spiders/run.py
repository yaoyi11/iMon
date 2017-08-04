from scrapy import cmdline

cmd = 'scrapy crawl qqnews -s JOBDIR=crawls/somespider-1'
cmdline.execute(cmd.split(' '))