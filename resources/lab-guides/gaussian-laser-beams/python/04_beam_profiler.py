"""
Automated Beam Profile Measurement System
==========================================

This script automates the knife-edge beam profile measurement using:
- Thorlabs KCube Stepper Motor Controller (KST101)
- National Instruments DAQ (USB-6009)
- Real-time data visualization

Hardware Requirements:
- Thorlabs KST101 Stepper Motor Controller
- Thorlabs ZST225 Linear Stage (or compatible stepper actuator)
- NI USB-6009 DAQ (or compatible NI DAQ)
- Photodetector connected to DAQ analog input (default: AI0)

Software Requirements:
- Thorlabs Kinesis SDK (https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)
- NI-DAQmx drivers (https://www.ni.com/en-us/support/downloads/drivers/download.ni-daq-mx.html)
- Python packages: pythonnet, nidaqmx, numpy, matplotlib

FIRST-TIME SETUP (Required):
-----------------------------
Before using this script, the KST101 must be configured with the correct
stage/actuator type. This is a one-time setup that stores settings in the
controller's internal memory.

IMPORTANT: The stage type MUST be configured via the KST101 front panel
or Thorlabs Kinesis software. Python cannot write to the controller's
internal settings memory.

Option 1 - Using the KST101 front panel (RECOMMENDED):
    1. Power on the KST101 (USB can be connected or not)
    2. Press the Menu button on the KST101
    3. Navigate to "Motor" or "Stage" settings
    4. Select your actuator type (e.g., ZST225)
    5. Save and exit the menu
    6. Power cycle the KST101 (disconnect and reconnect power)

Option 2 - Using Thorlabs Kinesis software:
    1. Open Kinesis and connect to the KST101
    2. When prompted, select your actuator type
    3. Close Kinesis (settings are saved to the controller)

VERIFYING CONFIGURATION:
When you run this script, it will display the detected stage configuration.
If the position shown by Python doesn't match the KST101 front panel display,
the stage type is misconfigured - use Option 1 above to fix it.

If the stage type is not configured, you will see an error:
"Object reference not set to an instance of an object"

FINDING YOUR SERIAL NUMBER:
---------------------------
The motor serial number is displayed on the KST101 front panel LCD
(e.g., "26002448"). This 8-digit number is needed to connect.

DAQ DEVICE DETECTION:
---------------------
The script automatically detects connected NI DAQ devices. If multiple
devices are found, you will be prompted to select one. Device names
(e.g., "Dev1", "Dev2") can be verified in NI MAX (Measurement &
Automation Explorer).

Usage:
    python 04_beam_profiler.py

The script will prompt for:
1. Motor serial number (from KST101 display)
2. Step size in mm (default: 0.05 mm)
3. Wait time after each step in ms (default: 500 ms)
4. Scan direction (forward/backward)

Output:
- CSV file: beam_profile_YYYYMMDD_HHMMSS.csv (position and voltage data)
- PNG plot: beam_profile_YYYYMMDD_HHMMSS.png (beam profile visualization)
- Real-time plot during measurement

TROUBLESHOOTING:
----------------
"Device not found" error:
    - Check USB connection
    - Verify serial number matches the KST101 display
    - Ensure no other software (Kinesis, APT) is using the controller

"Object reference not set" error:
    - Stage type not configured - see FIRST-TIME SETUP above

"No NI DAQ devices found" error:
    - Check DAQ USB connection
    - Verify device appears in NI MAX
    - Try unplugging and reconnecting the DAQ

Motor positions in wrong units:
    - Stage type may be misconfigured
    - Reconfigure using Kinesis or the KST101 front panel

Author: PHYS 4430
"""

import time
import csv
import traceback
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

# Thorlabs Kinesis imports (requires pythonnet and Kinesis SDK)
try:
    import clr
    clr.AddReference(
        "C:\\Program Files\\Thorlabs\\Kinesis\\"
        "Thorlabs.MotionControl.DeviceManagerCLI.dll"
    )
    clr.AddReference(
        "C:\\Program Files\\Thorlabs\\Kinesis\\"
        "Thorlabs.MotionControl.GenericMotorCLI.dll"
    )
    clr.AddReference(
        "C:\\Program Files\\Thorlabs\\Kinesis\\"
        "Thorlabs.MotionControl.KCube.StepperMotorCLI.dll"
    )
    from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
    from Thorlabs.MotionControl.DeviceManagerCLI import DeviceConfiguration
    from Thorlabs.MotionControl.GenericMotorCLI import MotorDirection
    from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper
    from System import Decimal
    THORLABS_AVAILABLE = True
