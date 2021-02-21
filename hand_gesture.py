import pyautogui
import cv2
import os
import numpy as np
import math
path='C:/Users/admin/Desktop/image processing/video'
    
    
vid_cap=cv2.VideoCapture(0)
    
success,image=vid_cap.read()
success='True'
    
while success:
    success,image=vid_cap.read()
    print('read new frame:',success)
        # get hand data from rectangle
    cv2.rectangle(image,(70,70),(300,300),(0,255,0),0)
    crop_image=image[70:300,70:300]
    #convert to grayscale
    gray=cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
    #applying gaussian blur
    value=(35,35)
    blurred=cv2.GaussianBlur(gray,value,0)
    #thresholdin :otsu's binarization method
    _, thresh1=cv2.threshold(blurred,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    #show threshold image
    cv2.imshow('Threshold',thresh1)
    
    #check Opencv version go avoid unpacking error
    (version,_, _)=cv2.__version__.split('.')
    
    if version=='3':
        img, contours, hierarchy=cv2.findContours(thresh1.copy(),cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE) 
        
    elif version=='2':
        contours , hierarchy=cv2.findCoutours(thresh1.copy(),cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)
        
    #find contour with max area
    cnt=max(contours , key=lambda x:cv2.contourArea(x))
    
    #create bounting rectangle around the contour (can skip bellow the lines)
    x,y,w,h=cv2.boundingRect(cnt)
    cv2.rectangle(crop_image,(x,y),(x+w,y+h),(0,0,255),0)
    
    #finding convex hull
    hull=cv2.convexHull(cnt)
    #finding convex defects
    print(hull)
    
        #drawing conturs
    drawing=np.zeros(crop_image.shape,np.uint8)
    cv2.drawContours(drawing,[cnt] ,-1,(0,255,0),0)
    cv2.drawContours(drawing,[hull],-1,(0,255,0),0)

    hull=cv2.convexHull(cnt,returnPoints=False)

    

    
    defects=cv2.convexityDefects(cnt,hull)
    count_defects=0
    cv2.drawContours(thresh1,contours ,-1,(0,255,0),3)
    
    
    #apllying cosine rule to find angle for all objects
    #wiyth angle,90 degree and ignore the defects
    for i in range(defects.shape[0]):
        s,e,f,d=defects[i,0]
        start=tuple(cnt[s][0])
        end=tuple(cnt[e][0])
        far=tuple(cnt[f][0])
        
        #finding length of all sides of triangle
        a=math.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)
        b=math.sqrt((far[0]-start[0])**2 + (far[1]-start[1])**2)
        c=math.sqrt((end[0]-far[0])**2 + (end[1]-far[1])**2)
    #apply cosine rule
        angle=math.acos((b**2+c**2-a**2)/(2*b*c))*57
        
        #ignore angles>90 and highlight rest
        
        if angle<=90:
            count_defects+=1
            cv2.circle(crop_image,far,1,[0,255,0],-1)
      
            #dist=cv2.pointPolygontest(cnt,far ,true)

#draw line from start to end ie finger tips
        cv2.line(crop_image,start,end,[0,255,0],2)
      #cv2.circle(crop_image,far,1,[0,255,0],-1)
      
      #define actions required
    ''' if count_defects==0:
        cv2.putText(image,'hello',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,2)
    elif count_defects==1:
        cv2.putText(image,'two',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,2)
    elif count_defects==2:
        cv2.putText(image,'three',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,2)
    elif count_defects==3:
        cv2.putText(image,'four',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,2)
    elif count_defects==4:
        cv2.putText(image,'five',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,2)'''
     
    if count_defects>=3:
        pyautogui.press('space')
        cv2.putText(image,'JUMP',(115,80),cv2.FONT_HERSHEY_SIMPLEX,2,2,2)
    
    
       #show image window 
    cv2.imshow('basic hand gesture',image)
    all_image=np.hstack((drawing,crop_image))
    cv2.imshow('countrs',all_image)
  
     
   # cv2.imwrite('C:/Users/admin/Desktop/image processing/video/frame1.jpg',image)
   # cv2.imwrite('C:/Users/admin/Desktop/image processing/video/frame2.jpg',crop_image)
    if cv2.waitKey(1)==ord('q'):
        break
    #k=cv2.waitKey(100)
    #if k==27:
       # break
    
vid_cap.release()
cv2.destroyAllWindows()