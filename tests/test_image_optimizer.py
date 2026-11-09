import tempfile
import unittest
from pathlib import Path
from PIL import Image

from src.image_optimizer import optimize_image, optimize_folder


class ImageOptimizerTests(unittest.TestCase):
    def test_optimize_png_creates_output_and_keeps_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "sample.png"
            output = root / "out" / "sample.png"
            Image.new("RGBA", (10, 10), (255, 0, 0, 100)).save(source)
            original_bytes = source.read_bytes()
            optimize_image(source, output)
            self.assertTrue(output.exists())
            self.assertEqual(source.read_bytes(), original_bytes)
            with Image.open(output) as result:
                self.assertEqual(result.mode, "RGBA")

    def test_rejects_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "file.gif"
            source.write_bytes(b"not an image")
            with self.assertRaises(ValueError):
                optimize_image(source, Path(temp) / "out.gif")


if __name__ == "__main__":
    unittest.main()
