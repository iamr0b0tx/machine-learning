import cv2

image = cv2.imread("search.jpg")
sample_image = cv2.imread("sample.jpg")

#cv2.imshow("frame", sample_image[len(sample_image)//4:len(sample_image)//2])
print(sample_image[0:3, 0:3])
##print(search_image[0])
def search_image(image, sample_image):
    if len(sample_image) > len(image) and len(sample_image[0]) > len(image[0]):
        ls = [len(image),len(image[0])]
        l = [len(sample_image), len(sample_image[0])]
        print("ls",ls)
        print("l",l)
        rang = l[0] - (ls[0]-1)
        rang2 = l[1] - (ls[1]-1)
        li = []
        
        for i in range(rang):
            for ii in range(rang2):
                print(i,i+ls[0], ii,ii+ls[1])
                #cv2.imshow("frame",sample_image[i:i+ls[0]])
                #cv2.imwrite("g.jpg",sample_image[i:i+ls[0], ii:ii+ls[1]])
                #input()
                check_range = sample_image[i:i+ls[0], ii:ii+ls[1]]
                li.append(abs(check_range - image))

        for x in li:
            print(x)
            

if __name__ == "__main__":
    search_image(image, sample_image)
