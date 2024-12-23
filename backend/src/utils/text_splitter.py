import re
from langchain.text_splitter import CharacterTextSplitter


class CustomTextSplitter:
    def __init__(self, chunk_size=1024, chunk_overlap=512):
        self.chunk_size = chunk_size
        self.splitter_level1 = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=r'[#]+ ',
            is_separator_regex=True,
            )
        self.splitter_level2 = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator='\n\n',
            is_separator_regex=False,
            )
        self.splitter_level3 = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator='\n',
            is_separator_regex=False,
            )

    def split(self, text: str) -> list[str]:
        chunks = self.splitter_level1.split_text(text)
        results = []
        for chunk in chunks:
            if len(chunk) > self.chunk_size:
                results.extend(self.splitter_level2.split_text(chunk))
            else:
                results.append(chunk)
        chunks = results
        results = []
        for chunk in chunks:
            if len(chunk) > self.chunk_size:
                results.extend(self.splitter_level3.split_text(chunk))
            else:
                results.append(chunk)
        return results


class NewCustomTextSplitter:
    def __init__(
            self,
            chunk_size: int = 1024,
            chunk_overlap: int = 512,
            separator_first_level: str = r'[#]+ ',
            separator_second_level: str = r'\n\n'
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator_first_level = separator_first_level
        self.separator_second_level = separator_second_level

    def split(self, text: str) -> list[str]:
        first_level_parts = re.split(self.separator_first_level, text)
        chunks = []

        for part in first_level_parts:
            if len(part) < self.chunk_size + 2 * self.chunk_overlap:
                chunks.append(part)
                continue

            second_level_parts = re.split(self.separator_second_level, part)

            for sub_part in second_level_parts:
                if len(sub_part) < self.chunk_size + 2 * self.chunk_overlap:
                    chunks.append(sub_part)
                    continue

                for sub_part_index in range(0, len(sub_part), self.chunk_size):
                    top_border = sub_part_index + self.chunk_size + self.chunk_overlap
                    bottom_border = 0 if sub_part_index == 0 else sub_part_index - self.chunk_overlap
                    chunks.append(sub_part[bottom_border:top_border])

        return [chunk.strip() for chunk in chunks]
