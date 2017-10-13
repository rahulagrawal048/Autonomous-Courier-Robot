'''
* Team Id: 3208
* Author List: Rahul Agrawal, Sarthak Gandhi, Abhinav Ahuja, Lakshay Sahni
* Filename: packages.py
* Theme: Courier Service ;eYRC Specific
* Functions: nodes(), shape(), addindict(), pickup(), updatefinalpicking(), findsourceandtarger(), main()
* Global Variables: NONE
*
'''

import numpy as np
import cv2
from collections import defaultdict
from operator import itemgetter
import sys
from scipy.spatial import distance
import scipy
import dijikstra
from tspgit import solve_tsp


'''
* Function Name: nodes
* Input: color_shapem grid, poin1
* Output: min1
* Logic: Returns the node nearest to the package to be delivered

'''

def nodes(color_shape,grid,poin1):
    min1=()
    minn=sys.maxint
    temp=()
    for m in range(0,len(grid)):
    
            if abs(cv2.pointPolygonTest(color_shape[0],grid[m],True))<minn:
                minn=abs(cv2.pointPolygonTest(color_shape[0],grid[m],True))
                temp=grid[m]
                
    min1=poin1[temp]
    return min1
'''
* Function Name: shape
* Input: contours
* Output: shape specific contours
* Logic: Identifies the shape of color-wise contours using their area
*
'''

def shape(contours):

    square=[]
    circle=[]
    triangle=[]

    for cnt in contours:
           
        if cv2.contourArea(cnt)>550:
            cv2.drawContours(img,[cnt],0,(0,0,0), 2)
            square.append(cnt)
        if cv2.contourArea(cnt)>400 and cv2.contourArea(cnt)<500:
            cv2.drawContours(img,[cnt],0,(0,0,0), 2)
            circle.append(cnt)
        if cv2.contourArea(cnt)>200 and cv2.contourArea(cnt)<300:
            cv2.drawContours(img,[cnt],0,(0,0,0), 2)
            triangle.append(cnt)

    return square,circle,triangle

'''
* Function Name: addindict
* Input: c2color,min1,min2, color, shape
* Output: None
* Logic: updates c2color dictionary
*
'''
def addindict(c2color,min1,min2,color,shape):
    if min1 not in c2color:
        c2color[min1]=[(color,shape)]
    else:
        c2color[min1].append((color,shape))

    if min2 not in c2color:
        c2color[min2]=[(color,shape)]
    else:
        c2color[min2].append((color,shape))

'''
* Function Name: pickup
* Input: color_shape, boxes
* Output: min2
* Logic: Identifies the warehouse in which the delivery package is present using point polygon test and assigns the corressponding pickup junction
*
'''

def pickup(color_shape,boxes):

    centroid=[]
    min2=()
    M = cv2.moments(color_shape[1])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    centroid.append((cx,cy))
    for i in range(0,len(boxes)):
        if(cv2.pointPolygonTest(boxes[i],(cx,cy),False))==1:
            min2=(1,i+1)
    return min2   

'''
* Function Name: updatefinalpicking
* Input: final,min1,picking,min2,coloe
* Output: None
* Logic: updates list of pickup and delivery junctions
*
'''

def updatefinalpicking(final,min1,picking,min2,color):
    final.append((min1,color))
    picking.append((min2,color))

'''
* Function Name: findsourceandtarget
* Input: img, grid, poin1, boxes
* Output: list of pickup and delivery junctions
* Logic: Identifies list of pickup and delivery junctions using contours, shape detection, and point polygon test
*
'''

