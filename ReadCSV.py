import pandas as pd
import matplotlib.pyplot as plt

# Define read file
def read():    
    while 1:
        try:
            Name = input("\nEnter the directory you would like to approximate: ")
            f_no = input("\nWhich flight you would like to adjust?: ")
            dirName = "C:/Users/liche/Desktop/Path planning/dataset/%s/%s.csv" % (Name, Name)
            df = pd.read_csv(dirName, sep=",", usecols =["id","x","y","z","flight"])
            df2 = df.loc[df['flight'] == int(f_no)]

            del df2 ['flight']
            xy = df2.values.tolist()
            clist = []
            for item in xy:
                clist.append(item)

            return clist, Name, f_no       
            break
        except (IOError, NameError):
            print("This is not a valid instance. Please put in a valid directory name! Please also make sure the  %s.csv file format is correct(utf-8).")
        except (IndexError):
            print("Please make sure your %s_s.csv's first and last value are the same. ")

if __name__ == '__main__':
    print(read())
