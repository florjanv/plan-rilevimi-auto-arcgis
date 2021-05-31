import arcpy
import math

#parcels and centroids
workspace = r"workspace_path"
parcels = r"parcel_featureclass_krrgjsh"
cntr = r"Parcel_centroid_krrgjsh"
arcpy.env.workspace = workspace


#variables
parcel_id=[]
max_xy = []
min_xy = []
max_XYdist = []
scale=[]
cntr_centroid=[]

with arcpy.da.SearchCursor(parcels, ['OID@', 'SHAPE@WKT','SHAPE@XY','ID']) as cursor:
    for row in cursor:
        pX=[]
        pY=[]
        parcel_id.append(row[3])
        a = row[1].replace("MULTIPOLYGON (((","").replace(")))","")
        c = a.split(", ")
        for i in c:
            temp = i.split(" ")
            pX.append(float(temp[0]))
            pY.append(float(temp[1]))
        max_xy.append([max(pX),max(pY)])
        min_xy.append([min(pX),min(pY)])
        dX = max(pX)-min(pX)
        dY = max(pY)-min(pY)
        max_XYdist.append([dX,dY])
        if dX < 650 and dY < 510:
            scale.append(2500)
        elif dX < 1315 and dY < 1040:
            scale.append(5000)
        elif dX < 2640 and dY < 2110:
            scale.append(10000)
        elif dX > 2640 and dY > 2110:
            scale.append(25000)
        cntr_centroid.append(row[2])

try:
    arcpy.CreateFeatureclass_management(workspace,"plGrid","POLYGON",None,None,None,'PROJCS["Transverse_Mercator",GEOGCS["GCS_GRS 1980(IUGG, 1980)",DATUM["D_unknown",SPHEROID["GRS80",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",20],PARAMETER["scale_factor",1],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["Meter",1]]')
    arcpy.AddField_management("plGrid","parcel_id","TEXT",250)
    arcpy.AddField_management("plGrid","min_xy","TEXT",250)
    arcpy.AddField_management("plGrid","max_xy","TEXT",250)
    arcpy.AddField_management("plGrid","max_XYdist","TEXT",250)
    arcpy.AddField_management("plGrid","cntr_centroid","TEXT",250)
    arcpy.AddField_management("plGrid","scale","LONG")
except:
    print "Fushat dhe shapfile ekzistojne"


with arcpy.da.InsertCursor("plGrid",["SHAPE@","parcel_id","min_xy","max_xy","max_XYdist","cntr_centroid","scale"]) as cursor:
    for i in range(len(parcel_id)):
        dx = 0
        dy = 0
        if scale[i]==5000:
            dx, dy = 1325, 1050
        elif scale[i] == 10000:
            dx, dy = 2650, 2100
        elif scale[i] > 10000:
            dx, dy = 6625, 5250
        else:
            dx, dy = 662.5, 525
        print parcel_id[i], min_xy[i], max_xy[i], max_XYdist[i], cntr_centroid[i], scale[i]
        array = arcpy.Array([arcpy.Point(cntr_centroid[i][0]-dx/2, cntr_centroid[i][1]-dy/2), arcpy.Point(cntr_centroid[i][0]+dx/2, cntr_centroid[i][1]-dy/2),arcpy.Point(cntr_centroid[i][0]+dx/2, cntr_centroid[i][1]+dy/2), arcpy.Point(cntr_centroid[i][0]-dx/2, cntr_centroid[i][1]+dy/2)])
        cursor.insertRow([arcpy.Polygon(array),parcel_id[i], str(min_xy[i][0])+","+str(min_xy[i][1]), str(max_xy[i][0])+","+str(max_xy[i][1]), str(max_XYdist[i][0])+","+str(max_XYdist[i][1]), str(list(cntr_centroid[i])[0])+","+str(list(cntr_centroid[i])[1]),scale[i]])

arcpy.FeatureVerticesToPoints_management("plGrid","plGrid_vertices")
arcpy.AddXY_management("plGrid_vertices")
print "Done"


