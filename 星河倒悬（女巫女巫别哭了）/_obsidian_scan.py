"""Obsidian wikilink/tag/frontmatter 全面扫描"""
import re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).parent

all_files = {}
has_frontmatter = []
no_frontmatter = []
all_links = []
all_tags = []

for f in ROOT.rglob("*.md"):
    if f.name.startswith("_"):
        continue
    try:
        content = f.read_text(encoding="utf-8")
    except Exception:
        continue
    rel = str(f.relative_to(ROOT)).replace("\\", "/")
    all_files[rel] = content

    if content.startswith("---"):
        has_frontmatter.append(rel)
    else:
        no_frontmatter.append(rel)

    # Extract wikilinks [[...]]
    wls = re.findall(r"\[\[([^\]]+)\]\]", content)
    for wl in wls:
        target = wl.split("|")[0].split("#")[0].strip()
        all_links.append((rel, target))

    # Extract tags #tag (Obsidian-style: must not be inside code blocks)
    # Remove code blocks first
    clean = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    clean = re.sub(r"`[^`]+`", "", clean)
    tags = re.findall(r"(?:^|\s)#([\w一-鿿\-/]+)", clean)
    for t in tags:
        all_tags.append((rel, t))

# Check broken links
broken_links = []
resolved = 0
broken = 0

for src, target in all_links:
    if "://" in target or (".png" in target or ".jpg" in target or ".json" in target or ".py" in target):
        resolved += 1
        continue
    if target.endswith(".md"):
        target = target[:-3]

    target_clean = target.lower().replace(" ", "-").replace("·", "-").replace("\\", "/")
    found = False
    for fp in all_files:
        fp_clean = fp.lower().replace(" ", "-").replace("·", "-").replace("\\", "/")
        if fp_clean.endswith(".md"):
            fp_clean = fp_clean[:-3]
        if target_clean in fp_clean or fp_clean.endswith("/" + target_clean):
            found = True
            break
    if found:
        resolved += 1
    else:
        broken += 1
        broken_links.append((src, target))

# Output
print("=== 文档概况 ===")
print(f"总文档数: {len(all_files)}")
print(f"有 frontmatter: {len(has_frontmatter)}")
print(f"无 frontmatter: {len(no_frontmatter)}")

print(f"\n=== Wikilink 概况 ===")
print(f"总 wikilink 数: {len(all_links)}")
print(f"已解析: {resolved}")
print(f"断链: {broken}")

if broken_links:
    print("\n--- 断链列表 ---")
    by_src = defaultdict(list)
    for src, target in broken_links:
        by_src[src].append(target)
    for src, targets in sorted(by_src.items()):
        for t in targets:
            print(f"  [{src}] -> [[{t}]]")

print(f"\n=== 标签概况 ===")
print(f"总标签数: {len(all_tags)}")
tag_counts = Counter(t for _, t in all_tags)
print(f"不同标签数: {len(tag_counts)}")
if tag_counts:
    print("\n标签使用频次:")
    for tag, count in tag_counts.most_common(50):
        print(f"  #{tag}: {count}次")

print(f"\n=== 无 frontmatter 的文档 ({len(no_frontmatter)}) ===")
for f in no_frontmatter:
    print(f"  {f}")

# Check wikilink frequency
print(f"\n=== 最多被引用的文档 ===")
ref_counts = Counter(t for _, t in all_links)
for target, count in ref_counts.most_common(20):
    print(f"  [[{target}]]: {count}次被引用")

# Check which docs have NO incoming links
linked_docs = set()
for _, t in all_links:
    t_clean = t.lower().replace(" ", "-").replace("·", "-").replace("\\", "/")
    if t_clean.endswith(".md"):
        t_clean = t_clean[:-3]
    for fp in all_files:
        fp_clean = fp.lower().replace(" ", "-").replace("·", "-").replace("\\", "/")
        if fp_clean.endswith(".md"):
            fp_clean = fp_clean[:-3]
        if t_clean in fp_clean or fp_clean.endswith("/" + t_clean):
            linked_docs.add(fp)

unlinked = set(all_files.keys()) - linked_docs
# Exclude some known standalone files
standalone = {"00-总目录.md", "Phase1-开发计划.md", "战斗系统评估与优化.md", "世界观元素选用分析.md",
              "紫微命盘与道宫映射设计.md", "想象战斗画面.md"}
unlinked_filtered = {f for f in unlinked if f not in {x.replace(chr(92), "/") for x in standalone}}
print(f"\n=== 零被引文档 ({len(unlinked_filtered)}) ===")
for f in sorted(unlinked_filtered):
    print(f"  {f}")
