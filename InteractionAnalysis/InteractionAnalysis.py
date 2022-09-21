import pandas as pd
from time import strptime
import pandas as pd
import numpy as np
import datetime
import dateutil.parser as dateparse
import json

splitdate = datetime.datetime(2022,2,24)
delta = datetime.timedelta(days=100)
threshold = 0.50

def getRepliesByMediaWar():
    f1 = r'..\..\DataSources\replies_with_media_war.xlsx'
    tweetdf = pd.read_excel(f1)
    return tweetdf


def getUniqueAccountList():
    f1 = r"..\..\DataSources\user_accounts_list_war.csv"
    df = pd.read_csv(f1)
    df.columns = ['author_id', 'Date', 'count']
    return df


def getBotsList():
    botList = pd.read_csv(
        r"..\..\DataSources\BotsUni.csv")
    return botList


def createUserRepliesbyAccountCount():
    f = open("..\..\raw\replies_with_media_war.json", "r")

    data = json.loads(f.read())
    df = pd.DataFrame()

    for tweet in data:
        record = []
        if "meta" in tweet:  # Revisar
            print("meta")
        else:
            record.append(tweet["author_id"])
            record.append(tweet["created_at"])
            df = pd.concat([df, pd.DataFrame(record).T], ignore_index=True)

    df = df.sort_values(by=['author_id'])

    df2 = getUniqueAccountList()


    df = df.merge(df2, how='left', on='id')
    df = df.sort_values(by=['created_at'])
    df = df.drop_duplicates(subset=['id'])

    return df


# Takes repliesByAccountCount and Attaches bot score to each. Returns Full Data Set
def allAccounts_AttachBotScore(df):
    try:
        df["Date"] = pd.to_datetime(df['created_at']).dt.tz_localize(None)
    except:
        df["Date"] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    botList = getBotsList()
    botList = botList.set_index('id')
    allBots = pd.merge(botList, df, left_index=True, right_index=True)
    return allBots

# Takes Dateframe and returns Before After Dataframes


def getBeforeAfterDf(df):
    date = datetime.datetime(2022, 2, 24)
    splitdate = np.datetime64(date)

    try:
        df["Date"] = pd.to_datetime(df['date']).dt.tz_localize(None)
    except:
        try:
            df["Date"] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        except:
            df["Date"] = pd.to_datetime(df['created_at']).dt.tz_localize(None)

    beforeList = df[df['Date'] < splitdate]
    afterList = df[df['Date'] > splitdate]

    return (beforeList, afterList)


def getBotsByConversationType_Count():
    f1 = r'C:\Github\Bellingcat\DataSources\Bellingcat_Conversations_Type_war.xlsx'
    f3 = r'C:\Github\Bellingcat\DataSources\FaustoRepliesData.csv'

    convtypedf = pd.read_excel(f1, usecols=['conversation_id', 'Final Type'])
    tweetdf = getRepliesByMediaWar()['conversation_id', 'id']

    df = tweetdf.merge(convtypedf, on='conversation_id')
    df = df.drop(['conversation_id'], axis=1)
    fdf = pd.read_csv(f3)

    complete = fdf.merge(df, on='id')

    other = complete.groupby(['Final Type', 'botlike'])[
        'id'].count().reset_index()

    return df


def createRepliesHashtags():
    f2 = r'..\..\raw\replies_with_media_war.json'

    data = json.loads(open(f2, "r").read())
    df = pd.DataFrame()

    for tweet in data:
        if "meta" in tweet:
            print("meta")
        else:
            if "entities" in tweet:
                if "hashtags" in tweet["entities"]:
                    for hashtag in tweet["entities"]['hashtags']:
                        record = []
                        record.append(tweet["id"])
                        record.append(tweet["author_id"])
                        record.append(hashtag['tag'])
                        df = pd.concat(
                            [df, pd.DataFrame(record).T], ignore_index=True)

    df.columns = ['id', 'author_id', 'hashtag']
    
    return df

# Takes a BotsDF and Merges Bot Score Account Data to each Tweet
def mergeRepliestoBot(df):
    df = df.set_index('id')
 
    repliesdf = getRepliesByMediaWar()
    repliesdf = repliesdf.set_index('author_id')
    fulldf = pd.merge(repliesdf, df, left_index=True, right_index=True)
    return fulldf


def appendTimePeriodCol(df):
    date = datetime.datetime(2022, 2, 24)
    splitdate = np.datetime64(date)

    df['time_period'] = np.where(df['Date'] > splitdate, 'After', 'Before')

    return df


def appendTypeBots(df):
    df['type'] = df[["astroturf",
                    "fake_follower",
                     "financial",
                     "other",
                     "self_declared",
                     "spammer"]].idxmax(axis=1)
    return df

def applyThreshold(df):
    return df[df['overall'] > threshold] 

def applyAntiThreshold(df):
    return df[df['overall'] <= threshold]
