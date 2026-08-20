/* ===== Shared data for ChinaETFGuide (classic script — defines globals) ===== */
/* All figures are indicative snapshots compiled from public fund / exchange
   sources as of August 2026. Verify before investing. */

const ETFs = [
  {tk:"MCHI",issuer:"iShares (BlackRock)",name:"iShares MSCI China ETF",theme:"Broad",expo:"Offshore",
   expoDetail:"MSCI China — HK-listed H-shares + US ADRs (~80% HK/US, ~17% A-share via Connect)",
   expense:0.59,aum:"$6.2B",yield:"~2.0%",yieldN:2.0,holdings:575,
   top:["Tencent","Alibaba","China Construction Bank"],index:"MSCI China Index",
   best:"Core, diversified China holding in one position"},
  {tk:"FXI",issuer:"iShares (BlackRock)",name:"iShares China Large-Cap ETF",theme:"Large-cap",expo:"Offshore",
   expoDetail:"Top 50 H-shares listed in Hong Kong (100% HKD)",
   expense:0.74,aum:"$4.2B",yield:"~2.0%",yieldN:2.0,holdings:52,
   top:["Alibaba","China Construction Bank","Tencent"],index:"FTSE China 50 Index",
   best:"Large-cap, income tilt (SOE banks & telecoms)"},
  {tk:"KWEB",issuer:"KraneShares",name:"KraneShares CSI China Internet ETF",theme:"Internet",expo:"Offshore",
   expoDetail:"China internet — HK-listed + US ADRs (Tencent, Alibaba, PDD, Meituan)",
   expense:0.69,aum:"$5.2B",yield:"~0.5%",yieldN:0.5,holdings:40,
   top:["Tencent","Alibaba","PDD"],index:"CSI Overseas China Internet Index",
   best:"High-conviction China tech / internet bet"},
  {tk:"ASHR",issuer:"Xtrackers (DWS)",name:"Xtrackers Harvest CSI 300 China A-Shares ETF",theme:"A-shares",expo:"Onshore",
   expoDetail:"Mainland A-shares via CSI 300 — true onshore access (RMB)",
   expense:0.65,aum:"$1.5B",yield:"~2.1%",yieldN:2.1,holdings:300,
   top:["Ping An","Kweichow Moutai","China Merchants Bank"],index:"CSI 300 Index",
   best:"Direct mainland A-share exposure"},
  {tk:"CQQQ",issuer:"Invesco",name:"Invesco China Technology ETF",theme:"Tech",expo:"Offshore",
   expoDetail:"Broad China tech — internet + semis + hardware (HK + ADRs)",
   expense:0.65,aum:"$3.2B",yield:"~2.1%",yieldN:2.1,holdings:182,
   top:["Tencent","Meituan","Baidu"],index:"FTSE China Inclusive Technology Index",
   best:"Tech beyond internet (chips, hardware, EV supply chain)"},
  {tk:"GXC",issuer:"SPDR (State Street)",name:"SPDR S&P China ETF",theme:"Broad",expo:"Offshore",
   expoDetail:"Broad China via S&P methodology — HK + ADRs, quality screen",
   expense:0.59,aum:"$0.48B",yield:"~2.2%",yieldN:2.2,holdings:1344,
   top:["Alibaba","Tencent","China Construction Bank"],index:"S&P China BMI Index",
   best:"Broad, low-cost alternative to MCHI"}
];

/* China ADRs — risk model: the dominant mitigant against a US delisting is a
   Hong Kong listing. Dual-primary HK = Low; HK secondary = Medium; no HK = High.
   Sources: investinchinesestocks.com, vested.blog, HKEX news (Aug 2026). */
