/* ===== live.js — best-effort live quotes with graceful fallback =====
   A pure static site cannot reliably hit most stock APIs from the browser:
   they require an API key and block cross-origin (CORS) requests. This module
   tries a public, key-less source (Stooq CSV) and, on ANY failure (offline,
   CORS, timeout, rate-limit), falls back to a weekly-refreshed cache file
   (assets/prices.json, produced by the GitHub Action) so visitors still see
   reasonably fresh numbers. If both fail, the page keeps its verified snapshot.

   To go fully live in production: point STOOQ (or replace fetchLive's URL) at
   your own keyed/proxied quote endpoint, and adapt parseCSV() to its shape. */
(function(){
  var STOOQ = "https://stooq.com/q/l/?s=";
  var CACHE = "/assets/prices.json";

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

  /* items: [{key, ticker, venue}] ; resolves -> {key: closeNumber|null, __meta:{live,cachedUpdated}} */
  function fetchLive(items){
    return new Promise(function(resolve){
      var results = {}; items.forEach(function(i){ results[i.key] = null; });
      var syms = items.map(function(i){ return toStooq(i.ticker, i.venue); }).join("+");
      var url = STOOQ + encodeURIComponent(syms) + "&f=sd2t2ohlcv&h&e=csv";
      var cached = {};
      var cachedUpdated = null;

      function finish(liveOk){
        // fill any still-null slots from the weekly cache
        Object.keys(results).forEach(function(k){
          if(results[k] == null){
            var item = items.find(function(i){ return i.key === k; });
            if(item){
              var ck = toStooq(item.ticker, item.venue).toUpperCase();
              if(cached[ck] != null) results[k] = cached[ck];
            }
          }
        });
        results.__meta = { live: liveOk, cachedUpdated: cachedUpdated };
        resolve(results);
      }

      // best-effort cache (non-blocking)
      fetch(CACHE, {cache:"no-store"}).then(function(r){ return r.json(); }).then(function(j){
        cached = (j && j.prices) || {};
        cachedUpdated = (j && j.updated) || null;
      }).catch(function(){});

      var done = false;
      var timer = setTimeout(function(){ if(!done){ done = true; finish(false); } }, 4500);
      fetch(url, {mode:"cors"}).then(function(res){
        if(!res.ok) throw new Error("http " + res.status);
        return res.text();
      }).then(function(txt){
        var parsed = parseCSV(txt, items);
        var anyLive = false;
        Object.keys(parsed).forEach(function(k){ if(parsed[k] != null){ results[k] = parsed[k]; anyLive = true; } });
        if(!done){ done = true; clearTimeout(timer); finish(anyLive); }
      }).catch(function(){
        if(!done){ done = true; finish(false); }
      });
    });
  }

  window.ChinaLive = { fetchLive: fetchLive, STOOQ: STOOQ };
})();
