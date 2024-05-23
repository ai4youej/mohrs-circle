import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider, TextBox

def plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta):
    # Calculate center and radius of Mohr's circle
    center = (sigma_x + sigma_y) / 2.0
    radius = np.sqrt(((sigma_x - sigma_y) / 2.0)**2 + tau_xy**2)

    # Create theta values for drawing circle
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = center + radius * np.cos(theta)
    circle_y = radius * np.sin(theta)

    # Clear previous plot and plot Mohr's circle
    ax.clear()
    ax1.clear()
    ax.plot(circle_x, circle_y, label='Mohr\'s Circle')

    # Plot points (sigma_x, -tau_xy) and (sigma_y, tau_xy)
    point1 = (sigma_x, -tau_xy)
    point2 = (sigma_y, tau_xy)
    ax.plot(point1[0], point1[1], 'ro')  # Plot point (sigma_x, -tau_xy)
    ax.plot(point2[0], point2[1], 'ro')  # Plot point (sigma_y, tau_xy)

    # Plot line between the points (sigma_x, -tau_xy) and (sigma_y, tau_xy)
    ax.plot([sigma_x, sigma_y], [-tau_xy, tau_xy], 'r--')

    # Annotate stress points
    ax.annotate(f'({sigma_x}, {-tau_xy:.2f})', point1, textcoords="offset points", xytext=(10,10), ha='center')
    ax.annotate(f'({sigma_y}, {tau_xy:.2f})', point2, textcoords="offset points", xytext=(10,-10), ha='center')

    # Plot maximum and minimum shear stress points and connect them with a line
    max_shear = (center, radius)
    min_shear = (center, -radius)
    ax.plot(max_shear[0], max_shear[1], 'bo')  # Max shear stress point
    ax.plot(min_shear[0], min_shear[1], 'bo')  # Min shear stress point
    ax.plot([center, center], [radius, -radius], 'b--')

    # Annotate max and min shear stress points
    ax.annotate(f'({center:.2f}, {radius:.2f})', max_shear, textcoords="offset points", xytext=(10,10), ha='center')
    ax.annotate(f'({center:.2f}, {-radius:.2f})', min_shear, textcoords="offset points", xytext=(10,-10), ha='center')

    # Set labels and title
    ax.set_xlabel('Normal Stress (σ)')
    ax.set_ylabel('Shear Stress (τ)')
    ax.set_title('Mohr\'s Circle Construction')
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.legend()

    # Ensure the circle is perfectly round
    ax.set_aspect('equal')
    ax1.set_aspect('equal')
    ax1.set_xlim([0, 2])
    ax1.set_ylim([0, 2])
    
    # Draw a square
    ax1.add_patch(patches.Rectangle((0.5, 0.5), 1, 1, edgecolor = 'black', fill = False))
    
    
    # Square center = (1, 1) / Draw stress arrows
    # (0.5, 0.5) to (1.5, 1.5)
    ratio = 0.002
    sx, sy, txy = sigma_x * ratio, sigma_y * ratio, tau_xy * ratio
    
    # Plot arrows for sigma_x
    ax1.arrow(0.25 + sx, 1, -2 * sx, 0, width = 0.005, color = 'red')
    ax1.arrow(1.75 - sx, 1,  2 * sx, 0, width = 0.005, color = 'red')
    
    # Plot arrows for sigma_y
    ax1.arrow(1, 1.75 - sy, 0,  2 * sy, width = 0.005, color = 'purple')
    ax1.arrow(1, 0.25 + sy, 0, -2 * sy, width = 0.005, color = 'purple')
    
    # Plot arrows for tau_xy
    ax1.arrow(1 - txy, 1.75, 2 * txy, 0, width = 0.005, color = 'purple')
    ax1.arrow(1 + txy, 0.25, -2 * txy, 0, width = 0.005, color = 'purple')
    ax1.arrow(0.25, 1 + txy, 0, -2 * txy, width = 0.005, color = 'red')
    ax1.arrow(1.75, 1 - txy, 0, 2 * txy, width = 0.005, color = 'red')
    
    # Refresh the figure
    fig.canvas.draw_idle()

