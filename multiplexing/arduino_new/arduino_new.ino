// Include required libraries
#include <SoftwareSerial.h>
#include <MQ135.h>

// Define the analog pin connections

MQ135 MQ135_ = MQ135(A0);
#define MQ135_PIN  A0
#define MQ2_PIN  A2
#define MQ7_PIN  A1



// ++++++++++++++++++++++   MQ2 (MQ7)   ++++++++++++++++++++++

#define  RL_VALUE 5     //define the load resistance on the board, in kilo ohms
#define  RO_CLEAN_AIR_FACTOR  9.83  

/***********************Software Related Macros************************************/
#define  CALIBARAION_SAMPLE_TIMES 50        //define how many samples you are going to take in the calibration phase
#define  CALIBRATION_SAMPLE_INTERVAL  500   //define the time interal(in milisecond) between each samples in the cablibration phase
#define  READ_SAMPLE_INTERVAL 50            //define how many samples you are going to take in normal operation
#define  READ_SAMPLE_TIMES  5               //define the time interal(in milisecond) between each samples in 
 
/**********************Application Related Macros**********************************/
#define  GAS_LPG 0
#define  GAS_CO 1
#define  GAS_SMOKE 2

/*****************************Globals***********************************************/
float  LPGCurve[3]  =  {2.3,0.21,-0.47};            //two points are taken from the curve. 
                                                    //with these two points, a line is formed which is "approximately equivalent"
                                                    //to the original curve. 
                                                    //data format:{ x, y, slope}; point1: (lg200, 0.21), point2: (lg10000, -0.59) 

float  COCurve[3]  =  {2.3,0.72,-0.34};             //two points are taken from the curve with these two points, 
                                                    //a line is formed which is "approximately equivalent" to the original curve.

float  SmokeCurve[3] = {2.3,0.53,-0.44};              //two points are taken from the curve. 
                                                    //with these two points, a line is formed which is "approximately equivalent" 
                                                    //to the original curve.
                                                    //data format:{ x, y, slope}; point1: (lg200, 0.53), point2: (lg10000,  -0.22)
float Ro = 10;                 //Ro is initialized to 10 kilo ohms

// ++++++++++++++++++++++++++++++++++++++++++++


// +++++++++++++++++++++++++++++++ MQ 7 ++++++++++++++++++++++++

float RS_gas = 0;
float ratio = 0;
float sensorValue_MQ135 = 0;
float sensorValue_MQ2 = 0;
float sensorValue_MQ7 = 0;
float sensor_volt = 0;
float R1 = 7200.0;





// Create a SoftwareSerial object to communicate with NodeMCU
SoftwareSerial node_esp8266(0, 1); // RX, TX



void setup() {
  // Start the serial communication with NodeMCU
  node_esp8266.begin(9600);
  Serial.begin(9600);

  // Serial.print("\n");
  // Initialize analog pins
  pinMode(MQ135_PIN, INPUT);
  pinMode(MQ2_PIN, INPUT);
  pinMode(MQ7_PIN, INPUT);



  // ##### MQ2 ################
  // Serial.print("Calibrating...\n");                
  Ro = MQCalibration(MQ2_PIN);                  //Calibrating the sensor. Please make sure the sensor is in clean air when you perform the calibration                    
  // Serial.print("Calibration is done...\n"); 
  // Serial.print("Ro=");
  // Serial.print(Ro);
  // Serial.print("kohm");

  delay(10000);
}

