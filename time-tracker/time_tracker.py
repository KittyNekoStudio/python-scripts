from datetime import date

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


def init():
    """
    Opens the time tracker file and gets all the previous times
    Returns the file time stored as a dictionary
    """
    file = open("template-time-tracker.md", "r")
    time = getPreviousTimes(file)
    file.close()

    return time


time = init()

print(time)
