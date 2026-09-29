import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# --- 1. Physics Parameters ---
m, M, g = 3, 5, 9.81
theta_deg = 30
L = 4.0

theta = np.radians(theta_deg)

# --- 2. Theoretical Accelerations ---
A = (m * g * np.sin(theta) * np.cos(theta)) / (M + m * (np.sin(theta)**2))
a_rel = (M + m) * g * np.sin(theta) / (M + m * (np.sin(theta)**2))

t_max = np.sqrt(2 * L / a_rel)
fps = 30
frames = int(fps * t_max)
t_vals = np.linspace(0, t_max, frames)

# --- 3. Setup Plot ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(-5, 3)
ax.set_ylim(-0.5, 3)
ax.set_aspect('equal')
ax.set_title("Block sliding on a movable wedge")

ax.axhline(0, color='black', lw=2)

wedge_line, = ax.plot([], [], 'b-', lw=3, label="Wedge (M)")
block_patch, = ax.plot([], [], 'rs', markersize=12, label="Block (m)")
trail_line, = ax.plot([], [], 'r:', alpha=0.6, label="Block Path")

block_trail_x, block_trail_y = [], []

# --- 4. Animation Update Function ---
def update(frame):
    t = t_vals[frame]
    X_wedge = -0.5 * A * (t**2)

    W_base = L * np.cos(theta)
    W_height = L * np.sin(theta)

    wedge_line.set_data([X_wedge, X_wedge + W_base, X_wedge, X_wedge], [0, 0, W_height, 0])

    s = 0.5 * a_rel * (t**2)
    x_block = X_wedge + s * np.cos(theta)
    y_block = W_height - s * np.sin(theta)

    block_patch.set_data([x_block], [y_block])

    block_trail_x.append(x_block)
    block_trail_y.append(y_block)
    trail_line.set_data(block_trail_x, block_trail_y)

    return wedge_line, block_patch, trail_line

# --- 5. Generate Animation & Display as Video ---
anim = FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=False)

# Close the static plot to force Colab to show only the video player
plt.close(fig)

# Display as HTML5 Video with Play/Pause controls
HTML(anim.to_html5_video())