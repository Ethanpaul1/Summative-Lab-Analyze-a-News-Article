import re
from collections import Counter
from pathlib import Path


WORD_PATTERN = re.compile(r"\b\w+\b")
PARAGRAPH_SPLIT_PATTERN = re.compile(r"\n\s*\n")
SENTENCE_PATTERN = re.compile(r"[^.!?]+[.!?]+[\"'\u201d\u2019)\]]*")
PERIOD_PLACEHOLDER = "<PERIOD>"
ABBREVIATIONS = (
    "Mr.",
    "Mrs.",
    "Ms.",
    "Dr.",
    "Prof.",
    "Sr.",
    "Jr.",
    "Inc.",
    "Ltd.",
    "Co.",
    "U.S.",
    "U.K.",
    "etc.",
)


def read_text_file(file_path):
    """Read a text file and return its contents as a string."""
    path = Path(file_path)

    if path.exists():
        return path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Could not find file: {file_path}")


def _get_words(text):
    """Return all words from the text with punctuation removed."""
    return WORD_PATTERN.findall(text.lower())


def count_specific_word(text, word):
    """Count the number of times a specific word appears in the text."""
    words = _get_words(text)
    target_word = word.lower()
    count = 0
    index = 0

    while index < len(words):
        if words[index] == target_word:
            count += 1
        index += 1

    return count


def identify_most_common_word(text):
    """Identify the most common word in the text."""
    words = _get_words(text)

    if words:
        word_counts = Counter(words)
        return word_counts.most_common(1)[0][0]
    else:
        return ""


def calculate_average_word_length(text):
    """Calculate the average length of all words in the text."""
    words = _get_words(text)

    if not words:
        return 0

    total_length = 0
    for word in words:
        total_length += len(word)

    return round(total_length / len(words), 2)


def count_paragraphs(text):
    """Count paragraphs based on blank line breaks."""
    paragraphs = PARAGRAPH_SPLIT_PATTERN.split(text.strip())
    count = 0

    for paragraph in paragraphs:
        if paragraph.strip():
            count += 1

    return max(count, 1)


def _protect_abbreviation_periods(text):
    """Protect periods in common abbreviations before sentence splitting."""
    protected_text = text

    for abbreviation in ABBREVIATIONS:
        protected_abbreviation = abbreviation.replace(".", PERIOD_PLACEHOLDER)
        protected_text = re.sub(
            re.escape(abbreviation),
            protected_abbreviation,
            protected_text,
            flags=re.IGNORECASE,
        )

    return protected_text


def count_sentences(text):
    """Count sentences while ignoring periods inside common abbreviations."""
    paragraphs = PARAGRAPH_SPLIT_PATTERN.split(text.strip())
    sentence_count = 0

    for paragraph in paragraphs:
        protected_paragraph = _protect_abbreviation_periods(paragraph.strip())
        sentences = SENTENCE_PATTERN.findall(protected_paragraph)

        for sentence in sentences:
            if WORD_PATTERN.search(sentence):
                sentence_count += 1

    return max(sentence_count, 1)


def main():
    article_path = Path(__file__).with_name("article.txt")
    text = read_text_file(article_path)
    specific_word = "ACME"

    print(
        f"The word '{specific_word}' appears {count_specific_word(text, specific_word)} times."
    )
    print(f"The most common word is '{identify_most_common_word(text)}'.")
    print(f"The average word length is {calculate_average_word_length(text):.2f}.")
    print(f"There are {count_paragraphs(text)} paragraphs.")
    print(f"There are {count_sentences(text)} sentences.")


if __name__ == "__main__":
    main()