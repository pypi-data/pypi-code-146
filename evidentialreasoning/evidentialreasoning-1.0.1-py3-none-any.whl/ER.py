#Author : Toan Nguyen Mau
import numpy as np
def ER_Aggregation(input,weights=[]):
    num_N = input.shape[1]-1  
    num_L = input.shape[0] 
    if weights==[]: weights = np.ones(num_L)/num_L
    weights2 = np.repeat([weights],num_N+1,axis=0).transpose()
    input2 = np.multiply(input,weights2)
    for inp in input2:
        inp[num_N] = 1-sum(inp[0:num_N])
    mnI = input2[0]
    for i in range(1,num_L):
        mnI_tmp = input2[i];
        #Calc K
        K=0
        for j in range(num_N):
            for j2 in range(num_N):
                if j !=j2:
                    K+= mnI[j]*mnI_tmp[j2]
        K = 1/(1-K)
        for j in range(num_N):
            tmp = mnI[j]*mnI_tmp[j] + mnI[num_N]*mnI_tmp[j] + mnI[j]*mnI_tmp[num_N]
            mnI[j] = K*tmp;

    mnI[num_N] = 1-sum(mnI[0:num_N])
    return mnI

def ER_Normaliation(input):
    num_N = input.shape[0]-1
    shared_ =input[num_N]/num_N
    output = np.array([input[i] + shared_ for i in range(num_N)])
    return output
if __name__ == "__main__":
    input = np.array([[0,0,0.2,0.2,0.6,0],[0,0,0.2,0.4,0.4,0],[0,0,0.2,0.8,0,0],[0,0,0.4,0.2,0.4,0]])
    weights = np.array([0.25,0.25,0.25,0.25])
    weights = np.array([1,1,1,1])
    a = ER_Aggregation(input,weights)
    print(a)
    b = ER_Normaliation(a)
    print(b)