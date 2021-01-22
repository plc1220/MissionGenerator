import itertools

# Function to slice dictionary into list
def slicing(di,m,direction):
    d = {k: v for k, v in di.items() if len(v)!=0}
    if abs(m)<=0.268:
        if direction == 0:
            full = []
            for i in d:
                item = []         
                for j in range(len(d[i])):
                    item_final = []
                    element = d[i][j]
                    item.append(element)
                    item = sorted(item, key=lambda x:x[1],reverse=False)
                    for k in range(len(item)):
                        index = int(item[k][0])
                        #index = index+1
                        item_final.append(index)
                full.append(item_final)
        elif direction == 1:
            full = []
            for i in d:
                item = []
                for j in range(len(d[i])):
                    item_final = []
                    element = d[i][j]
                    item.append(element)
                    item = sorted(item, key=lambda x:x[1],reverse=True)
                    for k in range(len(item)):
                        index = int(item[k][0])
                        item_final.append(index)
                full.append(item_final)
        full1 = [full for full,_ in itertools.groupby(full)]
    elif abs(m)>0.268:
        if direction == 0:
            full = []
            for i in d:
                item = []         
                for j in range(len(d[i])):
                    item_final = []
                    element = d[i][j]
                    item.append(element)
                    item = sorted(item, key=lambda x:x[2],reverse=False)
                    for k in range(len(item)):
                        index = int(item[k][0])
                        item_final.append(index)
                full.append(item_final)
        elif direction == 1:
            full = []
            for i in d:
                item = []
                for j in range(len(d[i])):
                    item_final = []
                    element = d[i][j]
                    item.append(element)
                    item = sorted(item, key=lambda x:x[2],reverse=True)
                    for k in range(len(item)):
                        index = int(item[k][0])
                        item_final.append(index)
                full.append(item_final)        
        full1 = [full for full,_ in itertools.groupby(full)]
    return full1

# Function to zigzag provided direction and list
def zigzag(di):
    layer = []
    row = len(di)
    for i in range(row):
        x = len(di[i])
        layer.append(x)
    
    col = max(layer)
    a = [x1+[0]*(col - len(x1)) for x1 in di]

    evenRow = 0
    oddRow = 1
    index = []
    while evenRow < row:
        for i in range(col):
            x = (a[evenRow][i])
            index.append(x)
        evenRow = evenRow + 2

        if oddRow < row:
            for i in range(col - 1, -1, -1):
                x = (a[oddRow][i])
                index.append(x)
        oddRow = oddRow + 2

    while(i<len(index)):
        if(index[i]==0):
            index.remove(index[i])
            col = col -1
            continue
        i = i+1
	
    index = [x - 1 for x in index]
    index = list(dict.fromkeys(index))
    return index
    

if __name__=='__main__':
    thisdict = {
        0:[],
        1:[[1,0,1],[2,0,2],[3,0,3],[4,1,2]],
        2:[[5,1,1],[4,1,2],[6,1,3],[7,1,4]],
        3:[[8,2,1],[9,2,2]],
        4:[],
        5:[[10,3,1]],
        6:[],
        7:[[11,3,2],[12,3,3]]
        
        }
    print(thisdict)
    thislist = slicing(thisdict,0.25,1)
    print(thislist)
    print(zigzag(thislist))
    
