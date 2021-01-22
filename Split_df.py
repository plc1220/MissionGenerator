import pandas as pd

Name = input("\nEnter the directory you would like to approximate: ")
dirname = "C:/Users/liche/Desktop/Path planning/dataset/%s/%s.csv" % (Name, Name)

df = pd.read_csv(dirname, usecols=["id","x","y","z","flight"])

category = list(df.flight.unique())

for j in category:
    df2 = df.loc[df["flight"] == j]
    df2.rename(columns={"id":"no"}, inplace =True)
    df2.to_csv((Name+'_'+str(j)+".csv"),index = False)
    print(df2)