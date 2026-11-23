#!/usr/bin/env python3
"""生成 sha256_清单.txt 与 evidence/acceptance_matrix.json。

清单排除自身与验收矩阵，避免重跑时自修改导致哈希漂移。
只用 Python 标准库，输出无时间戳。
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sha256_清单.txt"
MATRIX = ROOT / "evidence" / "acceptance_matrix.json"

REQUIRED = [
    "README.md",
    "luyiran-jingxueqing_C3C_协作方案.md",
    "luyiran-jingxueqing_C3C_技能画像_卢怡然.md",
    "luyiran-jingxueqing_C3C_技能画像_靖雪晴.md",
    "luyiran-jingxueqing_C3C_教学记录/01_技术到业务_库表字段核对.md",
    "luyiran-jingxueqing_C3C_教学记录/02_业务到技术_异常场景与用例前置条件.md",
    "luyiran-jingxueqing_C3C_教学记录/证据来源说明.md",
    "luyiran-jingxueqing_C3C_学习笔记_卢怡然.md",
    "luyiran-jingxueqing_C3C_学习笔记_靖雪晴.md",
    "luyiran-jingxueqing_C3C_联合产出/README.md",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/rules.json",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/audit.py",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/sample_before.json",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/sample_after.json",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/run_all.py",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/tests/test_audit.py",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/outputs/audit_before.json",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/outputs/audit_after.json",
    "luyiran-jingxueqing_C3C_联合产出/pod_audit/outputs/unittest.txt",
    "luyiran-jingxueqing_C3C_前后对比.md",
    "luyiran-jingxueqing_C3C_AAR.md",
    "luyiran-jingxueqing_C3C_AI日志.md",
    "luyiran-jingxueqing_C3C_目标与验收标准对照.md",
    "luyiran-jingxueqing_C3C_交付清单.md",
    "evidence/P27_来源摘录.md",
    "evidence/audit_before.json",
    "evidence/audit_after.json",
    "evidence/unittest.txt",
]

HONESTY_MARKERS = [
    ("luyiran-jingxueqing_C3C_教学记录/01_技术到业务_库表字段核对.md", "证据等级"),
    ("luyiran-jingxueqing_C3C_教学记录/02_业务到技术_异常场景与用例前置条件.md", "证据等级"),
    ("luyiran-jingxueqing_C3C_教学记录/证据来源说明.md", "不满足该硬性要求"),
    ("luyiran-jingxueqing_C3C_技能画像_靖雪晴.md", "待本人确认"),
    ("luyiran-jingxueqing_C3C_学习笔记_靖雪晴.md", "代拟稿"),
    ("luyiran-jingxueqing_C3C_交付清单.md", "未满足"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path):
    return path.relative_to(ROOT).as_posix()


def build_manifest():
    entries = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p in (MANIFEST, MATRIX):
            continue
        entries.append((sha256(p), rel(p)))
    MANIFEST.write_text(
        "".join("{}  {}\n".format(digest, path) for digest, path in entries),
        encoding="utf-8",
    )
    return entries


def verify_manifest(entries):
    checks = []
    for digest, path in entries:
        p = ROOT / path
        ok = p.is_file() and sha256(p) == digest
        checks.append({"path": path, "pass": ok})
    return checks


def main():
    entries = build_manifest()
    checks = []

    for item in REQUIRED:
        p = ROOT / item
        checks.append({"type": "required", "path": item,
                       "pass": p.is_file() and p.stat().st_size > 0})

    for path, marker in HONESTY_MARKERS:
        p = ROOT / path
        checks.append({"type": "honesty_marker", "path": path,
                       "marker": marker,
                       "pass": p.is_file() and marker in p.read_text(encoding="utf-8")})

    hash_checks = verify_manifest(entries)
    checks.extend({"type": "hash", "path": c["path"], "pass": c["pass"]}
                  for c in hash_checks)

    before = json.loads((ROOT / "evidence" / "audit_before.json").read_text(encoding="utf-8"))
    after = json.loads((ROOT / "evidence" / "audit_after.json").read_text(encoding="utf-8"))
    tests = (ROOT / "evidence" / "unittest.txt").read_text(encoding="utf-8")

    checks.append({"type": "audit", "path": "evidence/audit_before.json",
                   "pass": before["pass"] is False and before["finding_count"] >= 5})
    checks.append({"type": "audit", "path": "evidence/audit_after.json",
                   "pass": after["pass"] is True and after["finding_count"] == 0})
    checks.append({"type": "tests", "path": "evidence/unittest.txt",
                   "pass": "failures=0" in tests and "errors=0" in tests
                   and "ok=True" in tests})

    required_pass = sum(c["pass"] for c in checks if c["type"] == "required")
    manifest_pass = sum(c["pass"] for c in hash_checks)
    matrix = {
        "challenge": "C3C",
        "required_pass": required_pass,
        "required_total": len(REQUIRED),
        "manifest_pass": manifest_pass,
        "manifest_entries": len(entries),
        "all_pass": all(c["pass"] for c in checks),
        "audit_summary": {
            "before_findings": before["finding_count"],
            "after_findings": after["finding_count"],
            "tests_ok": "ok=True" in tests,
        },
        "known_gaps": [
            "搭档专业证明缺失，跨专业硬条件待确认",
            "无带时间戳的教学会话截图/录屏/聊天记录",
            "靖雪晴的画像/笔记/AAR 为代拟稿，待本人签字",
            "靖雪晴独立能力验证任务无证据",
            "L4 公开分享与通用协作模板未做",
        ],
        "checks": checks,
    }
    MATRIX.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")

    print("required {}/{} manifest {}/{} all_pass={}".format(
        required_pass, len(REQUIRED), manifest_pass, len(entries), matrix["all_pass"]))
    return 0 if matrix["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
