from redisvl.utils.vectorize import HFTextVectorizer
from typing import Any, Callable, List, Optional

class HF_Images(HFTextVectorizer):
    def embed(
        self,
        text: str,
        preprocess: Optional[Callable] = None,
        as_buffer: bool = False,
        **kwargs,
    ) -> List[float]:
        """Embed a chunk of text using the Hugging Face sentence transformer.

        Args:
            text (str): Chunk of text to embed.
            preprocess (Optional[Callable], optional): Optional preprocessing
                callable to perform before vectorization. Defaults to None.
            as_buffer (bool, optional): Whether to convert the raw embedding
                to a byte string. Defaults to False.

        Returns:
            List[float]: Embedding.

        """

        if preprocess:
            text = preprocess(text)
        embedding = self._client.encode([text])[0]
        return self._process_embedding(embedding.tolist(), as_buffer)