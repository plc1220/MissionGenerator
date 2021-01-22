import numpy as np
from sklearn.cluster import KMeans
from math import sqrt, ceil
from ReadCSV import read
    
def height_categorize(clist, dh):    
    # Get alt list from clist
    N = len(clist)

    alt_list = []
    for i in range (N):
        z = (clist[i][3])
        alt_list.append(z)

    lowest_alt = min(alt_list)
    highest_alt = max(alt_list)

    dalt = round(highest_alt-lowest_alt,3)

    # Cal number of layer
    NL = ceil(dalt/dh)
    print(NL)
    # Classify by alt layer
    layerlist = []
    for j in range(NL):
        layer = [k for k in alt_list if lowest_alt+(j*dh) <= ceil(k) <= (lowest_alt+((j+1)*dh))]
        layerlist.append(layer)

    corrected_list = {}
    for a in range(len(layerlist)):
        item = []
        for b in range(N):
            if alt_list[b] in (layerlist[a]):
                item.append(clist[b])
        corrected_list[a] = item
    return corrected_list
    
def lin_categorize(clist,m,dl,ilist):

    # Get lat list
    N = len(clist)
    coord_list=[]
    x_list = []
    y_list = []
    for i in range (N):
        x = (clist[i][1])
        y = (clist[i][2])
        xy = (x,y)
        coord_list.append(xy)
        x_list.append(x)
        y_list.append(y)

    ixlist = []
    iylist = []
    for i in range(2):
        j = ilist[i][0]
        k = ilist[i][1]
        ixlist.append(j)
        iylist.append(k)

    # Cal layer 
    ilonmax = max(iylist)
    ilonmin = min(iylist)
    max_coord = [i for i in ilist if (i[1] == ilonmax)]
    min_coord = [i for i in ilist if (i[1] == ilonmin)]
    
    c = min_coord[0][1]-m*(min_coord[0][0])
    c2 = max_coord[0][1]-m*(max_coord[0][0])
    dc = (c2-c)/sqrt((m**2)+1)
    dlayer = dl/1.113195e5
    layer = ceil(dc/dlayer)

    # Classify by lin layer
    layerlist = []
    for j in range(layer):
        lay = [k for k in coord_list if ((m*k[0])+(c+(((j)*dlayer)*(sqrt((m**2)+1)))) < k[1] <= ((m*k[0])+(c+(((j+1)*dlayer)*(sqrt((m**2)+1))))))]
        layerlist.append(lay)
        
    corrected_list = {}
    for a in range(len(layerlist)):
        item = []
        for b in range(N):
            if coord_list[b] in layerlist[a]:
                item.append(clist[b])
        corrected_list[a] = item
    return corrected_list

def lon_categorize(clist,dl):
    # Get lon list
    N = len(clist)
    
    x_list = []
    for i in range (N):
        x = (clist[i][1])
        x_list.append(x)

    lonmax = max(x_list)
    lonmin = min(x_list)
    dlon = lonmax - lonmin
    dlayer = dl/1.113195e5
    layer = ceil(dlon/dlayer)

    # Classify by lon layer
    layerlist = []
    for j in range(layer):
        lay = [k for k in x_list if (lonmin+(j*dlayer) <= k <= (lonmin+((j+1)*dlayer)))]
        layerlist.append(lay)
        
    corrected_list = {}
    for a in range(len(layerlist)):
        item = []
        for b in range(N):
            if x_list[b] in layerlist[a]:
                item.append(clist[b])
        corrected_list[a] = item
    return corrected_list



if __name__ == '__main__':

    # Get coordinate list
    clist = read()[0]
    #print(height_categorize(clist,2))
    print(lon_categorize(clist, 6.9))
    #print(lin_categorize(clist,0.1,7,[(3.2576012642462517, 101.49704843924285), (3.2576260111478206, 101.49680097022716)]))
