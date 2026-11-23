# luyiran-jingxueqing_C3C_交付清单

组名：`luyiran-jingxueqing`（卢怡然 + 靖雪晴）｜生成日期：2026-11-23
存放位置：桌面 `C3C/`（新建，未覆盖 C9/C10/C10H 等其他挑战目录）

## 1. 必交文件与用途

| 文件 | 用途 |
|---|---|
| `README.md` | 目录导航、真实性边界、复核命令 |
| `luyiran-jingxueqing_C3C_协作方案.md` | 两人背景、项目目标、谁教谁什么、为什么单独做不到 |
| `luyiran-jingxueqing_C3C_技能画像_卢怡然.md` | 技术侧技能自画像（8 项可证技能、3 项想学） |
| `luyiran-jingxueqing_C3C_技能画像_靖雪晴.md` | 业务/数据侧技能自画像（代拟稿，专业等待确认） |
| `luyiran-jingxueqing_C3C_教学记录/01_技术到业务_库表字段核对.md` | 知识迁移事件 01（技术→业务），证据等级 B |
| `luyiran-jingxueqing_C3C_教学记录/02_业务到技术_异常场景与用例前置条件.md` | 知识迁移事件 02（业务→技术），证据等级 B |
| `luyiran-jingxueqing_C3C_教学记录/证据来源说明.md` | 说明为何没有会话截图，列补齐清单 |
| `luyiran-jingxueqing_C3C_学习笔记_卢怡然.md` | 技术侧学了什么/卡在哪/怎么突破 |
| `luyiran-jingxueqing_C3C_学习笔记_靖雪晴.md` | 业务侧学习笔记代拟稿，留本人填写/签字栏 |
| `luyiran-jingxueqing_C3C_联合产出/README.md` | 联合产出说明、运行命令、规则来源对照 |
| `luyiran-jingxueqing_C3C_联合产出/pod_audit/audit.py` | 零依赖核对器：5 类规则的可执行实现 |
| `.../pod_audit/rules.json` | 规则包，每条规则标注 P27 来源 |
| `.../pod_audit/sample_before.json` | 修正前错误复现样例（按材料记录的真实错误构造） |
| `.../pod_audit/sample_after.json` | 按口径修正后样例 |
| `.../pod_audit/tests/test_audit.py` | 6 个单测，验证规则抓得住真实错误 |
| `.../pod_audit/run_all.py` | 一键生成 before/after 报告 + 单测日志 |
| `.../pod_audit/outputs/audit_before.json` | 修正前报告：6 条问题 |
| `.../pod_audit/outputs/audit_after.json` | 修正后报告：0 条问题 |
| `.../pod_audit/outputs/unittest.txt` | 6/6 单测通过日志 |
| `luyiran-jingxueqing_C3C_前后对比.md` | 两人前后能力对比，逐项标注证据等级 |
| `luyiran-jingxueqing_C3C_AAR.md` | 双人联合复盘：做了什么/学到什么/怎么验证/失败与改进 |
| `luyiran-jingxueqing_C3C_AI日志.md` | 12 轮 AI 使用记录（5 轮 P27 + 7 轮本次），含人工否定 AI 的实例 |
| `luyiran-jingxueqing_C3C_目标与验收标准对照.md` | L1–L4、两套评分口径、10 项必交、5 个红旗逐项对照 |
| 本文件 | 文件用途清单与未满足要求 |

## 2. 证据与工具

| 文件 | 用途 |
|---|---|
| `evidence/P27_来源摘录.md` | P27 原件逐字摘录（密码已脱敏）与来源哈希 |
| `evidence/audit_before.json` | 修正前报告副本，供评审直接读取 |
| `evidence/audit_after.json` | 修正后报告副本 |
| `evidence/unittest.txt` | 单测日志副本 |
| `evidence/acceptance_matrix.json` | 机器可读验收矩阵（生成物） |
| `tools/finalize.py` | 生成哈希清单与验收矩阵，排除自身避免漂移 |
| `sha256_清单.txt` | 全目录文件 SHA-256（排除清单与矩阵自身） |

## 3. 自检结果

- 可运行产物：修正前 6 条问题、修正后 0 条问题；6/6 单测通过；
- 必交文件与证据文件：见 `evidence/acceptance_matrix.json`（字段 `required_pass` / `manifest_pass` / `all_pass`）；
- 复核命令：`cd 桌面/C3C && python tools/finalize.py`。

## 4. 未满足的要求（如实列出）

| # | 缺口 | 影响 | 补齐方式 |
|---|---|---|---|
| 1 | **跨专业证明缺失** | C3C 规则 1 硬条件；靖雪晴专业未在 P27 材料中记录，不反推 | 搭档填写专业/年级或提供学生证明 |
| 2 | **≥2 次教学会话截图/录屏/聊天记录缺失** | L2 硬条件，rubric 知识迁移证据 30% 受损 | 补 2 段带时间戳的对话截图或复讲录屏，放入教学记录目录 |
| 3 | **靖雪晴的画像/笔记/AAR 为代拟稿，无本人签字** | 规则 2“每人学会一项新技能并有证据”不完整 | 本人逐条核对、填写“想学/卡点/突破”并签字 |
| 4 | **靖雪晴独立能力验证任务无证据** | L3“能力验证”不满足 | 请她独立运行 `audit.py` 并保存终端输出/提交记录 |
| 5 | **L4 公开分享与通用协作模板未做** | Platinum 级不可评 | 按 C4B 写公众号文章或在群内分享，并把模板抽象为通用文件 |
| 6 | **两人共同试用联合产出的记录缺失** | “联合产出”归属可能被质疑 | 补一次结对运行记录（截图 + 谁做了什么） |
| 7 | **P27 原始 prompt 未保存** | AI 日志部分只能按材料转述 | 若需满分，补当时的对话导出 |
| 8 | **需求方沟通记录仍缺**（P27 材料已标注） | 仅影响载体项目背景，不是 C3C 直接必交 | 由 P27 负责人后续补录 |

以上缺口均**没有用编造材料填补**。当前包可作为“结构完整、证据待补”的提交稿；
在第 1–4 项补齐前，不建议按“完整满足 C3C 全部规则”申报。
