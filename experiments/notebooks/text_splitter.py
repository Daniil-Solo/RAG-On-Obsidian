from langchain.text_splitter import CharacterTextSplitter


class CustomTextSplitter:
    def __init__(self, chunk_size=1024, chunk_overlap=512):
        self.chunk_size = chunk_size
        self.splitter_level1 = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=r'[#]+ ',
            is_separator_regex=True,
            keep_separator='start',
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

    def split_text(self, markdown_text: str) -> list[str]:
        chunks = self.splitter_level1.split_text(markdown_text)
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
