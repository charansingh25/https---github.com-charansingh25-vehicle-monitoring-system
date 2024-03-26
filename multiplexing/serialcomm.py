import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest

###################### CONNECTION START ########################3

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

for oneport in ports:
    portList.append(str(oneport))
    print(str(oneport))

val = input("select port : COM")
print(val)

portVar = "COM" + str(val)

for x in range(0, len(portList)):
    if portList[x].startswith("COM" + str(val)):
        print(portList[x])


serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

######################## CONNECTION END ###################

def map_value(value, from_low, from_high, to_low, to_high):
    # Map the 'value' from the 'from' range to the 'to' range
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)




mq135 = np.array([], dtype=float)
mq2 = np.array([], dtype=float)
mq7 = np.array([], dtype=float)

mq135_ppm = np.array([], dtype=float)
mq135_ppm = np.array([], dtype=float)
mq135_ppm = np.array([], dtype=float)


analog_mq135 = np.array([], dtype=float)
analog_mq2 = np.array([], dtype=float)
analog_mq7 = np.array([], dtype=float)

temp1 = ""
temp2 = ""
temp3 = ""
temp4 = ""
temp5 = ""
temp6 = ""
temp7 = ""
temp8 = ""
temp9 = ""

demo_value = 0


path = "E:\\Coding\\iot\\vehicle-monitoring\\modelfiles"
model = "5"
f = open(f"{path}\model_{model}.txt", "w")
while (demo_value < 40):
    if serialInst.in_waiting:
        packet = serialInst.readline()
        print(packet.decode('utf').rstrip())


        if(packet.decode('utf')):
            l = packet.decode('utf').split()
            # print(l)
            mq135_list = []
            mq2_list = []
            mq7_list = []


            if 'Analog' in packet.decode('utf'):
            # If the data is in analog form, store it in separate arrays
                mq135_demo = l[0].split(':')
                mq2_demo = l[1].split(':')
                mq7_demo = l[-1].split(':')

                # print(mq135_demo)
                # print(mq135_demo[0], mq135_demo[-1])
                analog_mq135 = np.append(analog_mq135, float(mq135_demo[-1]))
                analog_mq2 = np.append(analog_mq2, float(mq2_demo[-1]))
                analog_mq7 = np.append(analog_mq7, float(mq7_demo[-1]))

            else :

                mq135_demo = l[0].split(':')
                mq2_demo = l[1].split(':')
                mq7_demo = l[-1].split(':')

                # print(mq135_demo, mq2_demo, mq7_demo)

                mq135_value = float(mq135_demo[-1])
                mq2_value = float(mq2_demo[-1])
                mq7_value = float(mq7_demo[-1])

                mq135_value = round(((mq135_value)/1e6)*100, 2)

                temp1 += str(mq135_value) + " "
                temp2 += str(mq2_value) + " "
                temp3 += str(mq7_value) + " "

                mq135 = np.append(mq135, mq135_value)
                mq2 = np.append(mq2, mq2_value)
                mq7 = np.append(mq7, mq7_value)

                # # mq135 ppm converting
                # mq135_mapped = map_value(mq135_value, 0, 1023, 10, 1500)

                # # mq2 converting
                # mq2_mapped = map_value(mq2_value, 0, 1023, 300, 10000)

                # #mq7 converting 
                # mq7_mapped = map_value(mq7_value, 0, 1023, 20, 2000)

                # mq2_value = mq2_value
                # mq135_ppm = np.append(mq135_ppm, )




            print(mq135)
            print(mq2)
            print(mq7)


            demo_value+=1

    

serialInst.close()
# print(temp1)
# print(temp2)
# print(temp3)
# f.write(temp1+"\n")
# f.write(temp2+"\n")
# f.write(temp3)

# np.savetxt(f, mq135)
# np.savetxt(f, mq2)
# np.savetxt(f, mq7)



print('\n')
data = np.column_stack((mq135, mq2, mq7))


if data.shape[0] >0:
    # Use Isolation Forest for outlier detection
    clf = IsolationForest(contamination=0.1)  # Adjust the contamination parameter based on your dataset
    outliers = clf.fit_predict(data)

    # Filter out the outliers from the original arrays
    mq135_filtered = mq135[outliers != -1]
    mq2_filtered = mq2[outliers != -1]
    mq7_filtered = mq7[outliers != -1]

    # print(mq135_filtered)
    # print(mq2_filtered)
    # print(mq7_filtered)


    for mq135__ in mq135_filtered:
        temp4 += str(mq135__) + " "

    for mq2__ in mq2_filtered:
        temp5 += str(mq2__) + " "
    
    for mq7__ in mq7_filtered:
        temp6 += str(mq7__) + " "

    
    for analog_1 in analog_mq135:
        temp7 += str(analog_1) + " " 

    for analog_2 in analog_mq2:
        temp8 += str(analog_2) + " " 
    
    for analog_3 in analog_mq7:
        temp9 += str(analog_3) + " " 


    print(temp4)
    print(temp5)
    print(temp6)


    f.write(temp4+"\n")
    f.write(temp5+"\n")
    f.write(temp6+"\n")

    f.write('\n')
    f.write(temp7+"\n")
    f.write(temp8+"\n")
    f.write(temp9+"\n")
    

    f.close()


        
    # Plot original data with dots
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 2, 1)
    plt.scatter(range(len(mq135)), mq135, label='Original MQ135', marker='.')
    plt.title('MQ135 Original Data')

    plt.subplot(3, 2, 3)
    plt.scatter(range(len(mq2)), mq2, label='Original MQ2', marker='.')
    plt.title('MQ2 Original Data')

    plt.subplot(3, 2, 5)
    plt.scatter(range(len(mq7)), mq7, label='Original MQ7', marker='.')
    plt.title('MQ7 Original Data')

    # Plot filtered data with dots
    plt.subplot(3, 2, 2)
    plt.scatter(range(len(mq135_filtered)), mq135_filtered, label='Filtered MQ135', marker='.')
    plt.title('MQ135 Filtered Data')

    plt.subplot(3, 2, 4)
    plt.scatter(range(len(mq2_filtered)), mq2_filtered, label='Filtered MQ2', marker='.')
    plt.title('MQ2 Filtered Data')

    plt.subplot(3, 2, 6)
    plt.scatter(range(len(mq7_filtered)), mq7_filtered, label='Filtered MQ7', marker='.')
    plt.title('MQ7 Filtered Data')

    plt.tight_layout()
    plt.show()


