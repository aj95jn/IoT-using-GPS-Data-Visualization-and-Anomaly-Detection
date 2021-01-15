"""
GPS PROJECT CHECKPOINT 1: Parse an input GPS file and convert to a kml file that can be rendered on Google Earth.

GROUP 13 SUBMISSION

MEMBERS: VAISHNAVI BADAME
"""

"""
A function that will create the kml file required with the longitude, latitude and speed in knots file that can be 
rendered on google earth to show us a path.
"""


def detect_turn(o_angle, o_long, o_lat, n_angle):
    f_angle = float(n_angle) - float(o_angle)  # Obtaining difference between the angles of the considered
    # consecutive points
    with open("GPS_Hazards1.kml", "a") as pl:
        if f_angle < 0 and abs(f_angle) >= 30:  # code for detected left turn
            pl.write("""\t<Placemark>\n"""
                     """\t\t<description>Red PIN for A Stop</description>\n"""
                     """\t\t<Style id="normalPlacemark">\n"""
                     """\t\t\t<IconStyle>\n"""
                     """\t\t\t\t<color>ff0000ff</color>\n"""
                     """\t\t\t\t<Icon>\n"""
                     """\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/3.png</href>\n"""
                     """\t\t\t\t</Icon>\n"""
                     """\t\t\t</IconStyle>\n"""
                     """\t\t</Style>\n"""
                     """\t\t<Point>\n"""
                     """\t\t\t <coordinates>""")
            pl.write("%0.6f,%0.6f\n" % (o_long, o_lat))
            pl.write("""\t\t\t</coordinates>\n"""
                     """\t\t</Point>\n"""
                     """\t</Placemark>\n""")
            print("left turn starting at: ", o_long, o_lat)
        elif f_angle > 0 and abs(f_angle) >= 30:  # code for detected right turn
            pl.write("""\t<Placemark>\n"""
                     """\t\t<description>Red PIN for A Stop</description>\n"""
                     """\t\t<Style id="normalPlacemark">\n"""
                     """\t\t\t<IconStyle>\n"""
                     """\t\t\t\t<color>ff0000ff</color>\n"""
                     """\t\t\t\t<Icon>\n"""
                     """\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/4.png</href>\n"""
                     """\t\t\t\t</Icon>\n"""
                     """\t\t\t</IconStyle>\n"""
                     """\t\t</Style>\n"""
                     """\t\t<Point>\n"""
                     """\t\t\t <coordinates>""")
            pl.write("%0.6f,%0.6f\n" % (o_long, o_lat))
            pl.write("""\t\t\t</coordinates>\n"""
                     """\t\t</Point>\n"""
                     """\t</Placemark>\n""")
            print("right turn starting at: ", o_long, o_lat)


def renderkml():
    name = input("Enter the file name: ")  # Getting the file name from the user
    gps_file = open(name, "r")  # opening the input gps file
    data = gps_file.readlines()[5:]  # skipping the first 5 lines that were no required.
    data_counter = 0
    stopList = []
    with open("GPS_Hazards1.kml", "a") as pl:
        pl.seek(0)
        pl.truncate()  # Truncate the previous contents in the file
        pl.seek(0)
        pl.write("""<Document>\n""")

    with open("GPS_Hazards2.kml", "a") as pl:
        pl.seek(0)
        pl.truncate()  # Truncate the previous contents in the file
        pl.seek(0)
        pl.write("""<Document>\n""")

    """
    Opening file in write mode and writing the specified xml tags necessary to the kml file.
    """
    speedlist = []  # a list of speeds in knots from GPRMC
    for line in data:  # iteratingover all lines from input gps file
        attributes = line.split(",")  # splitting each line on a ','
        if attributes[0] == "$GPRMC" and len(attributes) == 13 and attributes[2] == 'A' and (
                attributes[1] != " " or attributes[2] != " " or attributes[3] != " " or attributes[4] != " " or
                attributes[5] != " " or attributes[6] != " " or attributes[7] != " " or attributes[8] != " " or
                attributes[9] != " " or attributes[12] != " " or attributes[
                    13] != " "):  # data cleaning in terms of length of attribute

            lat = float(attributes[3])  # assigning original latitude value
            if attributes[4] == 'S':  # check for + or - (if South, -, else positive)
                lat = -lat

            """
            Code to get degrees and minutes from the latitude value extracted above
            """
            lat_indegrees = int(lat / 100)  # getting tne degrees, no time included
            min_in_lat = lat - (lat_indegrees * 100)
            final_time_in_mins1 = (min_in_lat / 60)
            latitude = lat_indegrees + final_time_in_mins1  # final latitude value

            """
            Code to extract longitude value and get degrees and minutes just as in latitude above
            """
            long = float(attributes[5])
            if attributes[6] == 'W':
                long = -long

            long_indegrees = int(long / 100)
            min_in_long = long - (long_indegrees * 100)
            final_time_in_mins2 = (min_in_long / 60)
            longitude = long_indegrees + final_time_in_mins2

            """
            Extract thespeed value from '$GPRMC' then write to kml file and use same value for the immediate 
            next '$GPGGA'
            """
            speed_in_knots = float(attributes[7])
            speedlist.append(speed_in_knots)
            if (speed_in_knots == 0.00):
                stopList.append([longitude, latitude, speed_in_knots])

            if data_counter == 0:
                old_angle = attributes[8]
                old_lat = latitude
                old_long = longitude

            data_counter += 1

            if data_counter == 7:
                detect_turn(old_angle, old_long, old_lat, attributes[8])
                data_counter = 0

        else:  # same for '$GPGGA' case, only positions where values are found change
            continue

    """
    Writing the closing tag for the kml file
    """
    with open("GPS_Hazards1.kml", "a") as pl:
        pl.write("""</Document>\n""")

    with open("GPS_Hazards2.kml", "a") as pl:
        for items in stopList:
            pl.write("""\t<Placemark>\n"""
                     """\t\t<description>Red PIN for A Stop</description>\n"""
                     """\t\t<Style id="normalPlacemark">\n"""
                     """\t\t\t<IconStyle>\n"""
                     """\t\t\t\t<color>ff0000ff</color>\n"""
                     """\t\t\t\t<Icon>\n"""
                     """\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n"""
                     """\t\t\t\t</Icon>\n"""
                     """\t\t\t</IconStyle>\n"""
                     """\t\t</Style>\n"""
                     """\t\t<Point>\n"""
                     """\t\t\t <coordinates>""")
            pl.write("%0.6f,%0.6f,%0.2f \n" % (items[0], items[1], items[2]))
            pl.write("""\t\t\t</coordinates>\n"""
                     """\t\t</Point>\n"""
                     """\t</Placemark>\n""")

    with open("GPS_Hazards2.kml", "a") as pl:
        pl.write("""</Document>\n""")


"""
main function that call the required function render kml that will make the kml file
"""


def main():
    renderkml()


if __name__ == '__main__':
    main()