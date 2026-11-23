# C3C 双人协作与技能迁移 · 交付包

- 挑战 ID：`ch-20260717031415-0vi5d1`，截止 2026-12-31T23:59
- 组名：`luyiran-jingxueqing`（卢怡然 + 靖雪晴）
- 载体项目：P27「聚思达供应链·物流配送管理平台」真实协作中的**演示数据核对工作**
- 本包生成日期：2026-11-23

## 真实性边界（先看这里）

本包只使用本机可核对的真实材料：`P27_聚思达供应链物流配送管理平台_卢怡然_20261019_含成员分工.docx`
（SHA-256 `a78010844b0b35629d79d01dd12775627291cfc89a4b90938cf664832546f17f`）。

材料内有两人的**真实分工、具体核对动作和 AI 使用判断**；但材料内**没有**：
两人专业证明、带时间戳的教学会话截图/录屏/聊天记录、搭档本人对本包材料的签字确认。

因此：
- 教学记录写的是**依据 P27 材料复盘的知识迁移事件**，明确标注“非会话截图”；
- 技能画像中无材料支撑的字段写“待本人确认”，不猜专业、不编技能清单；
- 联合产出是新写的**可运行核对工具**，体现从 P27 核对经验中抽象出的方法，**不宣称搭档已实际运行过本工具**；
- 未满足项集中列在 `luyiran-jingxueqing_C3C_交付清单.md`，请提交前与搭档核对补证。

## 目录

| 路径 | 内容 |
|---|---|
| `luyiran-jingxueqing_C3C_协作方案.md` | 谁和谁、项目目标、为什么单独做不到 |
| `luyiran-jingxueqing_C3C_技能画像_卢怡然.md` | 技术侧技能自画像 |
| `luyiran-jingxueqing_C3C_技能画像_靖雪晴.md` | 业务/数据侧技能自画像（含待确认字段） |
| `luyiran-jingxueqing_C3C_教学记录/` | 2 次知识迁移事件记录 + 证据来源说明 |
| `luyiran-jingxueqing_C3C_学习笔记_卢怡然.md` | 技术侧学习笔记（依据材料整理） |
| `luyiran-jingxueqing_C3C_学习笔记_靖雪晴.md` | 业务侧学习笔记（代拟稿，待本人确认） |
| `luyiran-jingxueqing_C3C_联合产出/pod_audit/` | 可运行的数据核对器、规则、样例、单测与输出 |
| `luyiran-jingxueqing_C3C_前后对比.md` | 学之前/学之后能力对比（含证据等级） |
| `luyiran-jingxueqing_C3C_AAR.md` | 双人联合复盘 |
| `luyiran-jingxueqing_C3C_AI日志.md` | 双人 AI 使用全过程（依据材料 + 本包生成过程） |
| `luyiran-jingxueqing_C3C_目标与验收标准对照.md` | 四级任务、rubric、红旗逐项对照 |
| `luyiran-jingxueqing_C3C_交付清单.md` | 文件用途与未满足要求 |
| `evidence/` | P27 原文摘录、运行输出、验收矩阵 |
| `tools/finalize.py` | 生成哈希清单与验收矩阵 |
| `sha256_清单.txt` | 全目录 SHA-256 清单 |

## 复核命令

```bash
cd <本目录>
python "luyiran-jingxueqing_C3C_联合产出/pod_audit/run_all.py"
python "luyiran-jingxueqing_C3C_联合产出/pod_audit/tests/test_audit.py" -v
python tools/finalize.py
```

`run_all.py` 只用 Python 标准库；输出写入 `pod_audit/outputs/`，并同步复制到 `evidence/`。
