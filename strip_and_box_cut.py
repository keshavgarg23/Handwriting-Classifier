import cv2
import glob
import os

box_size = 113
counter = 1
crp_save_parent_folder = './cropped/'


def crop(image,offset=box_size):
        global counter
        start_w = 0
        start_h = 0
        (h,w,_) = image.shape
        while(start_h<h):       # not needed as such but if need of verticle cropping then needed
                while(start_w<w):
                        if(start_w+offset>w):
                                break
                        cropped = image[start_h:start_h+offset,start_w:start_w+offset]
                        cropped = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
                        # cv2.imshow('test',cropped)
                        # if(cv2.waitKey(0)& 0xFF == ord('q')):
                        #         break
                        cv2.imwrite(destination_folder+'/'+str(counter)+'.jpg',cropped)
                        start_w+=offset
                        counter+=1
                start_h+=offset

def resize_image(cropped):
        (h,w,c) = cropped.shape
        ratio = box_size/h
        w = w*ratio
        h=box_size
        cropped = cv2.resize(cropped,[int(w),int(h)],interpolation=cv2.INTER_AREA)
        return cropped



def save_pieces(source_img,box_size):
        img = cv2.imread(source_img)
        (h,w,c) = img.shape
        im2 = img
        print(h,w)
        global ratio
        if(h<w):
                ratio=720/h
                h=720
                w=int(ratio*w)
        else:
                ratio = 1240/h
                h=1240
                w = int(ratio*w)
        img = cv2.resize(img,[w,h],interpolation=cv2.INTER_AREA)        # resampling using pixel area relation
        
        print(ratio)
        
        print('W: ' ,w,'H: ',h)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  


        ret,thresh1 = cv2.threshold(gray, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)              # ret is threshold used
        print(ret)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 2)
        # cv2.imshow('test',dilation)
        # cv2.waitKey(0)
        # return

        #---Finding contours ---
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        img_cnt = 0
        for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                # if(w>25 and h>11):
                #         cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if(w>25 and h>11):
                        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                        x,y,w,h = int(x/ratio),int(y/ratio),int(w/ratio),int(h/ratio)
                        cropped = im2[y:y+h,x:x+w]
                        # cv2.imshow('cropped',cropped)
                        # cv2.waitKey(0)
                        resized = resize_image(cropped)         # convert height to box size mantaining the aspect ratio
                        # cv2.imshow('TEST',resized)
                        # cv2.waitKey(0)
                        crop(resized)           # crop and save box size boxes
                        img_cnt+=1



#--------------------------------MAIN----------------------------------



source_folder = './full_page_categorised/'

if(not os.path.isdir(crp_save_parent_folder)):
        os.mkdir(crp_save_parent_folder)

for auth_path in glob.glob(source_folder+'/*'):
        global destination_folder
        destination_folder = crp_save_parent_folder+auth_path.split('/')[-1]

        if(not os.path.isdir(destination_folder)):      # create folder if not there
                print('creating folder')
                os.mkdir(destination_folder)
        for img_path in glob.glob(auth_path+'/*'):
                print(img_path)
                save_pieces(img_path,box_size)