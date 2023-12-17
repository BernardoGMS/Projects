import numpy as np
import os
import csv
import pandas as pd
import random as rd

df = pd.read_csv("jef_data.csv")

print(df.head())

print(df.corr())