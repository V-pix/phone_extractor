import re
from pathlib import Path
from typing import List, Set, Tuple

from loguru import logger


class PhoneExtractor:
    """Класс для извлечения телефонных номеров из текстового файла"""
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.phone_pattern = re.compile(
            r"(?:\+7|8)?[\s\-.(]*(\d{3})[\s\-.)]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})"
        )
        self.collected_numbers: Set[str] = set()

    def format_number(self, groups: Tuple[str, str, str, str]) -> str:
        """Приводит найденный номер к единому формату"""
        code, part1, part2, part3 = groups
        return f"+7({code}){part1}-{part2}-{part3}"

    def extract(self) -> List[str]:
        """Извлекает уникальные номера телефонов"""
        result: List[str] = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    for match in self.phone_pattern.finditer(line):
                        d=match.groups()
                        formatted = self.format_number(match.groups())
                        if formatted not in self.collected_numbers:
                            self.collected_numbers.add(formatted)
                            result.append(formatted)
            logger.info(f"Найдено {len(result)} уникальных номеров")
        except FileNotFoundError:
            logger.error(f"Файл {self.file_path} не найден.")
        except Exception as e:
            logger.exception(f"Ошибка обработки файла: {e}")
        return result


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "input.txt"

    extractor = PhoneExtractor(str(file_path))
    phones = extractor.extract()

    for phone in phones:
        print(phone)


if __name__ == "__main__":
    main()