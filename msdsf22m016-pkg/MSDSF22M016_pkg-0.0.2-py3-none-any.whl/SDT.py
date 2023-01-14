AUTHOR = 'Shumaila Zahid'

# Function to calculate Speed
def cal_speed(dist, time):
    print(" Distance(km) :", dist);
    print(" Time(hr) :", time);
    return dist / time;
 
# Function to calculate distance travelled
def cal_dis(speed, time):
    print(" Time(hr) :", time) ;
    print(" Speed(km / hr) :", speed);
    return speed * time;
 
# Function to calculate time taken
def cal_time(dist, speed):
    print(" Distance(km) :", dist);
    print(" Speed(km / hr) :", speed);
    return dist / speed;