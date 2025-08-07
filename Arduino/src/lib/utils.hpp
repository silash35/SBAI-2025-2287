#pragma once
#include <HardwareSerial.h>
#include <string.h>

// Parse comma-separated float values
void parseFloats(String input, int numValues, float values[], const float fallback[]) {
  int prevComma = -1;
  for (int i = 0; i < numValues; i++) {
    int nextComma = (i < numValues - 1) ? input.indexOf(',', prevComma + 1) : input.length();
    String valueStr = input.substring(prevComma + 1, nextComma);

    if (valueStr.length() > 0) {
      values[i] = valueStr.toFloat(); // Convert string to float
    } else {
      values[i] = fallback[i]; // Use the fallback value
    }

    prevComma = nextComma;
  }
}

// print float array
void printFloats(Stream *serial, const float array[], int size) {
  for (int i = 0; i < size; i++) {
    Serial.print(array[i]);
    if (i < size - 1) { // Evita a última vírgula
      Serial.print(",");
    }
  }
  Serial.println();
  Serial.flush();
}

// Copy values from one array to another
void copyArray(const float source[], float destination[], int size) {
  for (int i = 0; i < size; i++) {
    destination[i] = source[i];
  }
}
