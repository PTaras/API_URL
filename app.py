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
        "full_url": "https://ua.jooble.org/desc/3829956827799475430?ckey=junior+python&rgn=-1&pos=3&elckey=7310617906279186082&p=1&sid=8697858405275103032&age=256&relb=100&brelb=100&bscr=46208.1006748641&scr=46208.1006748641&iid=-9043907292084026087",
        "url": 'https://bit.ly/33bKdpu',
        "date_created": "2020-09-30 18:01:16.901136",
        "livetime": 90
    },
    {
        "id": 1,
        "full_url": "https://ua.jooble.org/desc/8937534960256301908?ckey=junior+python&rgn=-1&pos=4&elckey=7310617906279186082&p=1&sid=8697858405275103032&age=592&relb=100&brelb=115&bscr=46141.2703960186&scr=46141.2703960186&iid=-3795500961814566229",
        "url": 'https://bit.ly/33bKdpr',
        "date_created": "2020-09-30 18:01:16.901136",
        "livetime": 90
    },
    {
        "id": 2,
        "full_url": "https://ua.jooble.org/desc/5553739797992449502?ckey=junior+python&rgn=-1&pos=5&elckey=7310617906279186082&p=1&sid=8697858405275103032&age=448&relb=100&brelb=100&bscr=45632.3665065175&scr=45632.3665065175&iid=-411529993657535455",
        "url": 'https://bit.ly/33bKdpt',
        "date_created": "2020-09-30 18:01:16.901136",
        "livetime": 400
    },
     {
        "id": 3,
        "full_url": "https://ua.jooble.org/desc/5553739797992449502?ckey=junior+python&rgn=-1&pos=5&elckey=7310617906279186082&p=1&sid=8697858405275103032&age=448&relb=100&brelb=100&bscr=45632.3665065175&scr=45632.3665065175&iid=-411529993657535455",
        "url": 'https://bit.ly/33bKdpt',
        "date_created": "2020-09-20 18:01:16.901136",
        "livetime": 185
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
                    if date_diff_default <= 90:
                        return "url old", 200
                    return url, 200

                elif url["livetime"] != 90:
                    date_diff = (date_now - date_created).days
                    if date_diff <= 0:
                        return "url old", 200
                    return url, 200
        return "url not found", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("full_url")
        parser.add_argument("date_created")
        parser.add_argument("livetime", default=90)
        params = parser.parse_args()
        for url in urls:
            if (id == url["id"]):
                return f"url with hash {id} already exists", 400
        url = {
            "id": int(id),
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
