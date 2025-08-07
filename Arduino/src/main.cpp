#include "model.hpp"
#include <Arduino.h>

// h1 (t-1), h2 (t-1), q (t-1), h1 (t), h2 (t), q (t)
float nn_input[INPUT_SIZE * STEPS] = {2.9745, 10.3644, 21.5, 2.9745, 10.3644, 21.5};

// h1 (t+1), h2 (t+1)
float nn_output[OUTPUT_SIZE] = {2.9745, 10.3644};

void setup() { Serial.begin(19200); }

void loop() {
  if (Serial.available() > 0) {
    // Reads a string in the format h1,h2,q
    String input = Serial.readStringUntil('\n');
    if (input.length() < 1) {
      return;
    }

    int firstComma = input.indexOf(',');
    int secondComma = input.indexOf(',', firstComma + 1);

    // Extracts h1, h2, and q
    if (firstComma != -1) {
      String h1Str = input.substring(0, firstComma);
      if (h1Str.length() > 0) {
        nn_input[INPUT_SIZE + 0] = h1Str.toFloat();
      }
    }

    if (secondComma != -1) {
      String h2Str = input.substring(firstComma + 1, secondComma);
      if (h2Str.length() > 0) {
        nn_input[INPUT_SIZE + 1] = h2Str.toFloat();
      }

      String qStr = input.substring(secondComma + 1);
      if (qStr.length() > 0) {
        nn_input[INPUT_SIZE + 2] = qStr.toFloat();
      }
    }

    neural_network(nn_input, nn_output);
    // Shifts current step to previous step
    for (int i = 0; i < INPUT_SIZE; i++) {
      nn_input[i] = nn_input[INPUT_SIZE + i];
    }
    nn_input[INPUT_SIZE + 0] = nn_output[0];
    nn_input[INPUT_SIZE + 1] = nn_output[1];

    // Prints result
    Serial.print(nn_output[0]);
    Serial.print(",");
    Serial.print(nn_output[1]);
    Serial.print(",");
    Serial.println(nn_input[INPUT_SIZE + 2]);
    Serial.flush();
  }
}
