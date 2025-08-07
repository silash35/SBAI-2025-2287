import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import colors as mcolors

import config as cf

colors = list(mcolors.TABLEAU_COLORS.keys())


def _save_or_show(filename: str | None = None):
    if filename is not None:
        plt.savefig(cf.figures_folder + filename + cf.image_format, dpi=cf.image_dpi)
        plt.close()
    else:
        plt.show()


def plot_loss(history, label=None, filename: str | None = None):
    fig = go.Figure()

    if isinstance(history[0], list):
        for i in range(len(history[0])):
            lbl = label[i] if label is not None else None
            values = [hist[i] for hist in history]
            fig.add_trace(go.Scatter(y=values, mode="lines", name=lbl))
    else:
        fig.add_trace(go.Scatter(y=history, mode="lines", name=label))

    fig.update_layout(
        # title="Erro do modelo a cada época",
        xaxis_title="Epochs",
        yaxis_title="Loss",
        width=1920,
        height=720,
        yaxis_range=[0, 10],
        margin=dict(l=20, r=20, t=20, b=20),
        font={"size": 36},
    )

    if filename is not None:
        fig.write_image(cf.figures_folder + filename + cf.image_format)

    fig.show()


def plot_tanks(
    t,
    tanks,
    labels=None,
    dashed_first=0,
    filename=None,
    legend_loc=None,
    figsize=(10, 4),
):
    plt.figure(figsize=figsize, layout="constrained")
    # plt.title("Níveis dos tanques pelo tempo")

    for i, tank in enumerate(tanks):
        label = labels[i] if (type(labels) is list) else labels
        plt.plot(
            t / (60 * 60),
            tank,
            label=label,
            linestyle="dotted" if i < dashed_first else "solid",
            linewidth=5 if i < dashed_first else None,
        )
    plt.xlabel("Tempo / h")
    plt.ylabel("Nível / cm")
    plt.legend(loc=legend_loc)
    plt.grid()

    _save_or_show(filename)


def plot_flow_and_level(t, flow, levels, levels_label=None, filename=None):
    _, axs = plt.subplots(2, figsize=(12, 5), layout="constrained")
    # axs[0].set_title("Vazão de entrada pelo tempo")
    axs[0].plot(t / (60 * 60), flow)
    axs[0].set_ylabel("Vazão / (cm$^3\\cdot$s$^{-1}$)")
    axs[0].set_xlabel("Tempo / h")
    axs[0].grid()

    # axs[1].set_title("Nível dos tanques pelo tempo")
    for i, level in enumerate(levels):
        label = levels_label[i] if (type(levels_label) is list) else levels_label
        axs[1].plot(t / (60 * 60), level, label=label)
    axs[1].set_ylabel("Nível / cm")
    axs[1].set_xlabel("Tempo / h")
    axs[1].legend()
    axs[1].grid()

    _save_or_show(filename)


def plot_density(values, labels, filename: str | None = None, width=20, extra=None):
    plt.rcParams.update({"font.size": 15})
    fig, axs = plt.subplots(3, figsize=(width, 8), layout="constrained")
    t_max = max([max(v) for v in values])
    for i in range(len(values)):
        mean_value = np.mean(values[i])
        ax = i // 3
        sns.histplot(
            values[i],
            kde=True,
            stat="density",
            bins=15,
            color=colors[i],
            ax=axs[ax],
        )
        axs[ax].axvline(
            mean_value,
            linestyle="--",
            linewidth=1.5,
            color=colors[i],
            label=f"{labels[i]}: {mean_value:.3f}s",
        )
        axs[ax].legend()
        axs[ax].set_ylabel(None)
        axs[ax].set_xlim(0, t_max)
        if ax != 2:
            axs[ax].set_xticklabels([])
        axs[ax].grid(True)
    if extra is not None:
        extra(plt)

    fig.supxlabel("Tempo / s")
    fig.supylabel("Densidade de Probabilidade")

    _save_or_show(filename)

    plt.rcParams.update({"font.size": 12})


def plot_boxplot(data, filename: str | None = None):
    plt.rcParams.update({"font.size": 28})
    plt.figure(figsize=(16, 9), layout="constrained")

    sns.boxplot(
        x="Tempos", y="Métodos", hue="Métodos", legend=False, palette="tab10", data=data
    )

    plt.xlabel("Tempo / s")
    plt.ylabel("")
    plt.grid()

    _save_or_show(filename)

    plt.rcParams.update({"font.size": 12})
