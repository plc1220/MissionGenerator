from ReadCSV import read
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.widgets import Slider
from Polygon import Concave_hull
from Function import F, F2
from Write_mission import write_waypoint

# Get lat lon from csv
Initiate = read()
dlist = Initiate[0]
Name = Initiate[1]
f_no = Initiate[2]
N = len(dlist)
clist = []
xlist = []
ylist = []
zlist = []
for i in range(N):
    x = dlist[i][1]
    y = dlist[i][2]
    z = dlist[i][3]
    xyz = x,y,z
    clist.append(xyz)
    xlist.append(x)
    ylist.append(y)
    zlist.append(z)

# Declare categorization method
while 1:
    user_choice = input("Please choose the categorization method: \n1) Height\n2) Line\n")
    if user_choice == '1' or user_choice == '2':
        break
    else:
        print("Please input 1 or 2 only")

if user_choice == '1':
    # Declare initial height difference
    h0 = 2

    # Plot
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25,bottom=0.25)
    ax.scatter(xlist, ylist, color='blue')
    ax.set_xlim(min(xlist)-0.00005,max(xlist)+0.00005)
    ax.set_ylim(min(ylist)-0.00005,max(ylist)+0.00005)

    # Create Slider
    axcolor = 'lightgoldenrodyellow'
    axh = plt.axes([0.25, 0.105, 0.65, 0.03], facecolor=axcolor)
    sh = Slider(axh, 'Height', 1, 3 , valinit = h0, valstep = 0.125)

    axdirection = plt.axes([0.8, 0.005, 0.1, 0.04])
    sdi = Slider(axdirection, 'Direction', 0, 1 , valinit = 0, valstep = 1)

    axm = plt.axes([0.8, 0.055, 0.1, 0.04], facecolor=axcolor)
    sm = Slider(axm, 'Sort', 0, 1 , valinit = 0, valstep = 1)

    # plot original
    l, = ax.plot(xlist,ylist,'bo-',marker='s')
    
    # Run categorization
    # Define update function
    def update(val):
        data = F2(sh.val,sm.val,sdi.val,dlist)
        # Plot
        list1 = data.tolist()
        x = [p[1] for p in list1]
        y = [p[2] for p in list1]
        # z = [p[3] for p in list1]
        l.set_xdata(x)
        l.set_ydata(y)
        #l.set_zdata(z)
        fig.canvas.draw()

    # Show
    sh.on_changed(update)
    sdi.on_changed(update)
    sm.on_changed(update)

    plt.show()

    path = F2(sh.val,sm.val,sdi.val,dlist)    
    
elif user_choice == '2':
    # Declare initial gradient
    m0 = 0.5

    # Get boudary data
    P_data = Concave_hull(dlist,m0)
    hull_pts = P_data[0]
    PCX = P_data[1]
    PCY = P_data[2]

    # Plot points and boundary
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25,bottom=0.25)
    ax.scatter(xlist, ylist, color='blue')
    ax.set_xlim(min(xlist)-0.00005,max(xlist)+0.00005)
    ax.set_ylim(min(ylist)-0.00005,max(ylist)+0.00005)
    plt.plot(PCX,PCY,'go')

    # Slice Lat 
    x_adjust = np.arange(min(xlist),max(xlist),0.0001)

    # Declare centre reference line
    c0 = PCY - m0*PCX
    y_adjust = m0*x_adjust + c0

    # Plot original trajectory and reference line
    l, = ax.plot(xlist,ylist)
    l2, = plt.plot (x_adjust, y_adjust, lw=1)

    # Create Slider
    axcolor = 'lightgoldenrodyellow'
    axm = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axlayer = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

    sm = Slider(axm, 'Gradient', -5, 5 , valinit = m0, valfmt = "%1.5f", valstep = 0.00001)
    slayer = Slider(axlayer, 'Layer', 4,10,valinit=6,valstep =0.01)

    axdirection = plt.axes([0.8, 0.025, 0.1, 0.04])
    sdi = Slider(axdirection, 'Direction', 0, 1 , valinit = 0, valstep = 1)

    # Define update function
    def update(val):
        data = F(sm.val,slayer.val,sdi.val,dlist,PCY,PCX)
        # Plot
        list1 = data[0].tolist()
        x = [p[1] for p in list1]
        y = [p[2] for p in list1]
        l.set_xdata(x)
        l.set_ydata(y)
        l2.set_ydata(data[1]*x_adjust+data[2])
        fig.canvas.draw()

    # Show
    sm.on_changed(update)
    slayer.on_changed(update)
    sdi.on_changed(update)

    plt.show()

    path = F(sm.val,slayer.val,sdi.val,dlist,PCY,PCX)[0]

# Save mission
df = pd.DataFrame(data=path, columns=["no", "x","y","z"])
print(df)
df.to_csv('dataset/%s/%s_%s.csv'% (Name, Name, f_no), index = False)
#spray_data = write_waypoint(df, Name, f_no)
