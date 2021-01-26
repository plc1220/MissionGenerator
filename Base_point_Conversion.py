#This script is for easy WGS84 to ublox format string conversion

def WGS_conversion(WGS_xy):
    lst = []
    for i in range(2):
        x_lp = int(WGS_xy[i][-2]+WGS_xy[i][-1])
        x_hp = int((WGS_xy[i][:-2]).replace('.',''))
        if x_lp > 50:
            x_hp = x_hp + 1
            x_lp = x_lp - 100
        item = x_hp, x_lp
        lst.append(item)
    return lst

if __name__ == '__main__':
    import numpy as np

    WGS84_x = input('Please enter the WGS84_y with 9 decinal points: ')
    WGS84_y = input('Please enter the WGS84_x with 9 decimal points: ')
    height = int(input('Please enter the z in cm: '))

    lst = WGS_conversion([WGS84_x,WGS84_y])
    arr = np.transpose(np.array(lst))
    coor_lst = (arr.flatten()).tolist()
    final_lst = [2,1000]
    index_lst = [1,2,3,5,6]
    item_lst = [coor_lst[0],coor_lst[1],height,coor_lst[2],coor_lst[3]]
    j = 0
    for i in index_lst:
        final_lst.insert(i,item_lst[j])
        j+=1
    print(final_lst)