import statistics
from scipy import stats
from datetime import datetime
import math
from ..core.functions import extract_data
from ..core.api.stats import getCurrentPrice
from ..core.api.historical import getHistoricalData
from ..fintwit.tweet import send_tweet, translate_data
from .functions import *
from .output import exportFractal, outputTable
import sys
from tabulate import tabulate

# For full detailed explanation on the calculation, visit:
# https://blogs.cfainstitute.org/investor/2013/01/30/rescaled-range-analysis-a-method-for-detecting-persistence-randomness-or-mean-reversion-in-financial-markets/


def collect_key_stats(ticker, timeframe):
    """
    This is the initial process of building out the key statistics to be inserted into the fractal calculator.
    Processes:
    1. Fetch max historical price data from IEX.
    2. Break list of prices into chunks based on exponential or linear scales, (see exponential_scales() function).
    3. Calculate key lists of data: daily returns, daily deviations from the means, and daily running totals. 
       Data will be organized into chunks based on scale.
    4. Calculate key statistics from returns, deviations, and running totals for each scale, (min, max, mean, range, stdev)
    5. Calculate the rescaled range from the standard deviations of returns of each scale.
    6. Calculate necessary stats for final rescale range analysis, gets log10 values of rescaled ranges

    Parameters
    ----------
    ticker      :str
                 stock ticker, stock data is retrieved from IEX Data

    Returns
    -------
    dict, dict
        Returns dict of scales with number of items in each scale.
        Returns dict of key stats to be used in final rescale range analysis calculation.
    """
    asset_prices = getHistoricalData(ticker, timeframe, True)
    if (asset_prices):
        prices = list(reversed(extract_data(asset_prices, 'close')))

        count = len(prices)

        # Arbitrary fractal scales
        scales = exponential_scales(count, 2, 6)
        # print(json.dumps(scales, indent=1))

        returns = returns_calculator(prices)
        deviations = deviations_calculator(returns, scales)
        running_totals = running_totals_calculator(deviations, scales)

        # Calculating statistics of returns and running totals
        range_stats = {}
        for scale, days in scales.items():
            range_stats[scale] = {}
            range_stats[scale]['means'] = chunked_averages(returns, days)
            range_stats[scale]['stDevs'] = chunked_devs(returns, days)
            range_stats[scale]['minimums'] = chunked_range(running_totals[scale], days)['minimum']
            range_stats[scale]['maximums'] = chunked_range(running_totals[scale], days)['maximum']
            range_stats[scale]['ranges'] = chunked_range(running_totals[scale], days)['range']

        # Calculating Rescale Range
        for scale, values in range_stats.items():
            range_stats[scale]['rescaleRanges'] = {}
            for i, value in values['ranges'].items():
                rescaleRange = (value / values['stDevs'][i] if (values['stDevs'][i] != 0) else 0)

                range_stats[scale]['rescaleRanges'][i] = rescaleRange

        # Key stats for fractal calculations
        for scale, values in range_stats.items():
            range_stats[scale]['keyStats'] = {}
            rescaleRanges = list(values['rescaleRanges'].values())
            range_stats[scale]['keyStats']['rescaleRangeAvg'] = statistics.mean(rescaleRanges)  # This is the rescaled range
            range_stats[scale]['keyStats']['size'] = scales[scale]
            range_stats[scale]['keyStats']['logRR'] = math.log10(statistics.mean(rescaleRanges)) if (statistics.mean(rescaleRanges) > 0) else 0
            range_stats[scale]['keyStats']['logScale'] = math.log10(scales[scale])

        return scales, range_stats, asset_prices
    else:
        print('Prices returned nil')
        sys.exit()


def perform_hurst_calculations(x, y, asset_prices):
    """
    This function performs hurst fractal calculations based on key stats returned from collect_key_stats()
    Processes:
    1. Organize data into arbitrary or practical ways of viewing the data. Currently two options, classic view or view
       I've optimized for short term stock market analysis: 
        basic_fractal_sections()
        trading_fractal_sections()
    2. Calculate linear regression from log10 scales and log10 rescaled ranges


    Parameters
    ----------
    x      :list
            list of log10 values for each chunk in scale
    y      :list
            list of log10 values for each chunk in scale

    Returns
    -------
    dict
        Returns dict linear regression statistics containing:
            hurstExponent, fractalDimension, r-squared, p-value, standardError
    """
    # Set how you want data to be organized
    sections = standard_fractal_sections(x, y, asset_prices)

    results = {}
    for i, section in sections.items():
        slope, intercept, r_value, p_value, std_err = stats.linregress(section['x'], section['y'])
        results[i] = {
            'hurstExponent': round(slope, 2),
            'fractalDimension': round((2 - slope), 2),
            'r-squared': round(r_value**2, 2),
            'p-value': round(p_value, 2),
            'standardError': round(std_err, 2)
        }
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    results['fullSeries'] = {
        'hurstExponent': round(slope, 2),
        'fractalDimension': round((2 - slope), 2),
        'r-squared': round(r_value**2, 2),
        'p-value': round(p_value, 2),
        'standardError': round(std_err, 2)
    }
    return results


def fractal_calculator(ticker, timeframe, output, sendtweet):
    """
    Main process thread. Will call on collect_key_stats() and perform_hurst_calculations()

    Parameters
    ----------
    ticker      :str
                 stock ticker, stock data is retrieved from IEX Data
    output      :str
                 Can either be table, csv, or tweet
                 (output always goes to table in terminal, table param ensures it only goes to table.)

    Returns
    -------
    dict
        Returns fractal statistics and can export to csv, output to terminal and tweet

    """
    scales, range_stats, asset_prices = collect_key_stats(ticker, timeframe)

    # Hurst Exponent Calculations
    fractal_results = {
        'rescaleRange': {}
    }
    # Adding rescale ranges to final data
    for scale, days in scales.items():
        fractal_results['rescaleRange'][scale] = round(range_stats[scale]['keyStats']['rescaleRangeAvg'], 2)

    # Calculating linear regression of rescale range logs
    log_RRs = scaled_data_collector(scales, range_stats, ['keyStats', 'logRR'])
    log_scales = scaled_data_collector(scales, range_stats, ['keyStats', 'logScale'])
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_scales, log_RRs)

    # Results
    fractal_results['regressionResults'] = perform_hurst_calculations(log_scales, log_RRs, asset_prices)
    outputTable(fractal_results, scales)  # Output will always go to table in terminal as well.

    # Tweet
    
    if (sendtweet):
        tweet_data = {}
        for scale, data in fractal_results['regressionResults'].items():
            if ("-" in scale):
                removeSeries = scale.replace("Series", "")
                textndate = removeSeries.split('(')
                dates = textndate[1].replace(')', "").split(' - ')
                start = datetime.strptime(dates[0], '%Y-%m-%d').strftime('%b %Y')
                end = datetime.strptime(dates[1], '%Y-%m-%d').strftime('%b %Y')
                key = textndate[0] + '({} - {})'.format(start, end)
            else: 
                key = scale

            tweet_data[key] = data['hurstExponent']
        
        headline = "${} {} Hurst Exponents\n".format(ticker, timeframe)
        tweet = headline + translate_data(tweet_data)
        send_tweet(tweet)



    # CSV Output
    if (output == 'csv'):
        exportFractal(fractal_results, scales)

