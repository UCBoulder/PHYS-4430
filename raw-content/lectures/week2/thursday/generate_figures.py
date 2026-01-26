"""
Generate Lecture Figures - Week 2 Thursday
==========================================

PHYS 4430 Week 2 Thursday Lecture

This script generates all figures for the Week 2 Thursday lecture slides
(Digital Sampling, Nyquist, Aliasing, FFT).

Usage:
    python generate_figures.py

All figures will be saved to the figures/ subdirectory.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Output directory
SCRIPT_DIR = Path(__file__).parent
FIGURES_DIR = SCRIPT_DIR / "figures"

# Create directory if it doesn't exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Aliases for compatibility with existing function code
THURSDAY_DIR = FIGURES_DIR

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
# TUESDAY LECTURE FIGURES
# =============================================================================

def tuesday_01_basic_plot():
    """Generate basic matplotlib plot example."""
    print("  Generating: tuesday_01_basic_plot.png")

    # Generate data
    t = np.linspace(0, 0.1, 1000)  # 100 ms
    frequency = 50  # Hz
    signal = np.sin(2 * np.pi * frequency * t)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t * 1000, signal, 'b-', linewidth=1.5)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('50 Hz Sine Wave')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.3, 1.3)

    # Add annotations showing key plot elements
    ax.annotate('plt.xlabel()', xy=(50, -1.05), fontsize=10, color='green',
                ha='center')
    ax.annotate('plt.ylabel()', xy=(-8, 0), fontsize=10, color='green',
                ha='center', rotation=90)
    ax.annotate('plt.title()', xy=(50, 1.15), fontsize=10, color='green',
                ha='center')

    plt.tight_layout()
    plt.savefig(TUESDAY_DIR / "tuesday_01_basic_plot.png")
    plt.close()


def tuesday_02_multiple_lines():
    """Generate multiple lines plot example."""
    print("  Generating: tuesday_02_multiple_lines.png")

    t = np.linspace(0, 0.05, 1000)  # 50 ms
    signal1 = np.sin(2 * np.pi * 100 * t)
    signal2 = 0.7 * np.sin(2 * np.pi * 200 * t)
    signal3 = signal1 + signal2

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t * 1000, signal1, 'b-', linewidth=1.5, label='100 Hz')
    ax.plot(t * 1000, signal2, 'r--', linewidth=1.5, label='200 Hz')
    ax.plot(t * 1000, signal3, 'g-', linewidth=2, label='Sum')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('Multiple Signals with Legend')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 50)

    plt.tight_layout()
    plt.savefig(TUESDAY_DIR / "tuesday_02_multiple_lines.png")
    plt.close()


def tuesday_03_scatter_with_fit():
    """Generate scatter plot with fit (beam profile example)."""
    print("  Generating: tuesday_03_scatter_with_fit.png")

    # Simulated beam profile data
    np.random.seed(42)
    positions = np.linspace(0, 10, 50)  # mm
    w = 2.0  # beam width
    x0 = 5.0  # center
    intensity_true = np.exp(-2 * (positions - x0)**2 / w**2)
    intensity_noisy = intensity_true + 0.05 * np.random.randn(len(positions))

    # Fine grid for fit line
    pos_fine = np.linspace(0, 10, 200)
    intensity_fit = np.exp(-2 * (pos_fine - x0)**2 / w**2)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(positions, intensity_noisy, c='blue', s=40, alpha=0.7,
               label='Data points', zorder=3)
    ax.plot(pos_fine, intensity_fit, 'r-', linewidth=2, label='Gaussian fit')
    ax.axvline(x=x0, color='gray', linestyle='--', alpha=0.5, label=f'Center = {x0} mm')
    ax.set_xlabel('Position (mm)')
    ax.set_ylabel('Intensity (a.u.)')
    ax.set_title('Beam Profile Measurement')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(TUESDAY_DIR / "tuesday_03_scatter_with_fit.png")
    plt.close()


def tuesday_04_line_styles():
    """Generate line styles reference."""
    print("  Generating: tuesday_04_line_styles.png")

    t = np.linspace(0, 1, 100)

    fig, ax = plt.subplots(figsize=(10, 6))

    styles = [
        ("'b-'", 'b-', "Blue solid"),
        ("'r--'", 'r--', "Red dashed"),
        ("'g:'", 'g:', "Green dotted"),
        ("'ko'", 'ko', "Black circles"),
        ("'m^-'", 'm^-', "Magenta triangles"),
        ("'c.-'", 'c.-', "Cyan dots+line"),
    ]

    for i, (code, style, desc) in enumerate(styles):
        y = 5 - i + 0.3 * np.sin(2 * np.pi * 3 * t)
        ax.plot(t, y, style, markersize=6, linewidth=2,
                label=f"{code} - {desc}")

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Matplotlib Line and Marker Styles')
    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, 6)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(TUESDAY_DIR / "tuesday_04_line_styles.png")
    plt.close()


def tuesday_05_single_ended_vs_differential():
    """Generate single-ended vs differential wiring diagram."""
    print("  Generating: tuesday_05_single_ended_vs_differential.png")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Common styling
    box_style = dict(boxstyle='round,pad=0.3', facecolor='lightblue',
                     edgecolor='black', linewidth=2)
    daq_style = dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
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
    plt.savefig(TUESDAY_DIR / "tuesday_05_single_ended_vs_differential.png")
    plt.close()


def tuesday_06_noise_sources_block_diagram():
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
    ax.text(8.8, 0.7, 'From datasheet', ha='center', fontsize=9, color='darkred')
    ax.text(8.8, 0.2, 'Gain-dependent', ha='center', fontsize=8,
            style='italic', color='gray')

    # Title
    ax.text(7, 6.3, 'Noise Sources in Photodetector Signal Chain',
            ha='center', va='center', fontsize=14, fontweight='bold')

    # Legend box
    ax.add_patch(plt.Rectangle((0.3, 5.3), 3.2, 1.2, facecolor='white',
                                edgecolor='gray', linewidth=1, alpha=0.9))
    ax.text(0.5, 6.2, 'Signal path', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightblue', edgecolor='none'))
    ax.text(0.5, 5.6, 'Noise source', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='mistyrose', edgecolor='none'))

    plt.tight_layout()
    plt.savefig(TUESDAY_DIR / "tuesday_06_noise_sources_block_diagram.png")
    plt.close()


# =============================================================================
# THURSDAY LECTURE FIGURES - SAMPLING
# =============================================================================

def thursday_01_sampling_2x():
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

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(t_true * 1000, signal_true, 'b-', linewidth=1, alpha=0.5,
            label='True signal (1 kHz)')
    ax.plot(t_sampled * 1000, signal_sampled, 'ro-', markersize=10,
            linewidth=1, label=f'Sampled at {sample_rate} Hz')

    # Highlight one period
    ax.axvspan(0, 1, alpha=0.15, color='yellow', label='One period')

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Sampling at 2× Nyquist: {signal_freq} Hz signal, {sample_rate} Hz sample rate\n'
                 f'Only 2 samples per period!')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    ax.set_ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_01_sampling_2x.png")
    plt.close()


def thursday_02_sampling_comparison():
    """Compare sampling at different rates."""
    print("  Generating: thursday_02_sampling_comparison.png")

    signal_freq = 1000  # 1 kHz
    duration = 0.005    # 5 ms

    # True signal
    t_true = np.linspace(0, duration, 5000)
    signal_true = np.sin(2 * np.pi * signal_freq * t_true)

    sample_rates = [2000, 2500, 4000, 5000, 10000, 20000]
    titles = ['2× (Nyquist limit)', '2.5×', '4×', '5×', '10×', '20×']

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle(f'Sampling a {signal_freq} Hz Signal at Different Rates', fontsize=16)

    for ax, rate, title in zip(axes.flat, sample_rates, titles):
        num_samples = int(rate * duration)
        t_sampled = np.arange(num_samples) / rate
        signal_sampled = np.sin(2 * np.pi * signal_freq * t_sampled)

        ax.plot(t_true * 1000, signal_true, 'b-', linewidth=1, alpha=0.4)
        ax.plot(t_sampled * 1000, signal_sampled, 'ro-', markersize=5, linewidth=0.5)

        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'{title}\n({rate} Hz, {num_samples} samples)')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 5)
        ax.set_ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_02_sampling_comparison.png")
    plt.close()


def thursday_03_nyquist_diagram():
    """Nyquist frequency diagram."""
    print("  Generating: thursday_03_nyquist_diagram.png")

    from matplotlib.patches import Rectangle, FancyArrowPatch

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

    # Labels below axis
    ax.text(0, 0.05, '0 Hz\n(DC)', ha='center', fontsize=12)
    ax.text(nyquist, 0.05, f'{int(nyquist/1000)} kHz\nNyquist\nFrequency',
            ha='center', fontsize=12, color='red', fontweight='bold')
    ax.text(sample_rate, 0.05, f'{int(sample_rate/1000)} kHz\nSample\nRate',
            ha='center', fontsize=12, color='blue')

    # Formula box
    ax.text(0.02, 0.95, r'$f_{Nyquist} = \frac{f_{sample}}{2} = \frac{10000}{2} = 5000$ Hz',
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
    plt.savefig(THURSDAY_DIR / "thursday_03_nyquist_diagram.png")
    plt.close()


def thursday_04_aliasing_basic():
    """Basic aliasing demonstration."""
    print("  Generating: thursday_04_aliasing_basic.png")

    sample_rate = 1000  # 1 kHz
    duration = 0.02     # 20 ms

    # True signal (high resolution)
    t_true = np.linspace(0, duration, 10000)

    # Sampling times
    num_samples = int(sample_rate * duration)
    t_sampled = np.arange(num_samples) / sample_rate

    # Two cases: below and above Nyquist
    cases = [
        (400, "400 Hz (Below Nyquist = 500 Hz)", "Measured correctly"),
        (600, "600 Hz (Above Nyquist!)", "Aliases to 400 Hz"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, (freq, title, note) in zip(axes, cases):
        # True signal
        signal_true = np.sin(2 * np.pi * freq * t_true)

        # Sampled signal
        signal_sampled = np.sin(2 * np.pi * freq * t_sampled)

        # Alias frequency
        alias_freq = abs(freq - sample_rate) if freq > sample_rate/2 else freq
        signal_alias = np.sin(2 * np.pi * alias_freq * t_true)

        ax.plot(t_true * 1000, signal_true, 'b-', alpha=0.4, linewidth=1,
                label=f'True signal ({freq} Hz)')
        ax.plot(t_sampled * 1000, signal_sampled, 'ro', markersize=8,
                label='Sampled points')

        if freq > sample_rate / 2:
            ax.plot(t_true * 1000, signal_alias, 'g--', linewidth=2,
                    label=f'Aliased signal ({alias_freq} Hz)')

        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'{title}\n{note}')
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 20)
        ax.set_ylim(-1.5, 1.5)

    plt.suptitle(f'Aliasing: Sample Rate = {sample_rate} Hz, Nyquist = {sample_rate//2} Hz',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_04_aliasing_basic.png")
    plt.close()


def thursday_05_aliasing_near_sample_rate():
    """Aliasing when signal is near sample rate."""
    print("  Generating: thursday_05_aliasing_near_sample_rate.png")

    sample_rate = 1000  # 1 kHz
    duration = 0.5      # 500 ms to show slow beating

    t_sampled = np.arange(int(sample_rate * duration)) / sample_rate

    cases = [
        (998, 2),    # 998 Hz aliases to 2 Hz
        (1000, 0),   # 1000 Hz aliases to DC
        (1002, 2),   # 1002 Hz aliases to 2 Hz
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    for ax, (freq, alias) in zip(axes, cases):
        signal_sampled = np.sin(2 * np.pi * freq * t_sampled)

        ax.plot(t_sampled * 1000, signal_sampled, 'r.-', markersize=2, linewidth=0.5)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'Signal: {freq} Hz\nAppears as: {alias} Hz')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 500)
        ax.set_ylim(-1.5, 1.5)

    plt.suptitle(f'Aliasing Near Sample Rate ({sample_rate} Hz) - "Beating" Effect',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_05_aliasing_near_sample_rate.png")
    plt.close()


def thursday_06_aliasing_900Hz():
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
    signal_alias = np.sin(2 * np.pi * alias_freq * t_true)

    fig, ax = plt.subplots(figsize=(12, 6))

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
    plt.savefig(THURSDAY_DIR / "thursday_06_aliasing_900Hz.png")
    plt.close()


def thursday_07_wagon_wheel():
    """Wagon wheel effect illustration."""
    print("  Generating: thursday_07_wagon_wheel.png")

    sample_rate = 24  # fps (movie frame rate)
    duration = 1.0    # 1 second

    t_sampled = np.arange(int(sample_rate * duration)) / sample_rate

    rotation_rates = [10, 12, 14, 24]
    apparent = [10, 0, -10, 0]  # Apparent rotation

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Wagon Wheel Effect: Movie Camera at 24 fps (Nyquist = 12 Hz)',
                 fontsize=14)

    for ax, rate, app in zip(axes.flat, rotation_rates, apparent):
        # Spoke angle over time
        theta = 2 * np.pi * rate * t_sampled
        spoke_pos = np.cos(theta)

        ax.plot(t_sampled * 1000, spoke_pos, 'b.-', markersize=8, linewidth=1)

        if app > 0:
            direction = f"{app} rot/s forward"
        elif app < 0:
            direction = f"{abs(app)} rot/s BACKWARD"
        else:
            direction = "STATIONARY"

        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Spoke Position')
        ax.set_title(f'Wheel: {rate} rot/s\nAppears: {direction}')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 500)
        ax.set_ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_07_wagon_wheel.png")
    plt.close()


def thursday_08_anti_alias_filter():
    """Anti-aliasing filter concept."""
    print("  Generating: thursday_08_anti_alias_filter.png")

    sample_rate = 1000
    duration = 0.05  # 50 ms

    t_true = np.linspace(0, duration, 5000)
    t_sampled = np.arange(int(sample_rate * duration)) / sample_rate

    # Signal with low and high frequency components
    signal_low = np.sin(2 * np.pi * 100 * t_true)  # 100 Hz - OK
    signal_high = 0.5 * np.sin(2 * np.pi * 800 * t_true)  # 800 Hz - will alias
    signal_total = signal_low + signal_high

    # Sampled versions
    sampled_unfiltered = (np.sin(2 * np.pi * 100 * t_sampled) +
                          0.5 * np.sin(2 * np.pi * 800 * t_sampled))
    sampled_filtered = np.sin(2 * np.pi * 100 * t_sampled)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Without filter
    ax = axes[0]
    ax.plot(t_true * 1000, signal_total, 'b-', alpha=0.4, linewidth=1,
            label='True: 100 Hz + 800 Hz')
    ax.plot(t_sampled * 1000, sampled_unfiltered, 'ro-', markersize=5,
            label='Sampled (aliased!)')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Amplitude')
    ax.set_title('WITHOUT Anti-Alias Filter\n800 Hz aliases to 200 Hz - Corrupted!')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 30)
    ax.set_ylim(-2, 2)

    # With filter
    ax = axes[1]
    ax.plot(t_true * 1000, signal_low, 'b-', alpha=0.4, linewidth=1,
            label='Filtered: 100 Hz only')
    ax.plot(t_sampled * 1000, sampled_filtered, 'go-', markersize=5,
            label='Sampled (clean!)')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Amplitude')
    ax.set_title('WITH Anti-Alias Filter\nHigh frequencies removed before sampling')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 30)
    ax.set_ylim(-2, 2)

    plt.suptitle('Anti-Aliasing Filter: Remove High Frequencies BEFORE Sampling',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_08_anti_alias_filter.png")
    plt.close()


# =============================================================================
# THURSDAY LECTURE FIGURES - FFT
# =============================================================================

def thursday_09_fft_single_freq():
    """FFT of single frequency sine wave."""
    print("  Generating: thursday_09_fft_single_freq.png")

    sample_rate = 1000
    duration = 1.0
    signal_freq = 50

    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate
    signal = np.sin(2 * np.pi * signal_freq * t)

    # FFT
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(n_samples, 1/sample_rate)
    n_pos = n_samples // 2
    freq_pos = frequencies[:n_pos]
    magnitude = np.abs(fft_result[:n_pos]) * 2 / n_samples

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Time domain
    ax1.plot(t * 1000, signal, 'b-', linewidth=0.8)
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title(f'Time Domain: {signal_freq} Hz Sine Wave')
    ax1.set_xlim(0, 100)
    ax1.grid(True, alpha=0.3)

    # Frequency domain
    ax2.plot(freq_pos, magnitude, 'r-', linewidth=1.5)
    ax2.axvline(x=signal_freq, color='green', linestyle='--', linewidth=2,
                label=f'Signal: {signal_freq} Hz')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Frequency Domain: Single Peak at Signal Frequency')
    ax2.set_xlim(0, 150)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_09_fft_single_freq.png")
    plt.close()


def thursday_10_fft_multiple_freq():
    """FFT of multiple frequency components."""
    print("  Generating: thursday_10_fft_multiple_freq.png")

    sample_rate = 1000
    duration = 1.0

    freqs = [50, 120, 200]
    amps = [1.0, 0.5, 0.3]

    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    signal = np.zeros(n_samples)
    for freq, amp in zip(freqs, amps):
        signal += amp * np.sin(2 * np.pi * freq * t)

    # FFT
    fft_result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(n_samples, 1/sample_rate)
    n_pos = n_samples // 2
    freq_pos = frequencies[:n_pos]
    magnitude = np.abs(fft_result[:n_pos]) * 2 / n_samples

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Time domain
    ax1.plot(t * 1000, signal, 'b-', linewidth=0.5)
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Time Domain: Complex Signal (Hard to Analyze!)')
    ax1.set_xlim(0, 100)
    ax1.grid(True, alpha=0.3)

    # Frequency domain
    ax2.plot(freq_pos, magnitude, 'r-', linewidth=1.5)
    for freq, amp in zip(freqs, amps):
        ax2.annotate(f'{freq} Hz\n(amp={amp})', xy=(freq, amp),
                     xytext=(freq+15, amp+0.1), fontsize=10,
                     arrowprops=dict(arrowstyle='->', color='green'))
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Frequency Domain: Three Distinct Peaks!')
    ax2.set_xlim(0, 300)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_10_fft_multiple_freq.png")
    plt.close()


def thursday_11_fft_noisy():
    """FFT finding signal in noise."""
    print("  Generating: thursday_11_fft_noisy.png")

    np.random.seed(123)

    sample_rate = 1000
    duration = 2.0
    signal_freq = 75

    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    clean_signal = np.sin(2 * np.pi * signal_freq * t)
    noise = 1.5 * np.random.randn(n_samples)
    noisy_signal = clean_signal + noise

    # FFT
    fft_result = np.fft.fft(noisy_signal)
    frequencies = np.fft.fftfreq(n_samples, 1/sample_rate)
    n_pos = n_samples // 2
    freq_pos = frequencies[:n_pos]
    magnitude = np.abs(fft_result[:n_pos]) * 2 / n_samples

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))

    # Clean signal
    axes[0, 0].plot(t * 1000, clean_signal, 'b-', linewidth=0.5)
    axes[0, 0].set_xlabel('Time (ms)')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].set_title(f'Clean Signal: {signal_freq} Hz')
    axes[0, 0].set_xlim(0, 100)
    axes[0, 0].grid(True, alpha=0.3)

    # Noisy signal
    axes[0, 1].plot(t * 1000, noisy_signal, 'r-', linewidth=0.3)
    axes[0, 1].set_xlabel('Time (ms)')
    axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].set_title('Noisy Signal (Signal Nearly Invisible!)')
    axes[0, 1].set_xlim(0, 100)
    axes[0, 1].grid(True, alpha=0.3)

    # FFT full range
    axes[1, 0].plot(freq_pos, magnitude, 'g-', linewidth=1)
    axes[1, 0].axvline(x=signal_freq, color='red', linestyle='--', linewidth=2)
    axes[1, 0].set_xlabel('Frequency (Hz)')
    axes[1, 0].set_ylabel('Magnitude')
    axes[1, 0].set_title('FFT: Signal Peak Visible Above Noise!')
    axes[1, 0].set_xlim(0, 200)
    axes[1, 0].grid(True, alpha=0.3)

    # FFT zoomed
    axes[1, 1].plot(freq_pos, magnitude, 'g-', linewidth=1.5)
    axes[1, 1].axvline(x=signal_freq, color='red', linestyle='--', linewidth=2,
                        label=f'{signal_freq} Hz')
    axes[1, 1].set_xlabel('Frequency (Hz)')
    axes[1, 1].set_ylabel('Magnitude')
    axes[1, 1].set_title('FFT Zoomed: Clear Peak at 75 Hz')
    axes[1, 1].set_xlim(50, 100)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle('FFT Finds Signals Hidden in Noise!', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_11_fft_noisy.png")
    plt.close()


def thursday_12_frequency_resolution():
    """Frequency resolution vs measurement duration."""
    print("  Generating: thursday_12_frequency_resolution.png")

    sample_rate = 1000
    signal_freq = 100

    durations = [0.1, 0.5, 1.0, 2.0]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Frequency Resolution: Longer Measurement = Sharper Peak', fontsize=14)

    for ax, duration in zip(axes.flat, durations):
        n_samples = int(sample_rate * duration)
        freq_resolution = sample_rate / n_samples

        t = np.arange(n_samples) / sample_rate
        signal = np.sin(2 * np.pi * signal_freq * t)

        # FFT
        fft_result = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(n_samples, 1/sample_rate)
        n_pos = n_samples // 2
        freq_pos = frequencies[:n_pos]
        magnitude = np.abs(fft_result[:n_pos]) * 2 / n_samples

        ax.plot(freq_pos, magnitude, 'b-', linewidth=1.5)
        ax.axvline(x=signal_freq, color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude')
        ax.set_title(f'T = {duration} s\nΔf = {freq_resolution:.1f} Hz')
        ax.set_xlim(80, 120)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_12_frequency_resolution.png")
    plt.close()


def thursday_13_waveform_spectra():
    """FFT of different waveform types."""
    print("  Generating: thursday_13_waveform_spectra.png")

    sample_rate = 10000
    duration = 0.1
    fundamental = 100

    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    # Different waveforms
    sine = np.sin(2 * np.pi * fundamental * t)
    square = np.sign(np.sin(2 * np.pi * fundamental * t))
    triangle = 2 * np.abs(2 * (t * fundamental - np.floor(t * fundamental + 0.5))) - 1
    sawtooth = 2 * (t * fundamental - np.floor(t * fundamental + 0.5))

    waveforms = [
        ('Sine Wave', sine),
        ('Square Wave', square),
        ('Triangle Wave', triangle),
        ('Sawtooth Wave', sawtooth),
    ]

    fig, axes = plt.subplots(4, 2, figsize=(14, 14))
    fig.suptitle(f'FFT of Different Waveforms (Fundamental = {fundamental} Hz)', fontsize=14)

    for i, (name, signal) in enumerate(waveforms):
        # Time domain
        axes[i, 0].plot(t * 1000, signal, 'b-', linewidth=1)
        axes[i, 0].set_xlabel('Time (ms)')
        axes[i, 0].set_ylabel('Amplitude')
        axes[i, 0].set_title(f'{name} - Time Domain')
        axes[i, 0].set_xlim(0, 30)
        axes[i, 0].grid(True, alpha=0.3)

        # FFT
        fft_result = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(n_samples, 1/sample_rate)
        n_pos = n_samples // 2
        freq_pos = frequencies[:n_pos]
        magnitude = np.abs(fft_result[:n_pos]) * 2 / n_samples

        axes[i, 1].plot(freq_pos, magnitude, 'r-', linewidth=1)
        axes[i, 1].set_xlabel('Frequency (Hz)')
        axes[i, 1].set_ylabel('Magnitude')
        axes[i, 1].set_title(f'{name} - Frequency Domain')
        axes[i, 1].set_xlim(0, 800)
        axes[i, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_13_waveform_spectra.png")
    plt.close()


def thursday_14_aliasing_table():
    """Visual aliasing reference table."""
    print("  Generating: thursday_14_aliasing_table.png")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Hide axes
    ax.axis('off')

    # Table data
    sample_rate = 1000
    data = [
        ['Signal Freq', 'Status', 'Appears As'],
        ['100 Hz', 'OK', '100 Hz'],
        ['400 Hz', 'OK', '400 Hz'],
        ['500 Hz', 'Nyquist limit', '500 Hz'],
        ['600 Hz', 'ALIASED', '400 Hz'],
        ['900 Hz', 'ALIASED', '100 Hz'],
        ['998 Hz', 'ALIASED', '2 Hz'],
        ['1000 Hz', 'ALIASED', '0 Hz (DC)'],
    ]

    # Create table
    table = ax.table(cellText=data,
                     loc='center',
                     cellLoc='center',
                     colWidths=[0.3, 0.35, 0.3])

    # Style header row
    for j in range(3):
        table[(0, j)].set_facecolor('#4472C4')
        table[(0, j)].set_text_props(color='white', fontweight='bold')

    # Style OK rows (green)
    for i in [1, 2]:
        for j in range(3):
            table[(i, j)].set_facecolor('#C6EFCE')

    # Style Nyquist row (yellow)
    for j in range(3):
        table[(3, j)].set_facecolor('#FFEB9C')

    # Style aliased rows (red)
    for i in [4, 5, 6, 7]:
        for j in range(3):
            table[(i, j)].set_facecolor('#FFC7CE')

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2)

    ax.set_title(f'Aliasing Reference Table\nSample Rate = {sample_rate} Hz, '
                 f'Nyquist = {sample_rate//2} Hz', fontsize=14, pad=20)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_14_aliasing_table.png")
    plt.close()


# =============================================================================
# THURSDAY LECTURE FIGURES - GAUSSIAN BEAMS
# =============================================================================

def thursday_gaussian_beam_diagram():
    """Generate Gaussian beam propagation diagram showing key parameters."""
    print("  Generating: thursday_gaussian_beam_diagram.png")

    # Enable LaTeX rendering for better equation display
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'serif'

    fig, ax = plt.subplots(figsize=(14, 7))

    # Parameters (normalized units for clarity)
    w0 = 1.0  # beam waist
    z_R = 3.0  # Rayleigh range
    lambda_eff = np.pi * w0**2 / z_R  # effective wavelength

    # z positions
    z = np.linspace(-8, 8, 500)

    # Beam width function: w(z) = w0 * sqrt(1 + (z/z_R)^2)
    def w(z_val):
        return w0 * np.sqrt(1 + (z_val / z_R)**2)

    # Upper and lower beam envelope
    w_z = w(z)
    ax.fill_between(z, -w_z, w_z, alpha=0.2, color='red', label='Beam intensity (1/e²)')

    # Beam envelope lines
    ax.plot(z, w_z, 'r-', linewidth=2)
    ax.plot(z, -w_z, 'r-', linewidth=2)

    # Asymptotic divergence lines (far field)
    theta = w0 / z_R  # divergence half-angle
    z_far = np.array([3, 8])
    ax.plot(z_far, theta * z_far, 'b--', linewidth=1.5, alpha=0.7)
    ax.plot(z_far, -theta * z_far, 'b--', linewidth=1.5, alpha=0.7)
    ax.plot(-z_far, theta * z_far, 'b--', linewidth=1.5, alpha=0.7)
    ax.plot(-z_far, -theta * z_far, 'b--', linewidth=1.5, alpha=0.7)

    # Beam axis (z-axis)
    ax.axhline(y=0, color='gray', linewidth=1, linestyle='-', alpha=0.5)
    ax.axvline(x=0, color='gray', linewidth=1, linestyle='--', alpha=0.5)

    # Mark beam waist w0
    ax.annotate('', xy=(0, w0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax.text(0.4, w0/2, r'$w_0$', fontsize=22, color='green', fontweight='bold')

    # Mark w(z) at z = z_R (√2 * w0)
    w_at_zR = w(z_R)
    ax.annotate('', xy=(z_R, w_at_zR), xytext=(z_R, 0),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
    ax.text(z_R + 0.3, w_at_zR/2, r'$w(z_R) = \sqrt{2}w_0$', fontsize=16, color='purple')

    # Mark Rayleigh range on z-axis
    ax.annotate('', xy=(z_R, -0.15), xytext=(0, -0.15),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
    ax.text(z_R/2, -0.5, r'$z_R$', fontsize=22, color='blue', ha='center', fontweight='bold')

    # Mark -z_R as well
    ax.annotate('', xy=(-z_R, -0.15), xytext=(0, -0.15),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
    ax.text(-z_R/2, -0.5, r'$z_R$', fontsize=22, color='blue', ha='center', fontweight='bold')

    # Mark divergence angle theta
    angle_z = 6
    angle_y = theta * angle_z
    ax.annotate('', xy=(angle_z, angle_y), xytext=(angle_z, 0),
                arrowprops=dict(arrowstyle='<->', color='darkblue', lw=1.5))
    ax.text(angle_z + 0.3, angle_y/2, r'$\theta$', fontsize=20, color='darkblue', fontweight='bold')

    # Add wavefront curvature indicators at positions that don't overlap annotations
    # Avoid: z=0 (waist marker), z=±3 (z_R markers), z=6 (theta annotation)
    # Wavefronts curve so center LEADS edges (convex in propagation direction)
    wavefront_positions = [-7.2, -5.2, -3.2, -1.2, 1.2, 3.2, 5.2, 7.2]
    for z_pos in wavefront_positions:
        w_pos = w(z_pos)
        y_wf = np.linspace(-w_pos * 0.85, w_pos * 0.85, 100)
        # Exaggerated curvature for visibility (more curved farther from waist)
        curvature = -0.08 * np.sign(z_pos) * y_wf**2
        ax.plot(z_pos + curvature, y_wf, color='gray', linewidth=1.2, alpha=0.5,
                linestyle='--')

    # Labels and annotations
    ax.set_xlabel('Propagation distance z', fontsize=18)
    ax.set_ylabel('Transverse position', fontsize=18)
    ax.set_title('Gaussian Beam Propagation', fontsize=22, fontweight='bold')

    # Key equations box (centered horizontally at top)
    eq_text = (r'$w(z) = w_0\sqrt{1 + \left(\frac{z}{z_R}\right)^2}$' + '\n' +
               r'$z_R = \frac{\pi w_0^2}{\lambda}$ (Rayleigh range)' + '\n' +
               r'$\theta = \frac{\lambda}{\pi w_0}$ (divergence)')
    ax.text(0.5, 0.94, eq_text, transform=ax.transAxes, fontsize=16,
            verticalalignment='top', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

    # Physical meaning box (centered horizontally at bottom)
    meaning_text = (r'Key Features:' + '\n'
                    r'$\bullet$ Waist $w_0$: minimum beam radius' + '\n'
                    r'$\bullet$ Rayleigh range $z_R$: distance to $\sqrt{2} \cdot w_0$' + '\n'
                    r'$\bullet$ Far field: beam expands linearly with angle $\theta$' + '\n'
                    r'$\bullet$ Wavefronts: flat at waist, curved elsewhere')
    ax.text(0.5, 0.06, meaning_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='bottom', horizontalalignment='center',
            multialignment='left',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal')

    # Remove y-axis numbers (not meaningful)
    ax.set_yticks([])

    # Custom x-axis labels
    ax.set_xticks([-z_R, 0, z_R])
    ax.set_xticklabels([r'$-z_R$', '0', r'$z_R$'], fontsize=18)

    plt.tight_layout()
    plt.savefig(THURSDAY_DIR / "thursday_gaussian_beam_diagram.png")
    plt.close()

    # Restore default settings so other figures aren't affected
    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = 'sans-serif'


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate all Thursday lecture figures."""
    print("\n" + "=" * 60)
    print("Generating Week 2 Thursday Lecture Figures")
    print("=" * 60)

    print(f"\nOutput directory: {FIGURES_DIR}")

    # Thursday figures - Sampling
    print("\n--- Digital Sampling ---")
    thursday_01_sampling_2x()
    thursday_02_sampling_comparison()
    thursday_03_nyquist_diagram()
    thursday_04_aliasing_basic()
    thursday_05_aliasing_near_sample_rate()
    thursday_06_aliasing_900Hz()
    thursday_07_wagon_wheel()
    thursday_08_anti_alias_filter()

    # Thursday figures - FFT
    print("\n--- FFT Introduction ---")
    thursday_09_fft_single_freq()
    thursday_10_fft_multiple_freq()
    thursday_11_fft_noisy()
    thursday_12_frequency_resolution()
    thursday_13_waveform_spectra()
    thursday_14_aliasing_table()

    # Thursday figures - Gaussian Beams
    print("\n--- Gaussian Beams ---")
    thursday_gaussian_beam_diagram()

    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print("=" * 60)

    # List generated files
    print("\nGenerated figures:")
    for f in sorted(FIGURES_DIR.glob("*.png")):
        print(f"  {f.name}")

    print(f"\nTotal: {len(list(FIGURES_DIR.glob('*.png')))} figures")


if __name__ == "__main__":
    main()
