from typing import Literal
import tiktoken
import re

APPROX_BUFFER = 1.1
TRIM_BUFFER = 0.8

# Cache for encoding to avoid repeated downloads
_encoding_cache = {}

def count_tokens(text: str, encoding_name="cl100k_base") -> int:
    if not text:
        return 0

    try:
        # Check cache first
        if encoding_name not in _encoding_cache:
            # Get the encoding with retry logic
            encoding = tiktoken.get_encoding(encoding_name)
            _encoding_cache[encoding_name] = encoding
        else:
            encoding = _encoding_cache[encoding_name]

        # Encode the text and count the tokens
        tokens = encoding.encode(text)
        token_count = len(tokens)
        
        return token_count
        
    except Exception as e:
        # Fallback to rough estimation if tiktoken fails
        print(f"Warning: tiktoken failed ({e}), using fallback token estimation")
        return _fallback_token_count(text)

def _fallback_token_count(text: str) -> int:
    """Fallback method to estimate tokens when tiktoken is unavailable"""
    # Rough estimation: 1 token ≈ 4 characters for English text
    # Adjust for different languages and special characters
    words = len(re.findall(r'\b\w+\b', text))
    chars = len(text)
    
    # Better estimation considering:
    # - English words: ~1.3 tokens per word
    # - Punctuation and spaces: ~0.3 tokens per 4 chars
    # - Special characters: ~1 token each
    
    estimated_tokens = int(words * 1.3 + chars * 0.075)
    return max(estimated_tokens, 1)  # At least 1 token for non-empty text


def approximate_tokens(
    text: str,
) -> int:
    return int(count_tokens(text) * APPROX_BUFFER)


def trim_to_tokens(
    text: str,
    max_tokens: int,
    direction: Literal["start", "end"],
    ellipsis: str = "...",
) -> str:
    chars = len(text)
    tokens = count_tokens(text)

    if tokens <= max_tokens:
        return text

    approx_chars = int(chars * (max_tokens / tokens) * TRIM_BUFFER)

    if direction == "start":
        return text[:approx_chars] + ellipsis
    return ellipsis + text[chars - approx_chars : chars]
