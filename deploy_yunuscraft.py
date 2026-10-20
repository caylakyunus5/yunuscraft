#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YunusCraft Suite — 14 Uygulama İndirme, Türkçe Yerelleştirme ve Surge Yayınlayıcı
"""

import os
import sys
import json
import time
import shutil
import urllib.request
import zipfile
import subprocess

APPS = [
    {
        "repo": "photocraft",
        "domain": "yunusfoto.surge.sh",
        "name": "YunusFoto",
        "title": "YunusFoto — Profesyonel Görsel Düzenleyici",
        "desc": "Katmanlar, maskeler, fırçalar ve gerçek PSD dosya desteği sunan Photoshop alternatifi.",
        "icon": "🖼️",
        "color": "#38bdf8",
        "pref_key": "photocraft.preferences",
    },
    {
        "repo": "lightcraft",
        "domain": "yunusisik.surge.sh",
        "name": "YunusIşık",
        "title": "YunusIşık — RAW ve Fotoğraf Geliştirme",
        "desc": "Tahribatsız RAW geliştirme, renk profilleri ve fotoğraf kütüphanesi yöneticisi.",
        "icon": "💡",
        "color": "#fbbf24",
        "pref_key": "lightcraft.preferences",
    },
    {
        "repo": "vectorcraft",
        "domain": "yunusvektor.surge.sh",
        "name": "YunusVektör",
        "title": "YunusVektör — Vektörel Çizim ve İllüstrasyon",
        "desc": "Bézier eğrileri, SVG düzenleme ve tipografi sunan Illustrator alternatifi.",
        "icon": "✒️",
        "color": "#f97316",
        "pref_key": "vectorcraft.preferences",
    },
    {
        "repo": "filmcraft",
        "domain": "yunusvideo.surge.sh",
        "name": "YunusVideo",
        "title": "YunusVideo — Video Kurgu ve Montaj",
        "desc": "Çok kanallı zaman çizelgesi, kırpma, geçişler ve ses miksajı sunan video kurgu stüdyosu.",
        "icon": "🎬",
        "color": "#a855f7",
        "pref_key": "filmcraft.preferences",
    },
    {
        "repo": "pdfcraft",
        "domain": "yunuspdf.surge.sh",
        "name": "YunusPDF",
        "title": "YunusPDF — Belge ve PDF Düzenleyici",
        "desc": "PDF sayfalarını birleştirme, bölme, metin ekleme, form doldurma ve imzalama.",
        "icon": "📄",
        "color": "#ef4444",
        "pref_key": "pdfcraft.preferences",
    },
    {
        "repo": "effectcraft",
        "domain": "yunusefekt.surge.sh",
        "name": "YunusEfekt",
        "title": "YunusEfekt — Görsel Efekt ve Kompozisyon",
        "desc": "Düğüm tabanlı görsel efektler, parçacık sistemleri ve hareketli grafik stüdyosu.",
        "icon": "✨",
        "color": "#ec4899",
        "pref_key": "effectcraft.preferences",
    },
    {
        "repo": "designcraft",
        "domain": "yunustasarim.surge.sh",
        "name": "YunusTasarım",
        "title": "YunusTasarım — Sayfa ve Mizanpaj Tasarımı",
        "desc": "Dergi, broşür, kitap ve e-yayın için çok sayfalı masaüstü yayıncılık stüdyosu.",
        "icon": "📐",
        "color": "#14b8a6",
        "pref_key": "designcraft.preferences",
    },
    {
        "repo": "gridcraft",
        "domain": "yunustablo.surge.sh",
        "name": "YunusTablo",
        "title": "YunusTablo — Tablo ve Hesap Çizelgesi",
        "desc": "Grafikler, formüller, pivot tablolar ve veri analizi sunan elektronik tablo aracı.",
        "icon": "📊",
        "color": "#22c55e",
        "pref_key": "gridcraft.preferences",
    },
    {
        "repo": "wordcraft",
        "domain": "yunusdokuman.surge.sh",
        "name": "YunusDoküman",
        "title": "YunusDoküman — Kelime İşlemci ve Doküman",
        "desc": "Gelişmiş biçimlendirme, stiller ve dışa aktarma yeteneklerine sahip kelime işlemci.",
        "icon": "📝",
        "color": "#3b82f6",
        "pref_key": "wordcraft.preferences",
    },
    {
        "repo": "deckcraft",
        "domain": "yunussunum.surge.sh",
        "name": "YunusSunum",
        "title": "YunusSunum — Etkileşimli Sunum Hazırlama",
        "desc": "Slayt tasarımı, animasyonlar, geçişler ve tam ekran sunum modu.",
        "icon": "📽️",
        "color": "#eab308",
        "pref_key": "deckcraft.preferences",
    },
    {
        "repo": "cadcraft",
        "domain": "yunuscad.surge.sh",
        "name": "YunusCAD",
        "title": "YunusCAD — 2D/3D Teknik Çizim ve Tasarım",
        "desc": "Mühendislik ve mimari çizimler için hassas parametrik CAD modelleme aracı.",
        "icon": "⚙️",
        "color": "#06b6d4",
        "pref_key": "cadcraft.preferences",
    },
    {
        "repo": "soundcraft",
        "domain": "yunusses.surge.sh",
        "name": "YunusSes",
        "title": "YunusSes — Çok Kanallı Ses Düzenleyici",
        "desc": "Ses dalga formu düzenleme, efektler, gürültü temizleme ve miksaj stüdyosu.",
        "icon": "🎙️",
        "color": "#f43f5e",
        "pref_key": "soundcraft.preferences",
    },
    {
        "repo": "craft-launcher",
        "domain": "yunuscraft-baslatici.surge.sh",
        "name": "YunusCraft Başlatıcı",
        "title": "YunusCraft Başlatıcı — WebAssembly Canvas Hub",
        "desc": "Tüm YunusCraft araçlarını tek ekranda toplayan yerel Canvas başlatıcı.",
        "icon": "🚀",
        "color": "#ffd479",
        "pref_key": "artcraft_launcher.preferences",
    },
]

WORK_DIR = "/home/user/yunuscraft_build"
os.makedirs(WORK_DIR, exist_ok=True)

# Hızlı geçiş menüsü HTML kodu (tüm uygulamaların altına eklenecek)
def build_floating_menu(current_domain):
    items_html = ""
    for app in APPS:
        is_cur = (app["domain"] == current_domain)
        active_cls = "font-weight:700;background:rgba(255,212,121,0.15);color:#ffd479;" if is_cur else "color:#e4e4e7;"
        items_html += f"""
        <a href="https://{app['domain']}" target="_blank" style="display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:8px;text-decoration:none;{active_cls}font-size:13px;transition:background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='{'rgba(255,212,121,0.15)' if is_cur else 'transparent'}'">
          <span style="font-size:16px;">{app['icon']}</span>
          <div style="flex:1;overflow:hidden;">
            <div style="font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{app['name']}</div>
            <div style="font-size:11px;color:#a1a1aa;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{app['desc']}</div>
          </div>
        </a>"""

    menu_code = f"""
