"""
Curve Fitting Example - Beam Profile Analysis
==============================================

This script demonstrates curve fitting techniques for analyzing
beam profile data from the knife-edge measurement.

Topics covered:
1. Loading data from CSV
2. Defining fit functions (error function for beam profile)
3. Performing nonlinear fits with scipy.optimize.curve_fit
4. Extracting parameter uncertainties
5. Calculating chi-squared
6. Plotting data, fit, and residuals

Usage:
    python 02_fitting_example.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf


def beam_profile_function(x, amplitude, center, width, offset):
    """
    Error function model for knife-edge beam profile measurement.

    When a knife edge is moved across a Gaussian beam, the transmitted
    power follows an error function.

    Parameters:
        x: Position of knife edge (m or mm)
        amplitude: Half the total voltage swing (V)
        center: Position of beam center (same units as x)
        width: Beam width parameter w (same units as x)
        offset: Vertical offset (V)

    Returns:
        Voltage as function of position
    """
    return amplitude * erf(np.sqrt(2) * (x - center) / width) + offset


def load_beam_data(filename):
    """
    Load beam profile data from CSV file.

    Expected format: two columns (position, voltage) with header row.

    Parameters:
        filename: Path to CSV file

    Returns:
        x: Position array
        y: Voltage array
    """
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    x = data[:, 0]
    y = data[:, 1]
    return x, y


def load_beam_data_with_errors(filename):
    """
    Load beam profile data with uncertainties from CSV file.

    Expected format: three columns (position, voltage, uncertainty)
    with header row.

    Parameters:
        filename: Path to CSV file

    Returns:
        x: Position array
        y: Voltage array
        y_err: Uncertainty array
    """
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    x = data[:, 0]
    y = data[:, 1]
    y_err = data[:, 2]
    return x, y, y_err


def fit_beam_profile(x, y, y_err=None):
    """
    Fit beam profile data to error function model.

    Parameters:
        x: Position array
        y: Voltage array
        y_err: Optional uncertainty array for weighted fit

    Returns:
        popt: Optimal parameters [amplitude, center, width, offset]
        perr: Parameter uncertainties
        pcov: Full covariance matrix
    """
    # Initial parameter guesses
    y_min, y_max = np.min(y), np.max(y)
    amplitude_guess = (y_max - y_min) / 2
    offset_guess = (y_max + y_min) / 2
    center_guess = x[np.argmin(np.abs(y - offset_guess))]
    width_guess = (x[-1] - x[0]) / 10  # Rough guess

    p0 = [amplitude_guess, center_guess, width_guess, offset_guess]

    print("Initial guesses:")
    print(f"  Amplitude: {amplitude_guess:.4f}")
    print(f"  Center: {center_guess:.6f}")
    print(f"  Width: {width_guess:.6f}")
    print(f"  Offset: {offset_guess:.4f}")

    # Perform the fit
    if y_err is not None:
        # Weighted fit using uncertainties
        popt, pcov = curve_fit(
            beam_profile_function, x, y,
            p0=p0,
            sigma=y_err,
            absolute_sigma=True
        )
    else:
        # Unweighted fit
        popt, pcov = curve_fit(
            beam_profile_function, x, y,
            p0=p0
        )

    # Extract uncertainties from covariance matrix
    perr = np.sqrt(np.diag(pcov))

    return popt, perr, pcov


def calculate_chi_squared(y_data, y_fit, y_err, num_params):
    """
    Calculate chi-squared and reduced chi-squared.

    Parameters:
        y_data: Measured data points
        y_fit: Fitted values
        y_err: Uncertainties on data points
        num_params: Number of fit parameters

    Returns:
        chi2: Chi-squared value
        chi2_red: Reduced chi-squared
        dof: Degrees of freedom
    """
    residuals = y_data - y_fit
    chi2 = np.sum((residuals / y_err) ** 2)
    dof = len(y_data) - num_params
    chi2_red = chi2 / dof

    return chi2, chi2_red, dof


def plot_fit_results(x, y, popt, y_err=None, save_filename=None):
    """
    Create publication-quality plot of data and fit with residuals.

    Parameters:
        x: Position array
        y: Voltage array
        popt: Fit parameters
        y_err: Optional uncertainty array
        save_filename: Optional filename to save plot
    """
    # Generate smooth curve for fit
    x_fit = np.linspace(x.min(), x.max(), 500)
    y_fit = beam_profile_function(x_fit, *popt)

    # Calculate residuals at data points
    y_fit_at_data = beam_profile_function(x, *popt)
    residuals = y - y_fit_at_data

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 8),
        gridspec_kw={'height_ratios': [3, 1]},
        sharex=True
    )

    # Top plot: Data and fit
    if y_err is not None:
        ax1.errorbar(x, y, yerr=y_err, fmt='o', markersize=4,
                     capsize=3, label='Data', color='blue', alpha=0.7)
    else:
        ax1.scatter(x, y, s=20, label='Data', color='blue', alpha=0.7)

    ax1.plot(x_fit, y_fit, 'r-', linewidth=2, label='Fit')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('Beam Profile Measurement')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Bottom plot: Residuals
    if y_err is not None:
        ax2.errorbar(x, residuals, yerr=y_err, fmt='o', markersize=4,
                     capsize=3, color='blue', alpha=0.7)
    else:
        ax2.scatter(x, residuals, s=20, color='blue', alpha=0.7)

    ax2.axhline(y=0, color='r', linestyle='--', linewidth=1)
    ax2.set_xlabel('Position (m)')
    ax2.set_ylabel('Residuals (V)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_filename:
        plt.savefig(save_filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_filename}")

    plt.show()


def main():
    """Main function demonstrating curve fitting."""

    print("\n" + "=" * 50)
    print("PHYS 4430 - Curve Fitting Demo")
    print("=" * 50 + "\n")

    # Example with synthetic data
    print("Generating synthetic beam profile data...")

    # True parameters
    true_params = {
        'amplitude': 1.5,
        'center': 0.01,  # 10 mm = 0.01 m
        'width': 0.001,  # 1 mm = 0.001 m
        'offset': 1.5
    }

    # Generate synthetic data
    np.random.seed(42)  # For reproducibility
    x_data = np.linspace(0.005, 0.015, 30)
    y_true = beam_profile_function(
        x_data,
        true_params['amplitude'],
        true_params['center'],
        true_params['width'],
        true_params['offset']
    )

    # Add noise
    noise_level = 0.05
    y_data = y_true + np.random.normal(0, noise_level, len(x_data))
    y_err = np.ones_like(y_data) * noise_level

    print(f"\nTrue parameters:")
    print(f"  Amplitude: {true_params['amplitude']:.4f} V")
    print(f"  Center: {true_params['center']*1000:.4f} mm")
    print(f"  Width: {true_params['width']*1000:.4f} mm")
    print(f"  Offset: {true_params['offset']:.4f} V")

    # Perform fit
    print("\nPerforming fit...")
    popt, perr, pcov = fit_beam_profile(x_data, y_data, y_err)

    print("\nFit results:")
    print(f"  Amplitude: {popt[0]:.4f} ± {perr[0]:.4f} V")
    print(f"  Center: {popt[1]*1000:.4f} ± {perr[1]*1000:.4f} mm")
    print(f"  Width: {popt[2]*1000:.4f} ± {perr[2]*1000:.4f} mm")
    print(f"  Offset: {popt[3]:.4f} ± {perr[3]:.4f} V")

    # Calculate chi-squared
    y_fit = beam_profile_function(x_data, *popt)
    chi2, chi2_red, dof = calculate_chi_squared(y_data, y_fit, y_err, 4)

    print(f"\nGoodness of fit:")
    print(f"  Chi-squared: {chi2:.2f}")
    print(f"  Degrees of freedom: {dof}")
    print(f"  Reduced chi-squared: {chi2_red:.2f}")
    print(f"  (Should be close to 1.0 for a good fit)")

    # Plot results
    print("\nPlotting results...")
    plot_fit_results(x_data, y_data, popt, y_err)

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
