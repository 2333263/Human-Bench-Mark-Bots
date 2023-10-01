import pyautogui
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage.exposure import equalize_hist
from skimage.morphology import binary_closing
from skimage import measure
import copy
import pytesseract
from imageio import imread
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_Locations(image,region,ax):
    colours=['red','green','blue','yellow','orange','purple','pink','brown'] #colours of blocks
    gray=rgb2gray(image) #convert to grayscale
    equiz=equalize_hist(gray) #equalize histogram
    thresh=threshold_mean(equiz) #get threshold
    binary=equiz>=thresh #binarize image
    square=np.ones((3,3)) #create square kernel
    closed=binary_closing(binary,square) #close image
    contours=measure.find_contours(closed,0.8) #find contours
    areas=[] #final area to click on
    vals=[] #values
    regions=[] #regions
    
    
    for data in contours:  #get regions
        #get min and max x and y values, theyre squares so this is usefule
        minX=np.min(data[:,1]) 
        maxX=np.max(data[:,1])
        minY=np.min(data[:,0])
        maxY=np.max(data[:,0])
        width=maxX-minX
        height=maxY-minY
        
        if(abs(width-height)<0.0001 and minY>=region[1] and maxY<=region[1]+region[3]):  #0.0001 because sometimes the contontours add a little bit of noise so it ensure we are checking the squares
            #if the region is a square and is in the test region
            regions.append([minX,minY,maxX,maxY]) #append region
            #ax.plot(data[:,1],data[:,0],linewidth=2)
    real_regions=[] #real regions
    
    #sometimes contontours will be picked up for the outside of the square and the inside of the square, so we need to remove the extras
    #this also prevents numbers with holes in them like 0 and 8 from causing issues
    for i in regions: #check if regions are inside other regions
        inside=False
        for j in regions:
            #if region i is not inside any other regions append it to real regions
            if(i!=j):
                if(i[0]>=j[0] and i[1]>=j[1] and i[2]<=j[2] and i[3]<=j[3]): #if region i is inside region j
                    inside=True 
                    break #break out of loop
        if(inside==False): #if region i is not inside any other regions
            real_regions.append(i) #append it to real regions
            #ax.add_patch(plt.Rectangle((i[0],i[1]),i[2]-i[0],i[3]-i[1],fill=False,edgecolor='red',linewidth=2))
    bad=False
    badCount=0
    for i in real_regions: #for each region
        cropped=copy.deepcopy(closed) #copy closed image
        cropped=cropped[int(i[1]):int(i[3]),int(i[0]):int(i[2])] #crop the copied image to be the square we are looking at
        val=pytesseract.image_to_string(cropped,config='--psm 9') #get the value of the square
        val=val.replace(" ","").strip("\n") #remove spaces and newlines
        print(val) #print value
        
        #these are common mistaken values, so we replace them with the correct value
        if(val=='E'):
            val='3'
        elif(val=='41' or val=='411'):
            val='11'
        elif(val=='&'):
            val='8'
        elif(val=='411'):
            val='11'
        elif(val=='Ey'):
            val='38'
        elif(val=='/2.' or val=='(2'):
            val='2'
        elif(val=='142' or val=='42'):
            val='12'
        elif(val=='413'):
            val='13'
        elif(val=='415'):
            val='15'
        elif(val=='EX)'):
            val='30'
        elif(val==',' or val=='|'):
            continue
        if(val not in vals): #if the value is not already in the list of values, just incase we didnt remove the second region earlier
            try:
                areas.append((int(val),i)) #append the value and the region to areas
                vals.append(val) #append the value to vals
            except:
                print("Could not convert to int:",val)
                
                ax.imshow(closed,cmap=plt.cm.gray)
                ax.add_patch(plt.Rectangle((i[0],i[1]),i[2]-i[0],i[3]-i[1],fill=False,edgecolor=colours[badCount],linewidth=2))
                badCount+=1
                bad=True
    
    areas.sort(key=lambda x:x[0]) #sort areas by value
    if(bad):
        plt.show()
        exit()
    print(areas) #print areas
    return(areas) #return areas
   




def main():
    fig,ax=plt.subplots()
    startTest=pyautogui.locateCenterOnScreen('ChimpTest/StartTest.png') #find location of start button 
    if(startTest==None):
        print("Could not find the StartTest button")
        return()
    region=pyautogui.locateOnScreen('ChimpTest/ChimpTest.png') #find location of test region
    pyautogui.click(startTest) #click start button
    
    while(True): #repeat for every level you wish to complete
        image=pyautogui.screenshot() #take screenshot
        image=np.array(image) #convert to numpy array
        locs=get_Locations(image,region,ax) #get locations of blocks
        for i in locs: #click on each block
            pyautogui.click(((i[1][0]+i[1][2])/2,(i[1][1]+i[1][3])/2))
        done=pyautogui.locateCenterOnScreen('ChimpTest/DONE.png')
        if(done!=None):
            break
        continueLoc=pyautogui.locateCenterOnScreen('ChimpTest/continue.png') #find location of continue button
        pyautogui.click(continueLoc) #click continue button
    
if __name__=="__main__":
    main()