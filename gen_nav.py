#!/usr/bin/env python
import re
from pathlib import Path

base_path = Path(__file__).resolve().parent
with (base_path / 'Arch-Instruction.md').open('r+') as fp:
  contents = fp.read()
  # Сначала нормализуем контент, удаляя все вставки кода
  contents2 = re.sub(r'`.*?`', '', contents, flags=re.S)

  contents2 = re.sub(r'\<!-- (nav) --\>.*?\<!-- /\1 --\>',
                     '', contents2, flags=re.S)

  # Теперь ищем заголовки
  headers = re.findall('^#.*', contents2, re.M)

  nav = ['# Оглавление', '']
  for header in headers:
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
    nav.append('   ' * (depth - 1) + f'1. [{name}](#{uri})')

  contents = re.sub(r'(?<=\<!-- (nav) --\>).*?(?=\<!-- /\1 --\>)',
                    '\n'.join(nav), contents, flags=re.S)

  fp.truncate()
  fp.seek(0)
  fp.write(contents)
