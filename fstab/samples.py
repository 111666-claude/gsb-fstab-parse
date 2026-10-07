"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "options":
        entries = core.parse("/dev/sda1 /mnt ext4 rw,noatime 0 0\n", core.Counter())
        _line({"options": len(entries[0].options)})
        return 0
    if name == "overlay":
        text = "/dev/a /mnt ext4 defaults 0 0\n/dev/b /mnt ext4 defaults 0 0\n"
        entries = core.parse(text, core.Counter())
        entry = core.find(entries, "/mnt", core.Counter())
        _line({"device": entry.device if entry else ""})
        return 0
    if name == "order":
        text = "/dev/b /a/b ext4 defaults 0 0\n/dev/a /a ext4 defaults 0 0\n"
        entries = core.parse(text, core.Counter())
        order = core.mount_order(entries, core.Counter())
        _line({"first": order[0] if order else ""})
        return 0
    if name == "pass":
        text = "/dev/a /a ext4 defaults 0 2\n/dev/b /b ext4 defaults 0 1\n"
        entries = core.parse(text, core.Counter())
        order = core.mount_order(entries, core.Counter())
        _line({"first": order[0] if order else ""})
        return 0
    if name == "work":
        lines = ["/dev/d%04d /m%04d ext4 defaults 0 0" % (i, i) for i in range(800)]
        entries = core.parse("\n".join(lines) + "\n", core.Counter())
        counter = core.Counter()
        for i in range(800):
            core.find(entries, "/m%04d" % i, counter)
        _line({"entries": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
