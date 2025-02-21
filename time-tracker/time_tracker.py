import argparse
import math
from datetime import date
from pathlib import Path

def stripFile(file):
    """
    Takes a file pointer reads it into a list and strips the unwanted strings
    Returns the striped file as a list
    """

    lines = file.readlines()

    # Removes comments
    lines = [line for line in lines if "\"" not in line]

    for index in range(len(lines)):
        lines[index] = lines[index].replace("\n", "")

    # Removes empty strings
    lines = list(filter(None, lines))

    return lines


def getPreviousTimes(file):
    """
    Takes a file and returns a dictionary that stores the time
    """

    lines = stripFile(file)

    time = {}

    day = ""
    for line in lines:
        if "##" in line:
            line = line.replace("## ", "")
            time[line] = {}
            day = line
        else:
            line = line.replace("- ", "")
            (activity, leftover) = line.split(":", 1)

            times = leftover.split(":", 2)
            time[day][activity] = (int(times[0]), int(times[1]), int(times[2]))

    return time


def getTime():
    """
    Opens the time tracker file and gets all the previous times
    Returns the file time stored as a dictionary
    """
    try:
        with open(FILENAME, "r") as file:
            time = getPreviousTimes(file)
    except:
        with open(FILENAME, "x"):
            time = {}

    return time


def initArgParse():
    parser = argparse.ArgumentParser(description = "Stores the time given by the user. Can give the total amount of time spent on an activity.")
    parser.add_argument("-a", "--add", nargs = 4,
                        help = "Store a new time value",
                        metavar = ("[ACTIVITY]", "[HOUR]", "[MINUTE]", "[SECOND]"))
    parser.add_argument("-t", "--total",
                        nargs = "?",
                        const = "all",
                        help = "Prints the total time of an activity, or all if no argument is passed.",
                        metavar = ("ACTIVITY"))
    parser.add_argument("-d", "--date", nargs = 2,
                        help = "Takes in month as number `1-12` and year as full year `2025`. Cannot be used withou `-t` flag. Prints the total time for an activity for a given month of a given year.",
                        metavar = ("[MONTH]", "[YEAR]"))

    args = parser.parse_args()

    return args


def activityAlreadyRecorded(activity, keys):
    """
    Takes the activity as a string and all activities in a day to compare against
    Returns true if activity has already been recorded
    """

    activity = activity.split("-", 1)[0]

    for i in range(len(keys)):
        j = keys[i].split("-", 1)[0]
        keys[i] = j

    return activity in keys


def addCurrentDate():
    """
    Adds current date to time-tracker file
    """
    time = getTime()
    if str(date.today()) not in time.keys():
        with open(FILENAME, "a") as file:
            file.write("\n" + "## " + DATE + "\n\n")


def getTotalTime(activity):
    """
    Takes all the activity and adds up all the time for that activity
    If no activity is passed activity it returns total time for all activities
    Returns a tuple of total times
    """
    time = getTime()
    totals = []
    values = []

    if activity == "all":
        print("Not implemented")
        return

    for outer_key in time.keys():
        for inner_key in time[outer_key].keys():
            if activity in inner_key:
                values.append(time[outer_key][inner_key])

    if values == []:
        print("Activity not found")
        return

    total = [0, 0, 0]
    for value in values:
        total[0] += value[0]
        total[1] += value[1]
        total[2] += value[2]

    seconds = 0
    seconds += total[0] * 3600
    seconds += total[1] * 60
    seconds += total[2]

    hours = math.trunc(seconds / 3600)
    minutes = math.trunc((seconds / 3600 - hours) * 60)
    seconds = math.trunc((((seconds / 3600 - hours) * 60) - minutes) * 60)
    total = [hours, minutes, seconds]

    return (activity, total)


def printTotalTime(total):
    """
    Takes a tuple of total times and the activity and prints them to stdout
    Returns nothing
    """
    if total is None:
        return

    activity = total[0]
    hours = total[1][0]
    minutes = total[1][1]
    seconds = total[1][2]

    print(activity + ": " + str(hours) + ":" + str(minutes) + ":" + str(seconds))


def addNewTime(newTime):
    """
    Takes a list storing the activity as a string and time
    Makes a new activity for the day or adds to it if it exists
    """

    activity = newTime[0]
    time = (newTime[1], newTime[2], newTime[3])
    previousTimes = getTime()

    if activityAlreadyRecorded(activity, list(previousTimes[DATE].keys())):
        lastSameActivity = ""
        for i in previousTimes[DATE].keys():
            if activity in i:
                lastSameActivity = i

        number = lastSameActivity.split("-", 1)[1]
        activity += "-" + str(int(number) + 1)
    else:
        activity += "-1"

    with open(FILENAME, "a") as file:
        file.write("- " + activity + ": " + time[0] + ":" +  time[1] + ":" +  time[2] + "\n")


FILENAME = str(Path.home()) + "/.timetracker.md"
DATE = str(date.today()) #"2025-1-21" 

addCurrentDate()

args = initArgParse()

# TODO! add total time by month
# TODO! add total time for all activities

if args.add:
    addNewTime(args.add)
elif args.total:
    if args.date:
        print("Date argument not implemented")
    total = getTotalTime(args.total)
    printTotalTime(total)
elif args.date:
    print("Cannot be used by itself, please use with `-t` total argument")

#time = getTime()
#print(time)
