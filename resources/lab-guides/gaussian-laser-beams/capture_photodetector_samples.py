"""
Capture photodetector voltage samples for Week 1 prelab exercise.

This script captures 200 voltage readings at 0.1-second intervals from a
PDA36A photodetector connected to a USB-6009 DAQ. The data is used in the
Week 1 prelab to compare uncertainty estimation methods.

Setup:
- PDA36A photodetector output -> USB-6009 AI0+
- PDA36A ground -> USB-6009 AI0-
- Laser beam on photodetector (nominally constant power)
- Let laser warm up for 5+ minutes before capturing

Usage:
    python capture_photodetector_samples.py
"""

import nidaqmx
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import signal

# Configuration
DAQ_CHANNEL = "Dev2/ai0"
NUM_SAMPLES = 200  # 5 minutes at 0.1s intervals
SAMPLE_INTERVAL = 0.1  # seconds between samples
OUTPUT_FILE = "photodetector_samples.csv"

def capture_samples(channel, num_samples, interval):
    """
    Capture voltage samples at fixed time intervals.

    Uses single-point reads at timed intervals rather than continuous
    acquisition to match the prelab description of "measurements taken
    at 0.1-second intervals."
    """
    samples = []

    print(f"Capturing {num_samples} samples at {interval}s intervals...")
    print(f"Total time: {num_samples * interval:.1f} seconds")
    print()

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(channel)

        start_time = time.time()
        for i in range(num_samples):
            # Wait until the next sample time
            target_time = start_time + i * interval
            while time.time() < target_time:
                time.sleep(0.001)  # Small sleep to avoid busy-waiting

            # Read single sample
            voltage = task.read()
            samples.append(voltage)

            # Progress indicator
            if (i + 1) % 20 == 0:
                print(f"  {i + 1}/{num_samples} samples captured...")

    return np.array(samples)

