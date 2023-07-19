% John's dirt-simple self-contained liquid-phase NMR simulator
% MATLAB version
% Homonuclear spin-1/2, scalar J-coupling and chemical shift
% 1-d FID and spectrum with exponential apodization
% The size of the interaction matrix determines the number of spins
% 
% Thanks to Ilya Kuprov for helpful examples
% See his web site spindynamics.org and watch his YouTube lectures
%
% john.price@colorado.edu

% Control parameters
fL=45.0;              % Larmor frequency in MHz. Used only to convert
                      % frequencies from ppm to Hz.
sampling_rate=3000;   % Sampling rate in Hz or 1/(simulation time step)
steps=3000;           % Number of time steps
zero_fill=4*steps;    % Zero-fill the FID to this many samples before FFT
T2=0.3;               % T2 time constant in seconds,
                      %    The FID decays with this time constant
phase=0;              % Phase of spectrum to plot in radians
                      %    real part is 0
                      %    imaginary part is pi/2

% Interaction matrix
% An NxN real matrix where N is the number of spins to be simulated
% N must be less than 12 on a typical workstation
% N must be less than 20 unless you have a quantum computer
%
% Diagonal elements are the Zeeman (chemical shift) coefficients in ppm
%
% Elements below the diagonal are scalar J-coupling coefficients in Hz
% For example, the number in the fouth row and second column is the
% coupling between spin 2 and spin 4 in Hz
%
% elements above the diagonal are not used
%
% Example: very dry ethanol showing non-exchanging OH proton
% spins: CH3   CH3   CH3   CH2   CH2   OH
inter=  [1.1   0     0     0     0     0
         0     1.1   0     0     0     0
         0     0     1.1   0     0     0
         6.81  6.81  6.81  3.6   0     0
         6.81  6.81  6.81  0     3.6   0
         0     0     0     5.37  5.37  5.3];

nspins=size(inter,1);      % find the number of spins

% Define the Pauli spin matrices and a unit matrix
% Include factor of 1/2 for correct spin-1/2 eigenvalues
sigma_x=(1/2)*[0 1; 1 0];
sigma_y=(1/2)*[0 -1i; 1i 0];
sigma_z=(1/2)*[1 0; 0 -1];
unit=[1 0; 0 1];

% Build the single-spin operators Sx{i}, Sy{i}, Sz{i}
% The index i labels which spin it operates on
% These are direct or Kronecker products of Pauli and unit matricies
% For example, Sy for the third spin in a four-spin system is
%      unit (x) unit (x) sigma_y (x) unit
% A cell is a MATLAB indexed array that can contain anything
Sx=cell(1,nspins); Sy=cell(1,nspins); Sz=cell(1,nspins);  % create empty arrays
for i=1:nspins        % which spin it acts on
    Sx_current=1; Sy_current=1; Sz_current=1;
    for k=1:nspins    % loop over all spins
        if k==i  % kron() in a Pauli matrix if this is the spin its acting on
            Sx_current=kron(Sx_current,sigma_x); 
            Sy_current=kron(Sy_current,sigma_y);
            Sz_current=kron(Sz_current,sigma_z);
        else     % else kron() in a unit matrix
            Sx_current=kron(Sx_current,unit);
            Sy_current=kron(Sy_current,unit);
            Sz_current=kron(Sz_current,unit);
        end
    end
    Sx{i}=Sx_current; Sy{i}=Sy_current; Sz{i}=Sz_current;
end
 
% Build magnetization operators
% These are sums over all spins of the single-spin operators
Mx=zeros(2^nspins); My=zeros(2^nspins); Mz=zeros(2^nspins);
for i=1:nspins
    Mx=Mx+Sx{i};
    My=My+Sy{i};
    Mz=Mz+Sz{i};
end

% Build the Hamiltonian (in rad/s units)
H=0;
for i=1:nspins
    for k=1:nspins
        if i==k
            H=H+2*pi*fL*inter(i,k)*Sz{i};       % Zeeman terms
        elseif i>k
            H=H+2*pi*inter(i,k)*(Sx{i}*Sx{k}+Sy{i}*Sy{k}+Sz{i}*Sz{k}); % J
        end
    end
end

% Define the observable.  
% I know plenty of law-abiding people who use non-Hermetian observables.
obs = Mx + 1i*My;    % Mx is real part, My is imaginary part

% Initialize the density matrix rho to Mx
rho=Mx;

% Propagator to advance the density matrix one time step
time_step=1/sampling_rate;
P=expm(-1i*H*time_step);     % MATLAB knows how to do matrix exponentiation

% Evolve the system and compute the observable
% The FID is the free-induction-decay, a complex time series
fid=zeros(1,steps);
for n=1:steps
    fid(n)=trace(obs*rho);   % MATLAB knows how to take a trace
    rho=P*rho*P';            % The prime means Hermetian conjugation
    if ~mod(n,200)            % Report progress
        disp(['step ' num2str(n)]);
    end
end

% Apodization (filtering) to simulate relaxation
% Multiply the FID by an exponential decay with time constant T2
duration=steps*time_step;
window_function=exp(-(duration/T2)*linspace(0,1,steps));
winfid=fid.*window_function;

% FFT with zero-filling
% Zero-filling has the effect of interpolating between frequency points
% which makes the spectrum smoother
spectrum=fftshift(fft(winfid,zero_fill));  % MATLAB's FFT output needs rearranging
time_series=linspace(0,(steps-1)*time_step,steps);  % in seconds
freq_series=linspace(-1/(2*time_step),1/(2*time_step),zero_fill);  %in Hz

% Plots, comment in or out as desired
% Real part of the apodized FID
figure('Name','FID');            % plot the real part of the apodized FID
plot(time_series,real(winfid));
xlabel('time (seconds)')

% Spectrum in Hz
figure('Name','Spectrum');       % plot the desired phase of the spectrum
plot(freq_series,real(exp(1i*phase)*spectrum)); 
set(gca,'XDir','reverse');       % NMR spectra are always plotted backwards
xlabel('frequency (Hz)')

% Spectrum in ppm
figure('Name','Spectrum');       % plot the desired phase of the spectrum
plot(freq_series/fL,real(exp(1i*phase)*spectrum)); 
set(gca,'XDir','reverse');       % NMR spectra are always plotted backwards
xlabel('frequency (ppm)')



