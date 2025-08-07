#include "config.hpp"
#include "lib/PID.hpp"
#include "lib/utils.hpp"
#include "model.hpp"
#include <Arduino.h>

// h1(t-1), h2(t-1), sp(t-1)
float serial_input[3] = {h1_0, h2_0, sp_0};
float serial_fallback[3] = {h1_0, h2_0, sp_0};

// h1(t), h2(t), q(t)
float serial_output[3] = {h1_0, h2_0, q_0};

// h1(t-2), h2(t-2), q(t-2), h1(t-1), h2(t-1), q(t-1)
float nn_input[INPUT_SIZE * STEPS] = {h1_0, h2_0, q_0, h1_0, h2_0, q_0};

// h1(t), h2(t)
float nn_output[OUTPUT_SIZE] = {h1_0, h2_0};

PID pid(kp, ki, kd);

void setup() {
  Serial.begin(SERIAL_SPEED);
  // Ensure the PID controller starts with the correct q value.
  pid.integral = sp_0 / ki;
}

void loop() {
  String input = Serial.readStringUntil('\n');
  if (input.length() < 1) {
    return;
  }

  parseFloats(input, 3, serial_input, serial_fallback);

  // Move previous values to t-2
  for (int i = 0; i < INPUT_SIZE; i++) {
    nn_input[i] = nn_input[INPUT_SIZE + i];
  }

  // Place new t-1 values into nn_input
  float q = pid.calculate(serial_fallback[2] - serial_fallback[1]);
  nn_input[INPUT_SIZE + 0] = serial_input[0];
  nn_input[INPUT_SIZE + 1] = serial_input[1];
  nn_input[INPUT_SIZE + 2] = q;

  neural_network(nn_input, nn_output);

  // If the next input has null values, these fallback values will be used instead.
  serial_fallback[0] = nn_output[0];
  serial_fallback[1] = nn_output[1];
  serial_fallback[2] = serial_input[2];

  // Print the output
  serial_output[0] = nn_output[0];
  serial_output[1] = nn_output[1];
  serial_output[2] = q;

  printFloats(&Serial, serial_output, 3);
}
