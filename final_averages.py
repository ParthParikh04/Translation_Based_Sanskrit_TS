import csv
import os 

STARTINDEX = 0
BATCHSIZE = 500

# Define function
def write_scores(scores, filename):
    print(scores)
    with open(os.path.join("results", os.path.join("cumulative", "{filename}.csv".format(filename=filename))), "w", newline="") as ind_csv_file:
        ind_csvwriter = csv.writer(ind_csv_file)
        ind_csvwriter.writerow(["rouge-1", "rouge-1", "rouge-1", "rouge-l",
                                "rouge-l", "rouge-l", "rouge-2", "rouge-2", "rouge-2"])
        ind_csvwriter.writerow(["r", "p", "f", "r", "p", "f", "r", "p", "f"])

        metrics = ["rouge-1", "rouge-l", "rouge-2"]

        for rouge in scores:
            row = []
            for score in metrics:
                row += rouge[score].values()
            ind_csvwriter.writerow(row)

files = ["cnn_dailymail"]
for file in files:    
    # Go through the code for english and sanskrit
    for language in ["english", "sanskrit"]:
        # Initialize dictionaries
        totals = {'rouge-1': {'r': 0, 'p': 0, 'f': 0}, 'rouge-l': {'r': 0, 'p': 0, 'f': 0}, 'rouge-2': {'r': 0, 'p': 0, 'f': 0}}
        averages_with_zeros = {'rouge-1': {'r': 0, 'p': 0, 'f': 0}, 'rouge-l': {'r': 0, 'p': 0, 'f': 0}, 'rouge-2': {'r': 0, 'p': 0, 'f': 0}}
        averages_without_zeros = {'rouge-1': {'r': 0, 'p': 0, 'f': 0}, 'rouge-l': {'r': 0, 'p': 0, 'f': 0}, 'rouge-2': {'r': 0, 'p': 0, 'f': 0}}
        score_count = 0
        zero_count = 0
        file_count = STARTINDEX

        # Go through full data for each file
        while True:
            filename = "scores_" + language + "_" + file + "_" + str(file_count) + ".csv"
            print(filename)
            if (not os.path.isfile(os.path.join("results", filename))):
                print("DNE")
                break
            
            # Load data
            with open(os.path.join("results", filename), "r") as f:
                reader = csv.reader(f)
                data_list = list(reader)
            file_count += BATCHSIZE

            # Update counts
            score_count += len(data_list[2:])

            # Add scores to running total
            for row in data_list[2:]:
                all_zeros = True
                for i in range(len(row)):
                    score = row[i]
                    # Convert score to float
                    try:
                        score = float(score)
                    except:
                        raise ValueError("Score is not a floating point number")
                    
                    # Update zero score count
                    if score != 0:
                        all_zeros = False
                    else:
                        continue

                    totals[data_list[0][i]][data_list[1][i]] += score
                
                zero_count += 1 if all_zeros else 0
        
        # Return if it is empty
        if score_count == 0:
            continue

        # Calculate averages
        for rouge in totals:
            for metric in totals[rouge].keys():
                averages_without_zeros[rouge][metric] = totals[rouge][metric] / (score_count - zero_count)
                averages_with_zeros[rouge][metric] = totals[rouge][metric] / score_count

        # Print details
        print("Total scores: " + str(score_count))
        print("Total zero scores: " + str(zero_count))

        # Write averages to file
        write_scores([averages_with_zeros], str(STARTINDEX) + "_" + str(file_count) + "_averages_with_zeros_" + language + "_" + file + ".csv")
        write_scores([averages_without_zeros], str(STARTINDEX) + "_" + str(file_count) + "_averages_without_zeros_" + language + "_" + file)
    