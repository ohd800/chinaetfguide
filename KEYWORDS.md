# ChinaETFGuide 关键词策略（结合哥飞 / gefei7 方法重选）

> 核心方法论（哥飞）：先收词→看搜索意图→再规划结构；每页只打一个具体词；树状内链逐级提权；
> 长尾 + 低竞争优先；用「程序化 SEO」把一套模板批量放大成成百上千页；内容必须差异化。
> 本站优势切口：**外国人 + 地区细分 + 工具化**（竞品 investinchinesestocks / vested / chinainvestors 都没做聚合）。

---

## 一、验证过的真实需求信号（来自检索）

高频真实 query（意图清晰、竞争相对可控）：
- `how to invest in Chinese stocks as a foreigner` / `from the US` / `from India` / `from the UK` / `from Singapore`
- `how to buy Chinese stocks as a foreigner` / `how to buy China A-shares as a foreigner`
- `best China ETF 2026` / `best China ETF for foreign investors`
- `MCHI vs FXI` / `KWEB vs MCHI` / `MCHI vs FXI vs KWEB`
- `Chinese ADR delisting risk` / `HFCAA China stocks explained` / `will Chinese ADRs be delisted`
- `what is an ADR` / `A-shares vs H-shares vs ADRs`
- `buy Alibaba stock as a foreigner` / `Tencent stock ticker US` / `how to buy BYD stock`
- `best broker for Chinese stocks` / `Interactive Brokers China A-shares` / `Stock Connect China foreign investors`

竞品弱点（我们的机会）：它们多是「一篇文章讲完所有」，没有把 **按国家细分 / 按公司细分 / 按 ETF 细分 / 工具化** 拆开——而这些细分词恰恰是低竞争、高意图的甜区。

---

## 二、核心关键词树（已建页面 → 已占词）

| 页面 | 主打词（每页一词） | 搜索意图 |
|---|---|---|
| `index.html` | invest in Chinese stocks as a foreigner | 导航/综述 |
| `etf.html` | China ETF comparison / best China ETF / MCHI vs FXI | 商业调研 |
| `adr.html` | Chinese ADR delisting risk / HFCAA China stocks | 信息+风险 |
| `broker.html` | how to buy Chinese stocks from [country] / best broker for Chinese stocks | 交易/转化 |
| `symbols.html` | [Company] stock ticker / how to buy [Company] stock as foreigner | 交易/转化 |
| `learn.html` | A-shares vs H-shares vs ADRs | 信息 |

> 已建 4 篇 guides 覆盖：how-to-invest / a-shares-vs-h-shares / adr-delisting-explained / best-china-etf。

---

## 三、长尾词清单（三级页 / 待建）

**A. 地区细分（geo-modifier，哥飞最强调的放大法）**
- how to invest in Chinese stocks from the US / UK / India / Singapore / Australia / Canada / Germany / UAE
- 同一模板 × 8+ 国家 = 8+ 页，且每个国家对应 broker finder 的一个 region 维度。

**B. 入门/概念（信息意图 → 引流）**
- what is an ADR (American Depositary Receipt)
- what are A-shares / what are H-shares
- China Stock Connect explained for foreigners
- are Chinese stocks safe for foreign investors

**C. 风险/决策（商业调研意图）**
- will Chinese ADRs be delisted in 2026
- HFCAA explained simply
- best China ETF 2026 for foreign investors
- MCHI vs FXI vs KWEB which is better

---

## 四、程序化 SEO 机会（最大增量，用现有数据模板批量生成）

**这是哥飞打法的核心杠杆：一套模板 + 一张数据表 = 成百上千页。**

### 1) 每个公司一页（已有 20 家数据，直接复用 `assets/data.js`）
模板字段：`公司名 / 英文名 / A股代码 / H股代码 / ADR代码 / 行业 / 外国人可买入口 / 一句话点评`
衍生词（每公司 3–5 个）：
- `How to buy Tencent stock` / `Tencent stock ticker` / `Tencent ADR vs HK share`
- `How to buy Alibaba stock as a foreigner` / `BABA Hong Kong ticker`
- `Buy BYD stock from the US` / `BYD ticker US`
- 覆盖：Tencent, Alibaba, BYD, Meituan, PDD, JD, Baidu, NIO, XPeng, Li Auto, NetEase, Trip.com, TME, Bilibili, WB, ICBC, CCB, China Mobile, Kweichow Moutai, CATL … → **60–100 页**

### 2) 每个 ETF 一页（已有 6 只数据）
模板字段：`ETF名 / 代码 / 费率 / AUM / 跟踪指数 / 主要持仓 / 适合谁 / vs 其他ETF`
衍生词：
- `MCHI ETF review` / `MCHI vs FXI` / `is MCHI a good ETF`
- `KWEB vs MCHI` / `best China internet ETF`
- `ASHR vs MCHI`（A股曝光对比）
- → **15–25 页**

### 3) 每个「地区×意图」一页（复用 broker finder 的 REGIONS/TARGETS 维度）
- `best broker for Chinese stocks in the US` / `in the UK` / `in India` / `in Singapore` / `in Australia`
- `can I buy Chinese stocks on Robinhood` / `Interactive Brokers China A-shares guide`
- → **20–40 页**

> 合计潜在页面：**100–200+ 页**，且全部由现有结构化数据驱动，维护成本低。这正是哥飞说的「程序化 SEO」。

---

## 五、关键词 → 页面映射 & 待建清单

**已有（占词完成）**：首页、ETF 对比器、ADR 检查器、券商 Finder、Ticker、Market101、4 篇 guides。

**建议新增（按优先级）**：
1. 【高】地区细分指南 × 8 国（how-to-invest-from-[country]）—— 直接复用 broker finder 逻辑，内链回工具。
2. 【高】公司单页 × 20（从 symbols 数据生成）—— 吃 `Tencent stock ticker` 类高意图词。
3. 【中】ETF 单页 × 6（从 etf 数据生成）—— 吃 `MCHI vs FXI` 类对比词。
4. 【中】概念页：what is an ADR / A-shares vs H-shares / Stock Connect explained。
5. 【低】地区×broker 页 × 5。

---

## 六、执行优先级（哥飞：先做能跑流量的）

1. **立刻可做（零新数据）**：把现有 4 个工具页 + guides 的 title/H1 已对齐核心词；补 `how-to-invest-from-[country]` 8 页（模板化）。
2. **第二波（用现有 data.js）**：用 symbols 数据脚本生成 20 个公司页 + 6 个 ETF 页（程序化）。
3. **第三波**：概念页 + 地区×broker 页。
4. **上线后**：GSC 提交 sitemap → 看哪些长尾词有展现 → 反哺补词（哥飞：用 Search Console 数据迭代词表）。

---

## 七、合规红线（金融站必守）
- 每页保留 `not financial advice` + 数据 as-of 标注（已有）。
- 不写「必涨/稳赚/保证收益」类词，避免被 Google 金融内容政策 / 广告政策打击。
- 程序化页面必须**差异化**（每页公司/数据不同），禁止一份模板只换标题——否则被判定薄内容（thin content）。
