# src/claws/night_stalk_v1_5.py
import numpy as np

class NightStalk:
    """
    Module: Night Stalk (Claw A)
    Logic: Momentum Breakdown & Liquidity Cliff Execution.
    Objective: Execute shorts when structural support collapses with high volume.
    """
    def __init__(self):
        self.vol_spike_threshold = 2.5    # Trigger when volume is 2.5x baseline
        self.support_zone = None          # Dynamically calibrated local floor
        self.is_hunting = True

    def scan_breakdown_signal(self, price_data, volume_data, local_low):
        """
        Identifies the 'Liquidity Cliff': High volume + price breaking local support.
        """
        current_price = price_data[-1]
        current_vol = volume_data[-1]
        avg_vol = np.mean(volume_data[-20:]) # 20-period baseline volume

        # The "Pounce" Condition: 
        # 1. Price penetrates the recently established local floor.
        # 2. Volume expansion confirms institutional/panic exit (>2.5x avg).
        if current_price < local_low:
            if current_vol > avg_vol * self.vol_spike_threshold:
                return "SIGNAL: LIQUIDITY_CLIFF_CONFIRMED | INITIATE_SHORT"
        
        return "STATUS: STALKING_SUPPORT_INTEGRITY"

    def calculate_exit(self, entry_price, volatility_index):
        # Dynamic take-profit based on exhaustion of the downward move
        return entry_price * (1 - (volatility_index * 0.5))
