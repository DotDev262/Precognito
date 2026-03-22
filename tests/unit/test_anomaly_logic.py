import pytest
import numpy as np

# --- INDUSTRIAL CONSTANTS (From BRD Section 17.2 & 25) ---
HEALTHY_BASELINE_RMS = 2.0  # mm/s
CRITICAL_THRESHOLD_RMS = 6.0 # mm/s
SAMPLING_RATE_HZ = 1000     # 1 kHz as per FR1
FAILURE_HORIZON_LIMIT = 48  # hours (High-Risk Threshold)

# --- CORE LOGIC (To be integrated into Precognito Analytics Suite) ---

def calculate_rms(signal):
    """Calculates the Root Mean Square of the vibration signal."""
    return np.sqrt(np.mean(np.array(signal)**2))

def estimate_rul(current_rms, degradation_rate):
    """
    Simplified RUL estimation based on degradation trend.
    In production, this would be handled by the LSTM model (Module 3).
    """
    if current_rms <= HEALTHY_BASELINE_RMS:
        return 500 # Default healthy life in hours
    
    # Simple linear projection for prototype logic
    remaining_headroom = 10.0 - current_rms # Assuming 10mm/s is total failure
    rul = remaining_headroom / degradation_rate
    return max(0, round(rul, 2))

def classify_severity(rms_value):
    """Classifies machine health based on ISO 10816 standards."""
    if rms_value < HEALTHY_BASELINE_RMS:
        return "GREEN"
    elif rms_value < CRITICAL_THRESHOLD_RMS:
        return "YELLOW"
    else:
        return "RED"

# --- UNIT TESTS (To be run via 'pytest') ---

def test_calculate_rms_accuracy():
    """TC_M1_02: Verify RMS calculation for a standard sine wave."""
    # A sine wave with amplitude 1 has an RMS of ~0.707
    t = np.linspace(0, 1, SAMPLING_RATE_HZ)
    signal = np.sin(2 * np.pi * 50 * t) # 50Hz vibration
    rms = calculate_rms(signal)
    assert pytest.approx(rms, 0.01) == 0.707

def test_anomaly_detection_logic():
    """TC_M2_01: Baseline Deviation Detection (Critical State)."""
    critical_signal = [6.8] * 100 # Simulated high vibration
    rms = calculate_rms(critical_signal)
    severity = classify_severity(rms)
    
    assert rms > CRITICAL_THRESHOLD_RMS
    assert severity == "RED"

def test_normal_condition_validation():
    """TC_M2_03: Verify that healthy machines are marked Green."""
    healthy_signal = [1.2] * 100
    rms = calculate_rms(healthy_signal)
    severity = classify_severity(rms)
    
    assert rms < HEALTHY_BASELINE_RMS
    assert severity == "GREEN"

def test_rul_prediction_logic():
    """TC_M3_01: Verify RUL calculation for a degrading asset."""
    # Machine vibrating at 7mm/s with a 0.1mm/s per hour degradation
    current_rms = 7.0
    deg_rate = 0.1
    rul = estimate_rul(current_rms, deg_rate)
    
    # (10.0 - 7.0) / 0.1 = 30 hours
    assert rul == 30.0
    assert rul < FAILURE_HORIZON_LIMIT # Should trigger US-2.1 alert

def test_edge_sampling_capacity():
    """Verify that the logic can handle 1000 samples (1kHz) without error."""
    large_signal = np.random.normal(0, 1, SAMPLING_RATE_HZ)
    try:
        calculate_rms(large_signal)
    except Exception as e:
        pytest.fail(f"RMS calculation failed at 1kHz sampling rate: {e}")

if __name__ == "__main__":
    print("Precognito Analytics Suite: Running local logic verification...")
    # This block allows running the script directly
    pytest.main([__file__])
