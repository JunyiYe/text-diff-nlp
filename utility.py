import difflib
import spacy

# Load spaCy model for natural language processing
nlp = spacy.load("en_core_web_sm")

# Function to tokenize text into sentences
def tokenize_sentences(text):
    # Process the text with spaCy
    doc = nlp(text)
    # Extract sentences and strip leading/trailing spaces
    return [sent.text.strip() for sent in doc.sents]

# Function to find similar sentence pairs between two texts
def find_similar_pairs(text1, text2, threshold=0.50):
    # Tokenize both texts into sentences
    text1_sentences = tokenize_sentences(text1)
    text2_sentences = tokenize_sentences(text2)

    # Calculate similarity scores for each sentence pair
    similarity_matrix = [[similar(sent1, sent2) for sent2 in text2_sentences] for sent1 in text1_sentences]

    # Initialize list to store matched pairs and a set for already used indices
    similar_pairs = []
    used_text2_indices = set()

    # Find the most similar sentence pair above the threshold
    for i, row in enumerate(similarity_matrix):
        max_similarity = 0
        most_similar_sent_index = None
        for j, sim_score in enumerate(row):
            if sim_score > max_similarity and j not in used_text2_indices:
                max_similarity = sim_score
                most_similar_sent_index = j

        if max_similarity > threshold and most_similar_sent_index is not None:
            similar_pairs.append((text1_sentences[i], text2_sentences[most_similar_sent_index]))
            used_text2_indices.add(most_similar_sent_index)

    return similar_pairs, len(text1_sentences), len(text2_sentences)

# Function to calculate similarity between two strings
def similar(a, b):
    # Use difflib to calculate similarity ratio
    return difflib.SequenceMatcher(None, a, b).ratio()

# Function to highlight differences between two strings
def highlight_differences(original, edited):
    diff = list(difflib.ndiff(original, edited))
    reconstructed_text = ""

    for word in diff:
        if word.startswith("- "):
            # Words in original but not in edited (highlight in red)
            reconstructed_text += f"\033[91m{word[2:]}\033[0m "
        elif word.startswith("  "):
            # Common words (highlight in blue)
            reconstructed_text += f"\033[94m{word[2:]}\033[0m "

    return reconstructed_text.strip()

# Function to apply highlighting to a specific sentence in the text
def apply_highlighting(text, sentence, highlighted):
    parts = text.split(sentence)
    return highlighted.join(parts)

# Function to highlight text based on similar sentence pairs
def highlight(text1, text2, similar_pairs):
    for sent1, sent2 in similar_pairs:
        words_sent1 = sent1.split()
        words_sent2 = sent2.split()

        # Highlight differences for both sentences
        highlighted_sent1 = highlight_differences(words_sent1, words_sent2)
        highlighted_sent2 = highlight_differences(words_sent2, words_sent1)

        # Apply the highlighted text to the original texts
        text1 = apply_highlighting(text1, sent1, highlighted_sent1)
        text2 = apply_highlighting(text2, sent2, highlighted_sent2)

    return text1, text2

# Main function to compare two texts and highlight differences
def text_diff(text1, text2):
    similar_pairs, len1, len2 = find_similar_pairs(text1, text2, threshold=0.50)
    highlighted_text1, highlighted_text2 = highlight(text1, text2, similar_pairs)

    print("Text-Diff-NLP Tool")
    print("\x1b[94mBlue: common parts\x1b[0m; \x1b[91mRed: different parts\x1b[0m; Black: unmatched sentences.")
    print("="*80)
    print("TEXT 1:\n")
    print(highlighted_text1)
    print("-"*80)
    print("TEXT 2:\n")
    print(highlighted_text2)