def findsourceandtarget(img,grid,poin1,boxes):
    #all things related to finding source and destination
    c2color=dict()
    #for purple color
    MIN=np.array([250,0,250],np.uint8)
    MAX=np.array([255,0,255],np.uint8)
    purple=cv2.inRange(img, MIN, MAX);
    #edges1 = cv2.Canny(purple,150,200)
    contours, hierarchy = cv2.findContours(purple,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    purple_square=[]
    purple_circle=[]
    purple_triangle=[]
    purple_square, purple_circle, purple_triangle= shape(contours)    
    min1=[]
    min2=[]
    final=[]
    picking=[]
    if len(purple_square)!=0:
        min1=nodes(purple_square,grid,poin1)
        min2=pickup(purple_square,boxes)
        updatefinalpicking(final,min1,picking,min2,"purple")
        addindict(c2color,min1,min2,"purple","square")
    if len(purple_circle)!=0:
        min1=nodes(purple_circle,grid,poin1)
        min2=pickup(purple_circle,boxes)
        updatefinalpicking(final,min1,picking,min2,"purple")
        addindict(c2color,min1,min2,"purple","circle")
        
    if len(purple_triangle)!=0:
        min1=nodes(purple_triangle,grid,poin1)
        min2=pickup(purple_triangle,boxes)
        updatefinalpicking(final,min1,picking,min2,"purple")
        addindict(c2color,min1,min2,"purple","triangle")
    
    #for blue color
    MIN=np.array([250,250,0],np.uint8)
    MAX=np.array([255,255,0],np.uint8)
    blue=cv2.inRange(img, MIN, MAX);
    contours, hierarchy = cv2.findContours(blue,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    blue_square=[]
    blue_circle=[]
    blue_triangle=[]
    blue_square, blue_circle, blue_triangle= shape(contours)    
    min1=[]
   
    if len(blue_square)!=0:
        min1=nodes(blue_square,grid,poin1)
        min2=pickup(blue_square,boxes)
        updatefinalpicking(final,min1,picking,min2,"blue")
        addindict(c2color,min1,min2,"blue","square")
        
    if len(blue_circle)!=0:
        min1=nodes(blue_circle,grid,poin1)
        min2=pickup(blue_circle,boxes)
        updatefinalpicking(final,min1,picking,min2,"blue")
        addindict(c2color,min1,min2,"blue","circle")
        
    if len(blue_triangle)!=0:
        min1=nodes(blue_triangle,grid,poin1)
        min2=pickup(blue_triangle,boxes)
        updatefinalpicking(final,min1,picking,min2,"blue")
        addindict(c2color,min1,min2,"blue","triangle")
        

    
    #for green color
    MIN=np.array([0,254,0],np.uint8)
    MAX=np.array([1,255,0],np.uint8)
    green=cv2.inRange(img, MIN, MAX);
    contours, hierarchy = cv2.findContours(green,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    green_triangle=[]
    green_circle=[]
    green_square=[]
    green_square, green_circle, green_triangle= shape(contours)    
    min1=[]
   
    if len(green_square)!=0:
        min1=nodes(green_square,grid,poin1)
        min2=pickup(green_square,boxes)
        updatefinalpicking(final,min1,picking,min2,"green")
        addindict(c2color,min1,min2,"green","square")
        
    if len(green_circle)!=0:
        min1=nodes(green_circle,grid,poin1)
        min2=pickup(green_circle,boxes)
        updatefinalpicking(final,min1,picking,min2,"green")
        addindict(c2color,min1,min2,"green","circle")

    if len(green_triangle)!=0:
        min1=nodes(green_triangle,grid,poin1)
        min2=pickup(green_triangle,boxes)
        updatefinalpicking(final,min1,picking,min2,"green")
        addindict(c2color,min1,min2,"green","triangle")
        
    
    #for orange color
    MIN=np.array([0,125,254],np.uint8)
    MAX=np.array([0,127,255],np.uint8)
    orange=cv2.inRange(img, MIN, MAX);
    contours, hierarchy = cv2.findContours(orange,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    orange_triangle=[]
    orange_circle=[]
    orange_square=[]
    orange_square, orange_circle, orange_triangle= shape(contours)    
    min1=[]
   
    if len(orange_square)!=0:
        min1=nodes(orange_square,grid,poin1)
        min2=pickup(orange_square,boxes)
        updatefinalpicking(final,min1,picking,min2,"orange")
        addindict(c2color,min1,min2,"orange","square")
        
    if len(orange_circle)!=0:
        min1=nodes(orange_circle,grid,poin1)
        min2=pickup(orange_circle,boxes)
        updatefinalpicking(final,min1,picking,min2,"orange")
        addindict(c2color,min1,min2,"orange","circle")
        
    if len(orange_triangle)!=0:
        min1=nodes(orange_triangle,grid,poin1)
        min2=pickup(orange_triangle,boxes)
        updatefinalpicking(final,min1,picking,min2,"orange")
        addindict(c2color,min1,min2,"orange","triangle")
        
    return final,picking,c2color


'''
* Function Name: decidedirection
* Input: length, shortestpath
* Output: prints the directions in which the robot need to travel
* Logic: Decides direction at the blue junctions according to the elements in the shortest path
*
'''

def decidedirection(length,shortestpath):

	
    print "move forward"       
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

                print "move forward"


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

                    print "move forward"

        
        i+=1


'''
* Function Name: next pickup
* Input: lis4, firstdestination, picked, trav
* Output: nextdestination, picked
* Logic: finds the next coordinate in the path
*
'''

def nextpickup(lis4,firstdestination,picked,trav):
    #print "initial",lis4
    #print "first dest.", firstdestination
    
    lis5=[x for x in lis4 if cmp(x,firstdestination)!=0]
    del lis4[:]
    lis4.extend(lis5)
    #print "lis4",lis4
    if(len(lis4)!=0):
    	
    
    	fpt2spt=distance.cdist(lis4,[firstdestination],"euclidean").tolist()
    	fpt2spt=fpt2spt.index(min(fpt2spt))
    	nextdestination=lis4[fpt2spt]
    	picked.extend([z for (x,y,z) in trav if cmp(y,nextdestination)==0])
    	return nextdestination, picked
    	
    	'''for i in fpt2spt:
        	if (i[0]==0.0):
           		fpt2spt.remove(i)'''
   	#if(len(lis4)==0):
		#return

'''
* Function Name: updategra_dijikstra
* Input: gra, graph, poin, white
* Output: n2npath
* Logic: Finds the final path using dijikstra algorithm
*
'''
def updategra_dijikstra(gra,graph,poin,white):
    
    n2npath=dict()
    for i in range(len(graph)):
        for j in range(len(graph)):
            if i==j or gra[i][j]!=0:
                continue
            n2npath[(graph[i],graph[j])]=dijikstra.stra(graph[i],graph[j],poin,white)
            l=n2npath[(graph[i],graph[j])][1:]#[x for x in n2npath[(graph[i],graph[j])]]
            #print l
            l.append(graph[j])
            l.reverse()
            n2npath[(graph[j],graph[i])]=l
            gra[i][j]=len(n2npath[(graph[i],graph[j])])
            gra[j][i]=gra[i][j]
    return n2npath

'''
* Function Name: processimage
* Input: img
* Output: Final path
* Logic: Finds the final path to be traversed by the robot by identifying the junctions and using dijikstra algorithm. Travelling salesman algorithm is also used
 to find the final path
*
'''

def processimage(img):
    
    a=0
    b=0
    grid=[]
    poin=defaultdict(list)#(0,1)---->(pixels)
    poin1=defaultdict(list)#(pixel)------>(0,1)
    #resize Image
    img = cv2.resize(img,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
    BLUE=[0,0,0]
    #add border
    img= cv2.copyMakeBorder(img,5,5,5,5,cv2.BORDER_CONSTANT,value=BLUE)
    h,w,c=img.shape
    #crop pickup junctions
    warehouse=img[0:115,:,:]
    #cv2.imshow("warehouse",warehouse)
    MIN=np.array([200,200,200],np.uint8)
    MAX=np.array([255,255,255],np.uint8)
    mines=cv2.inRange(img, MIN, MAX);
    kernel = np.ones((4,4),np.uint8)
    erosion = cv2.erode(mines,kernel,iterations = 1)
    boxes, hierarchy = cv2.findContours(erosion,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    boxes.reverse()
    white=[]
    traffic=[]
    for cnt in boxes:
        if cv2.contourArea(cnt)>100:
            white.append(cnt)
    #print len(white)
    #identify nodes coordinates(in discrete value)
    for a in range(0,7):
        for b in range(0,7):
            y=(a*(h-30))/6 +13
            x=(b*(w-30))/6+13
            grid.append((x,y))
            #discrete value conversion
            poin[(a,b)]=((x,y))
            poin1[(x,y)]=(a,b)
    
    #cicle on coordinates
    #print poin
    for i in range(0,len(grid)):
        cv2.circle(img,grid[i], 5, (0,0,255), -1)
    
    #for white boxes in warehouse
   
    MIN=np.array([255,255,255],np.uint8)
    MAX=np.array([255,255,255],np.uint8)
    mines=cv2.inRange(warehouse, MIN, MAX);
    boxes, hierarchy = cv2.findContours(mines,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    boxes.reverse()
    cv2.drawContours(warehouse,boxes,-1,(0,0,255), 3)
    #cv2.imshow("warehouse",warehouse)

    final1,picking1,c2color=findsourceandtarget(img,grid,poin1,boxes)

    final=[x for (x,y) in final1 ]
    picking=[x for (x,y)  in picking1 ]
    
    print "Pickup Junctions",picking1
    print "Delivery Junctions",final1
    start=(6,0)
    finalpath=[]
    sp=[]
    
    i=0
    a=0
    while (picking1 and a<2):     
	    result=distance.cdist(final, [(1,3)], 'euclidean').tolist()
	    #print "finalll",final
	    #print "pickingg",picking
	    i=0
	    for x in result:
	      x.append(i)
	      i+=1

	    s2d=dict()
	    d2s=dict()
	    for i in range(0,len(picking)):
	        s2d[picking[i]]=final[i]
	        d2s[final[i]]=picking[i]


	    # print result
	    result=sorted(result)
	    #print result
	    i=0
	    m=0
	    trav=[]
	    for x in result:
	      if(i>=4 and m<len(picking1)):
	        break
	      i+=1
	      m=m+1
	      index=x[1]
	      trav.append((final[index],picking[index],final1[index][1]))
	    #print "first 4 minimum"
	    cv2.imshow("images",img)

	    #print "trav",trav
	    lis4=[y for (x,y,z) in trav]


	    
	    #print lis4
	    st2fpt=distance.cdist(lis4,[start],"euclidean").tolist()
	    st2fpt=st2fpt.index(min(st2fpt))
	    firstdestination=lis4[st2fpt]

	    #print "firstdestination",firstdestination
	    
	    finalpath.append(dijikstra.stra(start,firstdestination,poin,white))
	    sp.extend(dijikstra.stra(start,firstdestination,poin,white))
	    
	    picked=[z for (x,y,z) in trav if cmp(y,firstdestination)==0]
	    #print picked
	    if(a==0):      
		    while (len(picked)<4):
		    	#k=k+1
		        nextdestination, picked=nextpickup(lis4,firstdestination,picked,trav)
		        #print "nextdestination", nextdestination
		        #print picked
		        finalpath.append(dijikstra.stra(firstdestination,nextdestination,poin,white))
		        sp.extend(dijikstra.stra(firstdestination,nextdestination,poin,white))
		        firstdestination=nextdestination


	    if(a==1):

			while(len(picked)<1):
				print "ss"
		        nextdestination, picked=nextpickup(lis4,firstdestination,picked,trav)
		        #print "nextdestination", nextdestination
		        #print picked
		        finalpath.append(dijikstra.stra(firstdestination,nextdestination,poin,white))
		        sp.extend(dijikstra.stra(firstdestination,nextdestination,poin,white))
		        firstdestination=nextdestination				
		        
	    
	    #print picked
	    #print finalpath

	    graph=[]
	    graph.append(nextdestination)
	    graph.extend([x for (x,y,z) in trav])
	    #print "graph",graph
	    changedgraph=[]
	    for i in graph:
	        if i not in changedgraph:
	            changedgraph.append(i)
	    graph=changedgraph
	    #print "changed graph",graph
	    gra=[[0 for x in range(len(graph))] for x in range(len(graph))] 
	    n2npath=updategra_dijikstra(gra,graph,poin,white)
	    #print n2npath
	    #print "graph matrix",gra
	    path=solve_tsp(gra)
	    if 0 in path:
	        path.remove(0)
	    #print path
	    li=[]
	    for i in path:
	        li.append(changedgraph[i])
	    #print li
	    #print li
	    source=nextdestination
	    #print n2npath
	    for i in li:
	        l=n2npath[(source,i)]
	        finalpath.append(l)
	        sp.extend(l)
	        source=i

	    for (x,y,z) in trav:
	    	if (y,z) in picking1:
	    		picking1.remove((y,z))
	    	if (x,z) in final1:
	    		final1.remove((x,z))
	    	for i in range(0,len(final)):
	    		#print i,picking,final
	    		if cmp((y,x),(picking[i],final[i]))==0:
	    			del final[i]
	    			del picking[i]
	    			break
	    if len(li)>0:
	    	start=li[len(li)-1]
	    # print start
	    #print "picking",picking1
	    #print "final",final1
	    #print "shortest path", sp
	    #print "final1",finalpath
	    a+=1
    finalpath.append(li[len(li)-1])
    sp.append(li[len(li)-1])
    #print "final",finalpath
    print "\nFinal path to be traversed by the robot"
    print sp

    return finalpath, sp

'''
* Function Name: main
* Input: None
* Output: The final path and the directions to be taken by the robot
* Logic: As explained above
*
'''
if __name__ == "__main__":
    
    img = cv2.imread('test4.jpg')
    finalpath, sp=processimage(img)
    l=len(sp)

    print "\nDirections to be taken by the robot at each node in the final path"

    decidedirection(l,sp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()