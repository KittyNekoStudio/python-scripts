import argparse
from datetime import date
from pathlib import Path

# TODO!
# To get the total of time for an activity as I read through the file getting the times
# I should store every unique activity, then look over all days and add the times together

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
                        help = "Prints the total time of an activity, or all if no argument is passed.",
                        metavar = ("ACTIVITY"))

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

if args.add:
    addNewTime(args.add)
elif args.total:
    print("Not implemented")

#time = getTime()
#print(time)
