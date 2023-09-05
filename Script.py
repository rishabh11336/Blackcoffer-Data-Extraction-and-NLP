# Importing necessary libraries
from bs4 import BeautifulSoup
import time
import csv
import requests
import pandas as pd
import numpy as np
import string
import nltk
import re
from nltk.tokenize import word_tokenize
import glob
# Import the CMU Pronouncing Dictionary from the NLTK corpus
from nltk.corpus import cmudict
# Download the CMU Pronouncing Dictionary data if not already downloaded
nltk.download('cmudict')
nltk.download('punkt')

# Opening or creating a CSV file named 'result.csv' in append mode for writing
# 'newline='': This parameter ensures that the new rows are properly separated with no extra newline characters
# 'encoding='utf-8'': This parameter specifies the character encoding for the file
with open('result.csv', 'a', newline='', encoding='utf-8') as resfile:
    # Creating a CSV writer object for the 'result.csv' file
    csv_writer = csv.writer(resfile)
    
    # Writing a header row in the CSV file with column names: 'URL_ID', 'URL', and 'TEXT'
    csv_writer.writerow(['URL_ID', 'URL', 'TEXT'])
    
    # Opening the CSV file named 'Input.csv' in read mode
    with open('Input.csv', mode='r') as file:
        # Creating a CSV reader object for the 'Input.csv' file
        csvFile = csv.reader(file)
        
        # Iterating through each row (line) in the CSV file
        for lines in csvFile:
            # Initializing an empty string to store extracted text from the web page
            extracted_text = ""
            
            # Making a GET request to the URL provided in the CSV's second column
            x = requests.get(lines[1])
            
            # Parsing the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(x.content, "html.parser")
            
            # Extracting all <p> elements from the parsed HTML
            p_elements = soup.find_all('p')
            
            # Looping through <p> elements to extract text content (skipping the first 16 and last 4 elements)
            for p_element in p_elements[16:-4]:
                extracted_text += p_element.get_text()
            
            # Creating a list of data to write into the 'result.csv' file: URL_ID, URL, and extracted text
            data = [lines[0], lines[1], extracted_text]
            
            # Writing the data list as a new row in the 'result.csv' file
            csv_writer.writerow(data)

# Reading the contents of 'result.csv' and storing it in a DataFrame named 'df'
df = pd.read_csv('result.csv')

# Creating a list called 'Documents'
# For each 'doc' in the 'TEXT' column of the DataFrame 'df':
# - If 'doc' is a non-empty string (not equal to 'nan'), tokenize it into words using word_tokenize
# - Otherwise, add an empty list
Documents = [word_tokenize(doc) if isinstance(doc, str) and doc.lower() != 'nan' else [] for doc in df['TEXT']]

# Using the glob library to find file paths matching the pattern "StopWords/*.txt"
stop_word_files = glob.glob("StopWords/*.txt")

# Creating an empty list to store stop words
stop_words = []

# Looping through each file path found by glob
for file_path in stop_word_files:
    # Opening the file in read mode using 'latin-1' encoding
    with open(file_path, 'r', encoding='latin-1') as file:
        # Reading the entire content of the file
        content = file.read()
        # Splitting the content into individual words using '\n' as the delimiter
        words = content.split('\n')
        # Extending the stop_words list with the words from the file
        stop_words.extend(words)


# (stop_words contains a list of tokenized stop words)

# Creating an empty list to store the refined stop words
final_stop_words = []

# Iterating through each tokenized stop word in the stop_words list
for doc in stop_words:
    # Checking if the tokenized stop word is a non-empty string and not equal to 'nan'
    if isinstance(doc, str) and doc.lower() != 'nan':
        # Extending the final_stop_words list with the tokenized words from the current stop word
        final_stop_words.extend(word_tokenize(doc))

# Converting the list of tokenized words to a set to remove duplicates,
# and then converting it back to a list
final_stop_words = list(set(final_stop_words))

# Creating an empty list named 'all_Documents' to store processed documents
all_Documents = []

# Iterating through each tokenized document in the 'Documents' list
for doc in Documents:
    list_of = []  # A temporary list to store words for the current document
    
    # Iterating through each word in the current tokenized document
    for word in doc:
        # Checking conditions to determine whether to include the word
        if (
            (word.lower() not in final_stop_words or word.upper() not in final_stop_words) and
            len(word) != 1 and len(word) != 2 and
            word[0] != "'" and word != "n't" and word[0] != "."
        ):
            list_of.append(word.lower())  # Adding the word to the temporary list
    
    # Adding the processed list of words for the current document to 'all_Documents'
    all_Documents.append(list_of)

# (positive_words contains a list of positive word strings)

# Using the glob library to find file paths matching the pattern "MasterDictionary/positive-words.txt"
positive_word_files = glob.glob("MasterDictionary/positive-words.txt")

