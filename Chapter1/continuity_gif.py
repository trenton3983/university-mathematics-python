import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path


def f(x):
    return 2 / x


def finverse(x):
    return 2 / x


x = np.linspace(0.5, 2)
x0 = 1
y = f(x)
y0 = f(x0)


def make_gif(
    gif_path="continuity.gif",
    eps_values=None,
    fps=12,
    dpi=150,
):
    gif_path = Path(gif_path)

    if eps_values is None:
        eps_values = np.round(np.arange(0.01, 0.401, 0.01), 2)

    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=dpi)

    (curve,) = ax.plot(x, y, "r")

    hlines = [
        ax.axhline(y=y0, color="k", linestyle=":"),
        ax.axhline(y=y0, color="k", linestyle=":"),
        ax.axhline(y=y0, color="k", linestyle=":"),
    ]
    vlines = [
        ax.axvline(x=x0, color="c", linestyle=":"),
        ax.axvline(x=x0, color="c", linestyle=":"),
        ax.axvline(x=x0, color="c", linestyle=":"),
    ]

    ax.set_xlim(float(np.min(x)), float(np.max(x)))
    ymin = float(np.min(y))
    ymax = float(np.max(y))
    pad = 0.05 * (ymax - ymin)
    ax.set_ylim(ymin - pad, ymax + pad)

    def update(frame_idx):
        eps = float(eps_values[frame_idx])

        y0p = y0 + eps
        y0m = y0 - eps
        x0p = float(finverse(y0p))
        x0m = float(finverse(y0m))

        horizontal = [y0, y0p, y0m]
        vertical = [x0, x0p, x0m]

        for ln, Y in zip(hlines, horizontal):
            ln.set_ydata([Y, Y])
        for ln, X in zip(vlines, vertical):
            ln.set_xdata([X, X])

        delta = min(abs(x0 - x0p), abs(x0 - x0m))
        ax.set_title(f"epsilon={eps:.2f}   delta={delta:.4f}")

        return [curve, *hlines, *vlines]

    anim = FuncAnimation(fig, update, frames=len(eps_values), blit=True)
    writer = PillowWriter(fps=fps)
    anim.save(gif_path, writer=writer)
    plt.close(fig)
    return gif_path


# Create the GIF
make_gif("continuity.gif")