except Exception as e:
    print(f"Warning: Thorlabs libraries not available: {e}")
    print("Motor control will not work without Kinesis SDK installed.")
    THORLABS_AVAILABLE = False

# NI-DAQmx imports
try:
    import nidaqmx
    NIDAQMX_AVAILABLE = True
except ImportError:
    print("Warning: nidaqmx not available. DAQ functions will not work.")
    NIDAQMX_AVAILABLE = False


class BeamProfiler:
    """
    Automated beam profile measurement system.

    This class coordinates the Thorlabs motor controller and NI DAQ to
    perform automated knife-edge beam profile measurements. It handles:
    - Motor connection, homing, and positioning
    - Voltage acquisition from the photodetector
    - Real-time visualization during scanning
    - Data export to CSV and PNG files

    The knife-edge method works by translating a razor blade across the
    beam while measuring transmitted power. The resulting S-curve can be
    differentiated to obtain the Gaussian beam profile, from which the
    beam width w can be extracted.

    Example usage:
        profiler = BeamProfiler("26002448", daq_device="Dev2")
        profiler.connect()
        profiler.home()
        positions, voltages = profiler.run_scan(step_size_mm=0.05)
        profiler.disconnect()
    """

    def __init__(self, serial_number, daq_device="Dev1", daq_channel="ai0"):
        """
        Initialize the beam profiler.

        Parameters:
            serial_number: Thorlabs motor controller serial number
            daq_device: NI DAQ device name (default: "Dev1")
            daq_channel: Analog input channel (default: "ai0")
        """
        self.serial_number = serial_number
        self.daq_device = daq_device
        self.daq_channel = daq_channel
        self.device = None
        self.positions = []
        self.voltages = []

    def get_stage_configuration(self):
        """
        Query the controller to get the current stage configuration.

        Returns:
            dict with 'settings_name', 'device_name', and other config info,
            or None if configuration cannot be read.
        """
        if self.device is None:
            return None

        try:
            # Try to get current configuration from device
            motor_config = self.device.LoadMotorConfiguration(
                self.serial_number,
                DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings
            )

            if motor_config is not None:
                return {
                    'settings_name': str(motor_config.DeviceSettingsName),
                    'description': str(motor_config.Description) if hasattr(motor_config, 'Description') else 'N/A',
                }
        except Exception as e:
            print(f"Could not read device settings: {e}")

        # Fall back to file settings
        try:
            motor_config = self.device.LoadMotorConfiguration(
                self.serial_number,
                DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
            )
            if motor_config is not None:
                return {
                    'settings_name': str(motor_config.DeviceSettingsName),
                    'description': str(motor_config.Description) if hasattr(motor_config, 'Description') else 'N/A',
                    'source': 'file'
                }
        except Exception:
            pass

        return None

    def connect(self):
        """
        Connect to the motor controller.

        This method:
        1. Builds the device list to discover connected controllers
        2. Creates a KCubeStepper object for the specified serial number
        3. Loads motor configuration from device memory (or file settings)
        4. Sets velocity parameters for smooth motion

        The motor configuration contains stage-specific parameters like
        steps per revolution, gear ratio, and travel limits. These must
        be configured on the KST101 (via front panel menu) before this
        script will work correctly.
        """
        if not THORLABS_AVAILABLE:
            raise RuntimeError("Thorlabs Kinesis SDK not available")

        print(f"Connecting to motor controller {self.serial_number}...")

        # Build device list - discovers all connected Thorlabs controllers
        DeviceManagerCLI.BuildDeviceList()

        # Check if device is connected
        if not DeviceManagerCLI.IsDeviceConnected(self.serial_number):
            raise RuntimeError(
                f"Device {self.serial_number} not found. "
                "Check USB connection and serial number."
            )

        # Create and connect device
        self.device = KCubeStepper.CreateKCubeStepper(self.serial_number)
        self.device.Connect(self.serial_number)
        time.sleep(0.5)

        # Wait for settings to initialize
        if not self.device.IsSettingsInitialized():
            print("Waiting for settings to initialize...")
            self.device.WaitForSettingsInitialized(5000)

        # Start polling
        self.device.StartPolling(250)
        time.sleep(0.25)

        # Enable device
        self.device.EnableDevice()
        time.sleep(0.5)

        # Load motor configuration
        # The configuration contains stage-specific parameters (steps/rev,
        # gear ratio, pitch) that convert between device units and real units.
        try:
            use_device_settings = (
                DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings
            )
            motor_config = self.device.LoadMotorConfiguration(
                self.serial_number, use_device_settings
            )
            if motor_config is None:
                raise ValueError("Device settings not available")
            print("Loaded motor configuration from device")
        except Exception as e:
            print(f"Could not load device settings: {e}")
            print("Trying file settings...")
            try:
                use_file_settings = (
                    DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
                )
                motor_config = self.device.LoadMotorConfiguration(
                    self.serial_number, use_file_settings
                )
                if motor_config is None:
                    raise ValueError("File settings not available")
                print("Loaded motor configuration from file")
            except Exception as e2:
                print(f"Warning: Could not load motor configuration: {e2}")
                print("Motor may not move correctly without configuration.")
                print("Configure the stage type via the KST101 front panel menu.")

        # Set velocity parameters
        try:
            vel_params = self.device.GetVelocityParams()
            vel_params.MaxVelocity = Decimal(1.0)  # 1 mm/s
            vel_params.Acceleration = Decimal(1.0)  # 1 mm/s²
            self.device.SetVelocityParams(vel_params)
            print("Velocity set to 1 mm/s")
        except Exception as e:
            print(f"Warning: Could not set velocity parameters: {e}")

        # Get device info
        info = self.device.GetDeviceInfo()
        print(f"Connected to: {info.Description}")
        print(f"Serial Number: {info.SerialNumber}")

        # Display current stage configuration
        stage_config = self.get_stage_configuration()
        if stage_config:
            print(f"Stage configuration: {stage_config['settings_name']}")

    def disconnect(self):
        """Disconnect from the motor controller."""
        if self.device is not None:
            self.device.StopPolling()
            self.device.Disconnect()
            print("Motor disconnected")

    def get_position(self):
        """Get current motor position in mm."""
        try:
            return float(str(self.device.Position))
        except:
            return float(self.device.Position.ToDouble(None))

    def move_to(self, position_mm, timeout_ms=60000):
        """
        Move motor to absolute position.

        Parameters:
            position_mm: Target position in mm
            timeout_ms: Timeout in milliseconds
        """
        print(f"Moving to {position_mm:.4f} mm...")
        self.device.MoveTo(Decimal(position_mm), timeout_ms)

        # Wait for move to complete
        while self.device.Status.IsMoving:
            time.sleep(0.01)

    def home(self, timeout_ms=60000):
        """Home the motor (move to reference position)."""
        print("Homing motor...")
        self.device.Home(timeout_ms)

        while self.device.Status.IsHoming:
            time.sleep(0.1)

        print(f"Homing complete. Position: {self.get_position():.4f} mm")

    def read_voltage(self):
        """Read voltage from DAQ."""
        if not NIDAQMX_AVAILABLE:
            raise RuntimeError("NI-DAQmx not available")

        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(
                f"{self.daq_device}/{self.daq_channel}"
            )
            voltage = task.read(number_of_samples_per_channel=1)
            if isinstance(voltage, list):
                return voltage[0]
            return voltage

    def run_scan(self, step_size_mm=0.05, wait_time_ms=500,
                 direction='forward', max_steps=100):
        """
        Run automated beam profile scan.

        Parameters:
            step_size_mm: Step size in mm
            wait_time_ms: Wait time after each step in ms
            direction: 'forward' or 'backward'
            max_steps: Maximum number of steps (safety limit)

        Returns:
            positions: List of positions (mm)
            voltages: List of voltages (V)
        """
        self.positions = []
        self.voltages = []

        # Determine movement direction
        if direction == 'forward':
            motor_dir = MotorDirection.Forward
            step = step_size_mm
        else:
            motor_dir = MotorDirection.Backward
            step = -step_size_mm

        # Set up real-time plotting
        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 6))
        line, = ax.plot([], [], 'b-o', markersize=4)
        ax.set_xlabel('Position (mm)')
        ax.set_ylabel('Voltage (V)')
        ax.set_title('Beam Profile Measurement (in progress)')
        ax.grid(True, alpha=0.3)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"beam_profile_{timestamp}.csv"

        # Create CSV file with header
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Position (mm)', 'Voltage (V)'])

        print("\n" + "=" * 50)
        print("Starting Beam Profile Measurement")
        print("=" * 50)
        print(f"Step size: {step_size_mm} mm")
        print(f"Wait time: {wait_time_ms} ms")
        print(f"Direction: {direction}")
        print(f"Output file: {filename}")
        print("\nPress Ctrl+C to stop early")
        print("=" * 50 + "\n")

        try:
            for step_num in range(max_steps):
                # Get current position and voltage
                position = self.get_position()
                voltage = self.read_voltage()

                # Store data
                self.positions.append(position)
                self.voltages.append(voltage)

                # Save to file immediately
                with open(filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([position, voltage])

                # Print progress
                print(f"Step {step_num + 1}: Position = {position:.4f} mm, "
                      f"Voltage = {voltage:.4f} V")

                # Update plot
                line.set_data(self.positions, self.voltages)
                ax.set_xlim(min(self.positions) - 0.1, max(self.positions) + 0.1)
                ax.set_ylim(min(self.voltages) - 0.1, max(self.voltages) + 0.1)
                plt.draw()
                plt.pause(0.01)

                # Move to next position
                next_position = position + step

                # Check if within safe range
                if next_position < -12 or next_position > 12:
                    print("Reached travel limit. Stopping scan.")
                    break

                self.move_to(next_position)

                # Wait for vibrations to settle
                time.sleep(wait_time_ms / 1000)

        except KeyboardInterrupt:
            print("\n\nScan stopped by user")

        plt.ioff()

        # Final plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.positions, self.voltages, 'b-o', markersize=4)
        ax.set_xlabel('Position (mm)')
        ax.set_ylabel('Voltage (V)')
        ax.set_title('Beam Profile Measurement Results')
        ax.grid(True, alpha=0.3)

        # Save plot
        plot_filename = filename.replace('.csv', '.png')
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved to: {plot_filename}")

        plt.show()

        print(f"\nData saved to: {filename}")
        print(f"Total points: {len(self.positions)}")

        return self.positions, self.voltages


def get_available_daq_devices():
    """
    Get list of available NI DAQ devices.

    Queries the NI-DAQmx system to find all connected DAQ devices.
    Device names (e.g., "Dev1", "Dev2") can be used to specify which
    DAQ to use for measurements.

    Returns:
        List of device name strings, or empty list if none found.
    """
    if not NIDAQMX_AVAILABLE:
        return []
    try:
        system = nidaqmx.system.System.local()
        return [device.name for device in system.devices]
    except Exception:
        return []


def main():
    """Main function for interactive beam profile measurement."""

    print("\n" + "=" * 60)
    print("PHYS 4430 - Automated Beam Profile Measurement")
    print("=" * 60 + "\n")

    # Check requirements
    if not THORLABS_AVAILABLE:
        print("ERROR: Thorlabs Kinesis SDK not found.")
        print("Please install Kinesis from: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control")
        return

    if not NIDAQMX_AVAILABLE:
        print("ERROR: NI-DAQmx not found.")
        print("Please install from: https://www.ni.com/en-us/support/downloads/drivers/download.ni-daq-mx.html")
        return

    # Detect DAQ devices
    daq_devices = get_available_daq_devices()
    if not daq_devices:
        print("ERROR: No NI DAQ devices found.")
        print("Check USB connection and NI MAX.")
        return

    if len(daq_devices) == 1:
        daq_device = daq_devices[0]
        print(f"DAQ device detected: {daq_device}")
    else:
        print(f"Available DAQ devices: {', '.join(daq_devices)}")
        daq_device = input(f"Enter DAQ device name (default {daq_devices[0]}): ").strip()
        if not daq_device or daq_device not in daq_devices:
            daq_device = daq_devices[0]
            print(f"Using: {daq_device}")

    # Get user input
    serial_number = input("Enter motor serial number (e.g., 26004813): ").strip()
    if not serial_number:
        serial_number = "26004813"
        print(f"Using default: {serial_number}")

    step_size = input("Enter step size in mm (default 0.05): ").strip()
    step_size = float(step_size) if step_size else 0.05

    wait_time = input("Enter wait time in ms (default 500): ").strip()
    wait_time = int(wait_time) if wait_time else 500

    direction = input("Enter direction (forward/backward, default forward): ").strip()
    if direction not in ['forward', 'backward']:
        direction = 'forward'

    # Create profiler with detected DAQ device
    profiler = BeamProfiler(serial_number, daq_device=daq_device)

    try:
        # Connect to motor
        profiler.connect()

        # Show current position
        print(f"\nCurrent position: {profiler.get_position():.4f} mm")

        # Offer to home
        home_response = input("\nHome the motor? (y/n, default y): ").strip()
        if home_response.lower() != 'n':
            profiler.home()

        # Offer to move to start position
        move_response = input("\nMove to specific start position? (y/n, default n): ").strip()
        if move_response.lower() == 'y':
            start_pos = float(input("Enter start position (mm): "))
            profiler.move_to(start_pos)

        # Confirm ready
        input("\nPress Enter to start the scan...")

        # Run scan
        profiler.run_scan(
            step_size_mm=step_size,
            wait_time_ms=wait_time,
            direction=direction
        )

    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()

    finally:
        profiler.disconnect()

    print("\nMeasurement complete!")


if __name__ == "__main__":
    main()
