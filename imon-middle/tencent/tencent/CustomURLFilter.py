from scrapy.dupefilter import RFPDupeFilter

class CustomURLFilter(object):
      """根据url过滤"""
      def __init__(self):
          self.urls_seen = set()

      def request_seen(self,item,spider):
          if item['url'] in self.urls_seen:
              raise DropItem("Duplicate item found: %s" % item)
          else:
              self.urls_seen.add(item['url'])
              return item