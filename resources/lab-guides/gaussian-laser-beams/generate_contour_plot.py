"""
Generate chi-squared contour plot for Gaussian Beams Week 2 lab guide.

This script creates the reference figure (contour.png) showing the chi-squared
landscape for fitting beam profile data with an error function model.

Usage:
    python generate_contour_plot.py

Output:
    contour.png in the same directory
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving figures
import matplotlib.pyplot as plt
from scipy.special import erf
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent


def beam_profile(x, amplitude, center, width, offset):
    """Error function model for knife-edge beam profile.

    Parameters:
        x: position (m)
        amplitude: half the voltage swing (V)
        center: beam center position (m)
        width: beam size w (m)
        offset: vertical offset (V)
    """
    return amplitude * erf(np.sqrt(2) * (x - center) / width) + offset


def chi_squared(width, center, x_data, y_data, amplitude_fixed, offset_fixed):
    """Calculate chi-squared for given parameters (assuming sigma=1)."""
    y_fit = beam_profile(x_data, amplitude_fixed, center, width, offset_fixed)
    return np.sum((y_data - y_fit)**2)


def main():
    # Load the data
    data_file = SCRIPT_DIR / "profile_data_without_errors.csv"
    data = np.loadtxt(data_file, delimiter=',', skiprows=1)
    x_data = data[:, 0]
    y_data = data[:, 1]

    print(f"Loaded {len(x_data)} data points")
    print(f"  x range: {x_data.min():.5f} to {x_data.max():.5f} m")
    print(f"  y range: {y_data.min():.3f} to {y_data.max():.3f} V")

    # Fixed parameters (from averaging first 6 and last 5 points)
    v_min = np.mean(y_data[:6])
    v_max = np.mean(y_data[-5:])
    amplitude_fixed = (v_max - v_min) / 2
    offset_fixed = (v_max + v_min) / 2

    print(f"\nFixed parameters:")
    print(f"  amplitude = {amplitude_fixed:.5f} V")
    print(f"  offset    = {offset_fixed:.5f} V")

    # Create grid for contour plot
    # Ranges chosen to show the minimum clearly
    center_range = np.linspace(0.01070, 0.01090, 100)
    width_range = np.linspace(0.00005, 0.00040, 100)
    B, W = np.meshgrid(center_range, width_range)

    # Calculate chi-squared for each combination
    Z = np.zeros_like(B)
    for i in range(len(width_range)):
        for j in range(len(center_range)):
            Z[i, j] = chi_squared(width_range[i], center_range[j], x_data, y_data,
                                  amplitude_fixed, offset_fixed)

    # Find the minimum for reporting
    min_idx = np.unravel_index(np.argmin(Z), Z.shape)
    best_width = width_range[min_idx[0]]
    best_center = center_range[min_idx[1]]
    min_chi2 = Z[min_idx]

    print(f"\nGraphical minimum:")
    print(f"  center = {best_center:.5f} m")
    print(f"  width  = {best_width:.6f} m")
    print(f"  chi^2  = {min_chi2:.2f}")

    # Create the contour plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Filled contours for background color
    contourf = ax.contourf(B, W, Z, levels=20, cmap='viridis_r')

    # Line contours with labels
    contour = ax.contour(B, W, Z, levels=10, colors='black', linewidths=0.5)
    ax.clabel(contour, inline=True, fontsize=12, fmt='%.0f')

    # Colorbar
    cbar = plt.colorbar(contourf, ax=ax, label='$\\chi^2$')
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label('$\\chi^2$', fontsize=16)

    # Labels matching the figure convention
    ax.set_xlabel('center of beam, $b$ (m)', fontsize=16)
    ax.set_ylabel('beam radius, $w$ (m)', fontsize=16)
    ax.set_title('$\\chi^2$ Contour Plot', fontsize=18)

    # Increase tick label size and rotate x-axis labels
    ax.tick_params(axis='both', labelsize=14)
    ax.tick_params(axis='x', rotation=45)

    # Mark the minimum
    ax.plot(best_center, best_width, 'r*', markersize=15, label='Minimum')
    ax.legend(loc='upper right', fontsize=14)

    plt.tight_layout()

    # Save the figure
    output_file = SCRIPT_DIR / "contour.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\nSaved figure to: {output_file}")


if __name__ == "__main__":
    main()
