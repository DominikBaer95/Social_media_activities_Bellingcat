import getDatafromEndpoint as getData
from time import sleep
import json

def getUserTimeline(user_id=""):
    url = "https://api.twitter.com"
    strEndpointURL1 = "/1.1/statuses/user_timeline.json"
    strEndpointURL = url + strEndpointURL1

    query = {
        'user_id': user_id, # +'893885808',
        'count': 200, 
        'include_rts': True , 
    }

    json_response = getData.from_Twitter(
        query=query, strEndpointURL=strEndpointURL, hasexpansions=False)
    return json_response


# will be variable in loop  Can be found on the Context Provider>Xl>l
#author_id = "2315512764"
# ?tweet.fields=" + author_id + "&" + "query=url:" + conversation_id
def getUserMentions(username):
    url = "https://api.twitter.com"
    strEndpointURL1 = "/1.1/search/tweets.json"
    strEndpointURL = url + strEndpointURL1

    query = {
        'q': str(username),
        'count': '100',
    }

    json_response = getData.from_Twitter(
        query=query, strEndpointURL=strEndpointURL, hasexpansions=False)
    with open("MichaelTweet.txt", mode='a') as json_file:
            json_file.write(json.dumps(json_response, indent=2))
            json_file.write("\n")
    return (json_response['statuses']) #we only need statuses for Bot or not. 


# will be variable in loop  Can be found on the Context Provider>Xl>l
# ?tweet.fields=" + author_id + "&" + "query=url:" + conversation_id
def getUserProfile(user_id=""):
    url = "https://api.twitter.com"
    strEndpointURL1 = "/1.1/users/show.json"
    strEndpointURL = url + strEndpointURL1

    query = {
        'id': user_id,  # +'893885808',
        'include_entities': 'false',
    }

   
    json_response = getData.from_Twitter(
        query=query, strEndpointURL=strEndpointURL, hasexpansions=False)
        # Prepares the data for the BotorNot
    return json_response

