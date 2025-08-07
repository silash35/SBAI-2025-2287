import matplotlib.pyplot as plt
import pandas as pd

from simulator import simulator

data_filename = "pirnn"
data = pd.read_csv(data_filename + ".csv")

sensor_off_time = 0
for index, value in data["h2_switch"].astype(bool).items():
    if not value:
        sensor_off_time = (index * simulator.dt) / (60 * 60)
        break
t = (data.index * simulator.dt) / (60 * 60)

# Plot two subplots: one for flow rate and another for levels
fig, ax = plt.subplots(
    2,
    figsize=(10, 4.5),
    layout="constrained",
    gridspec_kw={"height_ratios": [1, 1.5]},
    dpi=300,
)

ax[0].grid(True)
ax[0].plot(t, data["q"])
ax[0].set_ylabel("Vazão/(cm$^3\\cdot$s$^{-1}$)")
ax[0].set_xlabel("Tempo/h")

# fmt: off
ax[1].grid(True)

ax[1].plot(t, data["h1_serial"], label="$h_1$ (Arduino)", color="tab:orange")
ax[1].scatter(t, data["h1_sensor"], label="$h_1$ (Sensor)", color="tab:brown", s=1)

ax[1].plot(t, data["h2_serial"], label="$h_2$ (Arduino)", color="tab:purple")
ax[1].scatter(t, data["h2_sensor"], label="$h_2$ (Sensor)",  color="tab:blue", s=1)

ax[1].axvline(x=sensor_off_time, label="Interrupção dos sensores", linestyle="--", color="tab:red")

ax[1].set_ylabel("Nível/$cm$")
ax[1].set_xlabel("Tempo/h")
# fmt: on

plt.legend(loc="upper right")
plt.savefig("../LaTeX/common/figures/sil-" + data_filename + ".png")
