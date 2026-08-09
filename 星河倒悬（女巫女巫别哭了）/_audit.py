#!/usr/bin/env python3
"""
星河倒悬——全项目自动审计脚本
用法: python _audit.py [--fix] [--json]
  --json  输出 JSON 格式（供 CI/工具链消费）
  --fix   自动修复可修复的问题（需确认）

读取 _shared_data.json 作为权威数据源，扫描所有 .md 文件。
退出码: 0=全通过  1=有警告  2=有错误
"""

import json, re, sys, os
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "_shared_data.json"

# ─── 加载共享数据 ──────────────────────────────────────────
def load_data():
    if not DATA_FILE.exists():
        print(f"🔴 致命: {DATA_FILE} 不存在！请先创建共享数据文件。")
        sys.exit(2)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# ─── 加载所有文档 ──────────────────────────────────────────
def load_docs():
    docs = {}
    for f in ROOT.rglob("*.md"):
        if f.name.startswith('_'): continue  # 跳过系统文件
        try:
            docs[str(f.relative_to(ROOT))] = f.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError, OSError):
            pass  # 跳过无法读取的文件（编码/权限/系统错误）
    return docs

# ─── 颜色输出 ──────────────────────────────────────────────
class Colors:
    RED = '\033[91m'; YELLOW = '\033[93m'; GREEN = '\033[92m'
    CYAN = '\033[96m'; BOLD = '\033[1m'; RESET = '\033[0m'

def ok(msg): return f"{Colors.GREEN}✅{Colors.RESET} {msg}"
def warn(msg): return f"{Colors.YELLOW}⚠️ {Colors.RESET} {msg}"
def err(msg): return f"{Colors.RED}🔴{Colors.RESET} {msg}"

# ─── 主审计逻辑 ────────────────────────────────────────────
def audit(data, docs, json_output=False):
    errors = []
    warnings = []
    passed = []

    # ── 检查1: 废弃货币 ──
    deprecated_currencies = data['deprecated']['currencies']
    deprecated_modules = data['deprecated']['modules']
    # 以下文档正当地引用了废弃货币（审核报告/接口定义中的"已删除"说明）
    exempt_currency_docs = [
        'GDD一致性审核报告', '共享系统接口定义', '战斗系统评估与优化'
    ]

    for path, content in docs.items():
        # 统一路径分隔符为 /（Windows 上 path 含 \，但 JSON 中用 /）
        path_norm = path.replace('\\', '/')
        if any(dm.replace('\\', '/') in path_norm for dm in deprecated_modules):
            continue
        if any(ex in path_norm for ex in exempt_currency_docs):
            continue
        for currency in deprecated_currencies:
            if currency in content:
                lines = content.split('\n')
                found_lines = []
                for ln, line in enumerate(lines, 1):
                    # 检查：行中含废弃货币·但不是"废弃"声明·不是"共享标准"引用
                    if currency in line and '废弃' not in line and '共享标准' not in line:
                        # 额外：排除"白银两数"等合法复合词
                        if currency == '银两' and '白银两数' in line:
                            continue
                        found_lines.append(ln)
                if found_lines:
                    errors.append(f"废弃货币'{currency}': {path} 第{found_lines}行")

    if not any(any(dc in content and '废弃' not in content for dc in deprecated_currencies)
               for path, content in docs.items() if not any(dm in path for dm in deprecated_modules)):
        passed.append("废弃货币: 0残留")

    # ── 检查2: WuXing 枚举重复定义 ──
    for path, content in docs.items():
        if '共享系统接口' in path: continue
        if re.search(r'public\s+enum\s+WuXing\b', content):
            errors.append(f"WuXing枚举重定义: {path}（权威定义在共享系统接口定义.md）")

    if not any(re.search(r'public\s+enum\s+WuXing\b', c)
               for p, c in docs.items() if '共享系统接口' not in p):
        passed.append("WuXing枚举: 无重定义")

    # ── 检查3: 物价系数 ──
    coefficients = data['palace_price_coefficients']
    for path, content in docs.items():
        for palace, expected in coefficients.items():
            if palace == 'authority': continue
            # 查找 "XX宫.*系数.*数字" 的模式
            pattern = rf'{palace}.*?[系×][数].*?([\d.]+)'
            for m in re.finditer(pattern, content):
                found = float(m.group(1))
                if abs(found - expected) > 0.01:
                    # 排除共享接口自身的定义
                    if '共享系统接口' not in path:
                        warnings.append(f"物价系数不一致: {path}中{palace}={found}（权威={expected}）")

    passed.append("物价系数: 检查完成")

    # ── 检查4: BOSS 掉落 ──
    boss_rewards = {k:v for k,v in data['boss_rewards'].items() if k != 'authority'}
    for path, content in docs.items():
        for boss, reward in boss_rewards.items():
            expected_copper = reward['copper']
            expected_sc = reward['star_crystal']
            # 查找 BOSS名称附近 + 铜钱数字 + 星晶数字 的组合
            for m in re.finditer(rf'{boss}.*?(\d+)\s*文.*?(\d+)\s*(?:星晶|颗)', content):
                found_copper = int(m.group(1))
                found_sc = int(m.group(2))
                if found_copper != expected_copper or found_sc != expected_sc:
                    warnings.append(f"BOSS掉落: {path}中{boss}={found_copper}文+{found_sc}星晶（权威={expected_copper}+{expected_sc}）")

    passed.append("BOSS掉落: 检查完成")

    # ── 检查5: 废弃术语（仅检查deprecated_variants·跳过allowed_aliases） ──
    for term, info in data['standard_terms'].items():
        for dv in info.get('deprecated_variants', []):
            for path, content in docs.items():
                if dv in content:
                    if '共享系统接口' not in path and not any(dm.replace('\\', '/') in path.replace('\\', '/') for dm in deprecated_modules):
                        warnings.append(f"废弃术语'{dv}': {path}（建议改为'{term}'）")

    passed.append(f"术语统一: {len(data['standard_terms'])} 组标准术语已检查")

    # ── 检查6: GDD 共享接口引用 ──
    gdd_list = data['gdd_docs_requiring_shared_ref']
    for gdd in gdd_list:
        if gdd in docs:
            if '共享标准引用' not in docs[gdd] and '共享系统接口' not in docs[gdd]:
                errors.append(f"缺共享引用: {gdd}")

    if all('共享标准引用' in docs.get(g, '') or '共享系统接口' in docs.get(g, '') for g in gdd_list):
        passed.append(f"GDD共享引用: {len(gdd_list)}/{len(gdd_list)} 已引用")

    # ── 检查7: Wikilink 断链（仅检查.md目标·跳过代码块） ──
    for path, content in docs.items():
        # 去掉代码块中的内容，避免示例 wikilink 被误判
        clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        clean_content = re.sub(r'`[^`]+`', '', clean_content)
        refs = re.findall(r'\[\[([^\]]+)\]\]', clean_content)
        for ref in refs:
            # 跳过非.md文件引用（如 .json, .py 等）
            if not ref.endswith('.md') and '.' in ref:
                continue
            ref_clean = ref.lower().replace(' ','-').replace('·','-').replace('\\','/')
            found = any(ref_clean in dp.lower().replace(' ','-').replace('·','-').replace('\\','/') for dp in docs)
            if not found:
                warnings.append(f"断链: {path} → [[{ref}]]")

    passed.append("Wikilink: 检查完成")

    # ── 检查8: TODO/待定 ──
    for path, content in docs.items():
        if any(dm.replace('\\', '/') in path.replace('\\', '/') for dm in deprecated_modules): continue
        if 'AI生成原始版' in path: continue
        lines = content.split('\n')
        for ln, line in enumerate(lines, 1):
            # 跳过代码块和元引用（如表格中描述审计项的 TODO/待定标记）
            if ('待定' in line or 'TODO' in line or 'FIXME' in line) and '废弃' not in line:
                # 跳过 frontmatter（其 status 字段可能含"待补充"）
                # 跳过描述审计检查本身的元引用行
                if 'TODO/待定标记' in line or '待定项' in line:
                    continue
                warnings.append(f"待定项: {path}:{ln}: {line.strip()[:70]}")

    passed.append("TODO/待定: 检查完成")

    # ── 检查9: C# 花括号平衡 ──
    for path, content in docs.items():
        blocks = re.findall(r'```csharp\n(.*?)```', content, re.DOTALL)
        for i, block in enumerate(blocks):
            opens = block.count('{')
            closes = block.count('}')
            if opens != closes:
                errors.append(f"C#花括号: {path} block#{i+1} ({{={opens}, }}={closes}, 差{opens-closes})")

    passed.append("C#花括号: 检查完成")

    # ── 检查10: 项目统计 ──
    total_chars = sum(len(c) for c in docs.values())
    passed.append(f"项目规模: {len(docs)} 文档 · {total_chars:,} 字符")

    return errors, warnings, passed

