#pragma once

const float max_integral = q_max / ki;
const float min_integral = q_min / ki;

class PID {
public:
  float integral = 0;
  float last_error = 0;

  float kp;
  float ki;
  float kd;

  PID(float kp, float ki, float kd) : kp(kp), ki(ki), kd(kd) {}

  float calculate(float error) {
    // Calculate the proportional, integral, and derivative terms
    float p = kp * error;

    integral += (last_error + error) * dt / 2;
    if (integral > max_integral) {
      integral = max_integral;
    } else if (integral < min_integral) {
      integral = min_integral;
    }
    float i = ki * integral;

    float d = kd * ((error - last_error) / dt);

    // Calculate the output
    float output = p + i + d;
    if (output > q_max) {
      output = q_max;
    } else if (output < q_min) {
      output = q_min;
    }

    // Update the last error
    last_error = error;

    return output;
  }
};
