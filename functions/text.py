import re
from django.utils.html import format_html


def process_content(content):
    # Обновленная обработка ссылок
    section_link_pattern = re.compile(r"\[\[(\d+)#(.*?)\]\]")

    def replace_with_link(match):
        section_id, link_text = match.groups()
        return format_html('<a href="/section/{}/">{}</a>', section_id, link_text)
    content = section_link_pattern.sub(replace_with_link, content)

    # Обработка жирного текста
    bold_text_pattern = re.compile(r"\*\*(.*?)\*\*")
    content = bold_text_pattern.sub(r'<strong>\1</strong>', content)

    # Обработка красного текста
    red_text_pattern = re.compile(r"\*r\*(.*?)\*r\*")
    content = red_text_pattern.sub(r'<span style="color: red;">\1</span>', content)

    # Обработка зеленого текста
    green_text_pattern = re.compile(r"\*g\*(.*?)\*g\*")
    content = green_text_pattern.sub(r'<span style="color: green;">\1</span>', content)

    return content