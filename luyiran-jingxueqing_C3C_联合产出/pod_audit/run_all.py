#!/usr/bin/env python3
"""一件事跑完：生成修正前/后报告 + 单测日志，写入 outputs 与 C3C/evidence。"""

import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT.parent.parent / "evidence"
sys.path.insert(0, str(ROOT))

from audit import audit, load_json  # noqa: E402


def write_report(name, data_path, rules_path):
    report = audit(load_json(data_path), load_json(rules_path))
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    for directory in (ROOT / "outputs", EVIDENCE):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ("audit_{}.json".format(name))).write_text(text, encoding="utf-8")
    return report


def run_tests():
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "tests"), pattern="test_*.py", top_level_dir=str(ROOT / "tests")
    )
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    text = stream.getvalue() + "\nRESULT run={} failures={} errors={} ok={}\n".format(
        result.testsRun, len(result.failures), len(result.errors), result.wasSuccessful()
    )
    for directory in (ROOT / "outputs", EVIDENCE):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "unittest.txt").write_text(text, encoding="utf-8")
    return result.wasSuccessful(), result.testsRun


def main():
    rules = ROOT / "rules.json"
    before = write_report("before", ROOT / "sample_before.json", rules)
    after = write_report("after", ROOT / "sample_after.json", rules)
    ok, total = run_tests()
    print("before: pass={} findings={}".format(before["pass"], before["finding_count"]))
    print("after:  pass={} findings={}".format(after["pass"], after["finding_count"]))
    print("tests:  {}/{} ok".format(total if ok else 0, total))
    return 0 if (not before["pass"] and after["pass"] and ok) else 1


if __name__ == "__main__":
    sys.exit(main())
