import matplotlib.pyplot as plt
import pandas as pd

from simulator import simulator

data_filename = "pirnn-pi.csv"
figure_filename= "../LaTeX/common/figures/hil-pirnn-pi.png"
data = pd.read_csv(data_filename)

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
    gridspec_kw={"height_ratios": [1.5, 1]},
    dpi=300,
)

ax[0].grid(True)

ax[0].plot(t, data["h1_serial"], label="$h_1$ (PIRNN)", color="tab:orange")
ax[0].scatter(t, data["h1_sensor"], label="$h_1$ (Planta)", color="tab:brown", s=1)

ax[0].plot(t, data["h2_serial"], label="$h_2$ (PIRNN)", color="tab:purple")
ax[0].scatter(t, data["h2_sensor"], label="$h_2$ (Planta)", color="tab:blue", s=1)

ax[0].plot(t, data["sp"], label="$h_2$ (SP)", linestyle="--", color="tab:red")

ax[0].axvline(x=sensor_off_time, linestyle="dashdot", color="black")
ax[0].annotate(
    "Interrupção das medições",
    xy=(sensor_off_time, 10),
    xytext=(sensor_off_time - 0.35, 13),
    arrowprops=dict(arrowstyle="->", color="black"),
)

ax[0].set_ylabel("Nível / cm")
ax[0].set_xlabel("Tempo / h")
ax[0].legend(loc="upper right")

ax[1].grid(True)
ax[1].plot(t, data["q"])
ax[1].set_ylabel("Vazão / (cm$^3\\cdot$s$^{-1}$)")
ax[1].set_xlabel("Tempo / h")

plt.savefig(figure_filename)