void loop() {
  String output = "";
  String analog_output = "";
  // Read analog values from sensors

  sensorValue_MQ135 = analogRead(MQ135_PIN);
  // Serial.println(val);

  float mq135_ppm = MQ135_.getPPM();
  // int mq135_ppm = map(sensorValue_MQ135, 0, 1023, 10, 10000);
  // Serial.print("\nMQ135: ");
  // Serial.println(mq135_ppm);
  // int mq135Value = analogRead(MQ135_PIN);
  // int mq2Value = analogRead(MQ2_PIN);
  // int mq7Value = analogRead(MQ7_PIN);

  // Serial.println("MQ135 : ");
  // Serial.println(mq135Value);
  // Serial.print('\n');
  // Serial.println("MQ2 : ");
  // Serial.println(mq2Value);
  // Serial.print('\n');
  // Serial.println("MQ7 : ");
  // Serial.println(mq7Value);
  // Serial.print('\n');

  // ++++++++++++++++ MQ 7 +++++++++++++++++++
  sensorValue_MQ7 = analogRead(MQ7_PIN);
  sensor_volt = sensorValue_MQ7/1024*5.0;
  RS_gas = (5.0-sensor_volt)/sensor_volt;
  ratio = RS_gas/R1; //Replace R0 with the value found using the sketch above
  float x = 1538.46 * ratio;
  float mq7Value = pow(x,-1.709);
  // Serial.print("\nMQ7_PPM: ");
  // Serial.println(mq7_ppm);

  // float mq7Value = MQGetGasPercentage(MQRead(MQ7_PIN)/Ro,GAS_CO);
  // ++++++++++++++++++++++++++++++++++++++++++




  // ++++++++++++++++ MQ2 +++++++++++++++++++++++++
  
  sensorValue_MQ2 = analogRead(MQ2_PIN);
  float mq2Value = MQGetGasPercentage(MQRead(MQ2_PIN)/Ro,GAS_SMOKE);
  // Serial.print("\nMQ2_CO:"); 
  // Serial.print(mq2Value);

  // ++++++++++++++++++++++++++++++++++++++++++++++
  

  output = "MQ135:" + String(mq135_ppm) + " " + "MQ2:" + String(mq2Value) + " " + "MQ7:" + String(mq7Value);
  analog_output = "Analog-MQ135:" + String(sensorValue_MQ135) + " " + "MQ2:" + String(sensorValue_MQ2) + " " + "MQ7:" + String(sensorValue_MQ7);
  Serial.println(output);
  Serial.println(analog_output);


  // // Send data to NodeMCU
  // node_esp8266.print(mq135Value);
  // node_esp8266.print(",");
  // node_esp8266.print(mq2Value);
  // node_esp8266.print(",");
  // node_esp8266.println(mq7Value);
  node_esp8266.println(output);
  

  delay(1000); // Adjust delay as needed
}







 
/****************** MQResistanceCalculation ****************************************
Input:   raw_adc - raw value read from adc, which represents the voltage
Output:  the calculated sensor resistance
Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
         across the load resistor and its resistance, the resistance of the sensor
         could be derived.
************************************************************************************/ 
float MQResistanceCalculation(int raw_adc)
{
  return ( ((float)RL_VALUE*(1023-raw_adc)/raw_adc));
}
 
/***************************** MQCalibration ****************************************
Input:   mq_pin - analog channel
Output:  Ro of the sensor
Remarks: This function assumes that the sensor is in clean air. It use  
         MQResistanceCalculation to calculates the sensor resistance in clean air 
         and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
         10, which differs slightly between different sensors.
************************************************************************************/ 
float MQCalibration(int mq_pin)
{
  int i;
  float val=0;
 
  for (i=0;i<CALIBARAION_SAMPLE_TIMES;i++) {            //take multiple samples
    val += MQResistanceCalculation(analogRead(mq_pin));
    delay(CALIBRATION_SAMPLE_INTERVAL);
  }
  val = val/CALIBARAION_SAMPLE_TIMES;                   //calculate the average value
 
  val = val/RO_CLEAN_AIR_FACTOR;                        //divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                        //according to the chart in the datasheet 
 
  return val; 
}
/*****************************  MQRead *********************************************
Input:   mq_pin - analog channel
Output:  Rs of the sensor
Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
         The Rs changes as the sensor is in the different consentration of the target
         gas. The sample times and the time interval between samples could be configured
         by changing the definition of the macros.
************************************************************************************/ 
float MQRead(int mq_pin)
{
  int i;
  float rs=0;
 
  for (i=0;i<READ_SAMPLE_TIMES;i++) {
    rs += MQResistanceCalculation(analogRead(mq_pin));
    delay(READ_SAMPLE_INTERVAL);
  }
 
  rs = rs/READ_SAMPLE_TIMES;
 
  return rs;  
}
 
/*****************************  MQGetGasPercentage **********************************
Input:   rs_ro_ratio - Rs divided by Ro
         gas_id      - target gas type
Output:  ppm of the target gas
Remarks: This function passes different curves to the MQGetPercentage function which 
         calculates the ppm (parts per million) of the target gas.
************************************************************************************/ 
float MQGetGasPercentage(float rs_ro_ratio, int gas_id)
{
  if (gas_id == GAS_LPG ) {
     return MQGetPercentage(rs_ro_ratio,LPGCurve);
  } else if ( gas_id == GAS_CO ) {
     return MQGetPercentage(rs_ro_ratio, COCurve);
  } else if ( gas_id == GAS_SMOKE ) {
     return MQGetPercentage(rs_ro_ratio,SmokeCurve);
  }    
 
  return 0;
}
 
/*****************************  MQGetPercentage **********************************
Input:   rs_ro_ratio - Rs divided by Ro
         pcurve      - pointer to the curve of the target gas
Output:  ppm of the target gas
Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
         of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
         logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
         value.
************************************************************************************/ 
float  MQGetPercentage(float rs_ro_ratio, float *pcurve)
{
  return (pow(10,( ((log(rs_ro_ratio)-pcurve[1])/pcurve[2]) + pcurve[0])));
}