# Creating an empty list to store positive words
positive_words = []

# Looping through each file path found by glob
for file_path in positive_word_files:
    # Opening the file in read mode using 'latin-1' encoding
    with open(file_path, 'r', encoding='latin-1') as file:
        # Reading the entire content of the file
        content = file.read()
        # Splitting the content into individual words using '\n' as the delimiter
        words = content.split('\n')
        # Extending the positive_words list with the words from the file
        positive_words.extend(words)

# Creating an empty list to store positive scores
positive_score = []

# Iterating through each processed document in the 'all_Documents' list
for text in all_Documents:
    score = 0  # Initializing the score for the current document
    
    # Iterating through each word in the processed document
    for word in text:
        # Checking if the word is in the list of positive words
        if word in positive_words:
            score += 1  # Incrementing the score if the word is positive
    
    # Adding the calculated score for the current document to 'positive_score'
    positive_score.append(score)


# Adding the 'POSITIVE SCORE' column to the DataFrame and assigning the 'positive_score' list to it
df['POSITIVE SCORE'] = positive_score

# (negative_words contains a list of negative word strings)

# Using the glob library to find file paths matching the pattern "MasterDictionary/negative-words.txt"
negative_word_files = glob.glob("MasterDictionary/negative-words.txt")

# Creating an empty list to store negative words
negative_words = []

# Looping through each file path found by glob
for file_path in negative_word_files:
    # Opening the file in read mode using 'latin-1' encoding
    with open(file_path, 'r', encoding='latin-1') as file:
        # Reading the entire content of the file
        content = file.read()
        # Splitting the content into individual words using '\n' as the delimiter
        words = content.split('\n')
        # Extending the negative_words list with the words from the file
        negative_words.extend(words)


negative_score = []

# Iterating through each processed document in the 'all_Documents' list
for text in all_Documents:
    score = 0  # Initializing the score for the current document
    
    # Iterating through each word in the processed document
    for word in text:
        # Checking if the word is in the list of negative words
        if word in negative_words:
            score += 1  # Incrementing the score if the word is negative
    
    # Adding the calculated score for the current document to 'negative_score'
    negative_score.append(score)

# Adding the 'NEGATIVE SCORE' column to the DataFrame and assigning the 'negative_score' list to it
df['NEGATIVE SCORE'] = negative_score

# Adding the 'POLARITY SCORE' column to the DataFrame
# Calculating the polarity score using the formula and assigning it to the new column
df['POLARITY SCORE'] = (df['POSITIVE SCORE'] - df['NEGATIVE SCORE']) / (df['POSITIVE SCORE'] + df['NEGATIVE SCORE'] + 0.000001)

# Adding the 'SUBJECTIVITY SCORE' column to the DataFrame and initializing all values to 0
df['SUBJECTIVITY SCORE'] = 0

# Iterating through the DataFrame using index 'i'
for i in range(len(df['SUBJECTIVITY SCORE'])):
    # Calculating the subjectivity score using the formula and assigning it to the 'SUBJECTIVITY SCORE' column
    df['SUBJECTIVITY SCORE'][i] = (df['POSITIVE SCORE'][i] + df['NEGATIVE SCORE'][i]) / (len(all_Documents[i]) + 0.000001)


# Adding the 'AVG SENTENCE LENGTH' column to the DataFrame and initializing all values to 0
df['AVG SENTENCE LENGTH'] = 0
# Iterating through the DataFrame using index 'i'
for i in range(len(df['URL_ID'])):
    if isinstance(df['TEXT'][i], str) and df['TEXT'][i].lower() != 'nan':
        # Extract the paragraph from the 'TEXT' column
        paragraph = df['TEXT'][i]
        
        # Split the paragraph into sentences
        sentences = re.split(r'(?<=[.!?]) +', paragraph)
        
        # Initialize variables to count words and sentences
        total_words = 0
        total_sentences = len(sentences)
        
        # Count words in each sentence
        for sentence in sentences:
            words = sentence.split()
            total_words += len(words)
        
        # Calculate the average sentence length
        average_sentence_length = total_words / total_sentences
        
        # Assign the calculated average sentence length to the 'AVG SENTENCE LENGTH' column
        df['AVG SENTENCE LENGTH'][i] = average_sentence_length
    else:
        df['AVG SENTENCE LENGTH'][i] = 0


# Load the CMU Pronouncing Dictionary into a variable
pronouncing_dict = cmudict.dict()

# Define a function to count syllables in a word
def count_syllables(word):
    if word.lower() in pronouncing_dict:
        # For each pronunciation of the word in the dictionary, count syllables
        return max([len([y for y in x if y[-1].isdigit()]) for x in pronouncing_dict[word.lower()]])
    else:
        return 0
    
# Creating an empty list to store the count of complex words for each document
count_complexWord = []

