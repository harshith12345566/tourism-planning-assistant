"""
API Helper Utilities

This module provides utility functions for making HTTP requests
with proper error handling and timeout management.
"""

import requests
from typing import Dict, Any, Optional
import time


def make_request(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> Optional[Dict[str, Any]]:
    """
    Make an HTTP GET request with retry logic and error handling.
    
    Args:
        url: The URL to make the request to
        params: Optional query parameters
        headers: Optional request headers
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    
    Returns:
        JSON response as dictionary if successful, None otherwise
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            print(f"Error: Request timeout after {max_retries} attempts")
            return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            print(f"Error: Request failed - {str(e)}")
            return None
    
    return None


def make_post_request(
    url: str,
    data: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> Optional[Dict[str, Any]]:
    """
    Make an HTTP POST request with retry logic and error handling.
    
    Args:
        url: The URL to make the request to
        data: Optional POST data (string or dict)
        headers: Optional request headers
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    
    Returns:
        JSON response as dictionary if successful, None otherwise
    """
    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                data=data,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            print(f"Error: Request timeout after {max_retries} attempts")
            return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            print(f"Error: Request failed - {str(e)}")
            return None
    
    return None

