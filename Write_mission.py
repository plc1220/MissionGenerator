import pandas as pd
from math import radians,sin,cos,sqrt,asin,atan,atan2,degrees

# Define distance calculation
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

# Define gradient calculation

def gradient(alt_a, alt_b, distance):
    m = ((alt_b - alt_a) / distance)*100
    angle = degrees(atan(m/100))
    return m, angle

# Define bearing calculation

def bearing(point_a,point_b):

    lat1,lon1= point_a
    lat2,lon2= point_b

    dLat = lat2 - lat1
    dLon = lon2 - lon1

    theta = degrees(atan2(dLon,dLat))

    return theta

# Function to write mission file with cooordinates
def mission_writing(i, j, k, file, lat_list,lon_list,alt_list,alt,hgt,flow,spraytime):
    x = 3*j+1-(k*2)
    y = 3*j+2-(k*2)
    z = 3*j+3-(k*2)
    file.write (str(x)+'\t0\t3\t16\t1\t0\t0\t0\t'+str(lat_list[i])#
                +'\t'+str(lon_list[i])+'\t'+str((alt_list[i]-float(alt))+float(hgt))+'\t1\n'#
                +str(y)+'\t0\t10\t184\t9\t'+str(int(flow))+'\t1\t'#
                +str((float(spraytime)*2))+'\t0\t0\t0\t1')
    file.write ('\n'+str(z)+'\t0\t10\t93\t'+str(spraytime)+'\t0\t0\t0\t0\t0\t0\t1\n')

def durian_mission_writing(i, j, k, file, lat_list,lon_list,alt_list,alt,hgt,flow,spraytime):
    x = 3*j+1-(k*2)
    y = 3*j+2-(k*2)
    z = 3*j+3-(k*2)
    file.write (str(x)+'\t0\t3\t16\t2\t0\t0\t0\t'+str(lat_list[i])#
                +'\t'+str(lon_list[i])+'\t'+str((alt_list[i]-float(alt))+float(hgt))+'\t1\n'#
                +str(y)+'\t0\t10\t184\t9\t'+str(int(flow))+'\t1\t'#
                +str((float(spraytime)*2))+'\t0\t0\t0\t1')
    file.write ('\n'+str(z)+'\t0\t3\t18\t1\t0\t0\t0\t0\t0\t0\t1\n')

# Function that generate the text file according to mission format
def writewaypoint (TOP, gps_points, Name, MissionName, f_no):
    # Get user input
    lon = TOP[1]
    lat = TOP[2]
    alt = TOP[3]
    hgt = 5
    #hgt = input("Enter Mission Height:")
    flow1 = 1920
    spraytime = 2.25

    # Getting the first and the last point of the dataframe
    first = gps_points["y"][1], gps_points["x"][1]
    last = gps_points["y"].iloc[-1],gps_points["x"].iloc[-1]
    
    # Compare the distance between the first point and the last point to the take off point
    distance1 = distance(first,[float(lat),float(lon)])
    distance2 = distance(last,[float(lat),float(lon)])

    # Reverse the dataframe sequence if the take off point is closer to the last point
    if distance2 < distance1:
        gps_points = gps_points.iloc[::-1]
    
    # Convert the dataframe into lists
    lat_list = gps_points["y"].tolist()
    lon_list = gps_points["x"].tolist()
    alt_list = gps_points["z"].tolist()
        
    # Write Mission
    file = open("dataset/%s/%s/%s_%s_F%s.txt"%(Name, MissionName, Name, MissionName,f_no),"w")
    file.write('QGC WPL 110\n')
    #+'\n0	1	0	16	0	0	0	0\t'+str(lat)+'\t'+str(long)+'\t'+str(alt)+'\t1')

    nrows = len(gps_points)

    # Intermediate point calc
    j = 0
    trigger = 0
    for i in range(nrows):   
        if i == 0:
            k = 0
        else:
            k = i-1
        d = distance((lat_list[k],lon_list[k]),(lat_list[k+1],lon_list[k+1]))
        m = gradient(alt_list[k],alt_list[k+1],d)
        # if d > 10 and abs(m[0]) > 25 : # this is for normal operation
        if abs(m[0]) > 25: # this is for extreme case, reduce the value to increase sensitivity
            j += 1
            trigger += 1
            l = 3*(i+trigger) - 2*trigger 
            x_inter = lat_list[k+1]-lat_list[k]
            y_inter = lon_list[k+1]-lon_list[k]
            if m[0] > 0:
                file.write(str(l)+'\t0\t3\t16\t0\t0\t0\t0\t'+str(lat_list[k]+0.1*(x_inter))#
                +'\t'+str(lon_list[k]+0.1*(y_inter))+'\t'+str((alt_list[k+1]-float(alt))+float(hgt))+'\t1\n')
            elif m[0] < 0:
                file.write(str(l)+'\t0\t3\t16\t0\t0\t0\t0\t'+str(lat_list[k]+0.9*(x_inter))#
                +'\t'+str(lon_list[k]+0.9*(y_inter))+'\t'+str((alt_list[k]-float(alt))+float(hgt))+'\t1\n')

        mission_writing(i, j, trigger, file ,lat_list,lon_list,alt_list,alt,hgt,flow1,spraytime)
        j += 1
    file.close()

