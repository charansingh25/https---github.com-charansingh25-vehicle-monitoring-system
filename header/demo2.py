

RS_gas = 0.0
ratio = 0.0
sensorValue_MQ135 = 0.0
sensorValue_MQ2 = 0.0
sensorValue_MQ7 = 0.0
sensor_volt = 0.0
R1 = 7200.0


analog_values = [246.0, 213.0, 186.0, 172.0, 165.0, 160.0, 165.0, 224.0, 216.0, 259.0, 248.0, 247.0, 283.0, 206.0, 189.0, 201.0, 211.0, 188.0, 192.0, 196.0]  # Replace with your actual analogRead values
analog_values2 = [169.0, 178.0, 163.0, 165.0, 171.0, 175.0, 172.0, 183.0, 179.0, 182.0, 181.0, 183.0, 183.0, 178.0, 187.0, 185.0, 183.0, 182.0, 182.0, 177.0 ]  # Replace with your actual analogRead values
analog_values3 = [159.0, 159.0, 155.0, 154.0, 159.0, 161.0, 158.0, 158.0, 168.0, 160.0, 161.0, 158.0, 166.0, 161.0, 166.0, 160.0, 161.0, 153.0, 165.0, 134.0  ]  # Replace with your actual analogRead values
l = []
for i in analog_values:

    sensorValue_MQ7 = i
    sensor_volt = sensorValue_MQ7 / 1024 * 5.0
    RS_gas = (5.0 - sensor_volt) / sensor_volt
    ratio = RS_gas / R1
    x = 1538.46 * ratio
    mq7Value = pow(x, -1.709)

    l.append(round(mq7Value,2))

print(l)
