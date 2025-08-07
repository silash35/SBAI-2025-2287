#pragma once
#include "utils.hpp"
#include <avr/pgmspace.h>
#include <math.h>

float read_pgm(const float *ptr, int index) { return pgm_read_float_near(ptr + index); }

namespace NN {
// out = in*weights + bias
void Linear(const float in[], float out[], const float weights[], const float bias[],
  const int in_features, const int out_features) {
  for (int i = 0; i < out_features; i++) {
    out[i] = read_pgm(bias, i);
    for (int j = 0; j < in_features; j++) {
      out[i] += read_pgm(weights, i * in_features + j) * in[j];
    }
  }
}

// in = tanh(in)
void Tanh(float in[], int size) {
  for (int i = 0; i < size; i++) {
    in[i] = tanh(in[i]);
  }
}

// out = in*weights_ih + bias_ih ​+ h_prev*weights_hh ​+ bias_hh
void RNN(                   //
  const float in[],         // input
  float out[],              // output
  const float h_prev[],     // previous hidden state
  const float weights_ih[], // input to the hidden state weights
  const float weights_hh[], // hidden state to hidden state weights
  const float bias_ih[],    // input to the hidden state bias
  const float bias_hh[],    // hidden state to hidden state bias
  const int in_features,    // input size
  const int out_features    // output size
) {
  for (int i = 0; i < out_features; i++) {
    out[i] = read_pgm(bias_ih, i) + read_pgm(bias_hh, i);

    for (int j = 0; j < in_features; j++) {
      out[i] += read_pgm(weights_ih, i * in_features + j) * in[j];
    }

    for (int j = 0; j < out_features; j++) {
      out[i] += read_pgm(weights_hh, i * out_features + j) * h_prev[j];
    }
  }
}

// in = ((in - in_min) / (in_max - in_min)) * 2 - 1
void Normalize(float in[], const int size, const float in_min[], const float in_max[]) {
  for (int i = 0; i < size; i++) {
    in[i] = ((in[i] - in_min[i]) / (in_max[i] - in_min[i])) * 2 - 1;
  }
}

// in = ((in + 1) / 2) * (out_max - out_min) + out_min
void Denormalize(float in[], const int size, const float out_min[], const float out_max[]) {
  for (int i = 0; i < size; i++) {
    in[i] = ((in[i] + 1) / 2) * (out_max[i] - out_min[i]) + out_min[i];
  }
}

} // namespace NN
