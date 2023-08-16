# -*- coding: utf-8
import numpy as np
import numpy.matlib as matlib
from scipy.linalg import expm
import matplotlib.pylab as plt
from math import pi

# John's dirt-simple self-contained liquid-phase NMR simulator
#
# Homonuclear spin-1/2, scalar J-coupling and chemical shift
# 1-d FID and spectrum with exponential apodization
# The size of the interaction matrix determines the number of spins
# 
# Thanks to Ilya Kuprov for helpful examples
# See his web site spindynamics.org and watch his YouTube lectures
#
# john.price@colorado.edu
# Control parameters
fL = 45.0
# Larmor frequency in MHz. Used only to convert
# frequencies from ppm to Hz.
sampling_rate = 3000.
# Sampling rate in Hz or 1/(simulation time step)
steps = 3000
# Number of time steps
zero_fill = 4*steps
# Zero-fill the FID to this many samples before FFT
T2 = 0.3
# T2 time constant in seconds,
#    The FID decays with this time constant
phase = 0.
# Phase of spectrum to plot in radians
#    real part is 0
#    imaginary part is pi/2
# Interaction matrix
# An NxN real matrix where N is the number of spins to be simulated
# N must be less than 12 on a typical workstation
# N must be less than 20 unless you have a quantum computer
#
# Diagonal elements are the Zeeman (chemical shift) coefficients in ppm
#
# Elements below the diagonal are scalar J-coupling coefficients in Hz
# For example, the number in the fouth row and second column is the
# coupling between spin 2 and spin 4 in Hz
#
# elements above the diagonal are not used
#
# Example: very dry ethanol showing non-exchanging OH proton
# spins: CH3   CH3   CH3   CH2   CH2   OH
inter = np.matrix(
    [[ 1.1,    0,    0,    0,     0,    0],
     [   0,  1.1,    0,    0,     0,    0],
     [   0,    0,  1.1,    0,     0,    0],
     [6.81, 6.81, 6.81,  3.6,     0,    0],
     [6.81, 6.81, 6.81,    0,   3.6,    0],
     [   0,    0,    0, 5.37,  5.37,  5.3]]
)

nspins = np.shape(inter)[0]      # find the number of spins

# Define the Pauli spin matrices and a unit matrix
# Include factor of 1/2 for correct spin-1/2 eigenvalues
sigma_x = np.matrix('0 1; 1 0') / 2.
sigma_y = np.matrix('0 -1j; 1j 0') / 2.
sigma_z = np.matrix('1 0; 0 -1') / 2.
unit = np.identity(2)

# Build the single-spin operators Sx{i}, Sy{i}, Sz{i}
# The index i labels which spin it operates on
# These are direct or Kronecker products of Pauli and unit matricies
# For example, Sy for the third spin in a four-spin system is
#      unit (x) unit (x) sigma_y (x) unit

# create empty arrays
Sx = np.empty((nspins), dtype=np.object)
Sy = np.empty((nspins), dtype=np.object)
Sz = np.empty((nspins), dtype=np.object)

for i in range(nspins):    # which spin it acts on
    Sx_current, Sy_current, Sz_current = 1, 1, 1
    for k in range(nspins):
        if k == i:
            Sx_current = np.kron(Sx_current, sigma_x); 
            Sy_current = np.kron(Sy_current, sigma_y);
            Sz_current = np.kron(Sz_current, sigma_z);
        else:     # else kron() in a unit matrix
            Sx_current = np.kron(Sx_current, unit);
            Sy_current = np.kron(Sy_current, unit);
            Sz_current = np.kron(Sz_current, unit);
    Sx[i] = Sx_current
    Sy[i] = Sy_current
    Sz[i] = Sz_current
    
# Build magnetization operators
# These are sums over all spins of the single-spin operators
ns = 2**nspins
Mx = matlib.zeros((ns, ns), dtype='complex')
My = matlib.zeros((ns, ns), dtype='complex')
Mz = matlib.zeros((ns, ns), dtype='complex')
for i in range(nspins):
    Mx += Sx[i]
    My += Sy[i]
    Mz += Sz[i]
    
# Build the Hamiltonian (in rad/s units)
H = 0
for i in range(nspins):
    for k in range(nspins):
        if i == k:
            H += 2 * pi * fL * inter[i,k] * Sz[i]            # Zeeman terms
        elif i > k:
            H += 2 * pi * inter[i,k] * (Sx[i]*Sx[k] + Sy[i]*Sy[k] + Sz[i]*Sz[k]) # J
    
# Define the observable.  
# I know plenty of law-abiding people who use non-Hermetian observables.
obs = Mx + 1j * My     # Mx is real part, My is imaginary part

# Initialize the density matrix rho to Mx
rho = Mx

# Propagator to advance the density matrix one time step
time_step = 1./sampling_rate
P = np.mat(expm(-1j * H * time_step))

# Evolve the system and compute the observable
# The FID is the free-induction-decay, a complex time series
fid = np.zeros(steps, dtype='complex')
for n in range(steps):
    fid[n] = np.trace(obs * rho)
    rho = P * rho * P.H # The H means Hermetian conjugation
    if not n % 50:        # Report progress
        print('step {0}'.format(n))
    
# Apodization (filtering) to simulate relaxation
# Multiply the FID by an exponential decay with time constant T2
duration = steps * time_step
window_function = np.exp(-(duration/T2) * np.linspace(0, 1, steps))
winfid = fid * window_function

# FFT with zero-filling
# Zero-filling has the effect of interpolating between frequency points
# which makes the spectrum smoother
spectrum = np.fft.fftshift(np.fft.fft(winfid, zero_fill))

time_series = np.linspace(0, (steps-1) * time_step, steps)  # in seconds
freq_series = np.fft.fftshift(np.fft.fftfreq(zero_fill, time_step))  #in Hz

# Plots, comment in or out as desired
# Real part of the apodized FID
plt.figure(0)  # plot the real part of the apodized FID
plt.clf()
plt.plot(time_series, winfid.real)
plt.xlabel('time (seconds)')

# Spectrum in Hz
plt.figure(1)  # plot the desired phase of the spectrum
plt.clf()
plt.plot(freq_series, np.real(np.exp(1j * phase) * spectrum))
plt.gca().invert_xaxis()
plt.xlabel('frequency (Hz)')

# Spectrum in ppm
plt.figure(2)  # plot the desired phase of the spectrum
plt.clf()
plt.plot(freq_series/fL, np.real(np.exp(1j * phase) * spectrum))
plt.gca().invert_xaxis()
plt.xlabel('frequency (ppm)')