def plot_data(samples, interval):
    """
    Plot voltage samples over time, histogram, FFT analysis, and spectrogram.
    """
    time_points = np.arange(len(samples)) * interval
    mean = np.mean(samples)
    std = np.std(samples, ddof=1)

    # Compute FFT
    fft_vals = np.fft.rfft(samples - mean)  # Remove DC component
    fft_freq = np.fft.rfftfreq(len(samples), interval)
    fft_power = np.abs(fft_vals) ** 2

    # Find dominant frequency (excluding DC at index 0)
    dominant_idx = np.argmax(fft_power[1:]) + 1
    dominant_freq = fft_freq[dominant_idx]
    dominant_period = 1.0 / dominant_freq if dominant_freq > 0 else 0

    # Compute spectrogram
    # Use window size of ~60 seconds to see slow oscillations
    nperseg = min(600, len(samples) // 4)  # 60s window at 0.1s sampling
    noverlap = nperseg // 2
    f_spec, t_spec, Sxx = signal.spectrogram(samples - mean, fs=1/interval,
                                              nperseg=nperseg, noverlap=noverlap)

    _, ((ax1, ax2), (ax3, ax4), (ax5, ax_empty)) = plt.subplots(3, 2, figsize=(14, 14))

    # Time series plot
    ax1.plot(time_points, samples, 'b-', linewidth=0.8, alpha=0.7, label='Voltage samples')
    ax1.axhline(mean, color='r', linestyle='--', linewidth=1.5, label=f'Mean = {mean:.3f} V')
    ax1.axhline(mean + std, color='orange', linestyle=':', linewidth=1, label=f'±1σ = ±{std:.4f} V')
    ax1.axhline(mean - std, color='orange', linestyle=':', linewidth=1)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('Photodetector Voltage vs. Time')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Histogram
    ax2.hist(samples, bins=30, color='blue', alpha=0.7, edgecolor='black')
    ax2.axvline(mean, color='r', linestyle='--', linewidth=1.5, label=f'Mean = {mean:.3f} V')
    ax2.axvline(mean + std, color='orange', linestyle=':', linewidth=1, label='±1σ')
    ax2.axvline(mean - std, color='orange', linestyle=':', linewidth=1)
    ax2.set_xlabel('Voltage (V)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Voltage Samples')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    # FFT - Full spectrum
    ax3.semilogy(fft_freq[1:], fft_power[1:], 'b-', linewidth=1)
    ax3.axvline(dominant_freq, color='r', linestyle='--', linewidth=1.5,
                label=f'Peak: {dominant_freq:.4f} Hz\n(T = {dominant_period:.1f} s)')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Power')
    ax3.set_title('FFT Power Spectrum (Full)')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    # FFT - Zoomed to low frequencies (where oscillations are likely)
    max_freq_display = min(0.1, fft_freq[-1])  # Show up to 0.1 Hz (10 second periods)
    freq_mask = fft_freq <= max_freq_display
    ax4.plot(fft_freq[freq_mask], fft_power[freq_mask], 'b-', linewidth=1)
    if dominant_freq <= max_freq_display:
        ax4.axvline(dominant_freq, color='r', linestyle='--', linewidth=1.5,
                    label=f'Peak: {dominant_freq:.4f} Hz\n(T = {dominant_period:.1f} s)')
    ax4.set_xlabel('Frequency (Hz)')
    ax4.set_ylabel('Power')
    ax4.set_title('FFT Power Spectrum (Low Frequency Zoom)')
    ax4.grid(True, alpha=0.3)
    ax4.legend()

    # Spectrogram - shows frequency content evolution over time
    pcm = ax5.pcolormesh(t_spec, f_spec, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
    ax5.set_ylim([0, max_freq_display])  # Focus on low frequencies
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Frequency (Hz)')
    ax5.set_title('Spectrogram (Time-Frequency Analysis)')
    plt.colorbar(pcm, ax=ax5, label='Power (dB)')
    if dominant_freq <= max_freq_display:
        ax5.axhline(dominant_freq, color='r', linestyle='--', linewidth=1.5, alpha=0.7,
                    label=f'Dominant: {dominant_freq:.4f} Hz')
    ax5.legend()

    # Hide empty subplot
    ax_empty.axis('off')

    plt.tight_layout()
    plt.show()

    # Print FFT results
    print("=" * 60)
    print("FFT Analysis Results")
    print("=" * 60)
    print(f"Dominant frequency: {dominant_freq:.4f} Hz")
    print(f"Dominant period:    {dominant_period:.1f} seconds")
    print()

def main():
    print("=" * 60)
    print("Photodetector Sample Capture for Week 1 Prelab")
    print("=" * 60)
    print()
    print(f"DAQ Channel: {DAQ_CHANNEL}")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"Interval: {SAMPLE_INTERVAL}s")
    print()

    # Verify DAQ connection
    try:
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(DAQ_CHANNEL)
            test_voltage = task.read()
            print(f"DAQ connected. Current reading: {test_voltage:.3f} V")
    except Exception as e:
        print(f"Error connecting to DAQ: {e}")
        print("Check that the USB-6009 is connected and the channel is correct.")
        return

    print()
    input("Press Enter to start capture (ensure laser is on and stable)...")
    print()

    # Capture samples
    samples = capture_samples(DAQ_CHANNEL, NUM_SAMPLES, SAMPLE_INTERVAL)

    # Display statistics
    print()
    print("=" * 60)
    print("Capture Complete - Statistics")
    print("=" * 60)
    print(f"Mean voltage:              {np.mean(samples):.3f} V")
    print(f"Std deviation (single):    {np.std(samples, ddof=1):.4f} V")
    print(f"Std deviation of mean:     {np.std(samples, ddof=1) / np.sqrt(len(samples)):.5f} V")
    print(f"Min: {np.min(samples):.3f} V  Max: {np.max(samples):.3f} V")
    print()
    print("First 10 samples (for prelab Method B):")
    for i, v in enumerate(samples[:10]):
        print(f"  {v:.3f}", end="")
        if (i + 1) % 5 == 0:
            print()
    print()

    # Save to CSV
    with open(OUTPUT_FILE, 'w') as f:
        f.write("Voltage (V)\n")
        for v in samples:
            f.write(f"{v:.3f}\n")

    print(f"Data saved to: {OUTPUT_FILE}")
    print()

    # Plot the data
    plot_data(samples, SAMPLE_INTERVAL)

    # Reminder about prelab
    print("=" * 60)
    print("Next Steps")
    print("=" * 60)
    print("1. Review the statistics above")
    print("2. If the data looks reasonable, update the prelab with:")
    print("   - The first 10 values (for Method B eyeballing exercise)")
    print("   - Expected answers for Methods A, C, D")
    print("3. Consider whether the noise level is appropriate for teaching")
    print("   (not too small to see, not so large it obscures the signal)")

if __name__ == "__main__":
    main()
