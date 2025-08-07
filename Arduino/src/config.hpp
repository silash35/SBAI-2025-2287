#pragma once

// Serial config
const int SERIAL_SPEED = 19200;

// Simulation parameters
const float dt = 10; // [s]

// Controller parameters
const float kp = 1.5;
const float ki = 0.0015;
const float kd = 0;

// starting steady state
const float h1_0 = 2.9745;
const float h2_0 = 10.3644;
const float sp_0 = 10.3644;
const float q_0 = 21.5;

// Safety limits
const float q_min = 21.5;
const float q_max = 34.0;