const ADRs = [
  {tk:"BABA",co:"Alibaba Group",exch:"NYSE",sector:"E-commerce / Cloud",hk:"9988.HK",hkType:"Dual-primary (HK is primary since 2022)",risk:"Low",flag:true,
   flagText:"Named in a 2025 US House Select Committee delisting-demand letter — elevated political spotlight, but the HK primary listing is the strongest available mitigant."},
  {tk:"LI",co:"Li Auto",exch:"NASDAQ",sector:"Electric vehicles",hk:"2015.HK",hkType:"Dual-primary",risk:"Low",flag:false,flagText:""},
  {tk:"JD",co:"JD.com",exch:"NASDAQ",sector:"E-commerce",hk:"9618.HK",hkType:"Secondary listing",risk:"Medium",flag:false,flagText:""},
  {tk:"BIDU",co:"Baidu",exch:"NASDAQ",sector:"Search / AI",hk:"9888.HK",hkType:"Secondary; converting to dual-primary in 2026",risk:"Medium",flag:true,
   flagText:"Named in a 2025 US House Select Committee delisting-demand letter. Announced conversion to HK dual-primary (expected 2026), which would further reduce risk."},
  {tk:"NTES",co:"NetEase",exch:"NASDAQ",sector:"Gaming / Music",hk:"9999.HK",hkType:"Secondary; moving toward primary on volume rule",risk:"Medium",flag:false,flagText:""},
  {tk:"NIO",co:"NIO",exch:"NYSE",sector:"Premium EVs",hk:"9866.HK",hkType:"Secondary listing",risk:"Medium",flag:false,flagText:""},
  {tk:"XPEV",co:"XPeng",exch:"NYSE",sector:"Smart EVs",hk:"9868.HK",hkType:"Secondary listing",risk:"Medium",flag:false,flagText:""},
  {tk:"TCOM",co:"Trip.com",exch:"NASDAQ",sector:"Online travel",hk:"9961.HK",hkType:"Secondary listing",risk:"Medium",flag:false,flagText:""},
  {tk:"TME",co:"Tencent Music",exch:"NYSE",sector:"Music streaming",hk:"1698.HK",hkType:"Secondary listing",risk:"Medium",flag:false,flagText:""},
  {tk:"BILI",co:"Bilibili",exch:"NASDAQ",sector:"Video / community",hk:"9626.HK",hkType:"Secondary listing",risk:"Medium",flag:false,flagText:""},
  {tk:"WB",co:"Weibo",exch:"NASDAQ",sector:"Social media",hk:"9898.HK",hkType:"Secondary listing",risk:"Medium",flag:false,flagText:""},
  {tk:"PDD",co:"PDD Holdings (Pinduoduo / Temu)",exch:"NASDAQ",sector:"E-commerce",hk:null,hkType:"No Hong Kong listing",risk:"High",flag:false,
   flagText:"No HK listing as of Aug 2026 — if the US door closed there is no obvious place to land, so delisting exposure is materially higher than dual-listed peers."}
];

/* ===== Broker / Access Finder rules (educational; examples, not advice) ===== */
const REGIONS = [
  {k:"US", label:"United States"},
  {k:"EU", label:"Europe (EU/EEA)"},
  {k:"UK", label:"United Kingdom"},
  {k:"CA", label:"Canada"},
  {k:"AU", label:"Australia"},
  {k:"SG", label:"Singapore"},
  {k:"HK", label:"Hong Kong"},
  {k:"OTHER", label:"Other / Rest of world"}
];

const TARGETS = [
  {k:"etf", label:"China ETFs (US-listed: MCHI, FXI, KWEB, ASHR, GXC)"},
  {k:"adr", label:"China ADRs (BABA, JD, PDD, NIO…)"},
  {k:"hshare", label:"H-shares (HK-listed Chinese stocks, e.g. 9988.HK)"},
  {k:"ashare", label:"A-shares (mainland stocks)"}
];

const INV_TYPES = [
  {k:"retail", label:"Retail investor"},
  {k:"inst", label:"Institutional / qualified"}
];

