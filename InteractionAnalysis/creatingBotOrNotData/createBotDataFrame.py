import json
import this
from numpy import count_nonzero
import pandas as pd

i = 0

with open(r"..\..\botvalues.txt") as f:
    bots = []
    data = f.readlines()
    for index, line in enumerate(data):
        json_line = json.loads(line.strip())
        cap_Uni = json_line['cap']['universal']
        cap_Eng = json_line['cap']['english']
        user = json_line["user"]
        lang = user['majority_lang']
        username = user['user_data']['screen_name']
        userId = user['user_data']['id']
        verified = user['user_data']['verified']
        count_tweets = user['user_data']['statuses_count']

        scores = json_line['raw_scores']
        for key, value in scores.items():
            thisuser = {
                "user": username,
                "id": userId,
                "majority_lang": lang,
                "current_lang": key,
                "verified":verified,
                "count_tweets_total":count_tweets
            }
            for subkey, subvalue in value.items():
                thisuser[subkey] = subvalue
                if(subkey == 'universal'):
                    thisuser['cap'] = cap_Uni
                else:
                    thisuser['cap'] = cap_Eng
            bots.append(thisuser)
df = pd.DataFrame(bots)

df2 = pd.read_json(
    r'..\..\DataSources\user_accounts_list_war.json',  typ='series').to_frame()
df2 = df2.reset_index()
df2.columns = ['id', 'count_tweets_at_bellingcat']


dfeng = df[df['current_lang'] == 'english']
dfuni = df[df['current_lang'] == 'universal']

#
mergedfeng = pd.merge(dfeng, df2,  on='id', how='left')
mergedfuni = pd.merge(dfuni, df2,  on='id', how='left')

mergedfeng.to_csv(r"..\..\BotsEng.csv", index=False)
mergedfuni.to_csv(r"..\..\DataSources\BotsUni.csv", index=False)
