#Module in which we have function regarding rotation of Arrays
#Two Type of Rotations i.e. Left and Right Rotation.


#Reverse the whole Array in the Range(start to end) arguments used in Left and Right Rotations
def ReverseArray(start, end, arr):
    reverseCount=end-start+1  #total No of Elements we need to reverse in the giiven range
    counter=0
    while(reverseCount//2 != counter): #divide the range in half (in case of even no problem) (in case of odd we floor them )
        arr[start+counter],arr[end-counter]= arr[end-counter],arr[start+counter] #swap two extreme corner elements
        counter = counter +1
    return arr
    """This Function will Reverse the range in array given by start and end Arguements"""

    
    
#Rotate Array From Left and place the Elements given by Rotations on Right of array
def LeftRotate(arr, size, rotation): #array->[1,2,3,4,5],  size=5,   rotation=2
    """This Function will take Array, Size of Array and No. of Rotations as Arguements"""
    #1. Check Rotation Size
    if(rotation<=size):
        #1. step 1 reverse whole array
        start=0
        end=size-1
        arr=ReverseArray(start, end, arr) #->-[5,4,3,2,1]

        #2. Divide arrays on the base of No of Rotation and reverse them indivitually
        #first subArra and its Reversal
        start=0
        end=size-rotation-1
        arr=ReverseArray(start, end, arr) #->[3,4,5,2,1]


        #3. Second SubArray and its Reversal
        start= size-rotation
        end=size-1
        arr = ReverseArray(start, end, arr) #->[3,4,5,1,2]
        return arr
    else:
        print("Enter valid Number of rotation i.e. rotations must less than or equal to array size")
        
        
        
#Rotate Array from Right and Put Elements given in rotations at Left of Array
def RightRotate(arr, size, rotation): #array->[1,3,5,7,9,11,13,15],  size=8,   rotation=3
    """This Function will take Array, Size of Array and Positive No. of Rotations as Arguements"""
    #1. Check Rotation Size
    if(rotation<=size):
        #1. step 1 reverse whole array
        start=0
        end=size-1
        arr=ReverseArray(start, end, arr) #->-[15,13,11,9,7,5,3,1]

        #2. Divide arrays on the base of No of Rotation and reverse them indivitually
        #second sub array and reversal
        start=rotation
        end=size-1
        arr = ReverseArray(start, end, arr) #-[15,13,11,1,3,5,7,9]
        
        #first subArra and its Reversal
        start=0
        end=rotation-1
        arr=ReverseArray(start, end, arr)#->[11,13,15,1,3,5,7,9]
        return arr
    else:
        print("Enter valid Number of rotation i.e. rotations must less than or equal to array size")