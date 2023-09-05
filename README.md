# Blackcoffer Data Extraction & NLP

## Table of Contents

- [Introduction](#introduction)
- [Data Extraction](#data-extraction)
- [Data Analysis](#data-analysis)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Welcome to the Text Data Extraction and Analysis Project! This project is aimed at extracting textual data from specified URLs, performing text analysis, and computing various textual variables. The extracted data is used to gain insights into sentiment, readability, and other text-related attributes.

## Data Extraction

In this project, we use Python programming along with web scraping libraries such as BeautifulSoup and Selenium to extract text data from given URLs. Specifically, we extract the article title and article text while excluding any website headers, footers, or other irrelevant content. The extracted data is saved in text files with unique names based on the URL_ID.

## Data Analysis

The text data extracted from articles undergoes comprehensive analysis to compute the following variables:

- **Positive Score**: Measures the positivity of the text.
- **Negative Score**: Measures the negativity of the text.
- **Polarity Score**: Determines if the text is positive or negative.
- **Subjectivity Score**: Measures the subjectivity of the text.
- **Average Sentence Length**: Calculated as the number of words divided by the number of sentences.
- **Percentage of Complex Words**: The ratio of complex words to total words.
- **Fog Index**: Measures text readability using the Gunning Fox index.
- **Average Number of Words Per Sentence**: The average word count in each sentence.
- **Complex Word Count**: Counts words with more than two syllables.
- **Word Count**: Total words in the cleaned text.
- **Syllable Per Word**: The average syllables per word.
- **Personal Pronouns**: Counts of personal pronouns like "I," "we," "my," etc.
- **Average Word Length**: The average length of words in characters.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in the [Dependencies](#dependencies) section.
3. Run the Python program to extract data and perform analysis as per the provided instructions.

## Dependencies

This project relies on the following Python libraries and tools:

- BeautifulSoup
- Selenium
- NLTK (Natural Language Toolkit)
- ![Other](https://github.com/rishabh11336/Blackcoffer-Data-Extraction-and-NLP/blob/main/requirements.txt)

Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```
Sure, here's the provided text in markdown format:

## Usage

To use this project:

1. Place the URLs you want to analyze in the `input.xlsx` file.
2. Run the Python program to extract data and perform text analysis.
3. The output will be generated in CSV or Excel format, adhering to the structure defined in the "Output Data Structure.xlsx" file.

## Results

The results of the data extraction and analysis will provide valuable insights into the text data, including sentiment scores, readability metrics, and other textual attributes. These results can be used for various applications such as content analysis, sentiment analysis, and more.

## Contributing

If you'd like to contribute to this project, feel free to submit pull requests or open issues. We welcome contributions that enhance the functionality or usability of the project.

## License

This project is licensed under the [MIT License](LICENSE).
