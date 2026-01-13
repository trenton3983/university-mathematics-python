import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def f(x):
    return 2 / x

def finverse(x):
    return 2 / x

x = np.linspace(0.5, 2)
x0 = 1
y = f(x)
y0 = f(x0)

def draw_frame(eps, out_path, dpi=150):
    out_path = Path(out_path)

    y0p = y0 + eps
    y0m = y0 - eps
    x0p = finverse(y0p)
    x0m = finverse(y0m)

    vertical = [x0, x0p, x0m]
    horizontal = [y0, y0p, y0m]

    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=dpi)
    ax.plot(x, y, "r")

    for Y in horizontal:
        ax.axhline(y=Y, color="k", linestyle=":")
    for X in vertical:
        ax.axvline(x=X, color="c", linestyle=":")

    delta = min(abs(x0 - x0p), abs(x0 - x0m))
    ax.set_title(f"epsilon={eps:.2f}   delta={delta:.4f}")

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)

def make_avi(
    avi_path="continuity.avi",
    eps_values=None,
    fps=12,
    frames_dir="_frames_continuity",
):
    avi_path = Path(avi_path)
    frames_dir = Path(frames_dir)

    if eps_values is None:
        eps_values = np.round(np.arange(0.01, 0.401, 0.01), 2)

    frames_dir.mkdir(parents=True, exist_ok=True)

    frame_paths = []
    for i, eps in enumerate(eps_values):
        frame_path = frames_dir / f"frame_{i:04d}.png"
        draw_frame(float(eps), frame_path)
        frame_paths.append(frame_path)

    first = cv2.imread(str(frame_paths[0]))
    if first is None:
        raise RuntimeError("Failed to read first frame image.")

    h, w = first.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(str(avi_path), fourcc, fps, (w, h))

    for p in frame_paths:
        img = cv2.imread(str(p))
        if img is None:
            raise RuntimeError(f"Failed to read frame: {p}")
        if img.shape[1] != w or img.shape[0] != h:
            img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        writer.write(img)

    writer.release()
    return avi_path

# Create the AVI
make_avi("continuity.avi")
