import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Example time series
fs = 1000  # sampling rate in Hz
t = np.arange(0, 1, 1/fs)  # 1 second of data

# Example signal: 5 Hz + 40 Hz with noise
x = 1.0*np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*40*t) + 0.3*np.random.randn(len(t))


# --- Plot ---
plt.figure(figsize=(10, 4))
plt.plot(x)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Frequency Spectrum")
plt.grid()
plt.show()

# --- FFT ---
X = np.fft.fft(x)                  # Compute FFT
freqs = np.fft.fftfreq(len(x), 1/fs)  # Frequency axis
power = np.abs(X)**2              # Power spectrum
amplitude = np.abs(X)             # Amplitude spectrum

# Keep only positive frequencies
mask = freqs >= 0
freqs = freqs[mask]
power = power[mask]
amplitude = amplitude[mask]

# --- Plot ---
plt.figure(figsize=(10, 4))
plt.plot(freqs, amplitude)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Frequency Spectrum")
plt.grid()
plt.show()