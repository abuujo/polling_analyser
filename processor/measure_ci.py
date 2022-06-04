import pandas as pd
from scipy.stats import expon as dist

def measure_ci(df):
    # Remove the % sign 
    df['value'] = df['value'].str.replace('%', '')
    df.value = pd.to_numeric(df.value)

    # Consider the 12 closest neighbouring polls to determine smoothed value
    # Min one to catch latest and earliest polls.
    df["smooth"] = df["value"].rolling(12,min_periods=1,win_type='hamming',center=True).mean()

    # Measure the noise value between the smoothed line and the actual value
    df["noise"] = df["value"] - df["smooth"]

    # Get higher values > 0 for asymetrical conf interval
    upper_noise = df[df["noise"] > 0]["noise"]
    upper_params = dist.fit(upper_noise)

    # Get lower values < 0
    lower_noise = (df[df["noise"] < 0]["noise"]).abs()
    lower_params = dist.fit(lower_noise)

    # 95 % conf interval - range of values we expect 95% of outcomes to be within
    upper_bound_value = dist.ppf(95/100, *upper_params)
    lower_bound_value = dist.ppf(95/100, *lower_params)

    # Add to the smoothed line
    df["ci_top"] = df["smooth"] + upper_bound_value
    df["ci_bot"] = df["smooth"] - lower_bound_value

    return df