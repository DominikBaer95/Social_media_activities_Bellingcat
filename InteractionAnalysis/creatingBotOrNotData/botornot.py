from decimal import Decimal
import requests as rq
import json
import ijson
import os


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def testaccount(data):
    url = "https://botometer-pro.p.rapidapi.com/4/check_account"
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Host': 'botometer-pro.p.rapidapi.com',
        'X-RapidAPI-Key': 'KEY' # Insert your API key 
    }

    response = rq.request("POST", url, headers=headers, json=data)
    return response.json()


counter = 0
directory = r'C:\Github\Bellingcat\DataSources\interactions'
# Higher Scores = More Bot Like Behaviour
for file in os.listdir(directory):
    print(file)
    with open(os.path.join(directory, file)) as f:
        for record in ijson.items(f, "item", use_float=True):
            counter = counter + 1
            if counter < 4479:
                print(counter)
            else:
                bot_response = testaccount(record)
                with open(r'..\..\DataSources\botvalues.txt', 'a') as bots:
                    bots.write(json.dumps(
                        bot_response, cls=JSONEncoder) + "\n")
