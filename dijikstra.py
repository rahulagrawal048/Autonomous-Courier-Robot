import collections
import cv2

def missing(white, start, neigh, poin):
    centroid=((poin[start][0]+poin[neigh][0])/2,(poin[start][1]+poin[neigh][1])/2);
    missing=[]
    for i in range(0,len(white)):
        if(cv2.pointPolygonTest(white[i],centroid,False))==1:
            missing.append(neigh)
    return missing

def valid(sele,x,y,c2p,visited,white):
	temp=(sele[0]+x,sele[1]+y)
	if temp in c2p and temp not in visited and not missing(white,sele,temp,c2p) and temp not in missing(white,sele,temp,c2p):
		return 1
	else:
		return 0

def Dneigh(sele,c2p,visited,white):
	l=[]
	x=[-1,1,0,0]
	y=[0,0,1,-1]
	for i in range(0,4):
		if(valid(sele,x[i],y[i],c2p,visited,white)==1):
			l.append(((sele[0],sele[1]),(sele[0]+x[i],sele[1]+y[i]),1)) # 1 is wight
	return l

def stra(start,end,c2p,white):
	#print "dijikstra"
	sele=start
	nodenow=[]
	nodenow.append(((-1),sele,1))
	#print nodenow
	i=0
	visited=[]
	temp=dict()
	while nodenow and cmp(sele[1],end)!=0:
		i+=1
		sele=min(nodenow,key=lambda x:x[2])
		#print sele
		visited.append(sele[0])
		neigh=Dneigh(sele[1],c2p,visited,white)

		for x in neigh:
			if x[1] not in temp:
				temp[x[1]]=sele[1]
		nodenow.remove(sele)
		nodenow.extend(neigh)
		#print nodenow
	#print temp
	temp=collections.OrderedDict(sorted(temp.items()))
	#print temp
	sele=sele[0]
	path=[]
	#print temp	
	while cmp(start,sele)!=0:
		#print "gmail"
		path.append(sele)
		sele=temp[sele]
	path.append((start))
	path.reverse()
	return path
	