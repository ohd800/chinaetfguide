# ChinaETFGuide — SEO Plan (based on 哥飞 / gefei7 methodology)

> Methodology source: 哥飞 (公众号 gefei7) 出海 SEO 打法，核心要点：
> 1. 先收集关键词 → 看搜索意图 → 再规划网站结构（不先搭首页再想词）
> 2. 小而美：用首页/单页去打大站的内页，每页只聚焦一个具体关键词
> 3. 树状结构：首页(核心词) → 二级词页(工具) → 三级词内页(指南)，靠内链逐级提权
> 4. 站内改造：目标词进 title / H1 / 正文（循序渐进，不一次大改）；内容必须差异化
> 5. 技术动作：GSC + GA 提交、OG/Twitter 社交卡片、sitemap、robots、语义结构
> 6. 冷启动外链：Product Hunt / Hacker News / 周刊 / AI 导航站先拿第一批用户

## 1. 关键词 → 页面映射（树状）

| 层级 | 页面 | 主攻关键词（英文长尾） | 搜索意图 |
|---|---|---|---|
| 首页(核心) | index.html | invest in Chinese stocks as a foreigner | 总入口/导航 |
| 二级·工具 | etf.html | best China ETF / compare China ETFs | 对比决策 |
| 二级·工具 | adr.html | Chinese ADR delisting risk | 风险评估 |
| 二级·工具 | broker.html | how to buy Chinese stocks from US/EU/UK | 落地通道 |
| 二级·工具 | symbols.html (新) | China stock ticker / [公司] stock ticker | 查代码 |
| 三级·指南 | guides/how-to-invest.html | how to invest in Chinese stocks for beginners | 入门 |
| 三级·指南 | guides/a-shares-vs-h-shares.html | A-shares vs H-shares | 概念对比 |
| 三级·指南 | guides/adr-delisting-explained.html | what is ADR delisting risk | 概念解释 |
| 三级·指南 | guides/best-china-etf.html | best China ETF 2026 | 选型 |

## 2. 站内结构（内链策略）
- 首页 → 4 个工具页（卡片入口，锚文本多样：Compare China ETFs / Check ADR risk / Find a broker / Lookup a ticker）
- 每个工具页 → 回到首页 + 相关指南（如 etf.html → guides/best-china-etf.html）
- 每个指南 → 对应工具页（导流到可操作工具，提升转化）
- 全站统一 header 导航：Home / ETF / ADR Risk / Broker / Ticker / Guides / Market 101

## 3. 技术 SEO 清单（已落地）
- [x] 每页唯一 `<title>`（关键词前置，品牌后置）
- [x] 每页 `<meta description>`（含目标词 + 价值点）
- [x] Open Graph + Twitter Card（社交分享卡片）
- [x] `<link rel="canonical">`（占位域名，上线替换为真实域名）
- [x] JSON-LD：首页 Organization + WebSite；内页 BreadcrumbList；含 FAQ 页 FAQPage
- [x] `sitemap.xml` + `robots.txt`
- [x] `<html lang="en">`、语义化标签、移动端适配
- [ ] GSC 提交 + GA（上线后由用户接入，已留 GA 占位）
- [ ] 冷启动外链：Product Hunt / HN / 周刊 / AI 导航站（上线后执行）

## 4. 待用户补充
- 真实域名（替换 chinaetfguide.com 占位）→ 同时更新 canonical / og:url / sitemap
- Google Analytics ID（替换 G-XXXXXXX 占位）
- OG 图片 assets/og.png（建议 1200×630）
