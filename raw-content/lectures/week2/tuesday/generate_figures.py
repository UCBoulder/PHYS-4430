"""
Generate Lecture Figures - Week 2 Tuesday
==========================================

PHYS 4430 - Data Acquisition and Digital Sampling

This script generates all figures needed for the Week 2 Tuesday lecture slides.
Figures are saved as high-resolution PNGs in the figures/ subdirectory.

Usage:
    python generate_figures.py

Output:
    figures/*.png
"""

import numpy as np
import matplotlib.pyplot as plt
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
# DAQ DIAGRAMS
# =============================================================================

def single_ended_vs_differential():
    """Generate single-ended vs differential wiring diagram."""
    print("  Generating: tuesday_05_single_ended_vs_differential.png")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Common styling
    box_style = dict(boxstyle='round,pad=0.3', facecolor='lightblue',
                     edgecolor='black', linewidth=2)

    # === Single-Ended ===
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Single-Ended (8 channels)', fontsize=14, fontweight='bold')

    # Signal source box
    ax.text(1.5, 5, 'Signal\nSource', ha='center', va='center', fontsize=11,
            bbox=box_style)

    # DAQ box
    ax.add_patch(plt.Rectangle((5.5, 2), 3.5, 5, facecolor='lightyellow',
                                edgecolor='black', linewidth=2, zorder=1))
    ax.text(7.25, 6.3, 'USB-6009', ha='center', va='center', fontsize=12,
            fontweight='bold')

    # DAQ terminals
    ax.text(6.2, 5, 'AI0', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='gray'))
    ax.text(6.2, 3.5, 'GND', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='gray'))

    # Signal wire (red)
    ax.annotate('', xy=(5.7, 5), xytext=(2.5, 5),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(4, 5.4, 'Signal', ha='center', fontsize=10, color='red')

    # Ground wire (black)
    ax.annotate('', xy=(5.7, 3.5), xytext=(2.5, 3.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(4, 3.9, 'Ground', ha='center', fontsize=10, color='black')

    # Ground symbol at source
    ax.plot([1.5, 1.5], [3.5, 3.0], 'k-', lw=2)
    ax.plot([1.2, 1.8], [3.0, 3.0], 'k-', lw=2)
    ax.plot([1.3, 1.7], [2.8, 2.8], 'k-', lw=1.5)
    ax.plot([1.4, 1.6], [2.6, 2.6], 'k-', lw=1)

    # Measurement annotation
    ax.annotate('', xy=(8.5, 5), xytext=(8.5, 3.5),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax.text(9.2, 4.25, 'V', ha='center', va='center', fontsize=14,
            color='green', fontweight='bold')

    # === Differential ===
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Differential (4 channels)', fontsize=14, fontweight='bold')

    # Signal source box
    ax.text(1.5, 5, 'Signal\nSource', ha='center', va='center', fontsize=11,
            bbox=box_style)

    # DAQ box
    ax.add_patch(plt.Rectangle((5.5, 2), 3.5, 5, facecolor='lightyellow',
                                edgecolor='black', linewidth=2, zorder=1))
    ax.text(7.25, 6.3, 'USB-6009', ha='center', va='center', fontsize=12,
            fontweight='bold')

    # DAQ terminals
    ax.text(6.2, 5.2, 'AI0+', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='gray'))
    ax.text(6.2, 3.8, 'AI0−', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='gray'))

    # Signal+ wire (red)
    ax.annotate('', xy=(5.7, 5.2), xytext=(2.5, 5.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(4, 5.8, 'Signal +', ha='center', fontsize=10, color='red')

    # Signal- wire (blue)
    ax.annotate('', xy=(5.7, 3.8), xytext=(2.5, 4.5),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.text(4, 3.9, 'Signal −', ha='center', fontsize=10, color='blue')

    # Measurement annotation
    ax.annotate('', xy=(8.5, 5.2), xytext=(8.5, 3.8),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax.text(9.2, 4.5, 'V', ha='center', va='center', fontsize=14,
            color='green', fontweight='bold')

    # Add note about noise rejection
    ax.text(7.25, 2.5, 'Better noise\nrejection', ha='center', va='center',
            fontsize=10, style='italic', color='darkgreen')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tuesday_05_single_ended_vs_differential.png")
    plt.close()


def noise_sources_block_diagram():
    """Generate photodetector noise sources block diagram."""
    print("  Generating: tuesday_06_noise_sources_block_diagram.png")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Block styles
    signal_style = dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                        edgecolor='black', linewidth=2)
    component_style = dict(boxstyle='round,pad=0.4', facecolor='lightblue',
                           edgecolor='black', linewidth=2)
    noise_style = dict(boxstyle='round,pad=0.3', facecolor='mistyrose',
                       edgecolor='red', linewidth=1.5)
    output_style = dict(boxstyle='round,pad=0.4', facecolor='lightgreen',
                        edgecolor='black', linewidth=2)

    # Main signal chain (y=4)
    y_main = 4

    # Light source
    ax.text(1, y_main, 'Light\n(photons)', ha='center', va='center',
            fontsize=11, bbox=signal_style)

    # Arrow
    ax.annotate('', xy=(2.5, y_main), xytext=(1.8, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    # Photodiode
    ax.text(3.8, y_main, 'Photodiode', ha='center', va='center',
            fontsize=11, bbox=component_style)

    # Arrow
    ax.annotate('', xy=(5.8, y_main), xytext=(5.1, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(5.45, y_main + 0.4, 'current', ha='center', fontsize=9, style='italic')

    # Transimpedance Amplifier
    ax.text(7.5, y_main, 'Transimpedance\nAmplifier', ha='center', va='center',
            fontsize=11, bbox=component_style)

    # Arrow
    ax.annotate('', xy=(10, y_main), xytext=(9.2, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(9.6, y_main + 0.4, 'voltage', ha='center', fontsize=9, style='italic')

    # Output
    ax.text(11.5, y_main, 'Output\nVoltage', ha='center', va='center',
            fontsize=11, bbox=output_style)

    # Arrow to DAQ
    ax.annotate('', xy=(13, y_main), xytext=(12.5, y_main),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(13.3, y_main, '→ DAQ', ha='left', va='center', fontsize=10)

    # === Noise Sources ===

    # Shot noise (at photodiode)
    ax.text(3.8, 1.8, 'Shot Noise', ha='center', va='center',
            fontsize=10, bbox=noise_style)
    ax.annotate('', xy=(3.8, 3.3), xytext=(3.8, 2.3),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5,
                               connectionstyle='arc3,rad=0'))
    ax.text(3.8, 1.0, '√(signal)', ha='center', fontsize=9, color='darkred')
    ax.text(3.8, 0.5, 'Quantum limit', ha='center', fontsize=8,
            style='italic', color='gray')

    # Johnson noise (at amplifier resistors)
    ax.text(6.2, 1.8, 'Johnson\nNoise', ha='center', va='center',
            fontsize=10, bbox=noise_style)
    ax.annotate('', xy=(6.8, 3.3), xytext=(6.2, 2.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5,
                               connectionstyle='arc3,rad=0.2'))
    ax.text(6.2, 0.7, '√(T × R)', ha='center', fontsize=9, color='darkred')
    ax.text(6.2, 0.2, 'Thermal', ha='center', fontsize=8,
            style='italic', color='gray')

    # Amplifier noise
    ax.text(8.8, 1.8, 'Amplifier\nNoise', ha='center', va='center',
            fontsize=10, bbox=noise_style)
    ax.annotate('', xy=(8.2, 3.3), xytext=(8.8, 2.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5,
                               connectionstyle='arc3,rad=-0.2'))
    ax.text(8.8, 0.7, '"Noise (RMS)"', ha='center', fontsize=9, color='darkred')
    ax.text(8.8, 0.2, '250 µV – 1.1 mV', ha='center', fontsize=8,
            style='italic', color='gray')

    # Title
    ax.text(7, 6.3, 'Noise Sources in Photodetector Signal Chain',
            ha='center', va='center', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tuesday_06_noise_sources_block_diagram.png")
    plt.close()


# =============================================================================
# SAMPLING AND NYQUIST FIGURES
# =============================================================================

def sampling_2x():
    """Sampling at exactly 2x Nyquist (minimum)."""
    print("  Generating: thursday_01_sampling_2x.png")

    signal_freq = 1000  # 1 kHz
    sample_rate = 2000  # 2 kHz (exactly 2x)
    duration = 0.005    # 5 ms

    # True signal
    t_true = np.linspace(0, duration, 5000)
    signal_true = np.sin(2 * np.pi * signal_freq * t_true)

    # Sampled signal
    num_samples = int(sample_rate * duration)
    t_sampled = np.arange(num_samples) / sample_rate
    signal_sampled = np.sin(2 * np.pi * signal_freq * t_sampled)

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(t_true * 1000, signal_true, 'b-', linewidth=1, alpha=0.5,
            label='True signal (1 kHz)')
    ax.plot(t_sampled * 1000, signal_sampled, 'ro-', markersize=10,
            linewidth=1, label=f'Sampled at {sample_rate} Hz')

    # Highlight one period (shifted so exactly 2 samples are clearly inside)
    ax.axvspan(0.25, 1.25, alpha=0.35, color='gold', label='One period')

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Sampling a {signal_freq} Hz signal at {sample_rate} Hz\n'
                 f'Only 2 samples per period!')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    ax.set_ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_01_sampling_2x.png")
    plt.close()


def sampling_comparison():
    """Compare sampling at different rates."""
    print("  Generating: thursday_02_sampling_comparison.png")

    signal_freq = 1000  # 1 kHz
    duration = 0.005    # 5 ms

    # True signal
    t_true = np.linspace(0, duration, 5000)
    signal_true = np.sin(2 * np.pi * signal_freq * t_true)

    sample_rates = [2000, 2500, 4000, 5000, 10000, 20000]
    titles = ['2× (Nyquist limit)', '2.5×', '4×', '5×', '10×', '20×']
    # Color code: red/orange for marginal, green for good
    title_colors = ['red', 'orange', 'green', 'green', 'green', 'green']

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    for ax, rate, title, color in zip(axes.flat, sample_rates, titles, title_colors):
        num_samples = int(rate * duration)
        t_sampled = np.arange(num_samples) / rate
        signal_sampled = np.sin(2 * np.pi * signal_freq * t_sampled)

        ax.plot(t_true * 1000, signal_true, 'b-', linewidth=2.5, alpha=0.4)
        ax.plot(t_sampled * 1000, signal_sampled, 'ro-', markersize=10, linewidth=1.5)

        ax.set_xlabel('Time (ms)', fontsize=20)
        ax.set_ylabel('Amplitude', fontsize=20)
        ax.set_title(f'{title}\n({rate} Hz)', color=color,
                     fontweight='bold', fontsize=22)
        ax.tick_params(axis='both', labelsize=16)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 5)
        ax.set_ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_02_sampling_comparison.png")
    plt.close()


def nyquist_diagram():
    """Nyquist frequency diagram."""
    print("  Generating: thursday_03_nyquist_diagram.png")

    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=(12, 5))

    sample_rate = 10000  # 10 kHz
    nyquist = sample_rate / 2

    # Draw regions
    valid = Rectangle((0, 0.2), nyquist, 0.6, facecolor='lightgreen',
                       edgecolor='green', linewidth=3, alpha=0.8)
    alias = Rectangle((nyquist, 0.2), nyquist, 0.6, facecolor='lightcoral',
                       edgecolor='red', linewidth=3, alpha=0.8)
    ax.add_patch(valid)
    ax.add_patch(alias)

    # Labels for regions
    ax.text(nyquist/2, 0.5, 'VALID REGION\n\nSignals measured\ncorrectly',
            ha='center', va='center', fontsize=13, fontweight='bold',
            color='darkgreen')
    ax.text(nyquist * 1.5, 0.5, 'ALIASING REGION\n\nSignals appear at\nwrong frequencies!',
            ha='center', va='center', fontsize=13, fontweight='bold',
            color='darkred')

    # Frequency markers
    ax.axvline(x=0, color='black', linewidth=2)
    ax.axvline(x=nyquist, color='red', linewidth=4, linestyle='--')
    ax.axvline(x=sample_rate, color='blue', linewidth=2)

    # Labels below axis (offset from lines to avoid overlap)
    ax.text(100, 0.1, '0 Hz\n(DC)', ha='left', fontsize=12, va='top')
    ax.text(nyquist + 300, 0.1, f'{int(nyquist/1000)} kHz\nNyquist\nFrequency',
            ha='left', fontsize=12, color='red', fontweight='bold', va='top')
    ax.text(sample_rate - 300, 0.1, f'{int(sample_rate/1000)} kHz\nSample\nRate',
            ha='right', fontsize=12, color='blue', va='top')

    # Formula box
    ax.text(0.12, 0.95, r'$f_N = \frac{f_s}{2} = \frac{10000}{2} = 5000$ Hz',
            transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    ax.set_xlim(-500, sample_rate + 500)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel('Frequency (Hz)', fontsize=14)
    ax.set_title('Nyquist Frequency: The Boundary Between Valid Measurement and Aliasing',
                 fontsize=14)
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_03_nyquist_diagram.png")
    plt.close()


def aliasing_basic():
    """Basic aliasing demonstration - focused on the key insight."""
    print("  Generating: thursday_04_aliasing_basic.png")

    sample_rate = 1000  # 1 kHz
    duration = 0.015    # 15 ms (shorter for clarity)

    true_freq = 600     # Above Nyquist
    alias_freq = 400    # What the computer sees

    # True signal (high resolution)
    t_true = np.linspace(0, duration, 10000)

    # Sampling times
    num_samples = int(sample_rate * duration)
    t_sampled = np.arange(num_samples) / sample_rate

    # Signals
    signal_true = np.sin(2 * np.pi * true_freq * t_true)
    signal_sampled = np.sin(2 * np.pi * true_freq * t_sampled)
    # Alias has phase inversion: sin(2π×600×t) sampled at 1000 Hz = -sin(2π×400×t)
    signal_alias = -np.sin(2 * np.pi * alias_freq * t_true)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(f'Sample Rate = {sample_rate} Hz  (Nyquist = {sample_rate//2} Hz)',
                 fontsize=18, fontweight='bold', y=0.98)

    # Panel 1: The true 600 Hz signal with sample points
    ax = axes[0]
    ax.plot(t_true * 1000, signal_true, 'b-', linewidth=2.5, alpha=0.7,
            label=f'True: {true_freq} Hz')
    ax.plot(t_sampled * 1000, signal_sampled, 'ro', markersize=12, zorder=5,
            label='Samples')
    ax.set_xlabel('Time (ms)', fontsize=16)
    ax.set_ylabel('Amplitude', fontsize=16)
    ax.set_title(f'Reality:\n{true_freq} Hz signal', fontsize=18, fontweight='bold')
    ax.legend(loc='upper right', fontsize=12)
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 15)
    ax.set_ylim(-1.5, 1.5)

    # Panel 2: Just the sample points (what the computer has)
    ax = axes[1]
    ax.plot(t_sampled * 1000, signal_sampled, 'ro', markersize=12)
    ax.set_xlabel('Time (ms)', fontsize=16)
    ax.set_ylabel('Amplitude', fontsize=16)
    ax.set_title('What the computer\nactually records', fontsize=18, fontweight='bold')
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 15)
    ax.set_ylim(-1.5, 1.5)
    ax.text(7.5, -1.2, 'Just 15 numbers!', ha='center', fontsize=14,
            style='italic', color='darkred')

    # Panel 3: The aliased interpretation
    ax = axes[2]
    ax.plot(t_true * 1000, signal_alias, 'g-', linewidth=3, alpha=0.8,
            label=f'Reconstructed: {alias_freq} Hz')
    ax.plot(t_sampled * 1000, signal_sampled, 'ro', markersize=12, zorder=5,
            label='Same samples!')
    ax.set_xlabel('Time (ms)', fontsize=16)
    ax.set_ylabel('Amplitude', fontsize=16)
    ax.set_title(f'What the computer\n"sees": {alias_freq} Hz', fontsize=18,
                 fontweight='bold', color='darkgreen')
    ax.legend(loc='upper right', fontsize=12)
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 15)
    ax.set_ylim(-1.5, 1.5)

    # Add arrows between panels
    fig.text(0.355, 0.5, '→', fontsize=40, ha='center', va='center',
             fontweight='bold', color='gray')
    fig.text(0.645, 0.5, '→', fontsize=40, ha='center', va='center',
             fontweight='bold', color='gray')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_04_aliasing_basic.png")
    plt.close()


def aliasing_900Hz():
    """Classic 900 Hz aliased to 100 Hz example."""
    print("  Generating: thursday_06_aliasing_900Hz.png")

    sample_rate = 1000
    signal_freq = 900
    alias_freq = 100
    duration = 0.02  # 20 ms

    t_true = np.linspace(0, duration, 10000)
    t_sampled = np.arange(int(sample_rate * duration)) / sample_rate

    signal_true = np.sin(2 * np.pi * signal_freq * t_true)
    signal_sampled = np.sin(2 * np.pi * signal_freq * t_sampled)
    # Alias has phase inversion: sin(2π×900×t) sampled at 1000 Hz = -sin(2π×100×t)
    signal_alias = -np.sin(2 * np.pi * alias_freq * t_true)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(t_true * 1000, signal_true, 'b-', alpha=0.4, linewidth=1,
            label=f'True signal: {signal_freq} Hz')
    ax.plot(t_true * 1000, signal_alias, 'g--', linewidth=2,
            label=f'Aliased signal: {alias_freq} Hz')
    ax.plot(t_sampled * 1000, signal_sampled, 'ro', markersize=10,
            label='Sampled points', zorder=5)

    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Amplitude', fontsize=12)
    ax.set_title(f'Aliasing Example: {signal_freq} Hz Signal Sampled at {sample_rate} Hz\n'
                 f'The samples fit BOTH curves! Computer sees {alias_freq} Hz.',
                 fontsize=13)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 20)
    ax.set_ylim(-1.5, 1.5)

    # Add annotation
    ax.annotate('Same points!', xy=(5, 0.8), fontsize=12,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "thursday_06_aliasing_900Hz.png")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate all lecture figures for Week 2 Tuesday."""
    print("\n" + "=" * 60)
    print("Generating Week 2 Tuesday Lecture Figures")
    print("=" * 60)
    print(f"\nOutput directory: {FIGURES_DIR}\n")

    # DAQ diagrams
    print("--- DAQ Diagrams ---")
    single_ended_vs_differential()
    noise_sources_block_diagram()

    # Sampling and Nyquist figures
    print("\n--- Sampling and Nyquist ---")
    sampling_2x()
    sampling_comparison()
    nyquist_diagram()
    aliasing_basic()
    aliasing_900Hz()

    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print("=" * 60)

    # List generated files
    print("\nGenerated files:")
    for f in sorted(FIGURES_DIR.glob("*.png")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