<!-- 🎨 YunusCraft Suite Hızlı Geçiş Menüsü -->
<div id="yunuscraft-hub-root" style="position:fixed;bottom:16px;right:16px;z-index:999999;font-family:system-ui,-apple-system,sans-serif;">
  <button id="yunuscraft-hub-btn" style="display:flex;align-items:center;gap:8px;background:#18181b;color:#ffd479;border:1px solid #3f3f46;border-radius:30px;padding:8px 14px;box-shadow:0 8px 24px rgba(0,0,0,0.5);cursor:pointer;font-size:13px;font-weight:700;transition:transform 0.15s,background 0.15s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" onclick="var p=document.getElementById('yunuscraft-hub-panel');p.style.display=(p.style.display==='none'?'flex':'none');">
    <span>🎨</span>
    <span>YunusCraft Stüdyo</span>
    <span style="font-size:10px;opacity:0.7;">▲</span>
  </button>
  <div id="yunuscraft-hub-panel" style="display:none;position:absolute;bottom:46px;right:0;width:320px;max-height:480px;background:#18181b;border:1px solid #3f3f46;border-radius:16px;box-shadow:0 16px 36px rgba(0,0,0,0.6);flex-direction:column;overflow:hidden;">
    <div style="padding:12px 16px;background:#27272a;border-bottom:1px solid #3f3f46;display:flex;align-items:center;justify-content:space-between;">
      <div style="font-weight:700;font-size:14px;color:#fff;">YunusCraft Stüdyosu</div>
      <a href="https://yunuscraft.surge.sh" style="color:#ffd479;font-size:11px;text-decoration:none;font-weight:600;">Ana Portal ↗</a>
    </div>
    <div style="overflow-y:auto;padding:8px;display:flex;flex-direction:column;gap:2px;">
      {items_html}
    </div>
  </div>
