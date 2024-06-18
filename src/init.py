"""
Accessibility Tool - A package for evaluating web pages for accessibility compliance.
"""

from .fetcher import fetch_html
from .parse import parse_html
from .checker import check_alt_attributes, check_heading_structure
from .reporter import generate_report

__all__ = [
    'fetch_html',
    'parse_html',
    'check_alt_attributes',
    'check_heading_structure',
    'generate_report',
]