# ─── 输出 ──────────────────────────────────────────────────
def print_report(errors, warnings, passed, json_output=False):
    if json_output:
        print(json.dumps({
            'status': 'error' if errors else ('warn' if warnings else 'ok'),
            'errors': errors, 'warnings': warnings, 'passed': passed
        }, ensure_ascii=False, indent=2))
        return

    print()
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  星河倒悬 —— 全项目自动审计{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print()

    if passed:
        for p in passed:
            print(f"  {ok(p)}")
        print()

    if warnings:
        print(f"{Colors.BOLD}  ⚠️ 警告 ({len(warnings)}){Colors.RESET}")
        for w in warnings:
            print(f"     {w}")
        print()

    if errors:
        print(f"{Colors.BOLD}  🔴 错误 ({len(errors)}){Colors.RESET}")
        for e in errors:
            print(f"     {e}")
        print()

    # 总结
    total = len(errors) + len(warnings)
    print(f"{Colors.BOLD}{'─'*60}{Colors.RESET}")
    if total == 0:
        print(f"  {ok('零问题 —— 项目数据完全一致')}")
    elif errors:
        print(f"  {err(f'{len(errors)} 个错误 + {len(warnings)} 个警告 —— 建议修复错误后再提交')}")
    else:
        print(f"  {warn(f'{len(warnings)} 个警告 —— 建议修复后重新审计')}")
    print(f"{Colors.BOLD}{'─'*60}{Colors.RESET}")
    print()

# ─── 主入口 ────────────────────────────────────────────────
def main():
    json_output = '--json' in sys.argv
    fix_mode = '--fix' in sys.argv

    print(f"  加载共享数据: {DATA_FILE.name} ...")
    data = load_data()

    print(f"  扫描文档 ...")
    docs = load_docs()
    print(f"  已加载 {len(docs)} 个文档\n")

    errors, warnings, passed = audit(data, docs, json_output)
    print_report(errors, warnings, passed, json_output)

    if fix_mode and (errors or warnings):
        print("  --fix 模式暂不支持自动修复·请手动处理上述问题")

    if errors: sys.exit(2)
    if warnings: sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
