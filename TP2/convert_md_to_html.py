import re
import sys

def convert_md_to_html(md_content):
    linhas = md_content.split('\n')
    linhas_html = []

