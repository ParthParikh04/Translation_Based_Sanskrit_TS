import pandas as pd
from statistics import mean
import scipy.stats as stats
import os
import csv

# Load data
with open(os.path.join("results", "scores_english_cnn_dailymail.csv"), "r") as f:
    reader = csv.reader(f)
    english_data = list(reader)

with open(os.path.join("results", "scores_sanskrit_cnn_dailymail.csv"), "r") as f:
    reader = csv.reader(f)
    sanskrit = list(reader)

# Initialize dictionaries
english_scores = {'rouge-1': {'r': [], 'p': [], 'f': []}, 'rouge-l': {'r': [], 'p': [], 'f': []}, 'rouge-2': {'r': [], 'p': [], 'f': []}}
sanskrit_scores = {'rouge-1': {'r': [], 'p': [], 'f': []}, 'rouge-l': {'r': [], 'p': [], 'f': []}, 'rouge-2': {'r': [], 'p': [], 'f': []}}

# Add scores to list
for row in english_data[2:]:
    for i in range(len(row)):
        score = row[i]
        # Convert score to float
        try:
            score = float(score)
        except:
            raise ValueError("Score is not a floating point number")
        
        english_scores[english_data[0][i]][english_data[1][i]].append(score)

for row in sanskrit[2:]:
    for i in range(len(row)):
        score = row[i]
        # Convert score to float
        try:
            score = float(score)
        except:
            raise ValueError("Score is not a floating point number")
        
        sanskrit_scores[sanskrit[0][i]][sanskrit[1][i]].append(score)

# Print t-test results
for metric in english_scores:
    for scores in english_scores[metric]:
        print(metric, scores)
        print("English Mean:")
        print(mean(english_scores[metric][scores]))
        print("Sanskrit Mean:")
        print(mean(sanskrit_scores[metric][scores]))
        print(stats.ttest_rel(english_scores[metric][scores], sanskrit_scores[metric][scores], alternative='greater'))
