from typing import Any, Callable

import casadi as ca
import numpy as np
import torch
from scipy.integrate import solve_ivp

g = 980.665  # gravidade (cm/s^2)


class Base_tanks:
    h_min = 0.0
    h_max = np.inf

    def __init__(self):
        pass

    def _edo(self, t, Y, q, pi):
        return [0.0, 0.0]

    def set_simulation_parameters(
        self, q: Callable[[Any, Any], Any], t_span, n_points, y0
    ):
        self.t_numpy = np.linspace(t_span[0], t_span[1], n_points)
        self.t_torch = torch.tensor(self.t_numpy, dtype=torch.float32)
        self.dt = self.t_numpy[1] - self.t_numpy[0]

        self.q = q
        self.q_torch = q(self.t_torch, torch)
        self.q_numpy = q(self.t_numpy, np)

        if y0 is not None:
            self.y0 = y0
        else:
            self.y0 = np.ones(2) * self.h_min

    def edo_numpy(self, t, Y, q):
        Y = np.clip(Y, self.h_min, self.h_max)

        return self._edo(t, Y, q, np.pi)

    def edo_torch(self, t, Y, q: Any = None):
        Y = torch.clip(Y, self.h_min, self.h_max)

        if q is not None:
            return self._edo(t, Y, q, torch.pi)
        return self._edo(t, Y, self.q(t, torch), torch.pi)

    def edo_casadi(self, t, Y, q):
        dh1dt, dh2dt = self._edo(t, Y, q, ca.pi)
        return ca.vertcat(dh1dt, dh2dt)

    def simulate_scipy(self, method: str):
        h1_values = np.zeros_like(self.t_numpy)
        h2_values = np.zeros_like(self.t_numpy)

        h_current = np.array(self.y0, dtype=np.float32)

        h1_values[0] = h_current[0]
        h2_values[0] = h_current[1]

        for i in range(len(self.t_numpy) - 1):
            sol = solve_ivp(
                self.edo_numpy,
                [0, self.dt],
                h_current,
                method=method,
                args=(self.q_numpy[i],),
            )

            h1_values[i + 1] = sol.y[0, -1]
            h2_values[i + 1] = sol.y[1, -1]
            h_current[0] = sol.y[0, -1]
            h_current[1] = sol.y[1, -1]

        return np.array([h1_values, h2_values])

    def simulate_casadi(self, method: str):
        # Definir as variáveis
        h1 = ca.MX.sym("h1")  # type: ignore
        h2 = ca.MX.sym("h2")  # type: ignore
        h = ca.vertcat(h1, h2)

        # Definir parâmetros
        q = ca.MX.sym("q_1")  # type: ignore

        f = self.edo_casadi(self.t_torch, h, q)

        ode = {"x": h, "p": q, "ode": f}

        # Resolver o sistema
        h1_values = np.zeros_like(self.t_numpy)
        h2_values = np.zeros_like(self.t_numpy)

        h_current = np.array(self.y0, dtype=np.float32)

        integrator = ca.integrator("integrator", method, ode, self.t_numpy[0], self.dt)
        for i in range(len(self.t_numpy)):
            h1_values[i] = h_current[0]
            h2_values[i] = h_current[1]

            if h1_values[i] > self.h_max:
                raise Exception("Tanque 1 cheio")
            elif h1_values[i] < self.h_min:
                raise Exception("Tanque 1 vazio")

            if h2_values[i] > self.h_max:
                raise Exception("Tanque 2 cheio")
            elif h2_values[i] < self.h_min:
                raise Exception("Tanque 2 vazio")

            h_current = integrator(x0=h_current, p=self.q(self.t_numpy[i], np))["xf"]

        return np.array([h1_values, h2_values])


class Spherical_tanks(Base_tanks):
    def __init__(self, alfa_1=0.56, alfa_2=0.30, D=29.7, d=0.8):
        """
        Parâmetros:
        alfa_1 : Coeficiente de vazão da válvula do primeiro tanque.
        alfa_2 : Coeficiente de vazão da válvula do segundo tanque.
        D: Diâmetro interno do reservatório em centímetros.
        d : Diâmetro interno do tubo em centímetros.
        """
        self.alfa_1 = alfa_1
        self.alfa_2 = alfa_2

        R = D / 2  # Raio interno do reservatório (cm)
        s = torch.pi * (d / 2) ** 2  # Área da seção interna da tubulação (cm²)
        self.s_1 = s
        self.s_2 = s
        self.R = R

        self.h_max = ((self.R * 2) / 10) * 9
        self.h_min = ((self.R * 2) / 10) * 1

    def _edo(self, t, Y, q, pi):
        # Dependent variables
        h1, h2 = Y[0], Y[1]

        # Equations
        dh1dt = (q - self.alfa_1 * self.s_1 * (2 * g * h1) ** (0.5)) / (
            pi * (2 * self.R * h1 - h1**2)
        )
        dh2dt = (
            self.alfa_1 * self.s_1 * (2 * g * h1) ** (0.5)
            - self.alfa_2 * self.s_2 * (2 * g * h2) ** (0.5)
        ) / (pi * (2 * self.R * h2 - h2**2))

        return [dh1dt, dh2dt]
