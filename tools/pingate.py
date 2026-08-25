import hashlib, re, sys
PIN_HASH = hashlib.sha256("2888".encode()).hexdigest()
html = open("/tmp/source.html", encoding="utf-8").read()
# Cheap lock: cap the blurred area to one viewport (desktop) and skip the filter entirely on mobile.
# Blurring a full 8000px+ document froze the renderer on test, so this is deliberate.
STYLE = ('<style id="pin-gate-style">'
 'body.pin-locked{overflow:hidden;height:100vh}'
 'body.pin-locked .wrap{max-height:100vh;overflow:hidden;filter:blur(14px);pointer-events:none;user-select:none}'
 '@media(max-width:720px){body.pin-locked .wrap{filter:none;opacity:.10}}'
 '.pin-overlay{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:radial-gradient(800px 500px at 50% 30%,rgba(124,58,237,.10),transparent 60%),rgba(247,246,243,.96);font-family:-apple-system,BlinkMacSystemFont,Inter,sans-serif;padding:16px;padding-bottom:calc(16px + env(safe-area-inset-bottom,0px))}'
 '.pin-box{background:#fff;border:1px solid #e7e5e0;border-radius:18px;padding:32px 26px;box-shadow:0 24px 60px -12px rgba(10,10,10,.18);text-align:center;width:min(360px,calc(100vw - 32px))}'
 '.pin-box .pin-icon{width:56px;height:56px;margin:0 auto 14px;border-radius:14px;background:linear-gradient(135deg,#4f46e5,#7c3aed);display:flex;align-items:center;justify-content:center;color:#fff}'
 '.pin-box h2{font-family:"Iowan Old Style",Baskerville,serif;margin:0 0 6px;font-size:22px;color:#0a0a0a}'
 '.pin-box p{margin:0 0 18px;color:#737373;font-size:13.5px}'
 '.pin-input{width:100%;padding:14px 16px;font-size:22px;font-family:ui-monospace,Menlo,monospace;text-align:center;letter-spacing:.4em;border:1px solid #d4d4d4;border-radius:10px;background:#fafaf7;outline:none}'
 '.pin-input:focus{border-color:#4f46e5;box-shadow:0 0 0 3px rgba(79,70,229,.12)}'
 '.pin-input.error{border-color:#be123c;animation:shake .35s}'
 '@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}'
 '.pin-btn{margin-top:12px;width:100%;padding:14px;min-height:48px;background:#0a0a0a;color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer}'
 '.pin-btn:hover{background:#262626}'
 '.pin-hint{margin-top:14px;font-size:11.5px;color:#a3a3a3}'
 '</style>')
OVERLAY = ('<div class="pin-overlay" id="pinOverlay"><div class="pin-box">'
 '<div class="pin-icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
 '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>'
 '<h2>Finanční briefing</h2><p>Zadej PIN pro zobrazení</p>'
 '<input id="pinInput" class="pin-input" type="password" inputmode="numeric" pattern="[0-9]*" maxlength="6" autofocus/>'
 '<button class="pin-btn" id="pinSubmit">Odemknout</button>'
 '<p class="pin-hint">Privátní obsah — Martin · Trading 212</p></div></div>')
SCRIPT = ('<script id="pin-gate-script">(function(){var PIN_HASH="' + PIN_HASH + '";var KEY="briefingUnlockedV1";'
 'var b=document.body,o=document.getElementById("pinOverlay"),i=document.getElementById("pinInput"),btn=document.getElementById("pinSubmit");'
 'async function s(s){var u=new TextEncoder().encode(s),h=await crypto.subtle.digest("SHA-256",u);'
 'return Array.from(new Uint8Array(h)).map(function(x){return x.toString(16).padStart(2,"0")}).join("")}'
 'function u(){o.style.display="none";b.classList.remove("pin-locked");try{localStorage.setItem(KEY,"1")}catch(e){}}'
 'async function t(){var v=i.value.trim();if(!v)return;var h=await s(v);if(h===PIN_HASH){u()}'
 'else{i.classList.add("error");setTimeout(function(){i.classList.remove("error");i.value="";i.focus()},400)}}'
 'b.classList.add("pin-locked");try{if(localStorage.getItem(KEY)==="1"){u();return}}catch(e){}'
 'btn.addEventListener("click",t);i.addEventListener("keypress",function(e){if(e.key==="Enter")t()})})()</' + 'script>')
html = html.replace("</head>", STYLE + "\n</head>", 1)
html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + OVERLAY, html, count=1)
html = html.replace("</body>", SCRIPT + "\n</body>", 1)
open("/tmp/repo-work/index.html","w",encoding="utf-8").write(html)
print("PIN gate OK | capped blur:", "max-height:100vh;overflow:hidden;filter:blur(14px)" in html,
      "| mobile no-filter:", "filter:none;opacity:.10" in html,
      "| pm-link fix:", "min-height:40px;padding:0 2px" in html)
