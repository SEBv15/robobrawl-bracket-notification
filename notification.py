import datetime

def notifyMatchSoon(team, matchTime, minutesUntil):
    print(" ".join([str(datetime.datetime.now()),"Team", team["name"], "has a match in", str(minutesUntil), "minutes"]))

def notifyTimeChanged(team, matchTime):
    print(" ".join([str(datetime.datetime.now()),"Match time for team",team["name"],"has changed to",str(matchTime)]))