def bagworm_mission (TOP, gps_points, Name, MissionName, f_no):

    # Get user input
    lon = TOP[1]
    lat = TOP[2]
    alt = TOP[3]
    #hgt = 5
    hgt = input("Enter Mission Height:")

    # Getting the first and the last point of the dataframe
    first = gps_points["y"][1], gps_points["x"][1]
    last = gps_points["y"].iloc[-1],gps_points["x"].iloc[-1]
    
    # Compare the distance between the first point and the last point to the take off point
    distance1 = distance(first,[float(lat),float(lon)])
    distance2 = distance(last,[float(lat),float(lon)])

    # Reverse the dataframe sequence if the take off point is closer to the last point
    if distance2 < distance1:
        gps_points = gps_points.iloc[::-1]
    
    # Convert the dataframe into lists
    lat_list = gps_points["y"].tolist()
    lon_list = gps_points["x"].tolist()
    alt_list = gps_points["z"].tolist()
        
    # Write Mission
    file = open("dataset/%s/%s/%s_%s_F%s.txt"%(Name, MissionName, Name, MissionName,f_no),"w")
    file.write('QGC WPL 110\n')
    #+'\n0	1	0	16	0	0	0	0\t'+str(lat)+'\t'+str(long)+'\t'+str(alt)+'\t1')

    nrows = len(gps_points)

    # Write bagworm mission
    j = 0
    for i in range(nrows):   
        if i == 0:
            k = 0
            l = 0
        elif i == 1:
            l = 0
        elif i == 2:
            k = 1
            l = 0
        else:
            k = i-1
            l = i-2

        d = distance((lat_list[k],lon_list[k]),(lat_list[k+1],lon_list[k+1]))
        m = gradient(alt_list[k],alt_list[k+1],d)
        t2 = bearing((lat_list[k],lon_list[k]),(lat_list[k+1],lon_list[k+1]))
        t = bearing((lat_list[l],lon_list[l]),(lat_list[l+1],lon_list[l+1]))
        dt = t2 - t

        # if d > 10 and abs(m[0]) > 25 : # uncomment this row if you are generating mission for young oil palm
        if abs(m[0])>25: # this is for mission that have vast difference in height 
            j += 1
            x_inter = lat_list[k+1]-lat_list[k]
            y_inter = lon_list[k+1]-lon_list[k]
            if m[0] > 0:
                file.write(str(j)+'\t0\t3\t16\t0\t0\t0\t0\t'+str(lat_list[l]+0.1*(x_inter))#
                +'\t'+str(lon_list[l]+0.1*(y_inter))+'\t'+str((alt_list[l+1]-float(alt))+float(hgt))+'\t1\n')
            elif m[0] < 0:
                file.write(str(j)+'\t0\t3\t16\t0\t0\t0\t0\t'+str(lat_list[l]+0.9*(x_inter))#
                +'\t'+str(lon_list[l]+0.9*(y_inter))+'\t'+str((alt_list[l]-float(alt))+float(hgt))+'\t1\n') 
        j += 1

        if abs(dt)> 45 or (k == i):
            file.write(str(j)+'\t0\t3\t16\t1\t0\t0\t0\t'+str(lat_list[k])#
                +'\t'+str(lon_list[k])+'\t'+str((alt_list[k]-float(alt))+float(hgt))+'\t1\n')            
        elif i!=0 and k!=0:
            file.write(str(j)+'\t0\t3\t16\t0\t0\t0\t0\t'+str(lat_list[k])#
                +'\t'+str(lon_list[k])+'\t'+str((alt_list[k]-float(alt))+float(hgt))+'\t1\n')
        

    file.write(str(j)+'\t0\t3\t16\t1\t0\t0\t0\t'+str(lat_list[-1])#
                +'\t'+str(lon_list[-1])+'\t'+str((alt_list[-1]-float(alt))+float(hgt))+'\t1\n')
    file.close()
               
