# A Translation-Based Approach to Sanskrit Text Summarization with the LongT5 Model

This research was conducted as part of the AP Research program at McDowell High School by Parth Parikh.

## Paper Abstract
As a working approach to abstractive text summarization in the language of Sanskrit does not currently exist, this paper explores an alternative to model retraining for the aforementioned. In general, applying text summarization to Sanskrit can permit a heightened understanding of cultural and historical texts of South Asia while also bettering understandings of other South Asian languages that are based on Sanskrit. This research specifically adopts a translation-based approach to text summarization to allow for the extension of natural language processing applications such as text summarization to low-resource languages that face data scarcity, such as Sanskrit. If this approach via the Google Neural Machine Translation model ultimately proves effective, financial and technological constraints associated with database creation and model retraining in low-resource languages would be alleviated. Unfortunately, however, the translation-based approach detailed in this paper demonstrated a significant loss in the quality of summarization via the translation-based approach in comparison to direct summarization in English when measured by Recall-Oriented Understudy for Gisting Evaluation scores reported by this research. Hence, future research can pursue a model retraining approach to better understand the overall language of Sanskrit and achieve a superior quality of text summarization in the language of Sanskrit.

## Code Specifications
### Database
The database should stored in a CSV file where the first row consists of headings of "article" and "highlights". The name of this file must then be updated in both the main.py and extract_sample.py files. This database should be stored in a folder called "data" in the current directory.

### Find ROUGE Scores and Averages
The main.py script is the primary script that is used to find ROUGE scores on the data. The results thereof will be a breakdown of ROUGE scores calculated on the given sample and two sets of average scores: one when including all scores of 0 and one excluding scores of 0. A "results" folder must be created in the home directory to store the results of this file.

### Cumulative Averages
The final_averages.py file compiles previously found ROUGE scores and provides the average score for each ROUGE metric. Results from this script are stored in a "cumulative" folder within the "results" folder created previously.

### t test Results
IMPORTANT: To run as expected, the calculate_ttest.py file requires ROUGE scores to be compiled into one single file stored in the results folder. The Python file can then be edited to account for its filename.

This script ultimately runs a one-tailed paired t test on the compiled ROUGE scores and prints results to the terminal