/* level: ok | warn | limited */
const BROKER_RULES = {
  etf: {
    US:    {level:"ok", path:"US-listed China ETFs are available through <b>any US brokerage</b>. They are US-domiciled funds, so there is no PRIIPs/KIID obstacle.",
            examples:["Schwab","Fidelity","Vanguard","Robinhood","Interactive Brokers"]},
    EU:    {level:"warn", path:"<b>US-domiciled ETFs (MCHI, FXI, KWEB, ASHR, GXC) generally cannot be sold to EU retail</b> under PRIIPs/KIID rules. Use a <b>UCITS</b> China ETF instead (EU-domiciled, KIID-compliant).",
            examples:["iShares MSCI China UCITS","Xtrackers CSI 300 UCITS","via Interactive Brokers / Saxo / DEGIRO / Trade Republic"]},
    UK:    {level:"warn", path:"Post-Brexit the UK mirrors much of PRIIPs; a <b>UCITS</b> China ETF is the safe route for retail. Some platforms allow US ETFs via specific arrangements — confirm first.",
            examples:["iShares MSCI China UCITS","via Interactive Brokers / Saxo / Hargreaves Lansdown"]},
    CA:    {level:"ok", path:"Accessible via Canadian brokers with US-market access. Confirm the specific fund is offered (availability varies by platform).",
            examples:["Interactive Brokers","Questrade","Wealthsimple","RBC Direct Investing"]},
    AU:    {level:"ok", path:"Via international brokers with US access, or trade <b>ASX-listed</b> China ETFs in AUD to avoid FX/custody friction.",
            examples:["Interactive Brokers","Stake","CommSec International","IZZ (iShares China, ASX)"]},
    SG:    {level:"ok", path:"Via local brokers with US access, or SGX-listed China ETFs.",
            examples:["Interactive Brokers","POEMS","Tiger","Moomoo"]},
    HK:    {level:"ok", path:"Via US-market access platforms, or buy HKEX-listed China ETFs directly.",
            examples:["Interactive Brokers","Futu","Tiger","HKEX-listed China ETFs"]},
    OTHER: {level:"ok", path:"Use a global broker with US-market access. Local rules vary — confirm with a local advisor.",
            examples:["Interactive Brokers (most universal)"]}
  },
  adr: {
    US:    {level:"ok", path:"Any US brokerage. Watch <b>HFCAA delisting &amp; VIE</b> risk — check the name in the ADR Risk Checker.",
            examples:["Schwab","Fidelity","Interactive Brokers","Robinhood"]},
    EU:    {level:"ok", path:"Buyable via brokers with US-stock access. ADRs are <b>stocks, not funds</b>, so PRIIPs/KIID does not block them — but HFCAA/VIE risk still applies (see ADR Risk Checker).",
            examples:["Interactive Brokers","Saxo","DEGIRO"]},
    UK:    {level:"ok", path:"Via brokers with US-stock access. PRIIPs does not apply to single stocks; mind HFCAA/VIE risk.",
            examples:["Interactive Brokers","Saxo","Hargreaves Lansdown"]},
    CA:    {level:"ok", path:"Via Canadian brokers with US-stock access.",
            examples:["Interactive Brokers","Questrade","Wealthsimple"]},
    AU:    {level:"ok", path:"Via international brokers with US-stock access.",
            examples:["Interactive Brokers","Stake","CommSec International"]},
    SG:    {level:"ok", path:"Via local brokers with US-stock access.",
            examples:["Interactive Brokers","POEMS","Tiger","Moomoo"]},
    HK:    {level:"ok", path:"Via US-market access platforms.",
            examples:["Interactive Brokers","Futu","Tiger"]},
    OTHER: {level:"ok", path:"Use a global broker with US-stock access. Confirm local rules with an advisor.",
            examples:["Interactive Brokers"]}
  },
  hshare: {
    US:    {level:"ok", path:"Via an international broker that offers the Hong Kong market (e.g. ADR's HK line, or buy the H-share directly as 9988.HK).",
            examples:["Interactive Brokers","Saxo"]},
    EU:    {level:"ok", path:"Via an international broker with HK market access, or buy a UCITS China ETF that holds H-shares.",
            examples:["Interactive Brokers","Saxo","UCITS China ETFs"]},
    UK:    {level:"ok", path:"Via an international broker with HK market access.",
            examples:["Interactive Brokers","Saxo"]},
    CA:    {level:"ok", path:"Via a broker with HK market access (Interactive Brokers is the most common).",
            examples:["Interactive Brokers"]},
    AU:    {level:"ok", path:"Via a broker with HK access, or ASX/SGX-listed China products.",
            examples:["Interactive Brokers","Stake","CommSec International"]},
    SG:    {level:"ok", path:"Direct HKEX access is easy from Singapore via local brokers.",
            examples:["Interactive Brokers","POEMS","Tiger","Moomoo"]},
    HK:    {level:"ok", path:"Direct HKEX access via any local broker — the simplest route of all.",
            examples:["Futu","Tiger","HSBC","Standard Chartered","Interactive Brokers"]},
    OTHER: {level:"ok", path:"Use a global broker with HK market access. Confirm local rules with an advisor.",
            examples:["Interactive Brokers","Saxo"]}
  },
  ashare: {
    US:    {level:"limited", path:"Most retail foreigners <b>cannot open a direct A-share account</b>. The easiest route is an <b>A-share ETF listed in the US</b> — <b>ASHR</b> (Xtrackers Harvest CSI 300) tracks the CSI 300. Broader China ETFs (MCHI/FXI) also hold some A-shares via Stock Connect.",
            examples:["ASHR (US-listed)","MCHI / FXI (partial A-share via Connect)","Interactive Brokers (ChinaConnect, eligible clients)"]},
    EU:    {level:"limited", path:"ASHR is a US ETF → PRIIPs blocks it for EU retail. Use a <b>UCITS</b> China A-share fund instead.",
            examples:["Xtrackers CSI 300 UCITS","Lyxor / Amundi MSCI China A UCITS","via Interactive Brokers / Saxo"]},
    UK:    {level:"limited", path:"Prefer a <b>UCITS</b> China A-share fund for retail. Direct A-share access via Stock Connect is limited to qualifying brokers.",
            examples:["Xtrackers CSI 300 UCITS","Interactive Brokers (eligible)"]},
    CA:    {level:"limited", path:"Reach A-shares via an A-share ETF (ASHR in the US, or a local UCITS equivalent) or Stock Connect through a qualifying broker.",
            examples:["ASHR (via US access)","Interactive Brokers (ChinaConnect)"]},
    AU:    {level:"limited", path:"Via an A-share ETF or Stock Connect through a qualifying international broker.",
            examples:["ASHR (via US access)","Interactive Brokers (ChinaConnect)"]},
    SG:    {level:"limited", path:"Singapore is a Stock Connect hub — some brokers offer A-share access; otherwise use an A-share ETF.",
            examples:["Interactive Brokers (ChinaConnect)","POEMS (eligible)","A-share ETFs"]},
    HK:    {level:"ok", path:"Hong Kong is the gateway: <b>Stock Connect</b> (Northbound) lets eligible HK accounts trade mainland A-shares directly.",
            examples:["Interactive Brokers (ChinaConnect)","Futu","Tiger","via Stock Connect"]},
    OTHER: {level:"limited", path:"For most foreign retail, A-share exposure is best reached <b>indirectly through a broad China ETF</b> rather than individual mainland stocks. Direct access needs Stock Connect / QFII via a qualifying broker.",
            examples:["Broad China ETF (MCHI/FXI/UCITS)","Interactive Brokers (eligible)"]}
  }
};

const BROKER_STATUS_LABEL = {ok:"✓ Generally accessible", warn:"⚠ Restricted — read notes", limited:"△ Harder — indirect route"};
