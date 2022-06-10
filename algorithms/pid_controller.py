import time
 
 
class PIDController:
 
    def __init__(self, p_value: float = .0, i_value: float = .0, d_value: float = .0, /,
                 sample_period: float = .0, expected_value: float = .0):
        self._p_value = p_value
        self._i_value = i_value
        self._d_value = d_value
        self._sample_period = sample_period
        self._cur_time = time.time()
        self._last_time = self._cur_time
        self._expected_value = expected_value
        self._value = .0
        self._last_error = .0
        self._d_term = .0
        self._i_term = .0
        self._p_term = .0
 
    def reset(self):
        self._p_term = .0
        self._i_term = .0
        self._d_term = .0
        self._last_error = .0
        self._value = .0
 
    def update(self, feedback_val: float):
        # calculate error
        error = self.expected_value - feedback_val
 
        # time elapses
        self._cur_time = time.time()
        delta_time = self._cur_time - self._last_time
 
        # error difference, delta e
        delta_error = error - self._last_error
 
        # if sample period not reached, pass
        if delta_time < self._sample_period:
            return self._value
 
        self._p_term = self._p_value * error  # proportional term
        self._i_term += error * delta_time  # integration term
 
        self._d_term = .0
        if delta_time > 0:
            self._d_term = delta_error / delta_time  # differential term
 
        self._last_time = self._cur_time
        self._last_error = error
        self._value = self._p_term + (self._i_value * self._i_term) + (self._d_value * self._d_term)
        return self._value
 
    @property
    def value(self):
        return self._value
 
    @property
    def expected_value(self):
        return self._expected_value
 
    @expected_value.setter
    def expected_value(self, val: float):
        self._verify_input(val)
        self._expected_value = val
 
    @property
    def sample_period(self):
        return self._sample_period
 
    @sample_period.setter
    def sample_period(self, val: float):
        self._verify_input(val)
        self._sample_period = val
 
    @property
    def p_value(self):
        return self._p_value
 
    @p_value.setter
    def p_value(self, val: float):
        self._verify_input(val)
        self._p_value = val
 
    @property
    def i_value(self):
        return self._i_value
 
    @i_value.setter
    def i_value(self, val: float):
        self._verify_input(val)
        self._i_value = val
 
    @property
    def d_value(self):
        return self._d_value
 
    @d_value.setter
    def d_value(self, val: float):
        self._verify_input(val)
        self._d_value = val
 
    @staticmethod
    def _verify_input(val):
        if not isinstance(val, (float, int)) or val < 0:
            raise ValueError("input is expected to be a positive float/integer")
 
 
if __name__ == "__main__":
 
    EXPECT_VALUE = 1.1
    pid_controller = PIDController(1.2, 1, .001, sample_period=.01, expected_value=EXPECT_VALUE)
    sample_num = 20
 
    feed_back = 10
    feed_back_list = []
    time_list = []
    expected_value_list = []
 
    for i in range(sample_num):
        feed_back += pid_controller.update(feed_back)
        time.sleep(.1)
        feed_back_list.append(feed_back)
        expected_value_list.append(EXPECT_VALUE)
        time_list.append(i)

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.interpolate import make_interp_spline
 
    x_points = np.linspace(min(time_list), max(time_list), 300)
    y_points = make_interp_spline(time_list, feed_back_list)(x_points)
 
    plt.figure(0)
    plt.ion()
    plt.grid(True)
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('PythonTEST PID', fontsize=15)
    plt.xlim((0, sample_num))
    plt.ylim((min(feed_back_list) - .5, max(feed_back_list) + .5))
    plt.plot(time_list, expected_value_list, "r")
    for i in range(len(x_points)):
        plt.scatter(x_points[i], y_points[i], marker=".", c="b")
        plt.pause(.005)
 
    plt.ioff()
    plt.show()
 