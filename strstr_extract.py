#!/usr/bin/env python3
"""
String extraction similar to C's strstr()
Extract base pattern from strings like:
  'Grape_Black_rot1' → 'Grape_Black_rot'
  'Disease_A_category_2' → 'Disease_A'
  'image_Healthy_v123' → 'Healthy'
"""

import re
import pandas as pd


def strstr_like(haystack, needle):
    """
    Find substring like C's strstr().

    Args:
        haystack: String to search in
        needle: String to find

    Returns:
        Substring from first match to end, or None if not found

    Example:
        strstr_like('Grape_Black_rot1', 'Grape')
        → 'Grape_Black_rot1'

        strstr_like('prefix_Healthy_suffix', 'Healthy')
        → 'Healthy_suffix'
    """
    if pd.isna(haystack):
        return haystack

    haystack = str(haystack)
    needle = str(needle)

    idx = haystack.find(needle)
    if idx != -1:
        return haystack[idx:]
    return None


def extract_base_pattern(text, patterns):
    """
    Find which pattern matches in text and return from pattern start.

    Args:
        text: String to search in
        patterns: List of patterns to look for
                 Example: ['Grape_Black_rot', 'Disease_A', 'Healthy', 'Other']

    Returns:
        Matched pattern base string, or original text if no match

    Examples:
        extract_base_pattern('prefix_Grape_Black_rot1_suffix',
                            ['Grape_Black_rot', 'Disease_A', 'Healthy'])
        → 'Grape_Black_rot'

        extract_base_pattern('image_123_Healthy_v2',
                            ['Grape_Black_rot', 'Disease_A', 'Healthy'])
        → 'Healthy'
    """
    if pd.isna(text):
        return text

    text = str(text)

    # Sort patterns by length (longest first) to match longest pattern first
    sorted_patterns = sorted(patterns, key=len, reverse=True)

    for pattern in sorted_patterns:
        if pattern in text:
            # Find where pattern starts
            # idx = text.find(pattern)
            # Return just the pattern base (without suffix numbers)
            return pattern

    return text


def extract_pattern_with_cleanup(text, patterns):
    """
    Extract pattern from text and remove any trailing numbers.

    Args:
        text: String to search in
        patterns: List of base patterns

    Returns:
        Cleaned pattern match

    Example:
        extract_pattern_with_cleanup('Grape_Black_rot123',
                                    ['Grape_Black_rot', 'Disease_A'])
        → 'Grape_Black_rot'
    """
    match = extract_base_pattern(text, patterns)
    # Remove trailing numbers
    cleaned = re.sub(r'\d+$', '', str(match))
    return cleaned


def find_pattern_in_series(series, patterns):
    """
    Find patterns in a pandas Series.

    Args:
        series: pandas Series of strings
        patterns: List of patterns to find

    Returns:
        Series with matched base patterns

    Example:
        df['Category'] = find_pattern_in_series(
            df['raw_names'],
            ['Grape_Black_rot', 'Disease_A', 'Healthy']
        )
    """
    return series.apply(lambda x: extract_base_pattern(x, patterns))


def extract_known_categories(text, known_categories):
    """
    From a messy string, extract which known category it belongs to.
    Returns the exact category name from your known list.

    Args:
        text: Messy input string (e.g., with prefix/suffix/numbers)
        known_categories: List of correct category names
                         Example: ['Grape_Black_rot', 'Disease_A', 'Healthy']

    Returns:
        Matched category name from known_categories

    Example:
        categories = ['Grape_Black_rot', 'Disease_A', 'Healthy', 'Other']

        extract_known_categories('image_Grape_Black_rot_v2_123', categories)
        → 'Grape_Black_rot'

        extract_known_categories('Disease_A_sample_45', categories)
        → 'Disease_A'
    """
    if pd.isna(text):
        return None

    text = str(text)

    # Sort by length (longest first) to match most specific pattern
    sorted_cats = sorted(known_categories, key=len, reverse=True)

    for cat in sorted_cats:
        if cat.lower() in text.lower():
            return cat
        if cat in text:
            return cat

    return None


# ════════════════════════════════════════════════════════════════════════════
# USAGE EXAMPLES
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("STRING EXTRACTION EXAMPLES (Like C's strstr())")
    print("=" * 80)

    # Example 1: Basic strstr-like function
    print("\n1. BASIC STRSTR-LIKE FUNCTION:")
    test_strings = [
        ('Grape_Black_rot1', 'Grape_Black_rot'),
        ('prefix_Healthy_suffix', 'Healthy'),
        ('Disease_A_v2_123', 'Disease_A'),
        ('unknown_category', 'Grape_Black_rot'),
    ]

    for text, pattern in test_strings:
        result = extract_base_pattern(text, [pattern])
        print(f"  extract_base_pattern('{text}', ['{pattern}'])")
        print(f"    → '{result}'\n")

    # Example 2: Match against multiple patterns
    print("\n2. MATCH AGAINST MULTIPLE PATTERNS:")
    categories = ['Grape_Black_rot', 'Disease_A', 'Disease_B', 'Healthy',
                  'Other']
    test_inputs = [
        'image_123_Grape_Black_rot_v2',
        'sample_Disease_A_category_45',
        'Healthy_variant_789',
        'prefix_Other_Disease_suffix',
        'completely_unknown_cat',
    ]

    for text in test_inputs:
        result = extract_base_pattern(text, categories)
        print(f"  Input: '{text}'")
        print(f"    → Matched: '{result}'\n")

    # Example 3: Extract with cleanup (remove numbers)
    print("\n3. EXTRACT AND CLEANUP (Remove trailing numbers):")
    test_messy = [
        'Grape_Black_rot1',
        'Disease_A2_extra_text',
        'Healthy123_v2',
        'Other_Disease_v1_2_3',
    ]

    for text in test_messy:
        result = extract_pattern_with_cleanup(text, categories)
        print(f"  Input: '{text}'")
        print(f"    → Cleaned: '{result}'\n")

    # Example 4: DataFrame integration
    print("\n4. PANDAS DATAFRAME INTEGRATION:")
    sample_data = {
        'raw_name': [
            'image_Grape_Black_rot_v1',
            'Disease_A_sample_2',
            'Healthy_variant_123',
            'prefix_Other_suffix_45',
            'unknown_v789',
        ],
        'confidence': [0.95, 0.87, 0.92, 0.65, 0.40]
    }

    df = pd.DataFrame(sample_data)

    print("\n  Before:")
    print(df.to_string(index=False))

    # Extract categories from raw names
    df['Category'] = df['raw_name'].apply(
        lambda x: extract_base_pattern(x, categories)
    )

    print("\n  After:")
    print(df.to_string(index=False))

    # Example 5: Using extract_known_categories (most useful)
    print("\n5. EXTRACT KNOWN CATEGORIES (Best for messy data):")
    messy_predictions = [
        'image_123_Grape_Black_rot_v2',
        'prefix_Disease_A_suffix',
        'Healthy_v3_sample_45',
        'completely_random_string',
        'Disease_B_unknown',
    ]

    for messy in messy_predictions:
        result = extract_known_categories(messy, categories)
        print(f"  Input: '{messy}'")
        print(f"    → Category: '{result}'\n")

    print("=" * 80)
