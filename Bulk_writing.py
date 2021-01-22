import pandas as pd
from Write_mission import writewaypoint, bagworm_mission

# Input filename
Name = input("\nEnter the directory you would like to plan: ")
Mission = input("\nEnter the mission you want to plan: ")
mission_dir = "dataset/%s/%s" % (Name, Mission)
Plot_dir = "dataset/%s" % (Name)

# Read take of point
TOP_df = pd.read_csv(Plot_dir+"/TOP.csv")

# Read Mission 
df = pd.read_csv((mission_dir+'/%s_adjusted.csv'%(Mission)), sep=",", usecols =["no","x","y","z","flight"],index_col='no')

category = list(df.flight.unique())

for i in category:
    gps_points = df.loc[df['flight'] == int(i)]
    print("Files to be written from is %s_%s_%s" % (Name, Mission, int(i)))
    while 1:
        try:
            TOP_id = int(input("Which take off point you would like to choose?"))-1
            break
        except (IOError, NameError):
            print("This is not a valid instance. Please put in a valid directory name! Please also make sure the  %s.csv file format is correct(utf-8).")
        except (IndexError):
            print("Please make sure your %s_s.csv's first and last value are the same. ")

    TOP = TOP_df.iloc[TOP_id].values.tolist()

    #writewaypoint(TOP,gps_points, Name, Mission, int(i))
    bagworm_mission(TOP, gps_points, Name, Mission, int(i))