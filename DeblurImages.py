import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert




# 1. Simulate oscillatory signal with some noise
fs = 1000       # sampling rate Hz
T = 1

phi = 0.8  # AR coefficient, controls decay of correlations
noise = np.random.normal(0, 1, fs*T)
x = np.zeros(fs*T)
for t in range(1, fs*T):
    x[t] = phi * x[t-1] + noise[t]


t = np.arange(0, T, 1/fs)
freq = 10       # oscillation frequency
signal = np.sin(2 * np.pi * freq * t) + 0.2*np.random.randn(len(t))

# 2. Analytic signal and phase
analytic_signal = hilbert(signal)
phase = np.angle(analytic_signal)

# 3. Compute pACF (Phase autocorrelation)
max_lag_cycles = 20   # up to 10 cycles
lags = np.arange(0, max_lag_cycles+0.1)  # lags in cycles
pACF = []

samples_per_cycle = 10
print(len(lags))
for lag in lags:
    shift = int(lag * samples_per_cycle)  # convert lag in cycles → samples
    if shift == 0:
        pACF.append(1.0)  # autocorrelation at lag 0 = 1
        continue
    # phase difference between original and lagged
    phase_diff = phase[:-shift] - phase[shift:]
    # plt.plot(phase_diff)
    # plt.plot(phase[:-shift])
    # plt.plot(phase[shift:])
    # plt.show()
    # compute PLV = |average of complex exponentials|
    plv = np.abs(np.mean(np.exp(1j*phase_diff)))
    # print(plv)
    pACF.append(plv)

pACF = np.array(pACF)

# 4. Normalize pACF to explained variance function
pACF_norm = pACF / np.sum(pACF)

# 5. Cumulative function
CF = np.cumsum(pACF_norm)
print(len(pACF_norm))
print(len(CF))
# 6. Lifetime score = first lag where CF > 0.9
threshold = 0.9
lifetime_idx = np.where(CF >= threshold)[0][0]
lifetime_cycles = lags[lifetime_idx]   # rhythmicity score

print(f"Rhythmicity score (pACF lifetime) = {lifetime_cycles:.2f} cycles")
plt.plot(signal)
plt.show()

plt.plot(phase)
plt.show()
# 7. Plot
plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.plot(lags, pACF, 'o-')
plt.xlabel("Lag (cycles)")
plt.ylim(-0.1, 1.1)
plt.ylabel("pACF")
plt.title("Phase Autocorrelation")

plt.subplot(1,3,2)
plt.plot(lags, pACF_norm, 'o-')
plt.xlabel("Lag (cycles)")
plt.ylabel("Normalized pACF")

plt.subplot(1,3,3)
plt.plot(lags, CF, 'o-')
plt.axhline(threshold, color='r', linestyle='--')
plt.axvline(lifetime_cycles, color='g', linestyle='--')
plt.xlabel("Lag (cycles)")
plt.ylabel("Cumulative pACF")
# plt.title(f"Lifetime = {lifetime_cycles/max_lag_cycles:.2f} cycles")
plt.tight_layout()
plt.show()



from scipy.signal import butter, filtfilt, hilbert

def bandpass_filter(data, fs, low, high, order=3):
    b,a = butter(order, [low/(0.5*fs), high/(0.5*fs)], btype='band')
    return filtfilt(b, a, data)

def compute_plv_phase_autocorr(signal, fs, low, high, lags, amp_thresh_pct=30, n_surrogates=200):
    """
    signal: 1D array
    fs: sample rate (Hz)
    low, high: bandpass range (Hz)
    lags: array of lags in seconds (can be negative too)
    amp_thresh_pct: percentile of amplitude envelope below which samples are masked
    n_surrogates: number of surrogates for null distribution (time-shift)
    """
    # 1) bandpass and analytic signal
    sig_filt = bandpass_filter(signal, fs, low, high)
    analytic = hilbert(sig_filt)
    amp = np.abs(analytic)
    phase = np.angle(analytic)
    N = len(signal)
    plt.plot(phase)
    plt.show()

    # 2) amplitude threshold (mask low-amplitude samples)
    thresh = np.percentile(amp, amp_thresh_pct)
    valid = amp >= thresh  # boolean mask

    # 3) function to compute PLV between phase and lagged phase at lag_samples
    def plv_at_lag(lag_samples, phase, valid_mask):
        # roll phase to create delayed copy
        phase_shifted = np.roll(phase, -lag_samples)
        # valid samples must be valid in both original and shifted positions
        valid_both = valid_mask & np.roll(valid_mask, -lag_samples)
        if valid_both.sum() == 0:
            return np.nan
        phase_diff = phase[valid_both] - phase_shifted[valid_both]
        return np.abs(np.mean(np.exp(1j * phase_diff)))

    lag_samps = (np.array(lags) * fs).astype(int)
    plv = np.array([plv_at_lag(ls, phase, valid) for ls in lag_samps])

    # 4) simple surrogate test: random circular shifts of phase to destroy temporal structure
    surrogates = np.zeros((n_surrogates, len(lag_samps)))
    rng = np.random.default_rng(0)
    for s in range(n_surrogates):
        shift = rng.integers(low=fs//2, high=N-1)  # random shift
        phase_surr = np.roll(phase, shift)
        for i, ls in enumerate(lag_samps):
            # compute surrogate PLV between original and surrogate shifted by lag
            # ensure valid samples for both
            valid_both = valid & np.roll(valid, -ls)
            if valid_both.sum() == 0:
                surrogates[s, i] = np.nan
            else:
                phase_diff_s = phase[valid_both] - np.roll(phase_surr, -ls)[valid_both]
                surrogates[s, i] = np.abs(np.mean(np.exp(1j * phase_diff_s)))

    # compute surrogate mean and 95th percentile
    sur_mean = np.nanmean(surrogates, axis=0)
    sur_95 = np.nanpercentile(surrogates, 95, axis=0)

    return {
        'lags': lags,
        'plv': plv,
        'amp': amp,
        'valid_mask': valid,
        'sur_mean': sur_mean,
        'sur_95': sur_95
    }

# ---------------------------
# simulate a signal: flat then rhythmic
fs = 500
t = np.arange(0, 10, 1/fs)
signal = np.zeros_like(t)
# flat for first 3 s, then a 10 Hz burst between 3-7s, then flat
signal += 0.01 * np.random.randn(len(t))  # low-level noise always present
idx = (t >= 3) & (t < 7)
signal[idx] += 1.0 * np.sin(2*np.pi*10*t[idx]) + 0.1*np.random.randn(idx.sum())

# compute pACF (PLV vs lag)
out = compute_plv_phase_autocorr(signal, fs, low=8, high=12, lags=np.arange(0, 0.5, 1/fs),
                                amp_thresh_pct=50, n_surrogates=300)

# plot results
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.plot(t, signal, label='raw signal')
plt.plot(t, out['amp']/np.max(out['amp']) * (signal.max()-signal.min()) + signal.min(),
         label='norm amp env (scaled)', alpha=0.6)
plt.axvspan(3,7,color='orange',alpha=0.1,label='rhythmic window')
plt.legend()
plt.title('Signal and amplitude envelope (scaled)')

plt.subplot(2,1,2)
lags = out['lags']
plt.plot(lags, out['plv'], label='PLV (masked)')
plt.plot(lags, out['sur_mean'], '--', label='Surrogate mean')
plt.fill_between(lags, out['sur_mean'], out['sur_95'], color='gray', alpha=0.3, label='surrogate 95th pct')
plt.xlabel('Lag (s)')
plt.ylabel('PLV / pACF')
plt.legend()
plt.tight_layout()
plt.show()