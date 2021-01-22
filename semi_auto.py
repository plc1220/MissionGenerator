import pandas as pd
import numpy as np
from math import radians,sin,cos,sqrt,asin

def distance(point_a,point_b):
    lat1,lon1= point_a
    lat2,lon2= point_b
    R = 6371
    
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians (lat1)
    lat2 = radians (lat2)
    
    a = sin(dLat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    return R*c*1000

def semi_auto(path, flight, trees):

    # Cross check path validity

    # extract path according to flight
    POS = path.loc[flight].iloc[:,[3,4]]
    POS.columns = ['lat','lon']
    POS.reset_index(drop=True, inplace=True)
    df = POS.values.tolist()
    trees = trees.values.tolist()
    treelist = []

    for i in range(len(df)-1):

        # Calculate distance
        dist = distance((df[i][1],df[i][0]),(df[i+1][1],df[i+1][0]))
        
        # Calculate step
        step = int(abs(dist*0.55))

        # Based on distance, generate points with even interval along the line
        xslice = np.linspace(df[i][0],df[i+1][0],step,retstep=True)
        xlist = xslice[0].tolist()
        yslice = np.linspace(df[i][1],df[i+1][1],step,retstep=True)
        ylist = yslice[0].tolist()
        xylist = list(zip(xlist, ylist))

        # Calculate radius
        radius = sqrt((xslice[1])**2+(yslice[1])**2)
        # Search
        for j in range(len(xylist)):      
            for k in range(len(trees)):
                if (sqrt((trees[k][0]-xylist[j][0])**2+(trees[k][1]-xylist[j][1])**2) < radius) and (trees[k] not in treelist):
                    treelist.append(trees[k])
        
    label_list= list(range(1,len(treelist)+1))

    final_df = pd.DataFrame(treelist, columns=["x","y","z","flight"])
    final_df.insert(0, "no", label_list, True)

    return final_df

if __name__ == '__main__':
    Name = input("\nEnter the directory you would like to approximate: ")
    MissionName = input("\nEnter the mission: ")
    f_no = input("\nWhich flight you would like to adjust?: ")
    dirname = "C:/Users/liche/Desktop/Path planning/dataset/%s/%s/%s" % (Name,MissionName,MissionName) 
    path = pd.read_csv((dirname+'_path.csv'),index_col='id')
    print(path)
    df = pd.read_csv((dirname+'.csv'),usecols =["id","x","y","z","flight"],index_col="id")
    print(df)
    df2 = df.loc[df['flight'] == int(f_no)]
    final_df = semi_auto(path,int(f_no),df2)
    print(final_df)