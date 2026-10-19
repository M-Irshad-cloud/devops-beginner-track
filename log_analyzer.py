import argparse
import re
from collections import Counter

# Nginx "combined" log format, with named groups for readability
LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<size>\d+) '
    r'"[^"]*" "(?P<agent>[^"]*)"'
)


def parse_file(path):
    entries, skipped = [], 0
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = LOG_PATTERN.match(line)
            if match:
                entries.append(match.groupdict())
            else:
                skipped += 1  # startup messages, malformed lines, etc.
    return entries, skipped


def main():
    parser = argparse.ArgumentParser(description="Analyze an Nginx access log")
    parser.add_argument("logfile", help="path to the log file")
    parser.add_argument("--top", type=int, default=5, help="how many top items to show")
    parser.add_argument("--errors-only", action="store_true", help="also list every 4xx/5xx request")
    args = parser.parse_args()

    entries, skipped = parse_file(args.logfile)
    total = len(entries)

    print("=== Log Analysis: " + args.logfile + " ===")
    print("Parsed requests : " + str(total))
    print("Skipped lines   : " + str(skipped))
    if total == 0:
        print("No valid access-log lines found.")
        return

    by_status = Counter(e["status"] for e in entries)
    by_class = Counter(e["status"][0] + "xx" for e in entries)
    by_path = Counter(e["path"] for e in entries)
    by_ip = Counter(e["ip"] for e in entries)
    errors = [e for e in entries if e["status"][0] in "45"]
    total_bytes = sum(int(e["size"]) for e in entries)

    print("")
    print("-- Status classes --")
    for cls, count in sorted(by_class.items()):
        print("  " + cls + ": " + str(count) + "  (" + str(round(count / total * 100, 1)) + "%)")

    print("")
    print("-- Status codes --")
    for code, count in sorted(by_status.items()):
        print("  " + code + ": " + str(count))

    print("")
    print("-- Top " + str(args.top) + " endpoints --")
    for path, count in by_path.most_common(args.top):
        print("  " + str(count).rjust(4) + "  " + path)

    print("")
    print("-- Top " + str(args.top) + " client IPs --")
    for ip, count in by_ip.most_common(args.top):
        print("  " + str(count).rjust(4) + "  " + ip)

    print("")
    print("Error rate (4xx+5xx): " + str(round(len(errors) / total * 100, 1)) + "%")
    print("Total bytes served  : " + str(total_bytes))

    if args.errors_only:
        print("")
        print("-- Error requests --")
        for e in errors:
            print("  " + e["time"] + "  " + e["method"] + " " + e["path"] + "  -> " + e["status"])


if __name__ == "__main__":
    main()
