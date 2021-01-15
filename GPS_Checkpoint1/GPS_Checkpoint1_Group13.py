"""
GPS PROJECT CHECKPOINT 1: Parse an input GPS file and convert to a kml file that can be rendered on Google Earth.

GROUP 13 SUBMISSION

MEMBERS: ANKIT JAIN, VAISHNAVI BADAME
"""

"""
A function that will create the kml file required with the longitude, latitude and speed in knots file that can be 
rendered on google earth to show us a path.
"""
def renderkml():

    gps_file = open("gps_data.txt", "r")  # opening the input gps file
    data = gps_file.readlines()[5:]  # skipping the first 5 lines that were no required.

    """
    Opening file in write mode and writing the specified xml tags necessary to the kml file.
    """
    with open("map.kml", "w+") as m:
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

    speedlist = []  # a list of speeds in knots from GPRMC
    for line in data:  # iteratingover all lines from input gps file
        attributes = line.split(",")  # splitting each line on a ','
        if attributes[0] == "$GPRMC":

            lat = float(attributes[3])  # assigning original latitude value
            if attributes[4] == 'S':  # check for + or - (if South, -, else positive)
                lat = -lat

            """
            Code to get degrees and minutes from the latitude value extracted above
            """
            lat_indegrees = int(lat / 100)  # getting tne degrees, no time included
            min_in_lat = lat - (lat_indegrees * 100)
            final_time_in_mins1 = (min_in_lat/60)
            latitude = lat_indegrees + final_time_in_mins1  # final latitude value


            """
            Code to extract longitude value and get degrees and minutes just as in latitude above
            """
            long = float(attributes[5])
            if attributes[6] == 'W':
                long = -long

            long_indegrees = int(long / 100)
            min_in_long = long - (long_indegrees * 100)
            final_time_in_mins2 = (min_in_long/60)
            longitude = long_indegrees + final_time_in_mins2

            """
            Extract thespeed value from '$GPRMC' then write to kml file and use same value for the immediate 
            next '$GPGGA'
            """
            speed_in_knots = float(attributes[7])
            speedlist.append(speed_in_knots)

            with open("map.kml", "a") as m:
                m.write("%0.6f,%0.6f,%0.2f \n" % (longitude, latitude, speed_in_knots))  # writing the required
                # longitude first, latitude and speed values to kml file

        else:   # same for '$GPGGA' case, only positions where values are found change
            lat = float(attributes[2])
            if attributes[3] == 'S':
                lat = -lat

            lat_indegrees = int(lat / 100)
            min_in_lat = lat - (lat_indegrees * 100)
            final_time_in_mins3 = (min_in_lat/60)
            latitude = lat_indegrees + final_time_in_mins3

            long = float(attributes[4])
            if attributes[5] == 'W':
                long = -long

            long_indegrees = int(long / 100)
            min_in_long = long - (long_indegrees * 100)
            final_time_in_mins4 = (min_in_long/60)
            longitude = long_indegrees + final_time_in_mins4

            with open("map.kml", "a") as m:  # appending each line of data in kml file
                m.write("%0.6f,%0.6f,%0.2f \n" % (longitude, latitude, speedlist[-1]))  # writing the obtained values
                # to required kml file with longitude first, then latitude and finally  speed in knots.

    """
    Writing the closing tags for the kml file
    """
    with open("map.kml", "a") as m:
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
