try:
    '''from translators.server import *

    text='This is the full text. I wonder if it works.'

    with open('sanskrit.txt', 'wt', encoding='utf-16') as file:
        translated = google(query_text=text,to_language='sa')
        print(translated)
        file.write(translated)
        file.close()
    '''
    # Import modules
    from translators.server import *
    from rouge_scoring.utils_nlp.eval.rouge.compute_rouge import *
    import pandas as pd
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import tqdm
    import time
    import csv
    import os

    # Set constants  
    STARTINDEX = 0
    BATCHSIZE = 10
    PATH = None # Specify your file path here

    if PATH == None:
        raise Exception("PATH must be specified")

    # Initiate errors_logged_text
    errors_logged_text = 0

    # Define functions
    # Remove elements where text/summary has a length greater than 5000 characters
    def validate_database(data):
        # Make sure lengths are equal
        if len(data["texts"]) != len(data["ideal_summaries"]):
                raise Exception("Database is invalid.")
        
        # Remove elements where text/summary has a length greater than 5000 characters
        i = 0
        total_removed = 0
        while (i < len(data["texts"])):
            # Remove "\n" characters
            data["texts"][i] = data["texts"][i].replace("\n", " ")

            # Remove elements where text/summary has a length greater than 5000 characters
            if len(data["texts"][i]) >= 5000 or len(data["ideal_summaries"][i]) >= 5000:
                data["texts"].pop(i)
                data["ideal_summaries"].pop(i)
                # print("Invalid data point removed at index " + str(i))
                total_removed += 1
            else:
                i += 1
        print("Total entries removed: " + str(total_removed))
        return data

    
    # Translate list of texts using Google Translate
    def translate_texts(texts, to_language):
        translated_texts = []
        for text in tqdm.tqdm(texts):
            # Add translated text to list
            error_count = 0
            while True:
                try:
                    translated = google(query_text=text, to_language=to_language)
                    break
                except Exception as e:
                    print("An error occurred while translating the following text:")
                    print(str(e))
                    print(type(text))
                    print(text)
                    print(to_language)
                    error_count += 1
                    print("Error count: " + str(error_count))
                    time.sleep(10)
                    if error_count == 10:
                        raise Exception("Too many errors occurred while translating text.")

            # Combine paragraphs into one string
            if type(translated) == list:
                for para in translated[1:]:
                    new = translated[0] + para
            else:
                new = translated

            # Fix issues in translated text and add to final list
            translated_texts.append(new)

            time.sleep(0.25)

        return translated_texts

    # Import text-summary pairs from CSV
    files = ["cnn_dailymail"]
    for filename in files:
        raw_data = pd.read_csv(
            r'{path}{filename}.csv'.format(path=PATH, filename=filename))

        # Summarize and translate text-summary pairs in batches of size batch_size
        for i in range(STARTINDEX, len(raw_data["article"].tolist()), BATCHSIZE):
            # Initialize/Reset structure to store data
            data = {"sanskrit": {"texts": [], "ideal_summaries": [], "generated_summaries": []}, 
                    "english": {"texts": [], "ideal_summaries": [], "generated_summaries": []}}

            # Update file name for each iteration 
            file = filename + "_" + str(i)

            # Place text-summary pairs into dictionary
            data["english"]["texts"] = raw_data["article"].tolist()[i:(i+BATCHSIZE)]
            data["english"]["ideal_summaries"] = raw_data["highlights"].tolist()[i:(i+BATCHSIZE)]

            # Validate
            data["english"] = validate_database(data["english"])

            # Translate texts and summaries to Sanskrit
            data["sanskrit"]["texts"] = translate_texts(data["english"]["texts"], "sa")
            data["sanskrit"]["ideal_summaries"] = translate_texts(data["english"]["ideal_summaries"], "sa")

            # Summarize the texts through the LongT5 model
            for text in tqdm.tqdm(data["english"]["texts"]):
                tokenizer = AutoTokenizer.from_pretrained(
                    "google/long-t5-tglobal-base")

                model = AutoModelForSeq2SeqLM.from_pretrained(
                    "google/long-t5-tglobal-base")

                encoding = tokenizer(text,
                                    padding='max_length',
                                    max_length=672,
                                    truncation=True,
                                    return_tensors='pt')

                decoded_ids = model.generate(input_ids=encoding['input_ids'],
                                            attention_mask=encoding['attention_mask'],
                                            max_length=512,
                                            top_p=.9,
                                            do_sample=True)

                generated_summary = tokenizer.decode(
                    decoded_ids[0], skip_special_tokens=True)

                data["english"]["generated_summaries"].append(generated_summary)

            # Translate the outputted summaries to Sanskrit
            data["sanskrit"]["generated_summaries"] = translate_texts(data["english"]["generated_summaries"], "sa")

            print(data)

            print("Total number of errors logged: " + str(errors_logged_text))            
            time.sleep(60)

except KeyboardInterrupt:
    import time
    print(time.localtime())

