"""
GPS PROJECT CHECKPOINT 1: Parse an input GPS file and convert to a kml file that can be rendered on Google Earth.

GROUP 13 SUBMISSION

MEMBERS: VAISHNAVI BADAME
"""

"""
A function that will create the kml file required with the longitude, latitude and speed in knots file that can be 
rendered on google earth to show us a path.
"""


def renderkml():
    """
        Getting the input text file from the user
    """
    name = input("Enter the file name: ")
    gps_file = open(name, "r")  # opening the input gps file
    data = gps_file.readlines()[5:]  # skipping the first 5 lines that were no required.

    """
    Opening file in write mode and writing the specified xml tags necessary to the kml file.
    """
    with open("GPS_Path.kml", "a") as m:
        m.seek(0)
        m.truncate()  # Truncate the previous contents in the file
        m.seek(0)
        m.write("""<?xml version="1.0" encoding="UTF-8"?>\n"""
                """<kml xmlns="http://www.opengis.net/kml/2.2">\n"""
                """<Document>\n"""
                """<Style id="yellowPoly">\n"""
                """\t<LineStyle>\n"""
                """\t\t<color>Af00ffff</color>\n"""
                """\t\t<width>6</width>\n"""
                """\t</LineStyle>\n"""
                """\t<PolyStyle>\n"""
                """\t\t<color>7f00ff00</color>\n"""
                """\t</PolyStyle>\n"""
                """</Style>\n"""
                """<Placemark><styleUrl>#yellowPoly</styleUrl>\n"""
                """\t<LineString>\n"""
                """\t\t<Description>Speed in Knots, instead of altitude.</Description>\n"""
                """\t<extrude>1</extrude>\n"""
                """\t<tesselate>1</tesselate>\n"""
                """\t<altitudeMode>absolute</altitudeMode>\n"""
                """\t<coordinates>\n""")


    fileList = []  # a list storing longitude, latitue and speed values to be written in .kml file
    speedlist = []  # a list of speeds in knots from GPRMC
    for line in data:  # iteratingover all lines from input gps file
        attributes = line.split(",")  # splitting each line on a ','
        if attributes[0] == "$GPRMC" and len(attributes) == 13 and attributes[2] == 'A' and (
                attributes[1] != " " or attributes[2] != " " or attributes[3] != " " or attributes[4] != " " or
                attributes[5] != " " or attributes[6] != " " or attributes[7] != " " or attributes[8] != " " or
                attributes[9] != " " or attributes[12] != " " or attributes[
                    13] != " "):  # data cleaning in terms of $GPRMC files

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

            fileList.append([longitude, latitude, speed_in_knots])
        else:
            continue

    """
    Writing the co-ordinates to the kml file along with the respective speeds
    """
    with open("GPS_Path.kml", "a") as m:
        for items in fileList:
            m.write("%0.6f,%0.6f,%0.2f \n" % (items[0], items[1], items[2]))


    """
    Writing the closing tags for the kml file
    """
    with open("GPS_Path.kml", "a") as m:
        m.write("""</coordinates>\n"""
                """</LineString>\n"""
                """</Placemark>\n"""
                """</Document>\n"""
                """</kml>""")

"""
main function that call the required function render kml that will make the kml file
"""


def main():
    renderkml()


if __name__ == '__main__':
    main()