"""Shared SmartWaste visual theme (login + dashboard)."""

MOUNTAIN_SVG = """
<svg class="sw-bg-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="gsky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#b8d9f0"/>
      <stop offset="55%" stop-color="#c8e6f8"/>
      <stop offset="100%" stop-color="#dceefb"/>
    </linearGradient>
  </defs>
  <rect width="1440" height="900" fill="url(#gsky)"/>
  <circle cx="720" cy="115" r="105" fill="white" opacity="0.25"/>
  <circle cx="720" cy="115" r="75" fill="white" opacity="0.92"/>
  <ellipse cx="250" cy="165" rx="130" ry="46" fill="white" opacity="0.78"/>
  <ellipse cx="150" cy="158" rx="88" ry="34" fill="white" opacity="0.72"/>
  <ellipse cx="1140" cy="148" rx="140" ry="52" fill="white" opacity="0.78"/>
  <polygon points="0,520 180,310 360,440 560,270 760,390 980,255 1180,365 1440,280 1440,900 0,900" fill="#9ec5dc" opacity="0.45"/>
  <polygon points="0,580 160,390 340,500 580,330 820,470 1060,320 1280,430 1440,360 1440,900 0,900" fill="#6aA8c4" opacity="0.58"/>
  <polygon points="0,650 150,430 370,540 640,360 900,510 1140,370 1360,480 1440,420 1440,900 0,900" fill="#3d87a4" opacity="0.72"/>
  <polygon points="0,720 140,500 320,610 600,420 880,570 1120,430 1340,540 1440,480 1440,900 0,900" fill="#1e6b82" opacity="0.88"/>
  <rect x="0" y="800" width="1440" height="100" fill="#0d3d4f"/>
  <polygon points="-10,900 50,680 110,900" fill="#071f28"/>
  <polygon points="1170,900 1240,700 1310,900" fill="#071f28"/>
  <polygon points="1360,900 1420,690 1480,900" fill="#071f28"/>
</svg>
"""


def shared_css(dashboard: bool = False) -> str:
    # Same sky gradient on login and dashboard so both pages feel connected
    overlay = (
        "background:linear-gradient(180deg,#B8D9F0 0%,#D4E8F5 12%,#EBF4FA 35%,#F4F9FC 60%,#F8FAFB 100%);"
    )
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Space+Grotesk:wght@500;700;900&display=swap');
*{{box-sizing:border-box;font-family:'Nunito',sans-serif;}}
h1,h2,h3,h4{{font-family:'Space Grotesk',sans-serif;}}
#MainMenu,footer,header{{visibility:hidden;}}
.block-container{{padding-top:1rem!important;max-width:100%!important;}}
.sw-bg-wrap{{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;overflow:hidden;}}
.sw-bg-svg{{width:100%;height:100%;}}
.sw-bg-overlay{{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;{overlay}}}
[data-testid="stSidebar"]{{
  background:rgba(255,255,255,.92)!important;
  backdrop-filter:blur(18px);
  border-right:1px solid rgba(74,144,196,.2);
}}
[data-testid="stSidebar"] *{{color:#1a2a3a!important;}}
[data-testid="stSidebar"] div[data-testid="stButton"]>button[kind="secondary"]{{
  background:transparent!important;color:#4a6a85!important;
}}
[data-testid="stSidebar"] div[data-testid="stButton"]>button[kind="primary"]{{
  background:linear-gradient(90deg,#4A90C4,#7EB8E8)!important;color:#fff!important;
}}
[data-testid="collapsedControl"]{{display:none!important;}}
.section-card{{
  background:rgba(255,255,255,.92);
  border:1px solid rgba(74,144,196,.18);
  backdrop-filter:blur(10px);
  border-radius:16px;
  padding:22px;
  box-shadow:0 2px 12px rgba(0,0,0,.06);
}}
.section-title{{font-size:1rem;font-weight:800;color:#1a2a3a;margin:0 0 14px;}}
.stat-card{{
  background:rgba(255,255,255,.92);
  border:1px solid rgba(74,144,196,.18);
  border-radius:16px;
  padding:18px 20px;
  box-shadow:0 2px 12px rgba(0,0,0,.06);
}}
.stat-card .slabel{{font-size:.75rem;color:#4a6a85;text-transform:uppercase;letter-spacing:.05em;}}
.stat-card .svalue{{font-size:1.75rem;font-weight:900;color:#1a2a3a;font-family:'Space Grotesk',sans-serif;}}
.stat-card .sdelta{{font-size:.78rem;color:#28A745;font-weight:600;}}
.stat-card .sdelta.red{{color:#DC3545;}}
.badge{{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.72rem;font-weight:700;}}
.badge-green{{background:rgba(74,222,128,.15);color:#4ade80;}}
.badge-red{{background:rgba(239,68,68,.15);color:#f87171;}}
.sw-table{{width:100%;border-collapse:collapse;font-size:.82rem;}}
.sw-table th{{color:#4a6a85;font-size:.72rem;text-transform:uppercase;padding:8px 12px;border-bottom:1px solid rgba(74,144,196,.15);}}
.sw-table td{{padding:10px 12px;color:#1a2a3a;border-bottom:1px solid rgba(74,144,196,.1);}}
.det-result-box{{
  background:#E8F5E9;
  border:1px solid rgba(40,167,69,.25);
  border-radius:12px;
  padding:16px;
  margin-top:12px;
}}
.login-hero{{text-align:center;padding:28px 16px 8px;color:#0d3d4f;}}
.login-hero h1{{margin:0;font-size:2.1rem;font-weight:900;letter-spacing:.02em;}}
.login-hero p{{margin:8px auto 0;font-size:.95rem;color:#4a6a85;font-weight:500;max-width:520px;line-height:1.5;}}
.login-card{{
  max-width:460px;margin:0 auto 40px;
  background:rgba(255,255,255,.42);
  backdrop-filter:blur(24px);
  border:1px solid rgba(255,255,255,.65);
  border-radius:24px;
  padding:36px 40px 32px;
  box-shadow:0 24px 60px rgba(13,61,79,.22);
}}
.login-card h2{{text-align:center;color:#0d3d4f;font-size:1.6rem;margin:0 0 24px;}}
div[data-testid="stButton"]>button[kind="primary"]{{
  background:linear-gradient(135deg,#2a8aa8,#1e6b82,#0d3d4f)!important;
  color:#fff!important;
  border:none!important;
  font-weight:800!important;
  border-radius:12px!important;
}}
</style>
<div class="sw-bg-wrap">{MOUNTAIN_SVG}</div>
<div class="sw-bg-overlay"></div>
"""
