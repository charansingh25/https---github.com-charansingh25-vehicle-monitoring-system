import math
import time

# ****************** MQResistanceCalculation ****************************************
# Input:   raw_adc - raw value read from ADC, which represents the voltage
# Output:  the calculated sensor resistance
# Remarks: The sensor and the load resistor form a voltage divider. Given the voltage
#          across the load resistor and its resistance, the resistance of the sensor
#          could be derived.
# ***************************************************************************************
def MQResistanceCalculation(raw_adc):
    return (RL_VALUE * (1023 - raw_adc) / raw_adc)


# ***************************** MQCalibration ****************************************
# Input:   mq_pin - analog channel
# Output:  Ro of the sensor
# Remarks: This function assumes that the sensor is in clean air. It uses
#          MQResistanceCalculation to calculate the sensor resistance in clean air
#          and then divides it by RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about
#          10, which differs slightly between different sensors.
# ***************************************************************************************
def MQCalibration(mq_pin):
    val = 0

    for i in range(CALIBRATION_SAMPLE_TIMES):  # take multiple samples
        val += MQResistanceCalculation(analogRead(mq_pin))
        time.sleep(CALIBRATION_SAMPLE_INTERVAL / 1000.0)

    val = val / CALIBRATION_SAMPLE_TIMES  # calculate the average value

    val = val / RO_CLEAN_AIR_FACTOR  # divided by RO_CLEAN_AIR_FACTOR yields the Ro
    # according to the chart in the datasheet

    return val


# *****************************  MQRead *********************************************
# Input:   mq_pin - analog channel
# Output:  Rs of the sensor
# Remarks: This function uses MQResistanceCalculation to calculate the sensor resistance (Rs).
#          The Rs changes as the sensor is in the different concentration of the target
#          gas. The sample times and the time interval between samples could be configured
#          by changing the definition of the macros.
# ***************************************************************************************
def MQRead(mq_pin):
    rs = 0

    for i in range(READ_SAMPLE_TIMES):
        rs += MQResistanceCalculation(analogRead(mq_pin))
        time.sleep(READ_SAMPLE_INTERVAL / 1000.0)

    rs = rs / READ_SAMPLE_TIMES

    return rs


# *****************************  MQGetGasPercentage **********************************
# Input:   rs_ro_ratio - Rs divided by Ro
#          gas_id      - target gas type
# Output:  ppm of the target gas
# Remarks: This function passes different curves to the MQGetPercentage function which
#          calculates the ppm (parts per million) of the target gas.
# ***************************************************************************************
def MQGetGasPercentage(rs_ro_ratio, gas_id):
    if gas_id == GAS_LPG:
        return MQGetPercentage(rs_ro_ratio, LPGCurve)
    elif gas_id == GAS_CO:
        return MQGetPercentage(rs_ro_ratio, COCurve)
    elif gas_id == GAS_SMOKE:
        return MQGetPercentage(rs_ro_ratio, SmokeCurve)

    return 0


# *****************************  MQGetPercentage **********************************
# Input:   rs_ro_ratio - Rs divided by Ro
#          pcurve      - pointer to the curve of the target gas
# Output:  ppm of the target gas
# Remarks: By using the slope and a point of the line, the x(logarithmic value of ppm)
#          of the line could be derived if y(rs_ro_ratio) is provided. As it is a
#          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic
#          value.
# ***************************************************************************************
def MQGetPercentage(rs_ro_ratio, pcurve):
    return pow(10, ((math.log(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0])




# ++++++++++++++++++++++   MQ2 (MQ7)   ++++++++++++++++++++++

RL_VALUE = 5     # define the load resistance on the board, in kilo ohms
RO_CLEAN_AIR_FACTOR = 9.83  

# ***********************Software Related Macros************************************
CALIBRATION_SAMPLE_TIMES = 50        # define how many samples you are going to take in the calibration phase
CALIBRATION_SAMPLE_INTERVAL = 500   # define the time interval (in milliseconds) between each sample in the calibration phase
READ_SAMPLE_INTERVAL = 50            # define how many samples you are going to take in normal operation
READ_SAMPLE_TIMES = 5               # define the time interval (in milliseconds) between each sample 

# **********************Application Related Macros**********************************
GAS_LPG = 0
GAS_CO = 1
GAS_SMOKE = 2

# *****************************Globals***********************************************
LPGCurve = [2.3, 0.21, -0.47]            # two points are taken from the curve.
                                        # with these two points, a line is formed which is "approximately equivalent"
                                        # to the original curve.
                                        # data format: {x, y, slope}; point1: (lg200, 0.21), point2: (lg10000, -0.59) 

COCurve = [2.3, 0.72, -0.34]             # two points are taken from the curve with these two points,
                                        # a line is formed which is "approximately equivalent" to the original curve.

SmokeCurve = [2.3, 0.53, -0.44]           # two points are taken from the curve.
                                        # with these two points, a line is formed which is "approximately equivalent"
                                        # to the original curve.
                                        # data format: {x, y, slope}; point1: (lg200, 0.53), point2: (lg10000, -0.22)

Ro = 10