def update_sigma_x(val):
    global sigma_x
    sigma_x = float(val)
    sigma_x_box.set_val(str(sigma_x))  # Update text box
    plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)

def update_sigma_y(val):
    global sigma_y
    sigma_y = float(val)
    sigma_y_box.set_val(str(sigma_y))  # Update text box
    plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)

def update_tau_xy(val):
    global tau_xy
    tau_xy = float(val)
    tau_xy_box.set_val(str(tau_xy))  # Update text box
    plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)

def submit_sigma_x(text):
    global sigma_x
    try:
        sigma_x = float(text)
        sigma_x_slider.set_val(sigma_x)  # Update slider
        plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)
    except ValueError:
        pass

def submit_sigma_y(text):
    global sigma_y
    try:
        sigma_y = float(text)
        sigma_y_slider.set_val(sigma_y)  # Update slider
        plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)
    except ValueError:
        pass

def submit_tau_xy(text):
    global tau_xy
    try:
        tau_xy = float(text)
        tau_xy_slider.set_val(tau_xy)  # Update slider
        plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)
    except ValueError:
        pass

def submit_theta(text):
    global theta
    try:
        theta = float(text)
        plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)
    except ValueError:
        pass
    
# Initial stress values
sigma_x = 30
sigma_y = -20
tau_xy = 10
theta = 34 # Degree

# Create figure and axes
fig, (ax, ax1) = plt.subplots(1, 2, figsize=(8, 6))
plt.subplots_adjust(bottom=0.4)

# Create sliders for sigma_x, sigma_y, and tau_xy
sigma_x_slider_ax = plt.axes([0.2, 0.25, 0.65, 0.03])
sigma_y_slider_ax = plt.axes([0.2, 0.2, 0.65, 0.03])
tau_xy_slider_ax = plt.axes([0.2, 0.15, 0.65, 0.03])
sigma_x_slider = Slider(sigma_x_slider_ax, 'σ_x:', -100, 100, valinit=sigma_x)
sigma_y_slider = Slider(sigma_y_slider_ax, 'σ_y:', -100, 100, valinit=sigma_y)
tau_xy_slider = Slider(tau_xy_slider_ax, 'τ_xy:', -100, 100, valinit=tau_xy)

# Create text boxes for sigma_x, sigma_y, tau_xy, and theta
sigma_x_box_ax = plt.axes([0.2, 0.05, 0.1, 0.05])
sigma_y_box_ax = plt.axes([0.4, 0.05, 0.1, 0.05])
tau_xy_box_ax = plt.axes([0.6, 0.05, 0.1, 0.05])
theta_box_ax = plt.axes([0.8, 0.05, 0.1, 0.05])

sigma_x_box = TextBox(sigma_x_box_ax, 'σ_x: ', initial=str(sigma_x))
sigma_y_box = TextBox(sigma_y_box_ax, 'σ_y: ', initial=str(sigma_y))
tau_xy_box = TextBox(tau_xy_box_ax, 'τ_xy: ', initial=str(tau_xy))
theta_box = TextBox(theta_box_ax, 'θ: ', initial=str(theta))
    
# Connect sliders to update functions
sigma_x_slider.on_changed(update_sigma_x)
sigma_y_slider.on_changed(update_sigma_y)
tau_xy_slider.on_changed(update_tau_xy)

# Connect text boxes to submit functions
sigma_x_box.on_submit(submit_sigma_x)
sigma_y_box.on_submit(submit_sigma_y)
tau_xy_box.on_submit(submit_tau_xy)
theta_box.on_submit(submit_theta)

# Plot initial Mohr's circle
plot_mohrs_circle(sigma_x, sigma_y, tau_xy, theta)

# Show interactive plot
plt.show()
