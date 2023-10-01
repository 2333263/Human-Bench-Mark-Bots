import pyautogui
import numpy as np
from skimage.color import rgb2gray
from skimage import measure
import mss


def main():
    while True:
        with mss.mss() as sct: #take screenshot
            temp=sct.monitors[1]  #this is because i have 2 monitors, you may need to change this
            monitor={'left':1068+temp['left'],'top':223+temp['top'],'width':1,'height':1} #get region of screenshot, this ensures we are only taking screenshots in the area that targets can spawn in
            screen=np.array(sct.grab(monitor)) #take screenshot
            screen=screen[:,:,:3]
            
        if(screen[0][0][0]==209 and screen[0][0][1]==135 and screen[0,0,2]==43):
            saveRegion=pyautogui.locateOnScreen('reaction time/saveTime.png')
            if(saveRegion!=None):
                break
            else:
                pyautogui.click(1068,223)
        elif(screen[0][0][0]==106 and screen[0][0][1]==219 and screen[0][0][2]==75):
            pyautogui.click(1068,223)
        
        
if __name__=="__main__":
    main()