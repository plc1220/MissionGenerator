import matplotlib.cm as cmx
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits import mplot3d

def scatter3d(name, x, y, z, cs, colorsMap='jet'):
    fig = plt.figure()
    ax1 = fig.add_subplot(111,projection='3d')
    ax1.plot3D(x,y,z,'--g')
    X = [x[0],x[-1]]
    Y = [y[0],y[-1]]
    Z = [z[0],z[-1]]
    ax1.scatter3D(X,Y,Z, s = 60, c='r',marker='s',cmap='magma')
    scatter = ax1.scatter3D(x,y,z,c=z,cmap='hsv')
    legend1 = ax1.legend(*scatter.legend_elements(),
                    loc="lower left", title="Classes")
    ax1.add_artist(legend1)
    plt.title(name)
    plt.show()

if __name__ == '__main__':

    Name = input("\nEnter the directory you would like to plan: ")
    Mission = input("\nEnter the mission you want to plan: ")
    mission_dir = "dataset/%s/%s" % (Name, Mission)

    df = pd.read_csv((mission_dir+'/%s_adjusted.csv'%(Mission)), sep=",", usecols =["no","x","y","z","flight"],index_col='no')

    category = list(df.flight.unique())

    for i in category:

        name = "%s_%s_F%s" %(Name,Mission,int(i))
        gps_points = df.loc[df['flight'] == int(i)]
        
        y = gps_points["y"].tolist()
        x = gps_points["x"].tolist()
        z = gps_points["z"].tolist()
        #label = gps_points["flight"].tolist()
        
        scatter3d(name,x,y,z,[0.0,1.0])#,label,[0.0,1.0])