# ------------------------------- # 
# Next Section for Analysis

def analyzeBotsHashtags():
    createRepliesHashtags()
    bdf = getBotsList()[['overall', 'id']]
    bdf = bdf.set_index('id')
    df = pd.merge(tdf, bdf, left_index=True, right_index=True)

    print(df[df['overall']>0.43]['hashtag'].value_counts())
    return df

def analyze_absoluteNumber():
    df = getUniqueAccountList()
    df = df.set_index('author_id')
    bots = allAccounts_AttachBotScore(df)
    bdf, adf = getBeforeAfterDf(bots)
    beforeNumber = bdf[bdf['overall'] > threshold]['user'].count()
    afterNumber = adf[adf['overall'] > threshold]['user'].count()
    return (beforeNumber, afterNumber)

def analyze_Language(df):
    values = df.majority_lang.value_counts(normalize=True)
    return values

def analyze_attachment(df):
    df['Sum'] = df['media_photo'] + df['media_videos']  + df['hashtags'] + df['urls']
    return df

def analyze_BotType():
    df = getUniqueAccountList()
    df = df.set_index('author_id')
    bots = applyThreshold(allAccounts_AttachBotScore(df))
    
    bdf, adf = getBeforeAfterDf(appendTypeBots(bots))
    print("Pre:" , bdf["type"].value_counts(normalize=True))
    print("Post: ", adf["type"].value_counts(normalize=True))

def analyze_FollowerIncrease():
    f = r"..\..\DataSources\Followers_final.xlsx"

    df = pd.read_excel(f)

    pre = df[df['Date'] == splitdate - delta]
    post = df[df['Date'] > splitdate + delta]
    onDate = df[df['Date'] == splitdate]

    # Tweets per Follower average
    print(pre['followers'])
    print(onDate['followers'])
    print(post['followers'])

# Type here refers to the column name. 
def describe_threshold(df, type):
    return df[df[type] > threshold].describe()


def count_threshold(df, type):
    return df[df[type] > threshold]['id'].count()


def compare_amount_bythreshold(newthreshold, type):
    first = count_threshold(threshold, type)
    second = count_threshold(newthreshold, type)
    return (first - second)/first

def IncreaseInBotLikeAccounts():
    print(getBeforeAfterDf(applyThreshold(getBotsList())))


def AmountOfContentCreated(): 
    before,after = getBeforeAfterDf(getRepliesByMediaWar())
    amountBefore = before['id'].count()
    amountAfter = after['id'].count()
    botsBefore, botsAfter = getBeforeAfterDf(mergeRepliestoBot(applyThreshold(getBotsList())))
    print(botsBefore['id'].count()) # / amountBefore)
    print(botsAfter['id'].count() ) #/ amountAfter)

def TypeOfBotLikeAccounts():
    analyze_BotType()

def AttachmentDifferenceBots():
    df = mergeRepliestoBot(applyThreshold(getBotsList()))
    df2 = analyze_attachment(df)
    before, after = getBeforeAfterDf(df2)
    print('before media_photo ' , before['media_photo'].sum())
    print('before media_videos ' , before['media_videos'].sum())
    print('before hashtags ' , before['hashtags'].sum())
    print('before urls ' , before['urls'].sum())
    print(before['Sum'].sum())
    print('--------------------------------------------------------')
    print('after media_photo ' , after['media_photo'].sum())
    print('after media_videos ' , after['media_videos'].sum())
    print('after hashtags ' , after['hashtags'].sum())
    print('after urls ' , after['urls'].sum())
    
    print(after['Sum'].sum())

def AttachmentDifference():
    df = mergeRepliestoBot(applyAntiThreshold(getBotsList()))
    df2 = analyze_attachment(df)
    before, after = getBeforeAfterDf(df2)

    print('before media_photo ' , before['media_photo'].sum())
    print('before media_videos ' , before['media_videos'].sum())
    print('before hashtags ' , before['hashtags'].sum())
    print('before urls ' , before['urls'].sum())
    print(before['Sum'].sum())
    print('--------------------------------------------------------')
    print('after media_photo ' , after['media_photo'].sum())
    print('after media_videos ' , after['media_videos'].sum())
    print('after hashtags ' , after['hashtags'].sum())
    print('after urls ' , after['urls'].sum())
    
    print(after['Sum'].sum())

print('============BOTS====================')
AttachmentDifferenceBots()
beforeTotal, afterTotal = getBeforeAfterDf(mergeRepliestoBot(applyThreshold(getBotsList())))
print('before total ' , beforeTotal['id'].count())
print('after total ' , afterTotal['id'].count())

print('============NOT BOTS====================')
AttachmentDifference()
beforeTotal1, afterTotal1 =  getBeforeAfterDf(mergeRepliestoBot(applyAntiThreshold(getBotsList())))
print('before total ' , beforeTotal1['id'].count())
print('after total ' , afterTotal1['id'].count())




