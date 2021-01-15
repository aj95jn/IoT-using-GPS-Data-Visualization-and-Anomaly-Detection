"""
GPS PROJECT FINAL BEST PATH FILE SUBMISSION: find the file name that has the best cost function as per defined.

GROUP 13 SUBMISSION

MEMBERS: VAISHNAVI BADAME
"""
import datetime # convert or do date manipulations
import glob # used for reading multiple files at once


def renderkml():

    final_cost_function = [] # final list that will hold all files cost function calculted
    file_name = [] # final file list that holds the file names

    """
    Code to read all 173 files present in one file
    """
    path = "C:/Users./ANKIT JAIN/Desktop/Masters Study Material/2nd SEM MATERIAL/Big data Analytics/GPS PROJECT/FILES/FILES_TO_WORK/*.txt"
    files = glob.glob(path)
    for name in files:  # a loop over all files to find cost function and hence, find minimum or best route
        gps_file = open(name, "r")  # opening the input gps file
        data = gps_file.readlines()[5:]  # skipping the first 5 lines that were no required.
        if len(data) > 100:  # data cleaning so as to consider a significant amount of points to find cost function
            count = 0
            points = 0
            times = {}  # a dictionary to hold key as points that act as row id and a list corresponding to
            # every id for all speeds where it is 0
            start_time = [] # a list to keep the first time record from the input file
            lastline = ""

            """
            A loop to find find the first or start time of the trip
            """
            for lines in data:
                if lines.split(",")[0][0:3] != "lng" and not lines.isspace() and not lines.split(",")[0] == "$GPVTG" and not lines.split(",")[0] == "$GPGSA":
                    lastline = lines
                att = lines.split(",")
                count = count + 1
                if count == 1:
                    start_time.append(att[1])

            """
            code to calculate the overall trip time
            """
            final_time = lastline.split(",")[1] # read the last line and take the time from 1st attribute
            start = start_time[0] # start time of trip
            datetimeFormat = '%H:%M:%S.%f' # conversion or display format
            time1 = final_time[0:2] + ":" + final_time[2:4] + ":" + final_time[4:]
            time2 = start[0:2] + ":" + start[2:4] + ":" + start[4:]

            # calculating the difference between end and start to get final trip time
            diff = datetime.datetime.strptime(time1, datetimeFormat) - datetime.datetime.strptime(time2, datetimeFormat)
            # print("The difference is: ", diff)
            trip_inMins = round((1 / 60) * diff.seconds, 2) # trip time in minutes
            # print("Trip time in minutes is: ",trip_inMins)


            speedlist = []  # a list of speeds in knots from GPRMC
            for line in data:  # iteratingover all lines from input gps file
                attributes = line.split(",")  # splitting each line on a ','

                """
                The following if is used as a data cleaning step so that no erroneous input is taken
                """
                if attributes[0] == "$GPRMC" and len(attributes) == 13 and attributes[2] == 'A' and (
                        attributes[1] != " " or attributes[2] != " " or attributes[3] != " " or attributes[4] != " " or
                        attributes[5] != " " or attributes[6] != " " or attributes[7] != " " or attributes[8] != " " or
                        attributes[9] != " " or attributes[12] != " " or attributes[13] != " "):

                    lat = float(attributes[3])  # assigning original latitude value
                    if attributes[4] == 'S':  # check for + or - (if South, -, else positive)
                        lat = -lat

                    lat_indegrees = int(lat / 100)  # getting tne degrees, no time included
                    min_in_lat = lat - (lat_indegrees * 100)
                    final_time_in_mins1 = (min_in_lat/60)
                    latitude = lat_indegrees + final_time_in_mins1  # final latitude value

                    long = float(attributes[5])
                    if attributes[6] == 'W':
                        long = -long

                    long_indegrees = int(long / 100)
                    min_in_long = long - (long_indegrees * 100)
                    final_time_in_mins2 = (min_in_long/60)
                    longitude = long_indegrees + final_time_in_mins2

                    speed_in_knots = float(attributes[7])
                    speedlist.append(speed_in_knots)

                    """
                    The following if is used to give a unique point count to a series of points where 
                    speed is 0 to keep track of total wait time as in out cost function. 
                    """
                    if speed_in_knots == 0.00:
                        if (points) not in times.keys(): # if key not in dictiionary, add it with an empty list
                            times[(points)] = []
                            times[(points)].append(attributes[1]) # append the time values corresponding to ids
                        else:
                            times[(points)].append(attributes[1])
                    elif speed_in_knots != 0.00:
                        points = points + 1  # if that series of points is now not 0, increment counter for new wait series

                else:   # no need to consider gga or lng as we have all values from rmc itself
                    continue

            sum = 0
            for keys in times.keys():
                if len(times[keys]) == 1:  # if only one item in dictionary list for a given id, skip it
                    continue
                else:
                    """
                    If multiple items, take tbhe difference between last and 1st elements in that list
                    """
                    temp_t1 = times[keys][0]
                    t1 = temp_t1[0:2] + ":" + temp_t1[2:4] + ":" + temp_t1[4:]
                    temp_t2 = times[keys][-1]
                    t2 = temp_t2[0:2] + ":" + temp_t2[2:4] + ":" + temp_t2[4:]
                    diff2 = datetime.datetime.strptime(t2, datetimeFormat) - datetime.datetime.strptime(t1, datetimeFormat)
                sum += diff2.seconds  # add all such differences for all ids

            final_wait_time = round(sum * (1 / 60), 2) # this is final wait time in minutes
            # print("The total wait time is: ", final_wait_time, "minutes")

            cost_function = (trip_inMins / 30) + (1 / 10) * (final_wait_time) # self defined cost function
            # print("The final cost function is: ", cost_function)
            final_cost_function.append([cost_function])  # appending the cost value to final cost list
            file_name.append(name) # appending the corresponding file name

    min_cost_function = min(final_cost_function) # getting the minimum cost value
    print("The minimum cost function is: ", min_cost_function)
    min_cost_function_index = final_cost_function.index(min(final_cost_function)) # fetching its index from the list
    best_file_name = file_name[min_cost_function_index] # corresponding to that index, fetch file name.
    print(best_file_name)


def main():
    renderkml()


if __name__ == '__main__':
    main()
