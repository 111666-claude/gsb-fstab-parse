import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fstab import core

TEXT = "/dev/sda1 / ext4 defaults 0 1\n"


class FstabTest(unittest.TestCase):
    def test_parse_fields(self):
        entry = core.parse(TEXT, core.Counter())[0]
        self.assertEqual((entry.device, entry.mountpoint, entry.fstype), ("/dev/sda1", "/", "ext4"))

    def test_order_field(self):
        entry = core.parse(TEXT, core.Counter())[0]
        self.assertEqual(entry.order, 1)

    def test_comment_skipped(self):
        self.assertEqual(len(core.parse("# c\n", core.Counter())), 0)

    def test_find_missing(self):
        entries = core.parse(TEXT, core.Counter())
        self.assertIsNone(core.find(entries, "/nope", core.Counter()))

    def test_mount_order_count(self):
        entries = core.parse(TEXT, core.Counter())
        self.assertEqual(len(core.mount_order(entries, core.Counter())), 1)

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse(TEXT, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
