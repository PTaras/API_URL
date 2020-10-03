from flask import Flask
from flask_restful import Api, Resource, reqparse
import calendar
from datetime import date, timedelta, datetime
import bitly_api

app = Flask(__name__)
api = Api(app)

con = bitly_api.Connection(access_token='3247522728e81c5c7402d8553c4faf43b214d005')

urls = [
    {
        "id": 0,
        "full_url": "https://ua.jooble.org/desc/3829956827799475430",
        "url": 'https://bit.ly/33bKdpuu',
        "date_created": "2020-09-30 18:01:16.901136",
        "livetime": 91
    },
    {
        "id": 1,
        "full_url": "https://ua.jooble.org/desc/8937534960256301908",
        "url": 'https://bit.ly/33bKddd',
        "date_created": "2020-06-30 18:01:16.901136",
        "livetime": 90
    },
    {
        "id": 2,
        "full_url": "https://ua.jooble.org/desc/5553739797992449502",
        "url": 'https://bit.ly/33bKdpp',
        "date_created": "2019-09-30 18:01:16.901136",
        "livetime": 400
    },
     {
        "id": 3,
        "full_url": "https://ua.jooble.org/desc/5553739797992449503",
        "url": 'https://bit.ly/33bKdrr',
        "date_created": "2020-09-20 18:01:16.901136",
        "livetime": 89
    },
     {
        "id": 4,
        "full_url": "https://ua.jooble.org/desc/3829956827799475568",
        "url": 'https://bit.ly/33bKdzz',
        "date_created": "2020-05-30 18:01:16.901136",
        "livetime": 91
    },
]

class URL(Resource):
    def get(self, id=0):
        if id == 0:
            return urls, 200
        for url in urls:
            date = url["date_created"]
            date_created = datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
            date_now = datetime.utcnow()
            if (url["id"] == id):
                if url["livetime"] == 90:
                    date_diff_default = (date_now - date_created).days
                    if date_diff_default >= 90:
                        return "This link is out of date!", 200
                    return url, 200

                elif url["livetime"] != 90:
                    date_diff = (date_now - date_created).days
                    if date_diff >= url["livetime"] or date_diff >= 365:
                        return "This link is out of date!", 200
                    return url, 200
        return "url not found", 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("full_url")
        parser.add_argument("date_created")
        parser.add_argument("livetime", default=90)
        params = parser.parse_args()
        for url in urls:
            if (params["full_url"] == url["full_url"]):
                return f"url {url['full_url']} already exists", 400
        url = {
            "id": len(urls) + 1,
            "full_url": params["full_url"],
            "url": (con.shorten(params["full_url"]))['url'],
            "date_created": str(datetime.utcnow()),
            "livetime": int(params["livetime"]),
        }

        urls.append(url)
        return url, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("full_url")
        parser.add_argument("date_created")
        parser.add_argument("livetime", default=90)
        params = parser.parse_args()
        for url in urls:
            if (id == url["id"]):
                url["full_url"] = params["full_url"]
                url["url"] = (con.shorten(params["full_url"]))['url']
                url["livetime"] =  int(params["livetime"])
                return url, 200

        url = {
            "id": int(id),
            "full_url": params["full_url"],
            "url": (con.shorten(params["full_url"]))['url'],
            "date_created": str(datetime.utcnow()),
            "livetime": int(params["livetime"])
        }

        urls.append(url)
        return url, 201

    def delete(self, id):
        global urls
        urls = [url for url in urls if url["id"] != id]
        return f"url with id {id} is deleted.", 200


api.add_resource(URL, "/urls", "/urls/", "/urls/<int:id>")
if __name__ == '__main__':
    app.run(debug=True)
