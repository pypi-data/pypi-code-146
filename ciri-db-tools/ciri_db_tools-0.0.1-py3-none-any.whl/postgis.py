import psycopg2
import sqlite3
from sqlite3 import Error
import subprocess
import geopandas as gpd
import matplotlib.pyplot as plt

def geospatial_plot(us_input, pw_input, hs_input, prt_input, db_input, srid_input, shapes_input, points_input):
    # pip install geopandas

    # Heroku server credentials are commented out. 
    conn_host = hs_input #"localhost"     #"ec2-44-208-151-7.compute-1.amazonaws.com"
    conn_user = us_input #"postgres"      #"zswibiltgwklpp"

    # For localhost, change password to your own
    conn_pass = pw_input #"cmpt276"       #"4cf90c60bef822bae7c0ce61e5ad0fc6233e578ca49a91ef5f60e2c2c28656d2"

    # Postgis will be the name of the new locally hosted spatial database
    conn_db = db_input #"postgis"         #"d7trfmnkdpljp6"
    conn_port = prt_input #5432
    conn_uri = "postgres://" + conn_user + ":" + conn_pass + "@" + conn_host + ":" + str(conn_port) + "/" + conn_db
    srid = srid_input #'ESPG: 102001'       # SRID 102001 -> https://epsg.io/102001

    shapes = shapes_input
    points = points_input

    try:
        # Check if connecting to no DB localhost or DB present server (Heroku)
        if conn_host == "localhost":
            print("Connecting to localhost. \n")
            Postgres_Connection = psycopg2.connect(host=conn_host, user=conn_user, password=conn_pass, database="postgres",port=5432)
            Postgres_Connection.autocommit = True
            Postgres_Cursor = Postgres_Connection.cursor()
            Postgres_Cursor.execute("SELECT datname from pg_database where datname='postgis'")
            Postgres_Presence = Postgres_Cursor.fetchone()
            if Postgres_Presence is None:
                print("No database postgis found. Creating DATABASE postgis. \n")
                Postgres_Cursor.execute('CREATE DATABASE postgis;')
            Postgres_Connection.close()
        if conn_host != "localhost":
            print("Connecting to DB on non-localhost server. \n")

        # Establish Postgis database connection
        PostGIS_Connection = psycopg2.connect(
        host = conn_host,
        user = conn_user,
        password = conn_pass,
        database = conn_db,
        port = 5432
        )
        PostGIS_Cursor = PostGIS_Connection.cursor()

        # Check if database has postgis extension, add if not.
        PostGIS_Cursor.execute("SELECT extname from pg_extension WHERE extname='postgis';")
        PostGIS_Presence = PostGIS_Cursor.fetchone()
        if PostGIS_Presence is None:
            print("Postgis extension not found. Creating EXTENSION postgis.")
            PostGIS_Cursor.execute("CREATE EXTENSION postgis;")
            PostGIS_Cursor.execute("COMMIT;")
        
        # Execute shell script to store .shp files to the database. Make sure that the server does not contain these tables already.
        PostGIS_Cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name='%(sh)s';", {"sh": shapes})
        PostGIS_Polygon_Table = PostGIS_Cursor.fetchone()
        if PostGIS_Polygon_Table is None:
            print("No sample_polygons table found. Building TABLE %(sh)s.", {"sh": shapes})
            sample_polygons_cmd = 'shp2pgsql -s 4326 ' + shapes + '.shp' + shapes + ' | psql -q ' + conn_uri
            subprocess.call(sample_polygons_cmd, shell=True)
        
        PostGIS_Cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name='%(pt)s';", {"pt": points})
        PostGIS_Points_Table = PostGIS_Cursor.fetchone()
        if PostGIS_Points_Table is None:
            print("No sample_points table found. Building TABLE %(pt)s.", {"pt": points})
            sample_points_cmd = 'shp2pgsql -s 4326'+ points +'.shp' + points + ' | psql -q ' + conn_uri
            subprocess.call(sample_points_cmd, shell=True)
        
        # Query and list site_id and geom from sample points
        PostGIS_Cursor.execute('SELECT geom, site_id from %(pt)s ORDER BY site_id ASC', {"pt": points})
        geom_points_results = PostGIS_Cursor.fetchall()
        geom_points_array = []
        site_id_points_array = []
        for points_row in geom_points_results:
            geom_points_array.append(points_row[0])
            site_id_points_array.append(points_row[1])

        # Query and list site_id and geom from sample polygons
        PostGIS_Cursor.execute('SELECT geom, site_id from %(sh)s ORDER BY site_id ASC', {"sh": shapes})
        geom_polygons_results = PostGIS_Cursor.fetchall()
        geom_polygons_array = []
        site_id_polygons_array = []
        for polygons_row in geom_polygons_results:
            geom_polygons_array.append(polygons_row[0])
            site_id_polygons_array.append(polygons_row[1])
        
        # Convert geom points array into WKT points array
        points_array = []
        for geom_point in geom_points_array:
            PostGIS_Cursor.execute("SELECT ST_AsText('" + geom_point + "');")
            points_wkt_results = PostGIS_Cursor.fetchall()
            for point in points_wkt_results:
                points_array.append(point[0])
        
        # Convert geom polygons array into WKT polygons array
        polygons_array = []
        for geom_polygon in geom_polygons_array:
            PostGIS_Cursor.execute("SELECT ST_AsText('" + geom_polygon + "');")
            polygons_wkt_results = PostGIS_Cursor.fetchall()
            for polygon in polygons_wkt_results:
                polygons_array.append(polygon[0])
        
        # Convert WKT points and polygons to GeoDataFrames with the correct projection
        pt = gpd.GeoSeries.from_wkt(points_array)
        pt.to_crs = srid
        poly = gpd.GeoSeries.from_wkt(polygons_array)
        poly.to_crs = srid

        # Create a list of plots and a list of site arrays
        plots = []
        plots.append(pt)
        plots.append(poly)
        site_types = []
        site_types.append(site_id_points_array)
        site_types.append(site_id_polygons_array)

        # Plot each geodataframe object and its corresponding Site_ID text label
        site_type_index = 0
        for plot in plots:
            plot.plot()
            site_id_index = 0
            for coord in pt:
                site_id = "Site_ID: " + str(site_types[site_type_index][site_id_index])
                plt.text(coord.x, coord.y, site_id)
                site_id_index += 1
            site_type_index +=1

        # Display the two plots and close the PG connection
        plt.show()
        PostGIS_Connection.close()
    except Error as e:
        print("An error occured.")
        print(e)
    finally:
        print("Script executed.")