import numpy as np
import cv2,time

template = cv2.imread('template.jpg')
    
def get_pos(image,template=template): 
    #image = cv2.imread('image.jpg')
    
    # resize images
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5) 
    template = cv2.resize(template, (0,0), fx=0.5, fy=0.5) 
     
    # Convert to grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
     
    # Find template
    result = cv2.matchTemplate(imageGray,templateGray, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if (max_val/abs(min_val)) > 0.8 and (max_val/abs(min_val)) < 1.2:
        top_left = max_loc
        h,w = templateGray.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)
        #print("min max",min_val, max_val, min_loc, max_loc,sep="\n")
        #screen shape
        sh,sw = 720,1280

        cv2.rectangle(image,top_left, bottom_right,(0,0,255),4)

        #image shape
        pos = (top_left[0] + (w/2), top_left[1] + (h/2))

        #scale
        h,w = imageGray.shape
        print(sh/h,sw/w,h,w)
        pos = (((sh*pos[0])/h),((sw*pos[1])/w))
        
    ##    # Show result
    ##    cv2.imshow("Template", template)
        cv2.imshow("Result", image)
          
    ##     
    ##    cv2.moveWindow("Template", 10, 50);
        cv2.moveWindow("Result", 150, 50);
    ##     
    ##    cv2.waitKey(0)
        
        return pos

def main():
    cap = cv2.VideoCapture(0)
    c = 0
    while (cap.isOpened()):
        ret,frame = cap.read()
        if ret:
            frame = cv2.flip(frame,180)
##            if c == 0:
##                cv2.imwrite("template.jpg",frame)
##                template = cv2.imread('template.jpg')
##                c = 1
            r = get_pos(frame)
            if r != None: print(r)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
