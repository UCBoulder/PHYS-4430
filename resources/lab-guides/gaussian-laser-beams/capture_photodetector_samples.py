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

# Configuration
DAQ_CHANNEL = "Dev1/ai0"
NUM_SAMPLES = 200
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
