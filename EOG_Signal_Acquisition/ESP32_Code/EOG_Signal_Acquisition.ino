const int H_EOG_PIN = 34;
const int V_EOG_PIN = 35;

const uint32_t SAMPLE_RATE = 256;
const uint32_t SAMPLE_INTERVAL_US = 1000000UL / SAMPLE_RATE;

uint32_t nextSampleTime;

void setup() {
  Serial.begin(115200);

  analogReadResolution(12);

  // ESP32 ADC attenuation
  analogSetPinAttenuation(H_EOG_PIN, ADC_11db);
  analogSetPinAttenuation(V_EOG_PIN, ADC_11db);

  nextSampleTime = micros();
}

void loop() {

  if ((int32_t)(micros() - nextSampleTime) >= 0) {

    nextSampleTime += SAMPLE_INTERVAL_US;

    int hEog = analogRead(H_EOG_PIN);
    int vEog = analogRead(V_EOG_PIN);

    Serial.print(hEog);
    Serial.print(",");
    Serial.println(vEog);
  }
}
