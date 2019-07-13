#!/usr/bin/env python
from pathlib import Path
import re

base_path = Path(__file__).resolve().parent
with (base_path / 'Arch-Instruction.md').open() as fp:
  contents = fp.read()
# Сначала нормализуем контент, удаляя все вставки кода
contents = re.sub(r'```.*?```', '', contents, flags=re.S)

# Теперь ищем заголовки
headers = re.findall('^#.*', contents, re.M)

for header in headers:
  l = len(header)
  name = header.lstrip('#')
  depth = len(header) - len(name)
  name = name.strip()
  # Теперь вырезаем ссылки
  name = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', name)
  uri = name.lower()
  # Вырезаем все не буквенно-цифровые символы
  # «-» то же не унжно вырезать
  uri = re.sub(r'[^\w\s-]', '', uri)
  # Заменяем пробелы на «-»
  uri = uri.replace(' ', '-')
  print('   ' * (depth - 1) + f'1. [{name}](#{uri})')
