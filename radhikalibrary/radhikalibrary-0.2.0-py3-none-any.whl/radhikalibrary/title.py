n=int(input('enter n='))#value of iterators
sum=0#inatilize sum

for i in range(1,n+1): #we have iteration upto n so we do n+1
  for j in range(1,i+1):
    print(2,end='')
  sum+=int(str(2)*i) #sum of that series..str (2)*i repeate 2 i rimes
  if i==n:
    break#here use break to skip + sign at last
  print('+',end='')
  #sum+=int(str(2)*i)#if we did sum here output get upto n-1 term
print('')  
print('sum of series=',sum)    