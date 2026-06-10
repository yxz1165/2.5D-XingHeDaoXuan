# 团结引擎 (Tuanjie Engine) — Version Reference

| Field | Value |
|-------|-------|
| **Engine Version** | 团结引擎 1.9.0 |
| **Release Date** | 2026-05-19 |
| **Project Pinned** | 2026-05-21 |
| **Last Docs Verified** | 2026-05-21 |
| **LLM Knowledge Cutoff** | May 2025 |

## Knowledge Gap Warning

团结引擎是 Unity 中国版，基于 Unity 引擎但独立发展。1.6+ 版本引入了大量
Unity 6 对应的新特性。LLM 训练数据中的 Unity 知识截止到 2022 LTS 左右，
与团结引擎 1.9.0 存在显著差异。始终在编写代码前查阅本目录下的参考文档。

## 版本历史

| 版本 | 发布日期 | 风险 | 主要特性 |
|------|---------|------|---------|
| 1.6 LTS | 2025 | MEDIUM | 首个 LTS，基础稳定 |
| 1.7 | 2026-03 | MEDIUM | Preview，新功能预览 |
| 1.8 | 2026-01 | MEDIUM | 开源 Demo《Tower Valley》 |
| 1.9.0 | 2026-05-19 | HIGH | 全局动态光照移动端、并行渲染、自适应光照探针 |

## 从标准 Unity 迁移注意事项

- **API 兼容性**：团结引擎与 Unity 6.x API 高度兼容，C# 脚本可直接使用
- **中国平台支持**：内置微信小游戏、抖音小游戏、鸿蒙 (HarmonyOS) 等平台导出
- **文档语言**：官方文档为中文，地址 https://docs.unity.cn/
- **包管理**：使用 Unity 中国版 Package Manager（部分包名与国际版不同）
- **TuanjieGI**：团结引擎独有全局光照系统，支持移动端实时动态光照

## Verified Sources

- 官方文档: https://docs.unity.cn/cn/tuanjiemanual/Manual/
- 下载页面: https://unity.cn/tuanjie/releases
- 开发者社区: https://developer.unity.cn/
- 团结 Hub: https://unity.cn/tuanjie
