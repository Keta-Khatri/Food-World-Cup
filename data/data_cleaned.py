import dash_design_kit as ddk
from matplotlib.pyplot import figure
import pandas as pd

# Global access to data collected. Data can be manipulated during callbacks.
# Initial load time high, but refresh time is minimized.
df = pd.read_csv("food-world-cup-data.csv")

# Cleaning data to remove redundant rows.
df.dropna(thresh=8, inplace=True)
df.columns = df.columns.str.replace(
    "Please rate how much you like the traditional cuisine of ", ""
)
df.columns = df.columns.str.replace(".", "")

df.to_csv("data_cleaned.csv", index=False)
