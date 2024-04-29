import matplotlib.pyplot as plt
import numpy as np

class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, setpoint, process_variable):
        error = setpoint - process_variable
        self.integral += error
        derivative = error - self.prev_error

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error

        return output

# Simple simulated system
def simulate_system(pid, setpoint, initial_value, time_steps):
    process_variable = initial_value
    output_values = []

    for _ in range(time_steps):
        control_signal = pid.compute(setpoint, process_variable)
        process_variable += 0.1 * control_signal  # Simulated system dynamics
        output_values.append(process_variable)

    return output_values

# PID controller parameters
Kp = 3
Ki = 0.1
Kd = 0.1

# Setpoint and initial value
setpoint = 10
initial_value = 0

# Create PID controller
pid = PIDController(Kp, Ki, Kd)

# Simulate the system
time_steps = 200
output_values = simulate_system(pid, setpoint, initial_value, time_steps)

# Plot results
time = np.arange(0, time_steps * 0.1, 0.1)
plt.plot(time, output_values, label='Process Variable')
plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
plt.xlabel('Time')
plt.ylabel('Process Variable')
plt.title('PID Controller Simulation')
plt.legend()
plt.show()
