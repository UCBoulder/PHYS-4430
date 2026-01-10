"""
DAQ Basics - Introduction to Data Acquisition with NI-DAQmx
===========================================================

This script demonstrates basic data acquisition operations using
the National Instruments USB-6009 DAQ device.

Topics covered:
1. Listing available DAQ devices
2. Reading a single voltage measurement
3. Reading multiple samples
4. Configuring sample rate
5. Saving data to CSV

Hardware required:
- NI USB-6009 (or compatible NI DAQ device)
- Signal source connected to AI0 (analog input 0)

Usage:
    python 01_daq_basics.py
"""

import nidaqmx
import nidaqmx.system
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def list_daq_devices():
    """
    List all connected NI-DAQ devices.

    Run this first to verify your DAQ is connected and find its name.
    """
    system = nidaqmx.system.System.local()

    print("=" * 50)
    print("Available NI-DAQ Devices")
    print("=" * 50)

    if len(system.devices) == 0:
        print("No devices found!")
        print("Check that your DAQ is connected via USB.")
        return None

    for device in system.devices:
        print(f"Device Name: {device.name}")
        print(f"Product Type: {device.product_type}")
        print(f"Serial Number: {device.serial_num}")
        print("-" * 50)

    return system.devices[0].name


def read_single_voltage(device="Dev1", channel="ai0"):
    """
    Read a single voltage measurement from the DAQ.

    Parameters:
        device: DAQ device name (e.g., "Dev1")
        channel: Analog input channel (e.g., "ai0")

    Returns:
        Voltage value in volts
    """
    with nidaqmx.Task() as task:
        # Configure the analog input channel
        task.ai_channels.add_ai_voltage_chan(
            f"{device}/{channel}",
            min_val=-10.0,
            max_val=10.0
        )

        # Read one sample
        voltage = task.read()

    return voltage


def read_multiple_samples(num_samples=1000, sample_rate=1000,
                          device="Dev1", channel="ai0"):
    """
    Read multiple voltage samples at a specified rate.

    Parameters:
        num_samples: Number of samples to acquire
        sample_rate: Samples per second (Hz)
        device: DAQ device name
        channel: Analog input channel

    Returns:
        times: Array of time values (seconds)
        voltages: Array of voltage values (volts)
    """
    with nidaqmx.Task() as task:
        # Configure the analog input channel
        task.ai_channels.add_ai_voltage_chan(
            f"{device}/{channel}",
            min_val=-10.0,
            max_val=10.0
        )

        # Configure timing for multiple samples
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
            samps_per_chan=num_samples
        )

        # Read all samples
        voltages = np.array(task.read(
            number_of_samples_per_channel=num_samples
        ))

    # Create corresponding time array
    times = np.arange(num_samples) / sample_rate

    return times, voltages


def save_data_to_csv(times, voltages, filename=None):
    """
    Save acquired data to a CSV file.

    Parameters:
        times: Array of time values
        voltages: Array of voltage values
        filename: Output filename (auto-generated if None)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"daq_data_{timestamp}.csv"

    # Stack data into columns
    data = np.column_stack((times, voltages))

    # Save with header
    np.savetxt(filename, data, delimiter=',',
               header='Time (s),Voltage (V)', comments='')

    print(f"Data saved to: {filename}")
    return filename


def plot_data(times, voltages, title="DAQ Measurement"):
    """
    Create a plot of the acquired data.

    Parameters:
        times: Array of time values
        voltages: Array of voltage values
        title: Plot title
    """
    plt.figure(figsize=(10, 6))
    plt.plot(times, voltages, 'b-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    """Main function demonstrating DAQ operations."""

    print("\n" + "=" * 50)
    print("PHYS 4430 - DAQ Basics Demo")
    print("=" * 50 + "\n")

    # Step 1: List available devices
    print("Step 1: Finding DAQ devices...")
    device_name = list_daq_devices()

    if device_name is None:
        return

    print(f"\nUsing device: {device_name}")

    # Step 2: Read a single voltage
    print("\nStep 2: Reading single voltage...")
    try:
        voltage = read_single_voltage(device=device_name)
        print(f"Measured voltage: {voltage:.4f} V")
    except Exception as e:
        print(f"Error reading voltage: {e}")
        return

    # Step 3: Read multiple samples
    print("\nStep 3: Reading 1000 samples at 1000 Hz...")
    try:
        times, voltages = read_multiple_samples(
            num_samples=1000,
            sample_rate=1000,
            device=device_name
        )
        print(f"Acquired {len(voltages)} samples over {times[-1]:.2f} seconds")
        print(f"Mean voltage: {np.mean(voltages):.4f} V")
        print(f"Std deviation: {np.std(voltages):.4f} V")
    except Exception as e:
        print(f"Error acquiring data: {e}")
        return

    # Step 4: Save data
    print("\nStep 4: Saving data to CSV...")
    filename = save_data_to_csv(times, voltages)

    # Step 5: Plot data
    print("\nStep 5: Plotting data...")
    plot_data(times, voltages, title="DAQ Basics - Sample Acquisition")

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
