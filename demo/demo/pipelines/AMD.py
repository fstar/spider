import pandas as pd


class demoPipeline(object):
    result = []

    def process_item(self, item, spider):
        # print("test1---->", item)
        self.result.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.result)
        df.to_excel(f"{spider.name}.xlsx", index=False)
        return