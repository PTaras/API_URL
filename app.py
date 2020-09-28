from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import datetime
import bitly_api

app = Flask(__name__)
api = Api(app)

con = bitly_api.Connection(access_token='3247522728e81c5c7402d8553c4faf43b214d005')

urls = [
    {
        "hash": 0,
        "full_url": "https://ua.jooble.org/desc/3829956827799475430?ckey=junior+python&rgn=-1&pos=3&elckey=7310617906279186082&p=1&shash=8697858405275103032&age=256&relb=100&brelb=100&bscr=46208.1006748641&scr=46208.1006748641&ihash=-9043907292084026087",
        "url": 'https://bit.ly/33bKdpu',
        "date_created": "2020-09-28 16:58:16.131995"
    },
    {
        "hash": '33bKdpr',
        "full_url": "https://ua.jooble.org/desc/8937534960256301908?ckey=junior+python&rgn=-1&pos=4&elckey=7310617906279186082&p=1&shash=8697858405275103032&age=592&relb=100&brelb=115&bscr=46141.2703960186&scr=46141.2703960186&ihash=-3795500961814566229",
        "url": 'https://bit.ly/33bKdpr',
        "date_created": "2020-09-28 16:58:16.131995"
    },
    {
        "hash": '33bKdpt',
        "full_url": "https://ua.jooble.org/desc/5553739797992449502?ckey=junior+python&rgn=-1&pos=5&elckey=7310617906279186082&p=1&shash=8697858405275103032&age=448&relb=100&brelb=100&bscr=45632.3665065175&scr=45632.3665065175&ihash=-411529993657535455",
        "url": 'https://bit.ly/33bKdpt',
        "date_created": "2020-09-28 16:58:16.131995"
    }
]


class URL(Resource):
    def get(self, hash=0):
        if hash == 0:
            return urls, 200
        for url in urls:
            if (url["hash"] == hash):
                return url, 200
        return "url not found", 404

    def post(self, hash):
        parser = reqparse.RequestParser()
        parser.add_argument("full_url")
        parser.add_argument("date_created")
        params = parser.parse_args()
        for url in urls:
            if (hash == url["hash"]):
                return f"url with hash {hash} already exists", 400
        url = {
            "hash": (con.shorten(params["full_url"]))['hash'],
            "full_url": params["full_url"],
            "url": (con.shorten(params["full_url"]))['url'],
            "date_created": str(datetime.utcnow())
        }
        urls.append(url)
        return url, 201

    def put(self, hash):
        parser = reqparse.RequestParser()
        parser.add_argument("full_url")
        parser.add_argument("date_created")
        params = parser.parse_args()
        for url in urls:
            if (hash == url["hash"]):
                url["full_url"] = params["full_url"]
                url["url"] = (con.shorten(params["full_url"]))['url']
                # url["date_created"] = datetime.now()
                return url, 200

        url = {
            "hash": (con.shorten(params["full_url"]))['hash'],
            "full_url": params["full_url"],
            "url": (con.shorten(params["full_url"]))['url'],
            "date_created": str(datetime.utcnow())
        }

        urls.append(url)
        return url, 201

    def delete(self, hash):
        global urls
        urls = [url for url in urls if url["hash"] != hash]
        return f"url with hash {hash} is deleted.", 200


api.add_resource(URL, "/urls", "/urls/", "/urls/<string:hash>")
if __name__ == '__main__':
    app.run(debug=True)
