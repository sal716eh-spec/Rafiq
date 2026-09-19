/* Shared theme control — 'system' (default, follows the OS), 'light', or 'dark'.
   Loaded as a normal blocking <script> as early as possible in <head>, before the
   stylesheet, so the data-theme attribute lands before first paint: no
   dark-then-light (or light-then-dark) flash on load. See site.css for how
   data-theme overrides the prefers-color-scheme media query. */
(function(){
  var KEY = 'bay_theme';

  function stored(){
    try{
      var v = localStorage.getItem(KEY);
      return (v === 'light' || v === 'dark') ? v : null;
    }catch(_){ return null; }
  }

  // Force the actual browser-chrome color (status bar / URL bar) to match a
  // forced theme too. The two <meta name="theme-color"> tags are picked by the
  // browser based on the OS scheme, not our override, so when a theme is
  // forced we point whichever tag the browser would otherwise honor at the
  // forced color. This only touches the in-memory DOM, so a fresh page load
  // always starts from the authored values again.
  function paintMeta(){
    var v = stored();
    if(!v) return; // 'system' — leave both tags exactly as authored
    var light = document.querySelector('meta[name="theme-color"][media*="light"]');
    var dark = document.querySelector('meta[name="theme-color"][media*="dark"]');
    if(!light || !dark) return;
    if(v === 'dark') light.setAttribute('content', dark.getAttribute('content'));
    else dark.setAttribute('content', light.getAttribute('content'));
  }

  function apply(){
    var v = stored();
    if(v) document.documentElement.setAttribute('data-theme', v);
    else document.documentElement.removeAttribute('data-theme');
  }

  window.RafiqTheme = {
    get: function(){ return stored() || 'system'; },
    set: function(v){
      try{
        if(v === 'system') localStorage.removeItem(KEY);
        else localStorage.setItem(KEY, v);
      }catch(_){}
      apply();
      paintMeta();
    }
  };

  // Set the CSS-driving attribute immediately — this script loads before the
  // <meta name="theme-color"> tags in every page, so paintMeta can't find them
  // yet at this point; it runs once they exist instead, which is a few
  // milliseconds later and never visible as a flash the way the page
  // background would be.
  apply();
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', paintMeta);
  } else {
    paintMeta();
  }
})();
