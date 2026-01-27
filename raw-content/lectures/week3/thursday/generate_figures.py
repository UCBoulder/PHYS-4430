"""
Generate Lecture Figures - Week 3 Thursday
==========================================

PHYS 4430 - Lenses and Gaussian Beams

This script generates all figures needed for the Week 3 Thursday lecture slides.
Figures are saved as high-resolution PNGs in the figures/ subdirectory.

Usage:
    python generate_figures.py

Output:
    figures/*.png
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc, Wedge
from matplotlib.patches import Rectangle, Polygon, Circle, Ellipse
from matplotlib.lines import Line2D
from pathlib import Path

# Output directory
SCRIPT_DIR = Path(__file__).parent
FIGURES_DIR = SCRIPT_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Set style for all figures
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.2,
})


# =============================================================================
# THIN LENS FIGURES
# =============================================================================

def thin_lens_diagram():
    """Generate thin lens ray diagram showing object, lens, and image."""
    print("  Generating: thursday_01_thin_lens.png")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(-1, 13)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    # Optical axis
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)

    # Lens position
    lens_x = 5
    lens_height = 2.5

    # Draw lens (double convex shape)
    lens_left = lens_x - 0.15
    lens_right = lens_x + 0.15

    # Simple lens representation with curved sides
    theta = np.linspace(-np.pi/2, np.pi/2, 50)
    curve_radius = 3

    # Left curve
    left_curve_x = lens_left - curve_radius * (1 - np.cos(theta)) * 0.15
    left_curve_y = lens_height * np.sin(theta)

    # Right curve
    right_curve_x = lens_right + curve_radius * (1 - np.cos(theta)) * 0.15
    right_curve_y = lens_height * np.sin(theta)

    # Fill lens
    lens_x_coords = np.concatenate([left_curve_x, right_curve_x[::-1]])
    lens_y_coords = np.concatenate([left_curve_y, right_curve_y[::-1]])
    ax.fill(lens_x_coords, lens_y_coords, color='lightblue', alpha=0.7,
            edgecolor='blue', linewidth=2)

    # Object (arrow)
    obj_x = 1.5
    obj_height = 1.5
    ax.annotate('', xy=(obj_x, obj_height), xytext=(obj_x, 0),
                arrowprops=dict(arrowstyle='->', color='darkblue', lw=3))

    # Image (inverted arrow)
    img_x = 9
    img_height = -1.0
    ax.annotate('', xy=(img_x, img_height), xytext=(img_x, 0),
                arrowprops=dict(arrowstyle='->', color='darkred', lw=3))

    # Focal points
    f = 2.5
    ax.plot(lens_x - f, 0, 'ko', markersize=8)
    ax.plot(lens_x + f, 0, 'ko', markersize=8)
    ax.text(lens_x - f, -0.5, 'F', ha='center', fontsize=12, fontweight='bold')
    ax.text(lens_x + f, -0.5, "F'", ha='center', fontsize=12, fontweight='bold')

    # Ray 1: Parallel to axis, through focal point
    ax.plot([obj_x, lens_x], [obj_height, obj_height], 'g-', lw=1.5, alpha=0.8)
    ax.plot([lens_x, img_x + 1], [obj_height, img_height - 0.3], 'g-', lw=1.5, alpha=0.8)

    # Ray 2: Through center of lens (straight)
    ax.plot([obj_x, img_x + 0.5], [obj_height, img_height - 0.15], 'orange', lw=1.5, alpha=0.8)

    # Ray 3: Through front focal point, exits parallel
    ax.plot([obj_x, lens_x], [obj_height, 0.5], 'purple', lw=1.5, alpha=0.8)
    ax.plot([lens_x, img_x + 0.5], [0.5, 0.5], 'purple', lw=1.5, alpha=0.8)

    # Labels
    ax.text(obj_x, obj_height + 0.4, 'Object', ha='center', fontsize=12,
            fontweight='bold', color='darkblue')
    ax.text(img_x, img_height - 0.5, 'Image', ha='center', fontsize=12,
            fontweight='bold', color='darkred')
    ax.text(lens_x, lens_height + 0.4, 'Lens', ha='center', fontsize=12,
            fontweight='bold', color='blue')

    # Distance labels
    ax.annotate('', xy=(obj_x, -2.3), xytext=(lens_x, -2.3),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text((obj_x + lens_x) / 2, -2.7, r'$S_1$', ha='center', fontsize=14,
            fontweight='bold')

    ax.annotate('', xy=(lens_x, -2.3), xytext=(img_x, -2.3),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text((lens_x + img_x) / 2, -2.7, r'$S_2$', ha='center', fontsize=14,
            fontweight='bold')

    # Equation box
    ax.text(11.5, 2, r'$\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}$',
            ha='center', va='center', fontsize=16,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                     edgecolor='orange', linewidth=2))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_01_thin_lens.png")
    plt.close()


def gaussian_beam_lens():
    """Generate diagram showing Gaussian beam transformation through a lens."""
    print("  Generating: thursday_02_beam_lens.png")

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-3.5, 3.0)
    ax.set_aspect('equal')
    ax.axis('off')

    # Parameters
    lens_x = 7
    w0_in = 0.8  # Input beam waist
    w0_out = 0.4  # Output beam waist (smaller = focused)
    zR_in = 3.0  # Input Rayleigh range
    zR_out = 1.5  # Output Rayleigh range

    waist_in_x = 2  # Input waist position
    waist_out_x = 11  # Output waist position

    # Draw input beam envelope
    z_in = np.linspace(0, lens_x - 0.4, 100)
    w_in = w0_in * np.sqrt(1 + ((z_in - waist_in_x) / zR_in) ** 2)

    ax.fill_between(z_in, w_in, -w_in, color='red', alpha=0.2)
    ax.plot(z_in, w_in, 'r-', lw=2)
    ax.plot(z_in, -w_in, 'r-', lw=2)

    # Draw output beam envelope
    z_out = np.linspace(lens_x + 0.4, 14, 100)
    w_out = w0_out * np.sqrt(1 + ((z_out - waist_out_x) / zR_out) ** 2)

    ax.fill_between(z_out, w_out, -w_out, color='blue', alpha=0.2)
    ax.plot(z_out, w_out, 'b-', lw=2)
    ax.plot(z_out, -w_out, 'b-', lw=2)

    # Draw CONVEX lens (bulges outward)
    lens_height = 2.0
    theta = np.linspace(-np.pi / 2, np.pi / 2, 50)

    # For convex lens: curves bulge OUTWARD (away from center)
    lens_center = lens_x
    lens_thickness = 0.4  # thickness at center
    curve_depth = 0.3  # how much the curves bulge out

    # Left surface curves left (bulges toward incoming beam)
    left_x = lens_center - lens_thickness / 2 - curve_depth * np.cos(theta)
    left_y = lens_height * np.sin(theta)

    # Right surface curves right (bulges toward outgoing beam)
    right_x = lens_center + lens_thickness / 2 + curve_depth * np.cos(theta)
    right_y = lens_height * np.sin(theta)

    # Combine to form lens shape
    lens_x_coords = np.concatenate([left_x, right_x[::-1]])
    lens_y_coords = np.concatenate([left_y, right_y[::-1]])
    ax.fill(lens_x_coords, lens_y_coords, color='lightblue', alpha=0.8,
            edgecolor='blue', linewidth=2)

    # Optical axis
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    # Waist markers
    ax.plot([waist_in_x, waist_in_x], [-w0_in - 0.2, w0_in + 0.2], 'r-', lw=3)
    ax.plot([waist_out_x, waist_out_x], [-w0_out - 0.2, w0_out + 0.2], 'b-', lw=3)

    # Labels (minimum font size 18)
    ax.text(waist_in_x, -1.8, r'$w_0$', ha='center',
            fontsize=20, color='darkred', fontweight='bold')
    ax.text(waist_in_x, -2.4, '(original waist)', ha='center',
            fontsize=18, color='darkred')

    ax.text(waist_out_x, -1.4, r"$w_0'$", ha='center',
            fontsize=20, color='darkblue', fontweight='bold')
    ax.text(waist_out_x, -2.0, '(new waist)', ha='center',
            fontsize=18, color='darkblue')

    ax.text(lens_x, lens_height + 0.4, 'Lens', ha='center', fontsize=20,
            fontweight='bold', color='blue')

    # Distance labels
    ax.annotate('', xy=(waist_in_x, -2.9), xytext=(lens_x, -2.9),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text((waist_in_x + lens_x) / 2, -3.3, r'$S_1$', ha='center', fontsize=22,
            fontweight='bold')

    ax.annotate('', xy=(lens_x, -2.9), xytext=(waist_out_x, -2.9),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text((lens_x + waist_out_x) / 2, -3.3, r'$S_2$', ha='center', fontsize=22,
            fontweight='bold')

    # Title
    ax.text(7, 2.8, 'Gaussian Beam Transformation by a Lens', ha='center',
            fontsize=22, fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_02_beam_lens.png")
    plt.close()


def diffraction_limit_diagram():
    """Generate diagram illustrating the diffraction limit concept."""
    print("  Generating: thursday_03_diffraction.png")

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(-1, 13)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Lens - CONVEX (bulges outward)
    lens_x = 4
    lens_height = 2.5

    theta = np.linspace(-np.pi / 2, np.pi / 2, 50)
    lens_thickness = 0.4
    curve_depth = 0.35

    # Left surface bulges left
    left_x = lens_x - lens_thickness / 2 - curve_depth * np.cos(theta)
    left_y = lens_height * np.sin(theta)

    # Right surface bulges right
    right_x = lens_x + lens_thickness / 2 + curve_depth * np.cos(theta)
    right_y = lens_height * np.sin(theta)

    lens_x_coords = np.concatenate([left_x, right_x[::-1]])
    lens_y_coords = np.concatenate([left_y, right_y[::-1]])
    ax.fill(lens_x_coords, lens_y_coords, color='lightblue', alpha=0.7,
            edgecolor='blue', linewidth=2)

    # Incoming beam (fills lens)
    beam_left = 0
    beam_width = lens_height

    ax.fill([beam_left, lens_x - 0.5, lens_x - 0.5, beam_left],
            [beam_width, beam_width, -beam_width, -beam_width],
            color='red', alpha=0.15)
    ax.plot([beam_left, lens_x - 0.5], [beam_width, beam_width], 'r-', lw=2)
    ax.plot([beam_left, lens_x - 0.5], [-beam_width, -beam_width], 'r-', lw=2)

    # Focused beam (converging then diverging)
    focus_x = 7
    focus_size = 0.15

    # Converging
    ax.fill([lens_x + 0.5, focus_x, lens_x + 0.5],
            [beam_width, 0, -beam_width],
            color='blue', alpha=0.15)
    ax.plot([lens_x + 0.5, focus_x], [beam_width, 0], 'b-', lw=2)
    ax.plot([lens_x + 0.5, focus_x], [-beam_width, 0], 'b-', lw=2)

    # Diverging
    div_end_x = 9.5
    div_height = 1.5
    ax.fill([focus_x, div_end_x, div_end_x, focus_x],
            [0, div_height, -div_height, 0],
            color='blue', alpha=0.15)
    ax.plot([focus_x, div_end_x], [0, div_height], 'b-', lw=2)
    ax.plot([focus_x, div_end_x], [0, -div_height], 'b-', lw=2)

    # Optical axis
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    # Focus point marker
    ax.plot(focus_x, 0, 'ko', markersize=10)

    # Dimension: lens diameter
    ax.annotate('', xy=(lens_x - 0.8, lens_height), xytext=(lens_x - 0.8, -lens_height),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(lens_x - 1.3, 0, 'D', ha='center', va='center', fontsize=22,
            fontweight='bold')

    # Dimension: focal length
    ax.annotate('', xy=(lens_x, -3.0), xytext=(focus_x, -3.0),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text((lens_x + focus_x) / 2, -3.4, 'f', ha='center', fontsize=22,
            fontweight='bold')

    # Spot size annotation
    ax.annotate('', xy=(focus_x + 0.4, 0.4), xytext=(focus_x + 0.4, -0.4),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax.text(focus_x + 0.9, 0, r'$w_0^{min}$', ha='left', va='center', fontsize=20,
            fontweight='bold', color='green')

    # Formulas box
    formulas = (r'$NA = \frac{D}{2f}$' + '\n\n' +
                r'$w_0^{min} \approx \frac{\lambda}{\pi \cdot NA}$')
    ax.text(11.5, 1.2, formulas, ha='center', va='center', fontsize=20,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                     edgecolor='orange', linewidth=2))

    # Labels
    ax.text(lens_x, lens_height + 0.5, 'Lens', ha='center', fontsize=20,
            fontweight='bold', color='blue')
    ax.text(focus_x, -0.9, 'Focus', ha='center', fontsize=20, fontweight='bold')

    # Title
    ax.text(5, 3.2, 'The Diffraction Limit', ha='center', fontsize=22,
            fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_03_diffraction.png")
    plt.close()


def prediction_workflow():
    """Generate diagram showing prediction workflow for Week 4."""
    print("  Generating: thursday_04_workflow.png")

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Box styles
    measure_style = dict(boxstyle='round,pad=0.5', facecolor='#ABEBC6',
                         edgecolor='black', linewidth=2)
    calc_style = dict(boxstyle='round,pad=0.5', facecolor='#AED6F1',
                      edgecolor='black', linewidth=2)
    predict_style = dict(boxstyle='round,pad=0.5', facecolor='#F9E79F',
                         edgecolor='black', linewidth=2)

    # Column 1: Measurements
    ax.text(2.5, 8, 'MEASURE', ha='center', fontsize=22, fontweight='bold',
            color='#27AE60')
    ax.text(2.5, 6.5, r'$w_0$ from fit' + '\n(Week 3)', ha='center',
            fontsize=18, bbox=measure_style)
    ax.text(2.5, 4.5, r'$S_1$' + '\n(waist to lens)', ha='center',
            fontsize=18, bbox=measure_style)
    ax.text(2.5, 2.5, r'$f$' + '\n(lens spec)', ha='center',
            fontsize=18, bbox=measure_style)

    # Column 2: Calculations
    ax.text(7, 8, 'CALCULATE', ha='center', fontsize=22, fontweight='bold',
            color='#2980B9')
    ax.text(7, 5.8, 'Thin lens equation:\n' + r'$S_2 = \frac{1}{1/f - 1/S_1}$',
            ha='center', fontsize=18, bbox=calc_style)
    ax.text(7, 3.2, 'Magnification:\n' + r"$w_0' = |S_2/S_1| \cdot w_0$",
            ha='center', fontsize=18, bbox=calc_style)

    # Column 3: Predictions
    ax.text(11.5, 8, 'PREDICT', ha='center', fontsize=22, fontweight='bold',
            color='#D68910')
    ax.text(11.5, 5.8, r"$S_2 \pm \sigma_{S_2}$" + '\n(new waist location)',
            ha='center', fontsize=18, bbox=predict_style)
    ax.text(11.5, 3.2, r"$w_0' \pm \sigma_{w_0'}$" + '\n(new waist size)',
            ha='center', fontsize=18, bbox=predict_style)

    # Arrows
    arrow_props = dict(arrowstyle='->', color='gray', lw=2.5)

    # Measure to Calculate
    ax.annotate('', xy=(5.0, 5.8), xytext=(4.0, 6.2), arrowprops=arrow_props)
    ax.annotate('', xy=(5.0, 5.0), xytext=(4.0, 4.5), arrowprops=arrow_props)
    ax.annotate('', xy=(5.0, 4.0), xytext=(4.0, 2.5), arrowprops=arrow_props)

    # Calculate to Predict
    ax.annotate('', xy=(9.8, 5.8), xytext=(8.8, 5.8), arrowprops=arrow_props)
    ax.annotate('', xy=(9.8, 3.2), xytext=(8.8, 3.2), arrowprops=arrow_props)

    # uncertainties package note
    ax.text(7, 1.0, 'Use `uncertainties` package for automatic propagation!',
            ha='center', fontsize=18, style='italic',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Title
    ax.text(7, 8.7, 'Week 4 Prediction Workflow', ha='center', fontsize=24,
            fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_04_workflow.png")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate all lecture figures for Week 3 Thursday."""
    print("\n" + "=" * 60)
    print("Generating Week 3 Thursday Lecture Figures")
    print("=" * 60)
    print(f"\nOutput directory: {FIGURES_DIR}\n")

    # Lens optics figures
    # Note: thursday_01_thin_lens.png is copied from:
    #   resources/lab-guides/gaussian-laser-beams/ray-diagram.png
    # (not generated by this script)
    print("--- Lens Optics Diagrams ---")
    gaussian_beam_lens()
    diffraction_limit_diagram()

    # Workflow figures
    print("\n--- Workflow Diagrams ---")
    prediction_workflow()

    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print("=" * 60)

    # List generated files
    print("\nGenerated files:")
    for f in sorted(FIGURES_DIR.glob("*.png")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
