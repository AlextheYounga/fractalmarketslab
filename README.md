Commands:

<!-- Donchian -->
python -c 'from fractalmarketslab.donchian.calculator import calculate; print(calculate("CHWY"))'
<!-- Value at Risk -->
python -c 'from fractalmarketslab.VaR.calculator import variancecovarianceVaR; print(variancecovarianceVaR("SPY"))'
<!-- Volatility -->
python -c 'from fractalmarketslab.volatility.calculator import calculate; print(calculate("SPY"))'
<!-- Signal -->
python -m fractalmarketslab.signal.scan_portfolio
python -c 'from fractalmarketslab.signal.lookup import lookup_signal; print(lookup_signal("EDV"))'
<!-- Trend -->
python -c 'from fractalmarketslab.trend.analyze import analyze; print(analyze("SPY"))'