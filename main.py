import requests
import time
import datetime
from notification import notifyTimeChanged, notifyMatchSoon

SECRET_ACCESS_TOKEN = "secretToken"
BRACKET = "8-team-example"
MINUTES_BEFORE = 5 # amount of minutes before the match to send the notification

previous = []
notified = []

def getMatches(bracket):
    rounds = []
    for bracketRound in bracket:
        rounds += bracketRound
    return rounds

def analyzeMatch(match, index, teams):
    global previous
    global notified

    try:
    #if True:
        if (len(previous) > index):
            # check if time changed
            if (previous[index]["time"] != match["time"] or previous[index]["date"] != match["date"]):
                teamsToNotify = filter(lambda t: t["name"] in match["teams"], teams)
                # remove team from notified list so they get the "match is in N minutes" message again
                for team in teamsToNotify:
                    if team["name"] in notified: 
                        notified.remove(team["name"]) # I DON'T KNOW IF I SHOULD ACTUALLY DO THIS. WHEN PEOPLE ADJUST THE TIME RIGHT BEFORE A MATCH, PEOPLE MIGHT GET SPAMMED
                    # notify both teams
                    notifyTimeChanged(team, match["date"], match["time"])

    except:
        print("error finding time modification")
    
    try:
    #if True:
        if (match["time"]):
            if (match["date"]):
                matchTime = datetime.datetime.strptime(match["date"] + " " + match["time"], '%m/%d/%Y %I:%M:%S %p')
            else:
                matchTime = datetime.datetime.strptime(datetime.datetime.strftime(datetime.date.today(),"%m/%d/%Y") + " " + match["time"], '%m/%d/%Y %I:%M:%S %p')

            delta = matchTime - datetime.datetime.now()

            # If match is in MINUTES_BEFORE minutes, alert
            minutesUntil = delta.total_seconds()/60
            if (minutesUntil <= MINUTES_BEFORE and minutesUntil > 0):
                teamsToNotify = filter(lambda t: t["name"] in match["teams"], teams)
                for team in teamsToNotify:
                    if not team["name"] in notified:
                        notified.append(team["name"])
                        notifyMatchSoon(team, minutesUntil)
        else:
            #print("NO TIME")
            pass
    except:
        print("error parsing time")


def mainLoop():
    while True:
        # get data
        r = requests.post('https://robobrawl.strempfer.dev/wp-json/robobrawl-bracket/v1/get-formatted-bracket/' + BRACKET, data = {'token':SECRET_ACCESS_TOKEN})
        data = r.json()

        # get matches as a 1D array
        matches = getMatches(data["winners"]) + getMatches(data["losers"])

        teams = data["teams"]

        for i in range(0, len(matches)):
            analyzeMatch(matches[i], i, teams)

        # lol, globals
        global previous
        previous = matches

        # sleep 10 seconds
        time.sleep(10)

if __name__ == "__main__":
    mainLoop()
