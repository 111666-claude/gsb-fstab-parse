"""解析 fstab 并给出挂载顺序。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Entry:
    def __init__(self, device, mountpoint, fstype, options, dump, order):
        self.device = device
        self.mountpoint = mountpoint
        self.fstype = fstype
        self.options = options
        self.dump = dump
        self.order = order


def parse(text, counter):
    entries = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        counter.scanned += 1
        fields = line.split()
        if len(fields) < 3:
            continue
        dump = int(fields[4]) if len(fields) > 4 else 0
        order = int(fields[5]) if len(fields) > 5 else 0
        options = fields[3] if len(fields) > 3 else "defaults"
        entries.append(Entry(fields[0], fields[1], fields[2], options, dump, order))
    return entries


def find(entries, mountpoint, counter):
    for entry in entries:
        counter.scanned += 1
        if entry.mountpoint == mountpoint:
            return entry
    return None


def mount_order(entries, counter):
    return [entry.mountpoint for entry in entries]
