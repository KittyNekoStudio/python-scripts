from datetime import date

# TODO!
# To get the total of time for an activity as I read through the file getting the times
# I should store every unique activity, then look over all days and add the times together

def getPreviousTimes(file):
    """
    Takes a file and reads from it
    returns time dictionary
    """

    file.seek(0)
    string = file.read()
    print(string)

    return {}


def init():
    file = open("time-tracker.md", "a+")
    time = getPreviousTimes(file)

    return (file, time)


(file, time) = init()
file.close()

print(time)

