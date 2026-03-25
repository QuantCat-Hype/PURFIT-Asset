# src/claws/pounce_strike_v1_5.py

class PounceStrike:
    """
    Module: Pounce Strike (Claw B)
    Logic: Dynamic Rebalancing & Support Hardening.
    Focus: Managing $HYPE leverage to subsidize $PURFIT floor liquidity.
    """
    def __init__(self, leverage=10, usdc_allocation=0.10):
        self.leverage = leverage            # 10x HYPE Long
        self.usdc_ratio = usdc_allocation   # 10% USDC Reserve
        self.grid_levels = 5                # Progressive buy-down layers
        self.floor_price = 0.000000059      # Calibrated Epoch 0.25 Floor
        
    def calculate_rebalance_trigger(self, current_hype_pnl, purfit_price):
        """
        Determines if HYPE profits should be rotated into $PURFIT buybacks.
        """
        # Logic: If HYPE PnL exceeds threshold, lock partial profit for $PURFIT support
        if current_hype_pnl > 0.05: # 5% move on 10x leverage is 50% ROI
            return "SIGNAL: ROTATE_HYPE_PROFIT_TO_PURFIT"
            
        # Logic: Grid Buy-down if $PURFIT hits support zones
        if purfit_price <= self.floor_price:
            return "SIGNAL: EXECUTE_GRID_BUY_STEP"
            
        return "STATUS: MAINTAINING_LEVERAGE_EXPOSURE"

    def execute_grid_logic(self, current_price, balance_usdc):
        """
        Calculates the weighted buy order based on grid depth.
        """
        if balance_usdc <= 0:
            return "ERROR: INSUFFICIENT_RESERVE"
            
        # Progressive allocation: Buying more as price drops further below floor
        buy_amount = balance_usdc * 0.20 # Deploy 20% of reserve per grid step
        return f"ACTION: DEPLOY_{buy_amount}_USDC_AT_{current_price}"

    def take_profit_scaling(self, purfit_price, entry_price):
        """
        Maintains the 10% USDC ratio by scaling out of $PURFIT on rallies.
        """
        if purfit_price > entry_price * 1.15: # 15% Rally
            return "ACTION: SCALE_OUT_TO_REFRESH_USDC_RESERVE"
        return "STATUS: HOLDING_ALPHA_POSITION"
