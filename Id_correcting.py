import pandas as pd

Name = input("\nEnter the directory you would like to approximate: ")
dirname = "C:/Users/liche/Desktop/Path planning/dataset/%s/%s.csv" % (Name, Name)

df = pd.read_csv(dirname, usecols=["id","x","y","z","flight"])

category = list(df.flight.unique())

print(category)

category_list = df.flight.values.tolist()

for j in category:
    label_id = 1    
    for k in range(len(category_list)):
        if df.iloc[k,4] == j: 
            df.at[k,'id'] = label_id
            label_id += 1
    label_id = 1

print(df)

df.to_csv('test.csv',index = False)