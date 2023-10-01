import pyautogui
import numpy as np
from skimage.color import rgb2gray
from skimage import measure
import mss


def main(): 
    StartPos=pyautogui.locateCenterOnScreen('Aim Trainer/target.png') #find location of start button
    region=pyautogui.locateOnScreen('Aim Trainer/area.png') #find location of test region
    pyautogui.click(StartPos)  #click start button
    for _ in range(30):  #repeat for every target
        with mss.mss() as sct: #take screenshot
            temp=sct.monitors[1]  #this is because i have 2 monitors, you may need to change this
            monitor={'left':region[0]+temp['left'],'top':region[1]+temp['top'],'width':region[2],'height':region[3]} #get region of screenshot, this ensures we are only taking screenshots in the area that targets can spawn in
            screen=np.array(sct.grab(monitor)) #take screenshot
            screen=screen[:,:,:3] #the mss takes the screen shot in the rgbA format, this is the fastest way to drop the A
        
        gray=rgb2gray(screen) #convert to grayscale
        contours=measure.find_contours(gray,0.8) #find contours
        contour=contours[-1] #the target is always the last contour, probably because skimage searches from the top left

        minY=int(min(contour[:, 0])) #find the min and max x and y values of the contour
        maxY=int(max(contour[:, 0]))
        minX=int(min(contour[:, 1])) 
        maxX=int(max(contour[:, 1])) 
        pyautogui.click(region[0]+(minX+maxX)/2,region[1]+(minY+maxY)/2) #click the center of the contour
        
#there is definitely a better way of doing this, specifically the only part of the region of the screen
# that has the rgb values [255,255,255] are the counter of how many targets are left
# and the target themselves, so if you just find the lowest pixel that is white in the screen shot that is the target

if __name__=="__main__":
    main()