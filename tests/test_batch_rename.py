import tempfile
import unittest
from pathlib import Path

from src.batch_rename import build_rename_plan, apply_rename_plan


class BatchRenameTests(unittest.TestCase):
    def test_preview_and_apply_rename(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "b.png").write_text("b")
            (folder / "a.jpg").write_text("a")
            plan = build_rename_plan(folder, "asset_", 1, 2)
            self.assertEqual(len(plan), 2)
            apply_rename_plan(plan)
            self.assertTrue((folder / "asset_01.jpg").exists())
            self.assertTrue((folder / "asset_02.png").exists())

    def test_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "photo.png").write_text("photo")
            (folder / "asset_01.png").mkdir()
            with self.assertRaises(FileExistsError):
                build_rename_plan(folder, "asset_", 1, 2)


if __name__ == "__main__":
    unittest.main()
