# -*- coding: cp1252 -*-
import numpy as np
import cv2
import Queue
import collections
from collections import defaultdict
import copy
from operator import itemgetter

######################### Shortest path ##############################
v=0

o=10
t=20
r=2*o-10
centroidd2=[]
def missing_links(img1, neigh1, start,poin1):
    
    #to detect white boxes
    hsv2 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    MIN=np.array([0,0,200],np.uint8)
    MAX=np.array([0,0,255],np.uint8)
    black=cv2.inRange(hsv2, MIN, MAX);
    blur=cv2.medianBlur(black,9)
    edges = cv2.Canny(blur,150,200)
    #contour around white boxes
    contours1, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #drawing golden lines between start and neighbours
    global centroidd2,v
    missing=[]
    v=v+1
    cimg1 = copy.copy(img1)
    
    lines=cv2.line(cimg1,(start),(neigh1),(54,193,245),3)
    
    #detecting golden lines    
    hsv3 = cv2.cvtColor(cimg1, cv2.COLOR_BGR2HSV)
    MIN1=np.array([0,150,180],np.uint8)
    MAX1=np.array([22,255,250],np.uint8)
    black1=cv2.inRange(hsv3, MIN1, MAX1);
    blur1=cv2.medianBlur(black1,9)
    edges1 = cv2.Canny(blur1,150,200)
    #contour around golden lines
    contours2, hierarchy = cv2.findContours(edges1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    M = cv2.moments(contours2[0])
    
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    centroidd2.append((cx,cy))
    cv2.circle(cimg1,(cx,cy),2,(0,255,0),-1)
    
    for k in range(0,len(contours1)):
        if cv2.pointPolygonTest(contours1[k],(cx,cy),False)==1:
          missing.append(neigh1)
  
    return missing    
        

def neighbours(img,start,poin1,visit):
   
    h,w,c=img.shape
    neigh=[]
    global t
    neigh.append((start[0]-(w-t-10)/5,start[1]))
    neigh.append((start[0],start[1]-(h-t-10)/5))
    neigh.append((start[0]+(w-t-10)/5,start[1]))
    neigh.append((start[0],start[1]+(h-t-10)/5))
   
    temp=[]
    for i in neigh:
       
        if i[0]>=0 and i[1]>=0 and i[0]<=h and i[1]<=w and poin1[i] not in visit.keys():
            #append only if points NOT in missing link
            if i not in missing_links(img,i,start,poin1):
                temp.append(i)
   
    neigh1=[]
    for i in temp:
        if poin1[i] not in visit.keys():
            neigh1.append(poin1[i])
   
            
    
    return neigh1


def shortest_path(img):
    '''
    * Function Name: shortest_path
    * Input: img – Any one of the test images
    * Output: length – length of shortest path
              shortest_path – the shortest path as a list of coordinates of form (x,y)
    * Example Call: l, sp = shortest_path(img)
                    >>> l = length, sp = shortest_path 
    '''

    l=(-1,-5)
    
    #add your code here

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    MIN=np.array([0,0,200],np.uint8)
    MAX=np.array([0,0,255],np.uint8)
    black=cv2.inRange(hsv, MIN, MAX);
    blur=cv2.medianBlur(black,9)
    edges = cv2.Canny(blur,150,200)
    
    
    a=0
    b=0
    grid=[]
    poin=defaultdict(list)
    poin1=defaultdict(list)
    h,w,c=img.shape
    #print h,w
    global o,t
    for a in range(0,6):
        for b in range(0,6):
            x=(b*(h-t-10))/5 +o
            y=(a*(w-t-10))/5 +o
            grid.append((x,y))
            poin[(a,b)]=((x,y))
            poin1[(x,y)]=(a,b)

    #Blue Dots
    for i in range(0,len(grid)):
        cv2.circle(img,grid[i], 1, (255,255,0), -1)
    contours1, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    MIN1=np.array([50,150,0],np.uint8)
    MAX1=np.array([200,255,255],np.uint8)
    black1=cv2.inRange(hsv, MIN1, MAX1);
    blur1=cv2.medianBlur(black1,9)
    edges1 = cv2.Canny(blur1,150,200)
    
    contours2, hierarchy = cv2.findContours(edges1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours2, -1, (0,0,255), 3)

    MIN2=np.array([0,150,0],np.uint8)
    MAX2=np.array([0,255,255],np.uint8)
    black2=cv2.inRange(hsv, MIN2, MAX2);
    blur2=cv2.medianBlur(black2,9)
    edges2 = cv2.Canny(blur2,150,200)
    
    contours3, hierarchy = cv2.findContours(edges2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours3, -1, (255,0,0), 3)
    


    start={}
    for i in range(0,len(grid)):
        if  cv2.pointPolygonTest(contours2[0],grid[i],True) > -50 :
            j=i
           
    start=poin1[grid[j]]
   
    end={}
    for i in range(0,len(grid)):
        if  cv2.pointPolygonTest(contours3[0],grid[i],True) > -50 :
            j=i
    img2=img
    img3 = copy.copy(img2)
    cv2.imshow('image',img2)
    end=poin1[grid[j]]
    visit= defaultdict(list)

    q=Queue.Queue()
    q.put(start)
    visit[start]=1
    parent=defaultdict(list)
    element=start
    parent[element]=(-1,-1)
    
    i=0
    while (q.qsize() > 0 and cmp(element,end)!=0):
        i=i+1
        
        element = q.get()
        
        neigh=neighbours(img,poin[element],poin1,visit)
       
        for elementss in neigh:
            q.put(elementss)
            visit[elementss]=1
            parent[elementss]=element
    od=collections.OrderedDict(sorted(visit.items()))
    
    
    solution=[]
    while(cmp(element,(-1,-1))!=0):
        solution.append(element)
        element=parent[element]
    solution.reverse();
    
    for i in range(0,len(solution)-1):
        lines=cv2.line(img3,(poin[solution[i]]),(poin[solution[i+1]]),(54,193,245),10)
     
    cv2.imshow('image',img3)
    final=[]
    for i in range(1,len(solution)):
        final.append(solution[i])
        
    return len(final), final

    
def decidedirection(length,shortestpath):       # this coding is if robot is moving forward, for backward just reverse the directions

    for i in range(1,l-1):


        x0=sp[i-1][0]
        y0=sp[i-1][1]
        x1=sp[i][0]
        y1=sp[i][1]
        x2=sp[i+1][0]
        y2=sp[i+1][1]



        if x1!=x2:

            if y0-y1==1:

                if x1-x2==-1:
                    print "turn left"

                elif x1-x2==1:
                    print "turn right"

            elif y0-y1==-1:

                if x1-x2==1:
                    print "turn left"

                elif x1-x2==-1:
                    print "turn right"

            elif y0-y1==0:

                print "delay(forward or backward)"


        if y1!=y2:

            if x0-x1==1:

                if y1-y2==-1:
                    print "turn right"

                elif y1-y2==1:
                        print "turn left"

            elif x0-x1==-1:

                if y1-y2==1:
                        print "turn right"

                elif y1-y2==-1:
                        print "turn left"

            elif x0-x1==0:

                    print "delay(forward or backward)"

        
        i+=1


########################  Main  #########################
img = cv2.imread('test_image3.jpg')
BLUE=[0,0,0]
           
constant= cv2.copyMakeBorder(img,5,5,5,5,cv2.BORDER_CONSTANT,value=BLUE)
        
img=constant
l, sp=shortest_path(img)
print "Length = ", l, "nodes"
print "Shortest Path:\n", sp

print ""
print "Directions to traverse"
print ""
print "Direction 1: to be decided acc to previous shortest path"
print "Direction 2: to be decided acc to starting node of sp"
decidedirection(l,sp)
cv2.waitKey(0)
cv2.destroyAllWindows()