# Iterating through each processed document in the 'all_Documents' list
for words in all_Documents:
    # Finding complex words (words with more than two syllables)
    complex_words = [word for word in words if count_syllables(word) > 2]
    
    # Adding the count of complex words for the current document to the list
    count_complexWord.append(len(complex_words))


# Creating an empty list to store the percentage of complex words for each document
PERCENTAGE_OF_COMPLEX_WORDS = []

# Iterating through the indices of 'count_complexWord' (assuming it has the same length as 'all_Documents')
for i in range(len(count_complexWord)):
    try:
        # Calculate the percentage of complex words in the document
        percentage = (count_complexWord[i] / len(all_Documents[i])) * 100
        PERCENTAGE_OF_COMPLEX_WORDS.append(percentage)
    except:
        # If there's an exception (e.g., division by zero), append 0
        PERCENTAGE_OF_COMPLEX_WORDS.append(0)

# Adding the 'PERCENTAGE OF COMPLEX WORDS' column to the DataFrame and assigning the 'PERCENTAGE_OF_COMPLEX_WORDS' list to it
df['PERCENTAGE OF COMPLEX WORDS'] = PERCENTAGE_OF_COMPLEX_WORDS

# Calculating the FOG Index for each document using the formula and assigning it to the 'FOG INDEX' column
df['FOG INDEX'] = 0.4 * (df['AVG SENTENCE LENGTH'] + df['PERCENTAGE OF COMPLEX WORDS'])

# Creating a new column 'AVG NUMBER OF WORDS PER SENTENCE' and assigning the values from 'AVG SENTENCE LENGTH' column
df['AVG NUMBER OF WORDS PER SENTENCE'] = df['AVG SENTENCE LENGTH']


# Adding the 'COMPLEX WORD COUNT' column to the DataFrame and assigning the 'count_complexWord' list to it
df['COMPLEX WORD COUNT'] = count_complexWord

# Creating a new column 'WORD COUNT' and initializing all values to 0
df['WORD COUNT'] = 0

# Iterating through the indices of 'all_Documents' (assuming it has the same length as 'df')
for i in range(len(all_Documents)):
    # Assigning the word count of the current document to the 'WORD COUNT' column
    df['WORD COUNT'][i] = len(all_Documents[i])

# Adding the 'SYLLABLE PER WORD' column to the DataFrame and initializing all values to 0
df['SYLLABLE PER WORD'] = 0

def avg_syllables(word):
    if word.lower() in pronouncing_dict:
        # For each pronunciation of the word in the dictionary, calculate syllables
        return np.average([len([y for y in x if y[-1].isdigit()]) for x in pronouncing_dict[word.lower()]])
    else:
        return 0
    
# Creating an empty list to store the average number of syllables per word for each document
SYLLABLE_PER_WORD = []

# Iterating through each processed document in the 'all_Documents' list
for words in all_Documents:
    # Calculating the average number of syllables per word using the 'avg_syllables' function
    syllable_avg_words = np.average([avg_syllables(word) for word in words])
    
    # Adding the calculated average to the 'SYLLABLE_PER_WORD' list
    SYLLABLE_PER_WORD.append(syllable_avg_words)

# Adding the 'SYLLABLE PER WORD' column to the DataFrame and assigning the 'SYLLABLE_PER_WORD' list to it
df['SYLLABLE PER WORD'] = SYLLABLE_PER_WORD

# Creating an empty list to store the count of specific pronouns for each document
count_pronoun = []

# List of all pronoun
pronouns = ["i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"]

# Iterating through each processed document in the 'Documents' list
for words in Documents:
    # Initializing a count for the specific pronouns
    count = 0
    
    # Iterating through each word in the document
    for word in words:
        # Checking if the word is not 'US' and is present in the 'pronouns' list
        if word != 'US' and word.lower() in pronouns:
            count += 1
    
    # Adding the count of specific pronouns for the current document to the list
    count_pronoun.append(count)

# Adding the 'PERSONAL PRONOUNS' column to the DataFrame and assigning the 'count_pronoun' list to it
df['PERSONAL PRONOUNS'] = count_pronoun

# Creating an empty list to store the average word length for each document
avg_word_length = []

# Iterating through each processed document in the 'all_Documents' list
for words in all_Documents:
    count = 0
    no_of_words = len(words)
    
    # Iterating through each word in the document
    for word in words:
        count += len(word)
    
    try:
        # Calculating and appending the average word length for the current document
        avg_word_length.append(count / no_of_words)
    except:
        # Handling exceptions, e.g., division by zero
        avg_word_length.append(0)

# Adding the 'AVG WORD LENGTH' column to the DataFrame and assigning the 'avg_word_length' list to it
df['AVG WORD LENGTH'] = avg_word_length

# Saving the DataFrame to a CSV file named "output1.csv" without the index column
df.to_csv("output1.csv", index=False)