def durian_waypoint(TOP, gps_points, Name, MissionName, f_no):
    # Get user input
    lon = TOP[1]
    lat = TOP[2]
    alt = TOP[3]
    hgt = 5
    #hgt = input("Enter Mission Height:")
    flow1 = 1920
    spraytime = 10

    # Getting the first and the last point of the dataframe
    first = gps_points["y"][1], gps_points["x"][1]
    last = gps_points["y"].iloc[-1],gps_points["x"].iloc[-1]
    
    # Compare the distance between the first point and the last point to the take off point
    distance1 = distance(first,[float(lat),float(lon)])
    distance2 = distance(last,[float(lat),float(lon)])

    # Reverse the dataframe sequence if the take off point is closer to the last point
    if distance2 < distance1:
        gps_points = gps_points.iloc[::-1]
    
    # Convert the dataframe into lists
    lat_list = gps_points["y"].tolist()
    lon_list = gps_points["x"].tolist()
    alt_list = gps_points["z"].tolist()
        
    # Write Mission
    file = open("dataset/%s/%s/%s_%s_F%s.txt"%(Name, MissionName, Name, MissionName,f_no),"w")
    file.write('QGC WPL 110\n')
    #+'\n0	1	0	16	0	0	0	0\t'+str(lat)+'\t'+str(long)+'\t'+str(alt)+'\t1')

    nrows = len(gps_points)

    # Intermediate point calc
    j = 0
    trigger = 0
    for i in range(nrows):   
        if i == 0:
            k = 0
        else:
            k = i-1
        d = distance((lat_list[k],lon_list[k]),(lat_list[k+1],lon_list[k+1]))
        m = gradient(alt_list[k],alt_list[k+1],d)
        if d > 10 and abs(m[0]) > 25 :
            j += 1
            trigger += 1
            l = 3*(i+trigger) - 2*trigger 
            x_inter = lat_list[k+1]-lat_list[k]
            y_inter = lon_list[k+1]-lon_list[k]
            if m[0] > 0:
                file.write(str(l)+'\t0\t3\t16\t0\t0\t0\t0\t'+str(lat_list[k]+0.1*(x_inter))#
                +'\t'+str(lon_list[k]+0.1*(y_inter))+'\t'+str((alt_list[k+1]-float(alt))+float(hgt))+'\t1\n')
            elif m[0] < 0:
                file.write(str(l)+'\t0\t3\t16\t0\t0\t0\t0\t'+str(lat_list[k]+0.9*(x_inter))#
                +'\t'+str(lon_list[k]+0.9*(y_inter))+'\t'+str((alt_list[k]-float(alt))+float(hgt))+'\t1\n')

        durian_mission_writing(i, j, trigger, file ,lat_list,lon_list,alt_list,alt,hgt,flow1,spraytime)
        j += 1
    file.close()

def write_waypoint (gps_points,instanceName,f_no):

    # Get user input
    print('Get home location')
    lat = input("Enter Latitude: ")
    long = input("Enter Longitude: ")
    alt = input("Enter Alt:")
    print ('\nGet Mission Parameters')
    hgt = input("Enter Mission Height:")
    spraytime = input('Enter Spray Time:')
    #flow = input('Enter flow rate (%): ')

    #flow1 = 1120 + (int(flow)*8)
    flow1 = 1900
    # Further process dataframe
    first = gps_points["y"][0],gps_points["x"][0]
    last = gps_points["y"].iloc[-1],gps_points["x"].iloc[-1]

    print(first)
    print(last)

    distance1 = distance(first,[float(lat),float(long)])
    distance2 = distance(last,[float(lat),float(long)])
    print(distance1)
    print(distance2)

    if distance2 < distance1:
        gps_points = gps_points.iloc[::-1]
    print(gps_points)
    lat_list = gps_points["y"].tolist()
    lon_list = gps_points["x"].tolist()
    alt_list = gps_points["z"].tolist()
    
    # Function to write mission file with cooordinates

    def mission_writing():
        x = 3*i+1
        y = 3*i+2
        z = 3*i+3
        file.write (str(x)+'\t0\t3\t16\t1\t0\t0\t0\t'+str(lat_list[i])+'\t'+str(lon_list[i])+'\t'+str((alt_list[i]-float(alt))+float(hgt))+'\t1\n'#
                    +str(y)+'\t0\t10\t184\t9\t'+str(int(flow1))+'\t1\t'#
                    +str((float(spraytime)*2))+'\t0\t0\t0\t1')
        file.write ('\n'+str(z)+'\t0\t10\t93\t'+str(spraytime)+'\t0\t0\t0\t0\t0\t0\t1')

    # Write
    file = open("dataset/%s/%s/%s_%s.txt"%(Name, MissionName, MissionName,f_no),"w")
    file.write('QGC WPL 110\n')
    #+'\n0	1	0	16	0	0	0	0\t'+str(lat)+'\t'+str(long)+'\t'+str(alt)+'\t1')

    nrows = len(gps_points)

    for i in range(nrows):
        mission_writing()
    file.close()
    
if __name__ == '__main__':
    
    Name = input("\nEnter the coordinates file you would like to generate mission from: ")
    m_no = input("\nWhich mission you would like to adjust?: ")
    dirName = "dataset/%s/%s/%s.csv" % (Name, m_no, m_no)
    df = pd.read_csv(dirName, sep=",", usecols =["no","x","y","z","flight"],index_col='no')
    #print(df)
    category = list(df.flight.unique())
    #print(category)
    lat_list = df["y"].tolist()
    lon_list = df["x"].tolist()
    alt_list = df["z"].tolist()

    #TOP = [0, 101.503661870956,3.25481185193968, 48]
    
    TOP = [0 , 101.6552603, 2.90959451937995, 26]
    for i in category:
        gps_points = df.loc[df['flight'] == int(i)]
        #print(gps_points["x"][1])
        #writewaypoint(TOP, gps_points, Name, m_no, i)
        #durian_waypoint(TOP, gps_points, Name, m_no, i)
        bagworm_mission(TOP, gps_points, Name, m_no, i)