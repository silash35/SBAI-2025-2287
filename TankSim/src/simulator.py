import casadi as ca

g = 980.665  # Gravity (cm/s²)


class Simulator:
    dt = 10

    def __init__(self, alfa_1=0.56, alfa_2=0.30, D=29.7, d=0.8):
        """
        Parameters:
        alfa_1 : Flow coefficient of the valve in the first tank.
        alfa_2 : Flow coefficient of the valve in the second tank.
        D: Internal diameter of the reservoir in centimeters.
        d : Internal diameter of the pipe in centimeters.
        """
        self.alfa_1 = alfa_1
        self.alfa_2 = alfa_2

        R = D / 2  # Internal radius of the reservoir (cm)
        s = ca.pi * (d / 2) ** 2  # Cross-sectional area of the pipe (cm²)
        self.s_1 = s
        self.s_2 = s
        self.R = R

    def update_alfas(self, alfa_1: float, alfa_2: float):
        self.alfa_1 = alfa_1
        self.alfa_2 = alfa_2

    def edo(self, t, Y, q):
        # Dependent variables
        h1, h2 = Y[0], Y[1]

        # Equations
        dh1dt = (q - self.alfa_1 * self.s_1 * (2 * g * h1) ** (0.5)) / (
            ca.pi * (2 * self.R * h1 - h1**2)
        )
        dh2dt = (
            self.alfa_1 * self.s_1 * (2 * g * h1) ** (0.5)
            - self.alfa_2 * self.s_2 * (2 * g * h2) ** (0.5)
        ) / (ca.pi * (2 * self.R * h2 - h2**2))

        return ca.vertcat(dh1dt, dh2dt)

    def get_next_point(self, q_current: float, h1_current: float, h2_current: float):
        h1 = ca.MX.sym("h1")
        h2 = ca.MX.sym("h2")
        h = ca.vertcat(h1, h2)

        # Define parameters
        q = ca.MX.sym("q_1")
        f = self.edo(0, h, q)

        ode = {"x": h, "p": q, "ode": f}

        integrator = ca.integrator("integrator", "rk", ode, 0, self.dt)
        h_current = [h1_current, h2_current]
        h_next = integrator(x0=h_current, p=q_current)["xf"].toarray().flatten()
        h_next = [float(h_next[0]), float(h_next[1])]

        return h_next


simulator = Simulator()
