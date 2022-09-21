import json
from operator import mod
import getUserData as GUD
from time import sleep

# Creates the BototNot object to be fed to the API

AllUsers = []
counter = 0
secondcounter = 1
# Loop here then addd to full dict

with open(r'..\..\DataSources\user_accounts_list_war.json') as json_file:
    idDict = json.loads(json_file.read())
    shortDict = {k: v for k, v in sorted(
        idDict.items(), key=lambda item: item[1], reverse=True)}
    suspended = 0
    print("Starting")
    for key in shortDict:
        print(key)
        userDict = {'user': {}, "timeline": {}, "mentions": {}}
        try:
            userProfile = GUD.getUserProfile(key)

            # userDict['user']['id'] = userProfile['id']
            userDict['user'] = userProfile

            username = "@" + userProfile['screen_name']
            timeline = GUD.getUserTimeline(key)
            userDict['timeline'] = timeline

            mentions = GUD.getUserMentions(username=username)
            userDict['mentions'] = mentions

            AllUsers.append(userDict)
            sleep(14)
            counter = counter + 1
            if counter >= 200:
                filename = r"..\..\DataSources\interaction" + str(secondcounter) + ".json"
                with open(filename, mode='x') as new_json:
                    new_json.write(json.dumps(AllUsers))
                AllUsers.clear()
                print(counter)
                secondcounter = secondcounter + 1
                counter = 0
        except:
            print("excepted")
            sleep(14)
            suspended = suspended + 1
            pass


print(suspended)
print(counter)

# This Dataset is not complete inside our repository. 
with open(r"..\..\DataSources\interaction.json", mode='a') as new_json:
    new_json.write(json.dumps(AllUsers))
