from math import sin, cos, sqrt, atan2, radians
import alphashape
from pyproj import Proj
from shapely.geometry import shape, Polygon, LineString

def Concave_hull(dlist,mi):

    # Extract useful data (lat,lon)
    clist = []
    xlist = []
    ylist = []
    for i in range(len(dlist)):
        x = dlist[i][1]
        y = dlist[i][2]
        xy = x,y
        clist.append(xy)
        xlist.append(x)
        ylist.append(y)

    # Generate concave hull

    hull = alphashape.alphashape(clist,0)

    hull_pts = hull.exterior.coords.xy

    hxlist=list(hull_pts[0])
    hylist=list(hull_pts[1])
    hlist=[]
    for i in range(len(hxlist)):
        hx = hxlist[i]
        hy = hylist[i]
        hxy = hx, hy
        hlist.append(hxy)
        
    # Project and cal area
    
    pa = Proj(proj='utm',zone=47,ellps='WGS84', preserve_units=False)
    x, y = pa(hylist,hxlist)

    cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
    area = shape(cop).area
    
    # Getting polygon centroid

    P = Polygon(hlist)
    PC = list(P.centroid.coords)
    PCX = PC[0][0]
    PCY = PC[0][1]

    # Getting largest square

    ax = min(xlist)-0.0001
    ay = min(ylist)-0.0001
    bx = max(xlist)+0.0001
    by = max(ylist)+0.0001

    a = ax,ay
    b = bx,by
    c = ax,by
    d = bx,ay

    slist = a,c,b,d
        

    S = Polygon(slist)
    
    minX = min(hxlist)-0.0005
    maxX = max(hxlist)+0.0005
    if mi!=0:
        m = -1/mi
        c = PCY - m*PCX
        YL1 = m*minX+c
        YL2 = m*maxX+c
        path = LineString([(minX,YL1),(maxX,YL2)])
    else:
        path = LineString([(PCX,(PCY-0.1)),(PCX,(PCY+0.1))])
    
    intersect1 = list(P.intersection(path).coords)
    intersect2 = list(S.intersection(path).coords)
    

    return hull_pts, PCX, PCY, area, intersect2,intersect1

if __name__ == '__main__':
    from ReadCSV import read
    dlist=read()[0]
    print(Concave_hull(dlist,0.1)[4])
    
