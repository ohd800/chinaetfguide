/* ===== live.js — best-effort live quotes with graceful fallback =====
   A pure static site cannot reliably hit most stock APIs from the browser:
   they require an API key and block cross-origin (CORS) requests. This module
   tries a public, key-less source (Stooq CSV) and, on ANY failure (offline,
   CORS, timeout, rate-limit), returns nulls so the page keeps its verified
   snapshot data. The tool always works; "live" is a bonus when the network
   and CORS allow it.

   To go fully live in production: point STOOQ (or replace fetchLive's URL) at
   your own keyed/proxied quote endpoint, and adapt parseCSV() to its shape. */
(function(){
  var STOOQ = "https://stooq.com/q/l/?s=";

  function toStooq(ticker, venue){ return (ticker + "." + venue).toLowerCase(); }

  function parseCSV(txt, items){
    var out = {}; items.forEach(function(i){ out[i.key] = null; });
    try{
      var lines = txt.trim().split("\n").slice(1);
      lines.forEach(function(l){
        var p = l.split(",");
        if(p.length < 8) return;
        var sym = p[0].toUpperCase();
        var close = parseFloat(p[6]);
        var hit = items.find(function(i){ return toStooq(i.ticker, i.venue).toUpperCase() === sym; });
        if(hit && !isNaN(close)) out[hit.key] = close;
      });
    }catch(e){}
    return out;
  }

  /* items: [{key, ticker, venue}] ; returns promise -> {key: closeNumber|null} */
  function fetchLive(items){
    return new Promise(function(resolve){
      var results = {}; items.forEach(function(i){ results[i.key] = null; });
      var syms = items.map(function(i){ return toStooq(i.ticker, i.venue); }).join("+");
      var url = STOOQ + encodeURIComponent(syms) + "&f=sd2t2ohlcv&h&e=csv";
      var done = false;
      var timer = setTimeout(function(){ if(!done){ done = true; resolve(results); } }, 4500);
      fetch(url, {mode:"cors"}).then(function(res){
        if(!res.ok) throw new Error("http " + res.status);
        return res.text();
      }).then(function(txt){
        var parsed = parseCSV(txt, items);
        Object.keys(parsed).forEach(function(k){ results[k] = parsed[k]; });
        if(!done){ done = true; clearTimeout(timer); resolve(results); }
      }).catch(function(){
        if(!done){ done = true; clearTimeout(timer); resolve(results); }
      });
    });
  }

  window.ChinaLive = { fetchLive: fetchLive, STOOQ: STOOQ };
})();
