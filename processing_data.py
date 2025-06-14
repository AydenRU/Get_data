import json
import datetime


class WorkInData:

    @staticmethod
    def open_json(adres: str):
        with  open(adres, encoding='utf-8') as comments:
            result_data = json.load(comments)
        if len(result_data) == 1:
            key = next(iter(result_data.keys()))
            return result_data[key]
        return result_data

    @staticmethod
    def jsontime_in_time(jstime):
        if jstime.endswith('Z'):
            jstime = jstime[:-1]
        return datetime.datetime.fromisoformat(jstime)

data_post = WorkInData.open_json('data\\posts.json')
data_comments = WorkInData.open_json('data\\comments.json')