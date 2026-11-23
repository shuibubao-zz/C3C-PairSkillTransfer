#!/usr/bin/env python3
"""P27-POD-Audit: 把 P27 协作中的人工数据核对口径固化为可重复执行的规则。

只用 Python 标准库。凭证引用为 map:// 形式，不读取或输出真实密码。
"""

import argparse
import json
import re
import sys
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def audit(data, rules):
    """返回可机读报告；findings 为空表示全部规则通过。"""
    findings = []

    def add(rule, path, message, observed):
        findings.append(
            {"rule": rule, "path": path, "message": message, "observed": observed}
        )

    pattern = re.compile(rules["terminal_id"]["pattern"])
    forbidden = set(rules["credential_ref"]["forbidden"])
    allowed_status = set(rules["pod_status"]["allowed"])
    required_scenarios = set(rules["required_scenarios"])
    login_required = bool(rules["login_step"]["required"])

    for i, driver in enumerate(data.get("drivers", [])):
        terminal = driver.get("terminal", "")
        path = "drivers[{}].terminal".format(i)
        if not pattern.match(terminal):
            add("terminal_id.pattern", path,
                "终端编号不符合 P27 库表绑定口径", terminal)
        ref = driver.get("credential_ref", "")
        if ref in forbidden:
            add("credential_ref.forbidden",
                "drivers[{}].credential_ref".format(i),
                "引用了迁移前的旧凭证引用", ref)

    for i, order in enumerate(data.get("delivery_orders", [])):
        status = order.get("pod_status", "")
        if status not in allowed_status:
            add("pod_status.allowed",
                "delivery_orders[{}].pod_status".format(i),
                "POD 状态不在允许集合中", status)

    scenarios = set(data.get("scenarios", []))
    missing = sorted(required_scenarios - scenarios)
    if missing:
        add("required_scenarios", "scenarios",
            "缺少业务必需场景", missing)

    if login_required:
        for i, case in enumerate(data.get("test_cases", [])):
            if not case.get("login_step", False):
                add("login_step.required",
                    "test_cases[{}].login_step".format(i),
                    "用例缺少前置登录步骤", False)

    return {
        "dataset": data.get("dataset", "unnamed"),
        "rules_version": rules.get("version", "unknown"),
        "checked": {
            "drivers": len(data.get("drivers", [])),
            "delivery_orders": len(data.get("delivery_orders", [])),
            "scenarios": len(data.get("scenarios", [])),
            "test_cases": len(data.get("test_cases", [])),
        },
        "pass": not findings,
        "finding_count": len(findings),
        "findings": findings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit P27 demo data against the shared P27 rule pack."
    )
    parser.add_argument("--data", required=True, help="待核对数据集 JSON")
    parser.add_argument("--rules", required=True, help="规则包 JSON")
    parser.add_argument("--out", help="报告输出路径（JSON）；不写则只打印摘要")
    args = parser.parse_args(argv)

    report = audit(load_json(args.data), load_json(args.rules))
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    summary = "{}: pass={} findings={}".format(
        report["dataset"], report["pass"], report["finding_count"]
    )
    print(summary)
    for f in report["findings"]:
        print("  - {} @ {}: {}".format(f["rule"], f["path"], f["message"]))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
