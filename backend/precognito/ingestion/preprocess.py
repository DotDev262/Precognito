import logging

logger = logging.getLogger(__name__)

def preprocess(data: dict) -> dict:
    """
    Standardize and clean incoming sensor data.
    """
    processed = {}
    
    # Required fields mapping
    mapping = {
        "temperature": ["temperature", "temp", "temp_c", "Air temperature [K]"],
        "vibration": ["vibration", "vib", "rotational_speed", "Rotational speed [rpm]"],
        "pressure": ["pressure", "press", "psi"],
        "torque": ["torque", "Torque [Nm]"],
        "tool_wear": ["tool_wear", "Tool wear [min]"]
    }

    for key, aliases in mapping.items():
        val = None
        for alias in aliases:
            if alias in data:
                val = data[alias]
                break
        
        if val is not None:
            try:
                processed[key] = round(float(val), 2)
            except (ValueError, TypeError):
                logger.warning(f"Failed to convert {key} value: {val}")
                processed[key] = 0.0
        else:
            # Default values if not present (could also leave out)
            processed[key] = 0.0

    return processed
