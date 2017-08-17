def abs_sub(a,b):
    return (0, abs(a[1] - b[1]))
def get_cluster(dataset):
    classes = [[] for x in range(len(dataset))]
    for d in dataset:
        for value in dataset:
            b = True
            for dr in dataset:
                if d == dr or dr == value:
                    continue
                v1 = abs_sub(value,d)
                v2 = abs_sub(value,dr)
                if v1[1] > v2[1]:
                    b = False
                    
            if b: classes[dataset.index(d)].append(value)
                    
    chunks = [[] for x in range(len(dataset))]
    for x in range(len(classes)):
        for y in classes[x]:
            if dataset[x] in classes[dataset.index(y)]:
                chunks[x].append(y)
    chunk_li = []
    for x in chunks:
        for y in x:
            for a in chunks:
                if a == x:
                    continue
                if y in a:
                    v = x+a
                    for j in v:
                        while v.count(j) > 1:
                            v.remove(j)
                    v = sorted(v)
                    if v not in chunk_li: chunk_li.append(v)
    if len(chunk_li) > 0: chunks = chunk_li.copy()
    chunk_li = []
    for x in chunks:
        if x not in chunk_li:
            chunk_li.append(x)
            
    chunks = chunk_li.copy()
    print("%d class found"%(len(chunks)))
    for x in range(len(chunks)):
        print(("class %d\n{}"%(x)).format(chunks[x]))
    return chunks
##get_cluster([(0.8,1),(1,1),(1,0.8),(1.8,2),(2,2),(2,1.8)])
##get_cluster([(1,2),(2,1),(3,2),(4,1),(5,2),(6,1)])
##get_cluster([(1,1),(1.5,2),(3,3)])

d = {"caleb":"male","christa":"female","nobu":"male","hansel":"male","ade":"male","princess":"female"}
li = []
for x in d:
    if d[x] == "male":
        v = 1
    else:
        v = 0
    li.append((x,v))
get_cluster(li)
