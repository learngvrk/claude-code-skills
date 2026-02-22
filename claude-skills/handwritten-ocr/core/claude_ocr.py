"""
Claude Vision API integration for handwriting OCR.

Sends each PDF page (as a PNG image) to Claude's Vision capability
and returns the extracted text.
"""

import base64
from typing import List, Optional, Callable

import anthropic


def extract_text_from_image(
    png_bytes: bytes,
    api_key: str,
    model: str,
    prompt: str,
    max_tokens: int = 4096,
) -> str:
    """
    Send a PNG image to Claude Vision and return the transcribed text.

    Args:
        png_bytes:  Raw PNG image bytes (one PDF page rendered as PNG)
        api_key:    Anthropic API key
        model:      Claude model ID (e.g. 'claude-sonnet-4-6')
        prompt:     Instruction prompt for OCR
        max_tokens: Max tokens in Claude's response

    Returns:
        Extracted text string from the handwritten page

    Raises:
        anthropic.APIStatusError: On HTTP errors from the API
        anthropic.APIConnectionError: On network failures
    """
    client = anthropic.Anthropic(api_key=api_key)
    image_data_b64 = base64.standard_b64encode(png_bytes).decode("utf-8")

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )

    return message.content[0].text


def extract_text_from_all_pages(
    png_bytes_list: List[bytes],
    api_key: str,
    model: str,
    prompt: str,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> List[str]:
    """
    Run OCR on each page sequentially and return a list of text strings.

    Sequential (not concurrent) to respect Anthropic API rate limits.

    Args:
        png_bytes_list:    List of PNG bytes, one per page
        api_key:           Anthropic API key
        model:             Claude model ID
        prompt:            OCR instruction prompt
        progress_callback: Optional callable(page_index, total_pages)

    Returns:
        List of extracted text strings, one per page, in order
    """
    results: List[str] = []
    total = len(png_bytes_list)

    for i, png_bytes in enumerate(png_bytes_list):
        if progress_callback:
            progress_callback(i, total)
        text = extract_text_from_image(png_bytes, api_key, model, prompt)
        results.append(text)

    if progress_callback:
        progress_callback(total, total)

    return results
