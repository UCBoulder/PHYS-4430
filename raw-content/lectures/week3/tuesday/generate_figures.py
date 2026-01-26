"""
Generate Lecture Figures - Week 3 Tuesday
==========================================

PHYS 4430 - Motor Control and Error Propagation

This script generates all figures needed for the Week 3 Tuesday lecture slides.
Figures are saved as high-resolution PNGs in the figures/ subdirectory.

Usage:
    python generate_figures.py

Output:
    figures/*.png
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.patches import Rectangle, Polygon
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
# MOTOR CONTROL FIGURES
# =============================================================================

def motor_system_diagram():
    """Generate motor controller system diagram."""
    print("  Generating: tuesday_01_motor_system.png")

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Box styles
    controller_style = dict(boxstyle='round,pad=0.4', facecolor='lightblue',
                            edgecolor='black', linewidth=2)
    motor_style = dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                       edgecolor='black', linewidth=2)
    stage_style = dict(boxstyle='round,pad=0.4', facecolor='lightgreen',
                       edgecolor='black', linewidth=2)
    computer_style = dict(boxstyle='round,pad=0.4', facecolor='lavender',
                          edgecolor='black', linewidth=2)

    y_main = 2.5

    # Computer
    ax.text(1.5, y_main, 'Computer\n(Python)', ha='center', va='center',
            fontsize=13, bbox=computer_style, fontweight='bold')

    # Arrow: Computer to Controller
    ax.annotate('', xy=(3.8, y_main), xytext=(2.5, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=2.5))
    ax.text(3.15, y_main + 0.5, 'USB', ha='center', fontsize=11, style='italic')

    # KST101 Controller
    ax.text(5.5, y_main, 'KST101\nController', ha='center', va='center',
            fontsize=13, bbox=controller_style, fontweight='bold')

    # Arrow: Controller to Motor
    ax.annotate('', xy=(8.0, y_main), xytext=(7.0, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=2.5))
    ax.text(7.5, y_main + 0.5, 'Power +\nControl', ha='center', fontsize=10, style='italic')

    # Stepper Motor
    ax.text(9.5, y_main, 'Stepper\nMotor', ha='center', va='center',
            fontsize=13, bbox=motor_style, fontweight='bold')

    # Arrow: Motor to Stage
    ax.annotate('', xy=(12.0, y_main), xytext=(11.0, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=2.5))
    ax.text(11.5, y_main + 0.5, 'Rotation', ha='center', fontsize=10, style='italic')

    # Translation Stage
    ax.text(13, y_main, 'Translation\nStage', ha='center', va='center',
            fontsize=13, bbox=stage_style, fontweight='bold')

    # Labels below
    ax.text(1.5, y_main - 1.2, 'Sends\ncommands', ha='center', fontsize=10, color='gray')
    ax.text(5.5, y_main - 1.2, '"Brain" that\ndrives motor', ha='center', fontsize=10, color='gray')
    ax.text(9.5, y_main - 1.2, 'Discrete\nsteps', ha='center', fontsize=10, color='gray')
    ax.text(13, y_main - 1.2, 'Linear\nmotion', ha='center', fontsize=10, color='gray')

    # Title
    ax.text(7, 4.5, 'Motor Controller System Components', ha='center', va='center',
            fontsize=16, fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tuesday_01_motor_system.png")
    plt.close()


def software_stack_diagram():
    """Generate software architecture stack diagram."""
    print("  Generating: tuesday_02_software_stack.png")

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Layer positions (bottom to top)
    layers = [
        ('Motor', 'Hardware', '#D4E6F1', 1.0),
        ('KST101 Controller', 'Hardware', '#D4E6F1', 2.2),
        ('USB Driver', 'Windows', '#F9E79F', 3.4),
        ('Thorlabs Kinesis SDK', '.NET Libraries', '#ABEBC6', 4.6),
        ('pythonnet', 'Python ↔ .NET Bridge', '#F5B7B1', 5.8),
        ('Your Python Script', 'Your Code!', '#D7BDE2', 7.0),
    ]

    box_width = 6
    box_height = 1.1
    x_center = 5.5

    for name, subtitle, color, y in layers:
        # Main box
        rect = FancyBboxPatch((x_center - box_width/2, y), box_width, box_height,
                              boxstyle="round,pad=0.02,rounding_size=0.15",
                              facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)

        # Text
        ax.text(x_center, y + box_height/2 + 0.15, name, ha='center', va='center',
                fontsize=22, fontweight='bold')
        ax.text(x_center, y + box_height/2 - 0.3, subtitle, ha='center', va='center',
                fontsize=16, color='gray', style='italic')

    # Arrows between layers
    arrow_x = x_center
    for i in range(len(layers) - 1):
        y_bottom = layers[i][3] + box_height
        y_top = layers[i + 1][3]
        y_mid = (y_bottom + y_top) / 2
        ax.annotate('', xy=(arrow_x, y_top), xytext=(arrow_x, y_bottom),
                    arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))

    # Side labels (centered vertically with each bracket section)
    ax.text(0.6, 2.15, 'Physical\nHardware', ha='center', va='center',
            fontsize=18, color='#2E86AB', fontweight='bold')
    ax.text(0.6, 4.55, 'System\nSoftware', ha='center', va='center',
            fontsize=18, color='#2E86AB', fontweight='bold')
    ax.text(0.6, 6.95, 'Python\nLayer', ha='center', va='center',
            fontsize=18, color='#2E86AB', fontweight='bold')

    # Bracket indicators (moved to not overlap with text)
    ax.plot([1.5, 1.5], [1.0, 3.3], 'k-', lw=1.5)
    ax.plot([1.45, 1.55], [1.0, 1.0], 'k-', lw=1.5)
    ax.plot([1.45, 1.55], [3.3, 3.3], 'k-', lw=1.5)

    ax.plot([1.5, 1.5], [3.4, 5.7], 'k-', lw=1.5)
    ax.plot([1.45, 1.55], [3.4, 3.4], 'k-', lw=1.5)
    ax.plot([1.45, 1.55], [5.7, 5.7], 'k-', lw=1.5)

    ax.plot([1.5, 1.5], [5.8, 8.1], 'k-', lw=1.5)
    ax.plot([1.45, 1.55], [5.8, 5.8], 'k-', lw=1.5)
    ax.plot([1.45, 1.55], [8.1, 8.1], 'k-', lw=1.5)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tuesday_02_software_stack.png")
    plt.close()


def troubleshooting_flowchart():
    """Generate troubleshooting flowchart."""
    print("  Generating: tuesday_03_troubleshooting.png")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Styles
    question_style = dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                          edgecolor='black', linewidth=2)
    action_style = dict(boxstyle='round,pad=0.3', facecolor='lightcoral',
                        edgecolor='black', linewidth=2)
    success_style = dict(boxstyle='round,pad=0.3', facecolor='lightgreen',
                         edgecolor='black', linewidth=2)

    # Start
    ax.text(6, 9.2, 'Start: Motor not working', ha='center', va='center',
            fontsize=14, fontweight='bold', bbox=question_style)

    # Step 1: Check Device Manager
    ax.text(6, 7.5, 'Check Device Manager:\n"Thorlabs APT Device" visible?',
            ha='center', va='center', fontsize=11, bbox=question_style)
    ax.annotate('', xy=(6, 8.5), xytext=(6, 8.9),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    # No branch - USB issue
    ax.text(2.5, 7.5, 'USB/Driver\nIssue', ha='center', va='center',
            fontsize=11, bbox=action_style)
    ax.annotate('', xy=(3.5, 7.5), xytext=(4.5, 7.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax.text(4, 7.85, 'No', ha='center', fontsize=10, color='red')

    # Yes branch
    ax.annotate('', xy=(6, 6.5), xytext=(6, 7.0),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    ax.text(6.3, 6.75, 'Yes', ha='left', fontsize=10, color='green')

    # Step 2: Python sees device
    ax.text(6, 5.5, 'BuildDeviceList() shows\nyour serial number?',
            ha='center', va='center', fontsize=11, bbox=question_style)

    # No branch - SDK issue
    ax.text(2.5, 5.5, 'Kinesis SDK or\npythonnet Issue', ha='center', va='center',
            fontsize=11, bbox=action_style)
    ax.annotate('', xy=(3.5, 5.5), xytext=(4.5, 5.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax.text(4, 5.85, 'No', ha='center', fontsize=10, color='red')

    # Yes branch
    ax.annotate('', xy=(6, 4.5), xytext=(6, 5.0),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    ax.text(6.3, 4.75, 'Yes', ha='left', fontsize=10, color='green')

    # Step 3: Movement works
    ax.text(6, 3.5, 'Motor moves when\ncommanded?',
            ha='center', va='center', fontsize=11, bbox=question_style)

    # No branch - Power/config issue
    ax.text(2.5, 3.5, 'Power, Limits, or\nConfiguration', ha='center', va='center',
            fontsize=11, bbox=action_style)
    ax.annotate('', xy=(3.5, 3.5), xytext=(4.5, 3.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax.text(4, 3.85, 'No', ha='center', fontsize=10, color='red')

    # Yes branch - Success!
    ax.annotate('', xy=(6, 2.2), xytext=(6, 3.0),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    ax.text(6.3, 2.6, 'Yes', ha='left', fontsize=10, color='green')

    ax.text(6, 1.5, 'Ready to go!', ha='center', va='center',
            fontsize=14, fontweight='bold', bbox=success_style)

    # Title
    ax.text(6, 10.3, 'Systematic Troubleshooting', ha='center', va='center',
            fontsize=16, fontweight='bold')

    # Fix suggestions on right side
    ax.text(9.5, 7.5, 'Try:\n• Check USB cable\n• Reinstall driver\n• Try different port',
            ha='left', va='center', fontsize=9, color='gray')
    ax.text(9.5, 5.5, 'Try:\n• Check Python bitness\n• Verify Kinesis path\n• Close other apps',
            ha='left', va='center', fontsize=9, color='gray')
    ax.text(9.5, 3.5, 'Try:\n• Check power supply\n• Home the stage\n• Check travel limits',
            ha='left', va='center', fontsize=9, color='gray')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tuesday_03_troubleshooting.png")
    plt.close()


# =============================================================================
# ERROR PROPAGATION FIGURES
# =============================================================================

def autodiff_concept():
    """Generate automatic differentiation concept diagram."""
    print("  Generating: tuesday_04_autodiff.png")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Box styles
    input_style = dict(boxstyle='round,pad=0.3', facecolor='lightblue',
                       edgecolor='black', linewidth=2)
    operation_style = dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                           edgecolor='black', linewidth=2)
    output_style = dict(boxstyle='round,pad=0.3', facecolor='lightgreen',
                        edgecolor='black', linewidth=2)

    y_main = 2.5

    # Input values with uncertainties
    ax.text(1.5, 3.5, r'$w_0 = 0.10 \pm 0.01$', ha='center', va='center',
            fontsize=12, bbox=input_style)
    ax.text(1.5, 1.5, r'$z = 1500 \pm 10$', ha='center', va='center',
            fontsize=12, bbox=input_style)

    # Arrows to operation
    ax.annotate('', xy=(4.0, 3.0), xytext=(2.5, 3.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.annotate('', xy=(4.0, 2.0), xytext=(2.5, 1.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    # Operation (formula)
    ax.text(5.5, y_main, r'$w(z) = w_0\sqrt{1 + (z/z_R)^2}$', ha='center', va='center',
            fontsize=13, bbox=operation_style)

    # Arrow to output
    ax.annotate('', xy=(8.0, y_main), xytext=(7.2, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    # Output with propagated uncertainty
    ax.text(10, y_main, r'$w = 3.02 \pm 0.02$', ha='center', va='center',
            fontsize=13, bbox=output_style, fontweight='bold')

    # Labels
    ax.text(1.5, 4.3, 'Inputs\n(with uncertainty)', ha='center', va='center',
            fontsize=11, color='gray')
    ax.text(5.5, 3.8, 'Operation', ha='center', va='center',
            fontsize=11, color='gray')
    ax.text(10, 3.5, 'Output\n(uncertainty propagated!)', ha='center', va='center',
            fontsize=11, color='gray')

    # Magic wand annotation
    ax.text(6.5, 1.3, 'uncertainties package tracks\nall partial derivatives\nautomatically!',
            ha='center', va='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    # Title
    ax.text(6, 4.7, 'Automatic Error Propagation with `uncertainties`', ha='center',
            fontsize=15, fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tuesday_04_autodiff.png")
    plt.close()


def predict_measure_compare_cycle():
    """Generate predict-measure-compare cycle diagram."""
    print("  Generating: tuesday_05_predict_cycle.png")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Circle positions (equilateral triangle)
    import math
    radius = 1.3
    angle_offset = math.pi / 2  # Start at top

    positions = []
    for i in range(3):
        angle = angle_offset - i * 2 * math.pi / 3
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        positions.append((x, y))

    # Labels and colors
    labels = ['PREDICT', 'MEASURE', 'COMPARE']
    subtexts = [
        'Calculate expected\nresults with\nuncertainties',
        'Collect data',
        'Do they agree\nwithin error bars?'
    ]
    colors = ['#AED6F1', '#ABEBC6', '#F9E79F']

    # Draw circles and labels
    circle_radius = 0.5
    for (x, y), label, subtext, color in zip(positions, labels, subtexts, colors):
        circle = Circle((x, y), circle_radius, facecolor=color,
                        edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y + 0.12, label, ha='center', va='center',
                fontsize=13, fontweight='bold')
        ax.text(x, y - 0.15, subtext, ha='center', va='center',
                fontsize=8, color='gray')

    # Draw arrows between circles
    arrow_style = dict(arrowstyle='->', color='black', lw=2,
                       connectionstyle='arc3,rad=0.2')

    # PREDICT -> MEASURE
    ax.annotate('', xy=(positions[1][0] - 0.3, positions[1][1] + 0.4),
                xytext=(positions[0][0] + 0.3, positions[0][1] - 0.35),
                arrowprops=arrow_style)

    # MEASURE -> COMPARE
    ax.annotate('', xy=(positions[2][0] + 0.15, positions[2][1] + 0.45),
                xytext=(positions[1][0] + 0.45, positions[1][1] + 0.15),
                arrowprops=arrow_style)

    # COMPARE -> PREDICT (or back to beginning)
    ax.annotate('', xy=(positions[0][0] - 0.45, positions[0][1] - 0.15),
                xytext=(positions[2][0] - 0.15, positions[2][1] + 0.45),
                arrowprops=arrow_style)

    # Center text
    ax.text(0, 0, 'The\nScientific\nMethod', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#2E86AB')

    # Agreement/disagreement annotations
    ax.text(1.8, -0.8, 'Agreement?\nTheory validated!', ha='center', va='center',
            fontsize=9, color='green',
            bbox=dict(boxstyle='round', facecolor='#D5F5E3', alpha=0.8))
    ax.text(1.8, -1.4, 'Disagreement?\nInvestigate!', ha='center', va='center',
            fontsize=9, color='red',
            bbox=dict(boxstyle='round', facecolor='#FADBD8', alpha=0.8))

    # Title
    ax.text(0, 1.9, 'The Predict-Measure-Compare Cycle', ha='center', va='center',
            fontsize=16, fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tuesday_05_predict_cycle.png")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate all lecture figures for Week 3 Tuesday."""
    print("\n" + "=" * 60)
    print("Generating Week 3 Tuesday Lecture Figures")
    print("=" * 60)
    print(f"\nOutput directory: {FIGURES_DIR}\n")

    # Motor control figures
    print("--- Motor Control Diagrams ---")
    motor_system_diagram()
    software_stack_diagram()
    troubleshooting_flowchart()

    # Error propagation figures
    print("\n--- Error Propagation Diagrams ---")
    autodiff_concept()
    predict_measure_compare_cycle()

    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print("=" * 60)

    # List generated files
    print("\nGenerated files:")
    for f in sorted(FIGURES_DIR.glob("*.png")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
