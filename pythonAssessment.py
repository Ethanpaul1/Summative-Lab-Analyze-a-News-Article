"""
News Article Text Analysis Script
Performs various text analysis tasks on a given news article.
"""

import re
from collections import Counter
from pathlib import Path


def read_text_file(filepath):
    """
    Read the contents of a text file into a string.
    
    Args:
        filepath (str or Path): The path to the text file to read
        
    Returns:
        str: The contents of the file, or empty string if file not found
    """
    try:
        file_path = Path(filepath)
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        else:
            print(f"Error: File '{filepath}' not found.")
            return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


def count_specific_word(text, search_word):
    """
    Count the number of occurrences of a specific word in the text.
    
    Args:
        text (str): The string to search through
        search_word (str): The word to search for
        
    Returns:
        int: The count of occurrences (0 if no matches found)
    """
    if not text or not search_word:
        return 0
    else:
        text_lower = text.lower()
        search_word_lower = search_word.lower()
        
        count = 0
        start = 0
        while True:
            position = text_lower.find(search_word_lower, start)
            if position == -1:
                break
            else:
                count += 1
                start = position + 1
        
        return count


def identify_most_common_word(text):
    """
    Identify the most common word in the text.
    
    Args:
        text (str): The string to analyze
        
    Returns:
        str: The most common word (or None if empty)
    """
    if not text or text.strip() == "":
        return None
    else:
        words = re.findall(r"\b\w+\b", text.lower())
        
        if not words:
            return None
        else:
            word_counter = Counter(words)
            most_common = word_counter.most_common(1)[0][0]
            return most_common


def calculate_average_word_length(text):
    """
    Calculate the average length of words in the text.
    Excludes punctuation and special characters.
    
    Args:
        text (str): The string to analyze
        
    Returns:
        float: The average word length
    """
    if not text or text.strip() == "":
        return 0
    else:
        words = re.findall(r"\b\w+\b", text)
        
        if not words:
            return 0
        else:
            total_length = 0
            for word in words:
                total_length += len(word)
            
            average_length = total_length / len(words)
            return average_length


def count_paragraphs(text):
    """
    Count the number of paragraphs in the text.
    Paragraphs are defined by empty line breaks.
    
    Args:
        text (str): The string to analyze
        
    Returns:
        int: The number of paragraphs
    """
    if not text or text.strip() == "":
        return 1
    else:
        paragraphs = text.split('\n\n')
        
        paragraph_count = 0
        for para in paragraphs:
            if para.strip():
                paragraph_count += 1
            else:
                continue
        
        if paragraph_count == 0:
            paragraph_count = 1
        
        return paragraph_count


def count_sentences(text):
    """
    Count the number of sentences in the text.
    Sentences are defined by periods, exclamation marks, and question marks.
    
    Args:
        text (str): The string to analyze
        
    Returns:
        int: The number of sentences
    """
    if not text or text.strip() == "":
        return 1
    else:
        sentence_count = 0
        sentence_endings = '.!?'
        
        for char in text:
            if char in sentence_endings:
                sentence_count += 1
            else:
                continue
        
        if sentence_count == 0 and text.strip():
            sentence_count = 1
        
        return sentence_count


if __name__ == "__main__":
    # Read the article file
    article = read_text_file("article.txt")
    
    if article:
        # Test each function
        print("Text Analysis Results")
        print("=" * 50)
        print(f"Word 'ACME' count: {count_specific_word(article, 'ACME')}")
        print(f"Most common word: '{identify_most_common_word(article)}'")
        print(f"Average word length: {calculate_average_word_length(article):.2f}")
        print(f"Number of paragraphs: {count_paragraphs(article)}")
        print(f"Number of sentences: {count_sentences(article)}")
        print("=" * 50)
    else:
        print("Failed to read article file.")

