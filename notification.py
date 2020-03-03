import datetime

def notifyMatchSoon(team, minutesUntil):
    print(" ".join([str(datetime.datetime.now()),"Team", team["name"], "has a match in", str(minutesUntil), "minutes"]))

def notifyTimeChanged(team, date, time):
    print(" ".join([str(datetime.datetime.now()),"Match time for team",team["name"],"has changed to",time,date]))
