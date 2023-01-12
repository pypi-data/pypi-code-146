"""
Extractor Module

Extract text content from files such as pdf, docx, txt etc.
"""
import os

import pdfplumber
import docx2txt
import html2text
from PyPDF2 import PdfReader


def get_file_ext(filepath) -> str:
    """
    Get extention of the file 
    
    :param filepath: path of the paths
    :return: file extention
    """
    split_tup = os.path.splitext(filepath)
    return split_tup[1]

def read_file(filepath) -> str:
    """
    Read content from a file
    
    :param filepath: path to file
    :return: file content
    """

    text = ""
    with open(filepath, 'r') as f:
        text = f.read()

    return text

def read_pdf(filepath) -> str:
    """
    Extract text from pdf files

    :param filepath: filepath to the pdf file
    :return: text present in pdf
    """
    text = ""
    
    reader = PdfReader(filepath)
    
    for page in reader.pages:
        text += page.extract_text()

    return text.strip()

def read_docx(filepath) -> str:
    """
    Extract text from docx files
    
    :param filepath: filepath to the docx file
    :return: text present in docx file
    """

    text = docx2txt.process(filepath)
    return text.strip()

def read_txt(filepath) -> str:
    """
    Extract text from txt file
    
    :param filepath: filepath to txt file
    :return: text present in txt file
    """

    text = read_file(filepath)

    return text.strip()

def read_html(filepath) -> str:
    """
    Extract text from a html file
    
    :param filepath: filepath to html file
    :return: text present in html file
    """

    html = read_file(filepath)
    text = html2text.html2text(html)

    return text.strip()

def extract_doc(filepath) -> str:
    """
    Extract text from documents such as pdf, docx, txt etc

    :param filepath: filepath to the document from which text needs to be extracted
    :return: text present in the document
    """

    ext = get_file_ext(filepath)

    if ext == '.pdf':
        return read_pdf(filepath)
    elif ext == '.docx':
        return read_docx(filepath)
    elif ext == '.txt':
        return read_txt(filepath)
    elif ext == '.html':
        return read_html(filepath)