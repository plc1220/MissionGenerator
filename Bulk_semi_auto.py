from semi_auto import semi_auto
import pandas as pd

Name = input("\nEnter the directory you would like to adjust: ")

MissionName = input("\nEnter the mission: ")

dirname = "dataset/%s/%s/%s" % (Name,MissionName,MissionName) 
path = pd.read_csv((dirname+'_path.csv'),index_col='id')
df = pd.read_csv((dirname+'.csv'),usecols =["id","x","y","z","flight"],index_col="id")

id_no = set(path.index.values.tolist())

final_df = []

for i in id_no:
    df2 = df.loc[df['flight'] == int(i)]
    flight_df = semi_auto(path,int(i),df2)
    final_df.append(flight_df)

final_df = pd.concat(final_df)

final_df.to_csv('dataset/%s/%s/%s_adjusted.csv'% (Name, MissionName, MissionName), index = False)


if len(final_df) != len(df):
    print('unequal')
    print(len(df)-len(final_df))