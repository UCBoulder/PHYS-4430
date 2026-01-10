"""
FFT Analysis - Fourier Transform and Spectral Analysis
======================================================

This script demonstrates Fourier transform techniques for
analyzing frequency content of signals.

Topics covered:
1. Computing FFT with numpy
2. Creating proper frequency axis
3. Interpreting the spectrum
4. Real-time spectral analysis
5. Nyquist frequency and aliasing

Usage:
    python 03_fft_analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt


def compute_fft(signal, sample_rate):
    """
    Compute the Fast Fourier Transform of a signal.

    Parameters:
        signal: 1D array of signal values
        sample_rate: Sampling rate in Hz

    Returns:
        frequencies: Array of frequency values (Hz)
        magnitude: Array of magnitude values
        phase: Array of phase values (radians)
    """
    n = len(signal)

    # Compute FFT
    fft_result = np.fft.fft(signal)

    # Compute frequency axis
    frequencies = np.fft.fftfreq(n, d=1/sample_rate)

    # Get magnitude and phase
    magnitude = np.abs(fft_result) / n  # Normalize by number of points
    phase = np.angle(fft_result)

    return frequencies, magnitude, phase


def compute_power_spectrum(signal, sample_rate):
    """
    Compute the one-sided power spectrum of a signal.

    For real signals, the spectrum is symmetric, so we only
    need the positive frequency half.

    Parameters:
        signal: 1D array of signal values
        sample_rate: Sampling rate in Hz

    Returns:
        frequencies: Array of positive frequency values (Hz)
        power: Array of power values
    """
    n = len(signal)

    # Compute FFT
    fft_result = np.fft.fft(signal)

    # One-sided spectrum (positive frequencies only)
    # For N points, we get N/2 + 1 unique frequencies
    n_unique = n // 2 + 1

    frequencies = np.fft.fftfreq(n, d=1/sample_rate)[:n_unique]
    frequencies = np.abs(frequencies)  # Make all positive

    # Power spectrum (magnitude squared)
    power = (np.abs(fft_result[:n_unique]) / n) ** 2

    # Double the power for frequencies that appear twice (all except DC and Nyquist)
    power[1:-1] *= 2

    return frequencies, power


def generate_test_signal(duration, sample_rate, frequencies, amplitudes):
    """
    Generate a test signal with multiple frequency components.

    Parameters:
        duration: Signal duration in seconds
        sample_rate: Samples per second
        frequencies: List of frequency components (Hz)
        amplitudes: List of corresponding amplitudes

    Returns:
        t: Time array
        signal: Signal array
    """
    n_samples = int(duration * sample_rate)
    t = np.arange(n_samples) / sample_rate

    signal = np.zeros(n_samples)
    for freq, amp in zip(frequencies, amplitudes):
        signal += amp * np.sin(2 * np.pi * freq * t)

    return t, signal


def plot_signal_and_spectrum(t, signal, sample_rate, title="Signal Analysis"):
    """
    Create a two-panel plot showing time domain and frequency domain.

    Parameters:
        t: Time array
        signal: Signal array
        sample_rate: Sampling rate in Hz
        title: Plot title
    """
    # Compute spectrum
    frequencies, power = compute_power_spectrum(signal, sample_rate)

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Time domain plot
    ax1.plot(t * 1000, signal, 'b-', linewidth=0.5)  # Time in ms
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title(f'{title} - Time Domain')
    ax1.grid(True, alpha=0.3)

    # Limit x-axis to show detail
    if len(t) > 1000:
        ax1.set_xlim(0, t[1000] * 1000)

    # Frequency domain plot
    ax2.plot(frequencies, power, 'r-', linewidth=1)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Power')
    ax2.set_title(f'{title} - Frequency Domain (Power Spectrum)')
    ax2.grid(True, alpha=0.3)

    # Set x-axis limit to Nyquist frequency
    nyquist = sample_rate / 2
    ax2.set_xlim(0, nyquist)

    plt.tight_layout()
    plt.show()


def demonstrate_aliasing(signal_freq, sample_rate):
    """
    Demonstrate aliasing when sampling below Nyquist rate.

    Parameters:
        signal_freq: Frequency of the signal (Hz)
        sample_rate: Sampling rate (Hz)
    """
    nyquist = sample_rate / 2

    print(f"\nAliasing Demonstration:")
    print(f"  Signal frequency: {signal_freq} Hz")
    print(f"  Sample rate: {sample_rate} Hz")
    print(f"  Nyquist frequency: {nyquist} Hz")

    if signal_freq > nyquist:
        # Calculate aliased frequency
        aliased_freq = abs(signal_freq - sample_rate * round(signal_freq / sample_rate))
        print(f"  WARNING: Signal frequency exceeds Nyquist!")
        print(f"  Aliased frequency: {aliased_freq} Hz")
    else:
        print(f"  Signal is below Nyquist - no aliasing expected")

    # Generate and plot
    duration = 0.1  # 100 ms
    t, signal = generate_test_signal(duration, sample_rate, [signal_freq], [1.0])

    # Also generate "true" signal at higher sample rate for comparison
    high_rate = 100000  # 100 kHz
    t_true, signal_true = generate_test_signal(duration, high_rate, [signal_freq], [1.0])

    fig, ax = plt.subplots(figsize=(12, 5))

    # Plot true signal
    ax.plot(t_true * 1000, signal_true, 'b-', linewidth=0.5,
            alpha=0.5, label='True signal')

    # Plot sampled points
    ax.plot(t * 1000, signal, 'ro-', markersize=4,
            label=f'Sampled at {sample_rate} Hz')

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Aliasing Demo: {signal_freq} Hz signal sampled at {sample_rate} Hz')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 10)  # Show first 10 ms

    plt.tight_layout()
    plt.show()


def real_time_fft_demo(duration=5, sample_rate=1000, update_interval=0.1):
    """
    Demonstrate real-time FFT analysis with simulated data.

    In actual lab use, this would read from the DAQ instead
    of generating synthetic data.

    Parameters:
        duration: Total duration in seconds
        sample_rate: Sample rate in Hz
        update_interval: Time between plot updates (seconds)
    """
    print("\nReal-time FFT Demo (with synthetic data)")
    print("Press Ctrl+C to stop early\n")

    # Set up interactive plotting
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Initialize empty plots
    line1, = ax1.plot([], [], 'b-', linewidth=0.5)
    line2, = ax2.plot([], [], 'r-', linewidth=1)

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Time Domain (last 1 second)')
    ax1.grid(True, alpha=0.3)

    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Power')
    ax2.set_title('Frequency Domain')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, sample_rate / 2)

    samples_per_update = int(update_interval * sample_rate)
    window_size = int(1.0 * sample_rate)  # 1 second window

    all_data = []

    try:
        for i in range(int(duration / update_interval)):
            # Simulate acquiring data (in real lab, read from DAQ)
            # Signal: 50 Hz + 120 Hz with some noise
            t_chunk = np.arange(samples_per_update) / sample_rate
            chunk = (np.sin(2 * np.pi * 50 * (i * update_interval + t_chunk)) +
                     0.5 * np.sin(2 * np.pi * 120 * (i * update_interval + t_chunk)) +
                     0.2 * np.random.randn(samples_per_update))

            all_data.extend(chunk)

            # Keep only last window_size samples
            if len(all_data) > window_size:
                all_data = all_data[-window_size:]

            data_array = np.array(all_data)

            # Update time domain plot
            t_plot = np.arange(len(data_array)) / sample_rate
            line1.set_data(t_plot, data_array)
            ax1.set_xlim(0, max(t_plot[-1], 0.1))
            ax1.set_ylim(np.min(data_array) - 0.5, np.max(data_array) + 0.5)

            # Update frequency domain plot
            if len(data_array) > 10:
                frequencies, power = compute_power_spectrum(data_array, sample_rate)
                line2.set_data(frequencies, power)
                ax2.set_ylim(0, max(power) * 1.1 + 0.001)

            plt.pause(update_interval * 0.8)

    except KeyboardInterrupt:
        print("\nStopped by user")

    plt.ioff()
    plt.show()


def main():
    """Main function demonstrating FFT analysis."""

    print("\n" + "=" * 50)
    print("PHYS 4430 - FFT Analysis Demo")
    print("=" * 50)

    # Demo 1: Simple signal analysis
    print("\n--- Demo 1: Single Frequency Signal ---")
    sample_rate = 1000  # 1 kHz
    duration = 1.0  # 1 second

    t, signal = generate_test_signal(duration, sample_rate, [50], [1.0])
    plot_signal_and_spectrum(t, signal, sample_rate, "50 Hz Sine Wave")

    # Demo 2: Multiple frequency components
    print("\n--- Demo 2: Multi-Frequency Signal ---")
    t, signal = generate_test_signal(
        duration, sample_rate,
        frequencies=[50, 120, 200],
        amplitudes=[1.0, 0.5, 0.3]
    )
    plot_signal_and_spectrum(t, signal, sample_rate, "Multi-Frequency Signal")

    # Demo 3: Aliasing
    print("\n--- Demo 3: Aliasing Demonstration ---")
    demonstrate_aliasing(signal_freq=1000, sample_rate=500)  # Undersampled
    demonstrate_aliasing(signal_freq=998, sample_rate=1000)  # Close to sample rate

    # Demo 4: Real-time FFT (optional - uncomment to run)
    print("\n--- Demo 4: Real-time FFT ---")
    user_input = input("Run real-time FFT demo? (y/n): ")
    if user_input.lower() == 'y':
        real_time_fft_demo(duration=10, sample_rate=1000)

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
