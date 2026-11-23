# 联合产出 · P27-POD-Audit 配送演示数据核对器

## 这是什么

把 P27 协作中**人工逐条核对库表字段**的动作，抽象成 5 条可机器执行的规则，
形成可重复运行的检查器。这是 C3C 二人的联合产出，不是 P27 原有代码。

- 业务/数据侧贡献（靖雪晴，P27 材料可证）：终端绑定口径、旧凭证引用问题、异常场景清单、用例前置登录要求；
- 技术侧贡献（卢怡然，P27 材料可证）：把口径实现为规则、脚本与自动测试；
- 待确认：两人是否实际一起试用过本工具——目前无会话证据，见 `../luyiran-jingxueqing_C3C_教学记录/证据来源说明.md`。

## 运行

```bash
cd luyiran-jingxueqing_C3C_联合产出/pod_audit
python run_all.py
```

输出（稳定、无时间戳，便于哈希复核）：
- `outputs/audit_before.json`、`evidence/audit_before.json`：修正前错误样例，`pass=false`，6 条问题；
- `outputs/audit_after.json`、`evidence/audit_after.json`：按口径修正后样例，`pass=true`，0 条问题；
- `outputs/unittest.txt`、`evidence/unittest.txt`：6 个单测全部通过。

也可单独运行：

```bash
python audit.py --data sample_before.json --rules rules.json --out /tmp/before.json
python tests/test_audit.py -v
```

## 规则来源对照

| 规则 | 来源 |
|---|---|
| `terminal_id.pattern` | 靖雪晴发现 AI 生成的 `PDA-2026001` 与库中 `PDA-SY-0001` 不符 |
| `credential_ref.forbidden` | 两人材料均记录旧凭证引用导致登录失败 |
| `pod_status.allowed` | P27 POD 状态口径（含王艺燃评审，项目背景，不计入二人互教证据） |
| `required_scenarios` | 靖雪晴的异常场景数据补充（材料中为“进行中”） |
| `login_step.required` | 靖雪晴补上 AI 用例中省略的前置登录 |

样例数据是**按材料记录的真实错误复现**构造的最小数据集，不宣称是 P27 原始交付文件；
凭证引用以 `map://` 表示，不含真实密码。

## 独立性

只用 Python 标准库（json / re / argparse / unittest / pathlib / io / contextlib / sys），
无第三方依赖，换机器可直接跑。
