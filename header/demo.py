import math

# Parameters for calculating ppm of CO2 from sensor resistance
PARA = 116.6020682
PARB = 2.769034857

# Parameters to model temperature and humidity dependence
CORA = 0.00035
CORB = 0.02718
CORC = 1.39538
CORD = 0.0018
CORE = -0.003333333
CORF = -0.001923077
CORG = 1.130128205

# Atmospheric CO2 level for calibration purposes,
# from "Globally averaged marine surface monthly mean data"
# available at https://gml.noaa.gov/ccgg/trends/gl_data.html
ATMOCO2 = 415.58  # Global CO2 Aug 2022

class MQ135:
    def __init__(self, pin, rzero=76.63, rload=10.0):
        self._pin = pin
        self._rzero = rzero
        self._rload = rload

    def getCorrectionFactor(self, t, h):
        # Linearization of the temperature dependency curve under and above 20 degrees C
        # below 20degC: fact = a * t * t - b * t - (h - 33) * d
        # above 20degC: fact = a * t + b * h + c
        # this assumes a linear dependency on humidity
        if t < 20:
            return CORA * t * t - CORB * t + CORC - (h - 33.) * CORD
        else:
            return CORE * t + CORF * h + CORG

    def getResistance(self, analog_read_value):
        return ((1023. / float(analog_read_value)) - 1.) * self._rload

    def getCorrectedResistance(self, t, h, analog_read_value):
        return self.getResistance(analog_read_value) / self.getCorrectionFactor(t, h)

    def getPPM(self, analog_read_value):
        return PARA * pow((self.getResistance(analog_read_value) / self._rzero), -PARB)

    def getCorrectedPPM(self, t, h, analog_read_value):
        return PARA * pow((self.getCorrectedResistance(t, h, analog_read_value) / self._rzero), -PARB)

    def getRZero(self, analog_read_value):
        return self.getResistance(analog_read_value) * pow((ATMOCO2 / PARA), (1. / PARB))

    def getCorrectedRZero(self, t, h, analog_read_value):
        return self.getCorrectedResistance(t, h, analog_read_value) * pow((ATMOCO2 / PARA), (1. / PARB))

class RandomMQ135:
    def __init__(self):
        self.mq135 = MQ135(pin=0)  # Assuming pin 0

    def calculate_ppm_values(self, analog_read_values):
        ppm_values = []

        for analog_read_value in analog_read_values:
            ppm = self.mq135.getPPM(analog_read_value)
            ppm_values.append(ppm)

        return ppm_values


# Example usage:
random_mq135 = RandomMQ135()
analog_values = [684.0, 682.0, 688.0, 693.0, 683.0, 699.0, 693.0, 699.0, 712.0, 698.0, 695.0, 706.0, 715.0, 701.0, 705.0, 708.0, 706.0, 700.0, 707.0, 662.0 ]  # Replace with your actual analogRead values

ppm_results = random_mq135.calculate_ppm_values(analog_values)

# for i, ppm in enumerate(ppm_results):
#     print(f"Analog Read Value {i+1}: PPM: {ppm}")
# Convert the PPM values to integers
ppm_results = list(map(int, ppm_results))

ppm_final = []
for i in ppm_results:
    ppm_final.append(round((i/1000000)*100, 2))

print(ppm_final)