</div>
<script>
  // Otomatik Türkçe Dil Zorlama
  (function() {{
    const prefs = ['photocraft', 'lightcraft', 'vectorcraft', 'filmcraft', 'pdfcraft', 'effectcraft', 'designcraft', 'gridcraft', 'wordcraft', 'deckcraft', 'cadcraft', 'soundcraft', 'artcraft_launcher', 'craft-launcher'];
    prefs.forEach(function(p) {{
      try {{
        const k = p + '.preferences';
        let o = {{}};
        try {{ o = JSON.parse(localStorage.getItem(k) || '{{}}'); }} catch(e){{}}
        o.interface = o.interface || {{}};
        o.interface.language = 'tr';
        localStorage.setItem(k, JSON.stringify(o));
      }} catch(e){{}}
    }});
    try {{
      localStorage.setItem('interface.language', 'tr');
      localStorage.setItem('language', 'tr');
      localStorage.setItem('locale', 'tr-TR');
    }} catch(e){{}}
    try {{
      Object.defineProperty(navigator, 'language', {{ get: () => 'tr-TR', configurable: true }});
      Object.defineProperty(navigator, 'languages', {{ get: () => ['tr-TR', 'tr', 'en-US'], configurable: true }});
    }} catch(e){{}}
  }})();
</script>
"""
    return menu_code

def download_and_extract(app):
    repo = app["repo"]
    name = app["name"]
    dest_dir = os.path.join(WORK_DIR, repo)
    if os.path.exists(dest_dir):
        print(f"[{name}] Zaten indirilmiş: {dest_dir}")
        return dest_dir

    print(f"[{name}] Son sürüm aranıyor: storytold/{repo}...")
    api_url = f"https://api.github.com/repos/storytold/{repo}/releases/latest"
    req = urllib.request.Request(api_url, headers={"User-Agent": "curl/7.88"})
    with urllib.request.urlopen(req) as resp:
        rel = json.load(resp)

    web_asset = None
    for a in rel.get("assets", []):
        aname = a.get("name", "").lower()
        if "web" in aname and aname.endswith(".zip"):
            web_asset = a
            break

    if not web_asset:
        raise RuntimeError(f"[{name}] Web zip dosyası bulunamadı!")

    zip_url = web_asset["browser_download_url"]
    print(f"[{name}] İndiriliyor: {web_asset['name']} ({web_asset['size']/1024/1024:.1f} MB)...")
    tmp_zip = f"/tmp/{repo}_web.zip"
    urllib.request.urlretrieve(zip_url, tmp_zip)

    print(f"[{name}] Arşiv açılıyor...")
    tmp_ext = f"/tmp/{repo}_extracted"
    shutil.rmtree(tmp_ext, ignore_errors=True)
    with zipfile.ZipFile(tmp_zip) as z:
        z.extractall(tmp_ext)

    # İçteki kök klasörü bul
    contents = os.listdir(tmp_ext)
    src_folder = tmp_ext
    if len(contents) == 1 and os.path.isdir(os.path.join(tmp_ext, contents[0])):
        src_folder = os.path.join(tmp_ext, contents[0])

    shutil.copytree(src_folder, dest_dir)
    print(f"[{name}] Hazırlandı: {dest_dir}")
    os.remove(tmp_zip)
    shutil.rmtree(tmp_ext, ignore_errors=True)
    return dest_dir

def patch_app_html(app, folder):
    idx_path = os.path.join(folder, "index.html")
    if not os.path.exists(idx_path):
        print(f"! index.html bulunamadı: {folder}")
        return

    # Sıkıştırılmış versiyonları kaldır (Surge'un güncel HTML'i vermesi için)
    for gz in ["index.html.gz", "index.html.br"]:
        p = os.path.join(folder, gz)
        if os.path.exists(p):
            os.remove(p)

    with open(idx_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # Başlık ve yükleme metinlerini Türkçeleştir
    import re
    html = re.sub(r"<title>.*?</title>", f"<title>{app['title']}</title>", html, flags=re.I)
    html = re.sub(r"Loading\s+[A-Za-z0-9_-]+(&hellip;|\.\.\.)?", f"{app['name']} Yükleniyor&hellip;", html, flags=re.I)

    # Menü ve Türkçe inject
    menu_code = build_floating_menu(app["domain"])
    if "</body>" in html:
        html = html.replace("</body>", f"{menu_code}\n</body>")
    else:
        html += menu_code

    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(html)

    # _headers kontrolü (WASM MIME type için)
    hdr_path = os.path.join(folder, "_headers")
    if not os.path.exists(hdr_path):
        with open(hdr_path, "w", encoding="utf-8") as f:
            f.write("/*\n  X-Content-Type-Options: nosniff\n\n/*.wasm\n  Content-Type: application/wasm\n  Cache-Control: public, max-age=31536000, immutable\n")

    print(f"[{app['name']}] index.html Türkçeleştirildi ve menü eklendi.")

def deploy_to_surge(folder, domain):
    print(f"🚀 Surge'e yayınlanıyor: {domain}...")
    cmd = ["/home/user/.local/bin/surge", folder, domain]
    env = os.environ.copy()
    env["PATH"] = f"/home/user/.local/bin:{env.get('PATH', '')}"
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120, env=env)
    if res.returncode == 0:
        print(f"✓ Başarılı: https://{domain}")
        return True
    else:
        print(f"✗ Hata ({domain}): {res.stderr or res.stdout}")
        return False

def build_main_portal():
    print("\n🌟 Ana Portal Oluşturuluyor: yunuscraft.surge.sh...")
    portal_dir = os.path.join(WORK_DIR, "main_portal")
    shutil.rmtree(portal_dir, ignore_errors=True)
    os.makedirs(portal_dir, exist_ok=True)

    cards_html = ""
    for app in APPS:
        if app["repo"] == "craft-launcher":
            continue
        cards_html += f"""
      <a href="https://{app['domain']}" target="_blank" class="card">
        <div class="card-icon" style="background:{app['color']}15; border-color:{app['color']}40; color:{app['color']};">
          {app['icon']}
        </div>
        <div class="card-content">
          <div class="card-title">
            <h3>{app['name']}</h3>
            <span class="badge">Aç ↗</span>
          </div>
          <p class="card-desc">{app['desc']}</p>
          <div class="card-meta">
            <span class="status-dot"></span> Canlıda (WASM) · {app['domain']}
          </div>
        </div>
      </a>"""

    portal_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YunusCraft — Profesyonel Açık Kaynak Yaratıcı Stüdyo Paketi</title>
  <meta name="description" content="Photoshop, Illustrator, Lightroom, Premiere, Acrobat vb. profesyonel araçların %100 açık kaynak ve tarayıcıda çalışan Rust/WASM alternatifleri.">
  <style>
    :root {{
      --bg: #09090b;
      --card-bg: #141417;
      --card-hover: #1c1c21;
      --border: #27272a;
      --border-hover: #3f3f46;
      --text: #f4f4f5;
      --text-muted: #a1a1aa;
      --accent: #ffd479;
      --accent-glow: rgba(255, 212, 121, 0.2);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
      padding-bottom: 60px;
    }}
    .header {{
      text-align: center;
      padding: 60px 20px 40px;
      max-width: 900px;
      margin: 0 auto;
    }}
    .badge-hero {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: rgba(255, 212, 121, 0.1);
      border: 1px solid rgba(255, 212, 121, 0.3);
      color: var(--accent);
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      margin-bottom: 20px;
    }}
    h1 {{
      font-size: clamp(32px, 5vw, 54px);
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 16px;
      background: linear-gradient(135deg, #ffffff 40%, #a1a1aa 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: clamp(16px, 2vw, 19px);
      color: var(--text-muted);
      max-width: 680px;
      margin: 0 auto 30px;
    }}
    .stats-bar {{
      display: flex;
      justify-content: center;
      gap: 32px;
      padding-top: 10px;
      border-top: 1px solid var(--border);
    }}
    .stat-item {{ text-align: center; }}
    .stat-val {{ font-size: 20px; font-weight: 700; color: #fff; }}
    .stat-lbl {{ font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }}
    .container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 20px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }}
    .card {{
      display: flex;
      gap: 18px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 22px;
      text-decoration: none;
      color: inherit;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }}
    .card:hover {{
      background: var(--card-hover);
      border-color: var(--border-hover);
      transform: translateY(-2px);
      box-shadow: 0 12px 30px rgba(0,0,0,0.4);
    }}
    .card-icon {{
      width: 52px;
      height: 52px;
      border-radius: 14px;
      border: 1px solid;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      flex-shrink: 0;
    }}
    .card-content {{ flex: 1; min-width: 0; }}
    .card-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }}
    .card-title h3 {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
    }}
    .badge {{
      font-size: 11px;
      font-weight: 600;
      background: rgba(255,255,255,0.08);
      padding: 3px 8px;
      border-radius: 6px;
      color: var(--accent);
    }}
    .card-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 12px;
    }}
    .card-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      color: #71717a;
      font-family: monospace;
    }}
    .status-dot {{
      width: 7px;
      height: 7px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
    }}
    .footer {{
      text-align: center;
      margin-top: 60px;
      color: #71717a;
      font-size: 13px;
      border-top: 1px solid var(--border);
      padding-top: 30px;
    }}
  </style>
</head>
<body>
  <header class="header">
    <div class="badge-hero">⚡ %100 Açık Kaynak · Pure Rust & WebAssembly</div>
    <h1>YunusCraft Yaratıcı Stüdyosu</h1>
    <p class="subtitle">
      Adobe Creative Suite'in tamamen açık kaynak, ücretsiz ve tarayıcınızda çalışan yeni nesil alternatifleri. Kurulum yok, üyelik yok, doğrudan tarayıcınızda çalışır.
    </p>
    <div class="stats-bar">
      <div class="stat-item"><div class="stat-val">13</div><div class="stat-lbl">Uygulama</div></div>
      <div class="stat-item"><div class="stat-val">0 TL</div><div class="stat-lbl">Ücretsiz</div></div>
      <div class="stat-item"><div class="stat-val">WASM</div><div class="stat-lbl">Performans</div></div>
      <div class="stat-item"><div class="stat-val">Türkçe</div><div class="stat-lbl">Yerel Arayüz</div></div>
    </div>
  </header>

  <main class="container">
    <div class="grid">
      {cards_html}
    </div>
  </main>

  <footer class="footer">
    <p>YunusCraft Suite · Taban: Storytold / ArtCraft Açık Kaynak Topluluğu · Apache 2.0 / MIT Lisansı</p>
    <p style="margin-top:6px;">Tüm uygulamalar istemci tarafında (WebAssembly) çalışır, verileriniz sunuculara iletilmez.</p>
  </footer>
</body>
</html>"""

    with open(os.path.join(portal_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(portal_html)

    # surge deploy yunuscraft.surge.sh
    deploy_to_surge(portal_dir, "yunuscraft.surge.sh")

def main():
    print("=" * 60)
    print("  YUNUSCRAFT 14 UYGULAMA DAĞITIM VE YERELLEŞTİRME BAŞLIYOR")
    print("=" * 60)

    for i, app in enumerate(APPS):
        print(f"\n--- [{i+1}/{len(APPS)}] {app['name']} ({app['domain']}) ---")
        try:
            folder = download_and_extract(app)
            patch_app_html(app, folder)
            deploy_to_surge(folder, app["domain"])
            # craft-launcher ise ayrıca yunuscraft-baslatici.surge.sh'ye de yayınla
            if app["repo"] == "craft-launcher":
                deploy_to_surge(folder, "yunuscraft-baslatici.surge.sh")
        except Exception as e:
            print(f"HATA ({app['name']}): {e}")

    # Ana Portal (yunuscraft.surge.sh) oluştur ve yayınla
    build_main_portal()

    print("\n" + "=" * 60)
    print("  TÜM DAĞITIMLAR TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    main()
