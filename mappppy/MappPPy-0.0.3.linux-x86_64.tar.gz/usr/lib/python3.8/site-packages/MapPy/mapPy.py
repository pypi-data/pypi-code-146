import webbrowser
import folium as f
from folium.plugins import HeatMap
import os
from statistics import mean


# Kilroy Was Here - acknowledgements to Gabriel Tower for writing this class
# and implementing it


class mapper:

    # Create a pointPlotter at given lat and long coords
    def createMap(self, lat, lon, zoom=10):
        return f.Map(location=[lat, lon], zoom_start=zoom)

    # Save pointPlotter as an HTML file in a subfolder of the current working directory
    def saveMap(self, map, name="pointPlotter.html"):
        if os.path.exists(os.getcwd() + "/maps"):
            if ".html" in name:
                map.save(os.getcwd() + "/maps/" + name)
            else:
                raise "Not .html file"
        else:
            os.mkdir(os.getcwd() + "/maps")

    # Call default web browser to open the HTML file containing the pointPlotter
    def showMap(self, map):
        map.save("pointPlotter.html")
        webbrowser.open("pointPlotter.html")

    # Create a pointPlotter marker with a thumbnail version of a specified image
    #   pointPlotter: the pointPlotter to add the marker to
    #   lat and long: coordinates of the marker you wish to add
    #   imgFileName: string containing full path name to image file
    #   scaleFactor: for creating an in-memory thumbnail (scaled-down) version of the image file

    def addMarker(self, map, lat, lon, mTooltip="", mColor="blue"):
        marker = f.Marker(
            location=[lat, lon],
            icon=f.Icon(color=mColor, icon="pin"),
            tooltip=mTooltip)
        marker.add_to(map)

    def heat(self, map, lat, lon, zoom=10):
        HeatMap(list(zip(lat, lon))).add_to(map)

    def choropleth(self, map):
        pass


class utils:

    # Given a list of [lat, long] coords, compute their mean
    # so pointPlotter can be centered about that point
    def getCenterPoint(self, ptList):
        return mean(ptList)

    # Given a lat and lon calculates the distance between two points using haversine
    def getDistance(self, lat, lon):
        pass
