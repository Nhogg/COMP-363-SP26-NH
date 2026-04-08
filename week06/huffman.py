from __future__ import annotations  # for cool type hinting

import heapq
from pathlib import Path

try:
    from pympler import asizeof
except ImportError as exc:
    raise ImportError(
        "This script requires pympler. Install it with 'pip install pympler'."
    ) from exc


class Node:
    """A simple binary tree node for a basic Huffman encoder."""

    def __init__(self, symbol: str | None, frequency: int):
        """Object constructor.

        Inputs
        ------
        frequency : int
          The frequency represented by this node. If the node has also a symbol,
          this is the frequency of the symbol. If no symbol is present, this is
          the sum of frequencies of the node's subtrees.
        symbol : char
          The symbol whose frequency we capture. If symbol is None, the node
          captures frequencies for subtrees under the node.

        Returns
        -------
        Instance of Node object with fields:
          frequency : as described above
          symbol : as described above
          left : pointer to left node child (default none)
          right : pointer to right node child (default none)
        """
        self.__frequency: int = frequency
        self.__symbol: str | None = symbol
        self.__left: None | Node = None
        self.__right: None | Node = None

    def __lt__(self, other: Node):
        """Redefine < for node to be based on frequency value."""
        return self.__frequency < other.get_frequency()

    def set_left(self, left: Node | None):
        """Setter for left child."""
        self.__left = left

    def set_right(self, right: Node | None):
        """Setter for right child."""
        self.__right = right

    def has_left(self):
        """Predicate accessor for left child."""
        return self.__left is not None

    def has_right(self):
        """Predicate accessor for right child."""
        return self.__right is not None

    def get_left(self):
        """Accessor for left child."""
        return self.__left

    def get_right(self):
        """Accessor for right child."""
        return self.__right

    def get_symbol(self) -> str:
        """Accessor for the symbol in a leaf node."""
        return self.__symbol

    def get_frequency(self):
        """Accessor for frequency."""
        return self.__frequency

    def is_leaf(self) -> bool:
        """Determines if node is a leaf node."""
        return self.__left is None and self.__right is None

    def __str__(self):
        """String representation of object."""
        return f"[ {self.__symbol}: {self.__frequency} ]"


class HuffmanCoder:
    def __init__(self):
        self.root: Node | None = None
        self.codes: dict[str, str] = {}

    def _build_frequencies(self, text: str) -> dict[str, int]:
        """Build a frequency dictionary for the characters in the input text."""
        frequencies: dict[str, int] = {}
        for char in text:
            if char in frequencies:
                frequencies[char] += 1
            else:
                frequencies[char] = 1
        return frequencies

    def _build_tree(self, frequencies: dict[str, int]) -> Node | None:
        """Build the Huffman tree using a priority queue."""
        forest: list[Node] = []

        for symbol, freq in frequencies.items():
            heapq.heappush(forest, Node(symbol, freq))

        while len(forest) > 1:
            n1 = heapq.heappop(forest)
            n2 = heapq.heappop(forest)

            parent = Node(None, n1.get_frequency() + n2.get_frequency())
            parent.set_left(n1)
            parent.set_right(n2)
            heapq.heappush(forest, parent)

        return heapq.heappop(forest) if forest else None

    def _generate_codes(self, node: Node | None, current_code: str):
        """Recursively generate the Huffman codes for each symbol."""
        if node is None:
            return

        if node.is_leaf():
            self.codes[node.get_symbol()] = current_code
            return

        self._generate_codes(node.get_left(), current_code + "0")
        self._generate_codes(node.get_right(), current_code + "1")

    def encode(self, text: str) -> str:
        """Encode a plain text string into a binary Huffman string."""
        self.codes = {}
        self.root = None

        if not text:
            return ""

        frequencies = self._build_frequencies(text)
        self.root = self._build_tree(frequencies)

        if self.root is None:
            return ""

        if self.root.is_leaf():
            self.codes[self.root.get_symbol()] = "0"
        else:
            self._generate_codes(self.root, "")

        return "".join(self.codes[char] for char in text)

    def decode(self, encoded_text: str) -> str:
        """Decode a binary Huffman string back into plain text."""
        if self.root is None:
            if encoded_text:
                raise ValueError("Cannot decode a non-empty message without a Huffman tree.")
            return ""

        if self.root.is_leaf():
            if any(bit != "0" for bit in encoded_text):
                raise ValueError("Single-symbol Huffman encodings may only contain '0' bits.")
            return self.root.get_symbol() * len(encoded_text)

        decoded_chars: list[str] = []
        current_node = self.root

        for bit in encoded_text:
            if bit == "0":
                current_node = current_node.get_left()
            elif bit == "1":
                current_node = current_node.get_right()
            else:
                raise ValueError(f"Invalid bit {bit!r} in encoded text.")

            if current_node is None:
                raise ValueError("Encoded text does not match the current Huffman tree.")

            if current_node.is_leaf():
                decoded_chars.append(current_node.get_symbol())
                current_node = self.root

        if current_node is not self.root:
            raise ValueError("Encoded text ended in the middle of a symbol.")

        return "".join(decoded_chars)


def analyze_text(label: str, text: str, show_codes: bool = False):
    """Encode, decode, and report compression statistics for a text."""
    coder = HuffmanCoder()
    encoded_text = coder.encode(text)
    decoded_text = coder.decode(encoded_text)

    if decoded_text != text:
        raise ValueError(f"Decoded text for {label} does not match the original input.")

    original_bits = len(text) * 8
    encoded_bits = len(encoded_text)
    tree_bytes = asizeof.asizeof(coder.root)
    tree_bits = tree_bytes * 8
    total_huffman_bits = encoded_bits + tree_bits
    message_bits_saved = original_bits - encoded_bits
    net_bits_saved = original_bits - total_huffman_bits

    print(f"=== {label} ===")
    print(f"Characters: {len(text)}")
    print(f"Original size (ASCII bits): {original_bits}")
    print(f"Encoded size (bits): {encoded_bits}")
    print(f"Bits saved by encoding alone: {message_bits_saved}")
    print(f"Huffman tree size (bytes): {tree_bytes}")
    print(f"Huffman tree size (bits): {tree_bits}")
    print(f"Total Huffman size (encoded + tree) (bits): {total_huffman_bits}")
    print(f"Net bits saved after tree overhead: {net_bits_saved}")

    if original_bits > 0:
        print(f"Encoding-only compression ratio: {encoded_bits / original_bits:.4f}")
        print(f"Net compression ratio: {total_huffman_bits / original_bits:.4f}")

    print(f"Decoded matches original: {decoded_text == text}")

    if show_codes:
        print("Codes:")
        for symbol, code in sorted(coder.codes.items(), key=lambda item: (len(item[1]), item[0])):
            printable_symbol = "SPACE" if symbol == " " else symbol
            print(f"  {printable_symbol!r}: {code}")

    if total_huffman_bits < original_bits:
        print("Conclusion: Huffman coding is more space-efficient than ASCII for this input.")
    else:
        print("Conclusion: Tree overhead outweighs the compression gains for this input.")

    print()


def main():
    short_text = "HELLO WORLD"
    analyze_text("HELLO WORLD demo", short_text, show_codes=True)

    bible_path = Path(__file__).with_name("kjv_bible.txt")
    bible_text = bible_path.read_text(encoding="utf-8")
    analyze_text("KJV Bible", bible_text)


if __name__ == "__main__":
    main()
