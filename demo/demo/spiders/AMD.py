from scrapy import Request, Spider
import pandas as pd

from demo.items.AMD import AMDItem
from demo.tools.timeFunction import get_current_day_time


class AMDSpider(Spider):
    name = "AMD"
    custom_settings = {
        "ITEM_PIPELINES": {
            "demo.pipelines.AMD.demoPipeline": 300

        },
    }

    def start_requests(self):
        url = "https://www.amd.com/en/products/specifications/processors"
        yield Request(url)

    def parse(self, response):
        html = response.text
        df = pd.read_html(html, encoding="utf-8")
        if len(df) == 0:
            return
        df = df[0]
        columns = df.columns
        for i, row in df.iterrows():
            one = AMDItem()
            for key in columns:
                filterkey = key.replace("*", ""). \
                              replace("/ ", "").\
                              replace("# ", "").\
                              replace(" ", "_").\
                              replace("(", "").\
                              replace(")", "").\
                              strip().lower()
                if filterkey in one.fields:
                    one[filterkey] = row[key]
            yield one











