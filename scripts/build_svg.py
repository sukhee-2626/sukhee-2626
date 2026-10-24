#!/usr/bin/env python3
"""Generates real (vector, SMIL) animated SVGs for the README. No dependencies: python3 scripts/build_svg.py"""
import math, random, os
from xml.sax.saxutils import escape as esc

random.seed(7)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
os.makedirs(os.path.join(OUT, "heads"), exist_ok=True)
A, B = "#00c9a7", "#7c3aed"
SANS = "Inter,'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"
MONO = "'Fira Code',ui-monospace,SFMono-Regular,Consolas,Menlo,monospace"

def w(path, s):
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f: f.write(s)

def lerp_hex(t):
    a = (124, 58, 237); b = (0, 201, 167)
    c = [round(a[i] + (b[i] - a[i]) * t) for i in range(3)]
    return "#%02x%02x%02x" % tuple(c)

# ---------------------------------------------------------------- HERO
def hero():
    W, H = 900, 440
    CX, CY, R = 655, 215, 196
    N, F, DUR = 210, 40, 24
    TILT = 0.35
    pts = []
    for i in range(N):
        y = 1 - 2 * (i + .5) / N; r = math.sqrt(1 - y * y); t = i * 2.399963
        pts.append((math.cos(t) * r, y, math.sin(t) * r))
    def proj(p, f):
        ay = 2 * math.pi * f / F
        cs, sn, cX, sX = math.cos(ay), math.sin(ay), math.cos(TILT), math.sin(TILT)
        x = p[0] * cs - p[2] * sn; z = p[0] * sn + p[2] * cs
        y = p[1] * cX - z * sX; z = p[1] * sX + z * cX
        s = 1 / (1.9 - z * .6)
        return CX + x * R * s * 1.6, CY + y * R * s * 1.6, z, s
    frames = [[proj(p, f) for p in pts] for f in range(F + 1)]
    # fixed neighbour pairs (3D distance) -> lines that rotate with the sphere
    pairs = []
    for i in range(N):
        d = sorted(((sum((pts[i][k] - pts[j][k]) ** 2 for k in range(3)), j) for j in range(N) if j != i))
        for dist, j in d[:3]:
            if i < j or (j, i) not in pairs: pairs.append((min(i, j), max(i, j)))
    pairs = sorted(set(pairs))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sukhee Sakthivel G M animated portfolio">']
    o.append(f'''<defs>
<linearGradient id="ng" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="{A}"/><stop offset=".5" stop-color="{B}"/><stop offset="1" stop-color="{A}"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<radialGradient id="gl"><stop offset="0" stop-color="{A}" stop-opacity=".22"/><stop offset=".45" stop-color="{B}" stop-opacity=".12"/><stop offset="1" stop-color="{B}" stop-opacity="0"/></radialGradient>
<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
<clipPath id="box"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="22" fill="#070b14"/>
<g clip-path="url(#box)">''')
    # glow that wanders (like the mouse glow)
    o.append('<circle r="230" fill="url(#gl)"><animateMotion dur="16s" repeatCount="indefinite" path="M260,200 C420,60 760,360 600,260 S180,330 260,200"/></circle>')
    # dust
    for _ in range(50):
        x = random.uniform(0, W); r = random.uniform(.6, 1.5); dur = random.uniform(40, 80)
        o.append(f'<circle cx="{x:.0f}" cy="{H+10}" r="{r:.1f}" fill="#b4c8ff" fill-opacity=".35"><animateTransform attributeName="transform" type="translate" from="0 0" to="0 -{H+30}" dur="{dur:.0f}s" begin="-{random.uniform(0,dur):.0f}s" repeatCount="indefinite"/></circle>')
    # lines
    for i, j in pairs:
        d = ";".join(f"M{frames[f][i][0]:.0f},{frames[f][i][1]:.0f}L{frames[f][j][0]:.0f},{frames[f][j][1]:.0f}" for f in range(F + 1))
        op = ";".join(f"{max(0, min(1, ((frames[f][i][2] + frames[f][j][2]) / 2 + .3) / 1.0)) * .42:.2f}" for f in range(F + 1))
        o.append(f'<path d="{d.split(";")[0]}" stroke="{A}" stroke-width=".7" fill="none"><animate attributeName="d" values="{d}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="{op}" dur="{DUR}s" repeatCount="indefinite"/></path>')
    # points
    for i in range(N):
        fr = [frames[f][i] for f in range(F + 1)]
        cx = ";".join(f"{q[0]:.1f}" for q in fr); cy = ";".join(f"{q[1]:.1f}" for q in fr)
        rr = ";".join(f"{(1.1 + q[2] * .8) * q[3] * 2.1:.2f}" for q in fr)
        fl = ";".join(lerp_hex(max(0, min(1, (q[2] + 1) / 2))) for q in fr)
        fo = ";".join(f"{max(.12, min(1, (q[2] + 1.2) / 2.4)):.2f}" for q in fr)
        o.append(f'<circle cx="{fr[0][0]:.1f}" cy="{fr[0][1]:.1f}" r="1.5" fill="{A}"><animate attributeName="cx" values="{cx}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="cy" values="{cy}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="r" values="{rr}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="fill" values="{fl}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="fill-opacity" values="{fo}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    # name (glow copy + gradient text, gentle float)
    o.append('<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="6s" repeatCount="indefinite"/>')
    for fill, extra in (("#00c9a7", ' filter="url(#blur)" opacity=".35"'), ("url(#ng)", "")):
        o.append(f'<g{extra}><text x="38" y="150" font-family="{SANS}" font-size="74" font-weight="800" fill="{fill}">Sukhee</text><text x="38" y="230" font-family="{SANS}" font-size="74" font-weight="800" fill="{fill}">Sakthivel G M</text></g>')
    o.append('</g>')
    # typing
    L = ["Orchestration Engineer @ Plot XYz.Ai", "Building AI-Powered Products", "Data Analyst Intern @ Oasis Infobyte",
         "Campus Ambassador, E-Cell IIT Bombay", "Media & Creative Head, GDG on Campus", "Generative AI · Cloud · Cybersecurity"]
    cw, X0, TY = 13.2, 40, 282
    TT, HOLD, TD, GAP = .07, 1.3, .035, .3
    spans = [len(s) * TT + HOLD + len(s) * TD + GAP for s in L]; T = sum(spans); off = 0
    for idx, s in enumerate(L):
        n = len(s); times = [(0.0, 0)]; t = off
        if off > 0: times = [(0.0, 0)]
        steps = []
        for k in range(1, n + 1): steps.append((off + k * TT, k))
        tdel = off + n * TT + HOLD
        for k in range(n - 1, -1, -1): steps.append((tdel + (n - k) * TD, k))
        times += steps
        kt = ";".join(f"{min(tt / T, .9999):.5f}" for tt, _ in times)
        wv = ";".join(f"{k * cw:.1f}" for _, k in times)
        cv = ";".join(f"{X0 + k * cw:.1f}" if (k > 0 or i == 0) else "-50" for i, (_, k) in enumerate(times))
        cv = ";".join(f"{X0 + k * cw:.1f}" if tt > 0 else "-50" for tt, k in times)
        # cursor hidden outside own window
        cvv = [];
        for tt, k in times:
            cvv.append(f"{X0 + k * cw:.1f}")
        cvv[0] = "-50"
        o.append(f'<clipPath id="c{idx}"><rect x="{X0}" y="{TY-24}" width="0" height="34"><animate attributeName="width" calcMode="discrete" values="{wv}" keyTimes="{kt}" dur="{T:.2f}s" repeatCount="indefinite"/></rect></clipPath>')
        o.append(f'<text x="{X0}" y="{TY}" font-family="{MONO}" font-size="22" font-weight="600" fill="{A}" textLength="{n*cw:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{idx})" xml:space="preserve">{esc(s)}</text>')
        o.append(f'<rect y="{TY-20}" width="10" height="26" fill="{A}" x="-50"><animate attributeName="x" calcMode="discrete" values="{";".join(cvv)}" keyTimes="{kt}" dur="{T:.2f}s" repeatCount="indefinite"/><animate attributeName="opacity" calcMode="discrete" values="1;0" keyTimes="0;.5" dur="1s" repeatCount="indefinite"/></rect>')
        off += spans[idx]
    o.append(f'<text x="40" y="326" font-family="{SANS}" font-size="16" font-weight="700" fill="#8a97b0">Orchestration Engineer @ Plot XYz.Ai |</text><text x="40" y="350" font-family="{SANS}" font-size="16" font-weight="700" fill="#8a97b0">Building AI-Powered Products</text>')
    # pill buttons
    x = 40
    for label in ("GitHub", "LinkedIn", "Kaggle", "sukheesakthivel07@gmail.com"):
        pw = len(label) * 8.2 + 40
        o.append(f'<g><rect x="{x}" y="378" width="{pw:.0f}" height="38" rx="19" fill="#0e1526" stroke="#ffffff22"/><text x="{x+pw/2:.0f}" y="402" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="#e6edf7">{esc(label)}</text></g>')
        x += pw + 12
    o.append('</g></svg>')
    w("hero.svg", "\n".join(o))

# ---------------------------------------------------------------- HEADINGS
def head(name, text):
    W = 760
    w(f"heads/{name}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 64" width="{W}" height="64" role="img" aria-label="{esc(text)}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="{A}"/><stop offset=".5" stop-color="{B}"/><stop offset="1" stop-color="{A}"/><animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1 0" dur="5s" repeatCount="indefinite"/></linearGradient></defs>
<text x="2" y="40" font-family="{SANS}" font-size="32" font-weight="800" fill="url(#g)">{esc(text)}</text>
<rect x="2" y="52" width="120" height="3" rx="1.5" fill="url(#g)"><animate attributeName="width" values="40;260;40" dur="4s" repeatCount="indefinite"/></rect>
</svg>''')

# ---------------------------------------------------------------- CARDS
def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n and cur: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    if cur: lines.append(cur)
    return lines

def card_body(x, y, cw, title, desc, tag, num, uid, delay, minh=0):
    lines = wrap(desc, int((cw - 48) / 8.0)) if desc else []
    h = 22 + 22 + 8 + len(lines) * 21 + (12 + 24 if tag else 0) + 22
    h = max(h, 110, minh)
    g = [f'<g transform="translate({x},{y})">']
    g.append(f'<clipPath id="k{uid}"><rect width="{cw}" height="{h}" rx="18"/></clipPath>')
    g.append(f'<rect width="{cw}" height="{h}" rx="18" fill="#0e1526" stroke="#ffffff1a"/>')
    g.append(f'<g clip-path="url(#k{uid})"><circle r="130" fill="url(#hl)"><animate attributeName="cx" values="-40;{cw+40};-40" dur="9s" begin="{delay}s" repeatCount="indefinite"/><animate attributeName="cy" values="{h*.2:.0f};{h*.85:.0f};{h*.2:.0f}" dur="9s" begin="{delay}s" repeatCount="indefinite"/></circle></g>')
    g.append(f'<rect width="{cw}" height="{h}" rx="18" fill="none" stroke="url(#bd)" stroke-opacity=".55"><animate attributeName="stroke-opacity" values=".15;.7;.15" dur="6s" begin="{delay}s" repeatCount="indefinite"/></rect>')
    if num: g.append(f'<text x="{cw-16}" y="52" text-anchor="end" font-family="{SANS}" font-size="44" font-weight="800" fill="#ffffff" fill-opacity=".06">{num}</text>')
    g.append(f'<text x="22" y="40" font-family="{SANS}" font-size="18" font-weight="700" fill="#e6edf7">{esc(title)}</text>')
    yy = 40 + 8
    for ln in lines:
        yy += 21; g.append(f'<text x="22" y="{yy}" font-family="{SANS}" font-size="14" fill="#8a97b0">{esc(ln)}</text>')
    if tag:
        tw = len(tag) * 6.9 + 24; ty = yy + 14
        g.append(f'<rect x="22" y="{ty}" width="{tw:.0f}" height="24" rx="12" fill="{A}" fill-opacity=".14"/><text x="{22+tw/2:.0f}" y="{ty+16}" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="{A}">{esc(tag)}</text>')
    g.append('</g>')
    return "\n".join(g), h

DEFS = f'''<defs><radialGradient id="hl"><stop offset="0" stop-color="{A}" stop-opacity=".20"/><stop offset="1" stop-color="{A}" stop-opacity="0"/></radialGradient>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{A}"/><stop offset="1" stop-color="{B}"/></linearGradient></defs>'''

def single_card(name, title, desc, tag, num=None, delay=0):
    cw = 430
    body, h = card_body(1, 1, cw, title, desc, tag, num, name, delay)
    w(f"cards/{name}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw+2} {h+2}" width="{cw+2}" height="{h+2}" role="img" aria-label="{esc(title)}">{DEFS}{body}</svg>')

def grid(name, items, cols=2):
    cw, gap = 430, 20
    parts2, rowy, i = [], 0, 0
    while i < len(items):
        idxs = list(range(i, min(i + cols, len(items))))
        rh = max(card_body(0, 0, cw, *items[k][:2], items[k][2], None, f"x{k}", 0)[1] for k in idxs)
        for c, k in enumerate(idxs):
            t, d, tg = items[k]
            body, _ = card_body(1 + c * (cw + gap), rowy + 1, cw, t, d, tg, None, f"{name}{k}", k * .7, rh)
            parts2.append(body)
        rowy += rh + gap; i += cols
    Wd = 2 + cols * cw + (cols - 1) * gap; Hd = rowy - gap + 2
    w(f"cards/{name}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Hd}" width="{Wd}" height="{Hd}" role="img" aria-label="{name}">{DEFS}{"".join(parts2)}</svg>')

def skills(name, S):
    cw, gap = 280, 20; Wd = 3 * cw + 2 * gap + 2
    parts, rowh, y = [], [], 1
    keys = list(S.items())
    for r in range(0, len(keys), 3):
        row = keys[r:r + 3]; hs = []
        for c, (k, v) in enumerate(row):
            x = 1 + c * (cw + gap); chips = v.split(","); cx, cy, cells = 22, 66, []
            for ci, ch in enumerate(chips):
                pw = len(ch) * 7.4 + 30
                if cx + pw > cw - 16: cx = 22; cy += 46
                cells.append(f'<g transform="translate({cx},{cy})"><g><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="4s" begin="{ci*.2:.1f}s" repeatCount="indefinite"/><rect width="{pw:.0f}" height="34" rx="12" fill="#0e1526" stroke="#ffffff22"/><text x="{pw/2:.0f}" y="22" text-anchor="middle" font-family="{SANS}" font-size="13.5" font-weight="700" fill="#e6edf7">{esc(ch)}</text></g></g>')
                cx += pw + 10
            h = cy + 34 + 22; hs.append(h)
            parts.append((x, y, h, k, "".join(cells), r + c))
        y += max(hs) + gap
    out = []
    for x, y0, h, k, cells, i in parts:
        rowmax = max(p[2] for p in parts if p[1] == y0)
        out.append(f'<g transform="translate({x},{y0})"><rect width="{cw}" height="{rowmax}" rx="18" fill="#0e1526" stroke="#ffffff1a"/><rect width="{cw}" height="{rowmax}" rx="18" fill="none" stroke="url(#bd)" stroke-opacity=".5"><animate attributeName="stroke-opacity" values=".15;.7;.15" dur="6s" begin="{i*.6}s" repeatCount="indefinite"/></rect><text x="22" y="40" font-family="{SANS}" font-size="18" font-weight="700" fill="#e6edf7">{esc(k)}</text>{cells}</g>')
    Hd = y - gap + 2
    w(f"cards/{name}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Hd}" width="{Wd}" height="{Hd}" role="img" aria-label="Technical skills">{DEFS}{"".join(out)}</svg>')


# ---------------------------------------------------------------- FALLING (code / particle rain)
def falling(name="falling", W=900, H=170, cols=46):
    GL = "01{}<>/;=+*#$&"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Falling particles animation">',
         f'<defs><clipPath id="b"><rect width="{W}" height="{H}" rx="22"/></clipPath><linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b14" stop-opacity="0"/><stop offset="1" stop-color="#070b14" stop-opacity=".85"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="22" fill="#070b14"/><g clip-path="url(#b)">']
    for c in range(cols):
        x = 14 + c * (W - 28) / (cols - 1); n = random.randint(5, 9); dur = random.uniform(3.2, 7.5); beg = -random.uniform(0, dur)
        col = A if c % 3 else B
        chars = "".join(f'<text x="0" y="{i*15}" font-family="{MONO}" font-size="13" font-weight="600" fill="{"#ffffff" if i==n-1 else col}" fill-opacity="{(0.12+0.88*i/(n-1)):.2f}" text-anchor="middle">{esc(random.choice(GL))}</text>' for i in range(n))
        o.append(f'<g transform="translate({x:.0f},0)"><g><animateTransform attributeName="transform" type="translate" from="0 -{n*15+10}" to="0 {H+20}" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/>{chars}</g></g>')
    for _ in range(40):  # falling dots
        x = random.uniform(0, W); r = random.uniform(.8, 2.2); dur = random.uniform(2.5, 6); beg = -random.uniform(0, dur)
        o.append(f'<circle cx="{x:.0f}" cy="0" r="{r:.1f}" fill="{random.choice([A,B,"#b4c8ff"])}" fill-opacity=".7"><animateTransform attributeName="transform" type="translate" from="0 -10" to="0 {H+10}" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#fd)"/></g><rect width="{W}" height="{H}" rx="22" fill="none" stroke="#ffffff1a"/></svg>')
    w(f"{name}.svg", "\n".join(o))

# ---------------------------------------------------------------- DATA (same as index.html)
P = [("plot-docs","plot-docs","Local-first AI office suite for Docs, Sheets, Slides, PDF, Markdown and HTML on Windows, macOS and Linux.","Electron · TypeScript"),
("Thinai","Thinai","Privacy-focused Android app running small language models on-device with a local API.","Dart · On-device AI"),
("MediNexus-AI-Updated","MediNexus AI","Healthcare platform: patient records, appointments, consent management, AI insights and patient portals.","React · TypeScript · Supabase · Gemini"),
("carelens-hospital-agent","CareLens","Hospital AI assistant for document extraction, health timelines, search, FAQ retrieval, appointments and audit trails.","React · TypeScript · Azure AI"),
("CodeGuardAI","CodeGuard","Browser-based GitHub security scanner with vulnerability analysis, security scoring, auto-fixes and Markdown reports.","React · GitHub REST API"),
("CAMPUS-NAV","Campus Navigator","Interactive college map and field-survey app with GPS detection, searchable destinations and saved pins.","React · Express · MySQL/TiDB"),
("SSOFFICE","SSOFFICE","Full-stack office suite: docs, sheets, slides, forms, mail, calendar, drive, tasks, automation and AI.","React · TypeScript · Supabase"),
("VastuAi","VastuAI","Floor-plan analyzer combining Gemini Vision with a custom rule engine, scoring and improvement tips.","React · Flask · Gemini Vision"),
("Place1-Ai","Place1-Ai","AI career copilot with polished frontend, backend API, authentication and database integration.","Next.js · Tailwind · Supabase"),
("prd-craftsman-10","PRD Craftsman","AI product-requirements prompt generator with structured templates.","TypeScript · Generative AI")]
H_ = [("Featastiv AI","3rd Prize, Ideathon ThinkTank 2026. AI healthcare scheduling and live queue management.","https://lnkd.in/g5aypTxY"),
("MediChain Spark","GDG TechSprint Hackathon 2025. Blockchain medical records with immutable transparency.","https://lnkd.in/gvartgug"),
("Certificate Portal","Official GDG TechSprint portal with Credential ID and QR verification, instant PDFs.","https://lnkd.in/gqbSV8Ay"),
("AI PRD Generator","Turns raw ideas into structured 11-section PRDs in seconds. Built with Lovable.","https://lnkd.in/gT4379-b")]
EXP = [("Orchestration Engineer","Plot XYz.Ai. Building AI-powered products.","Current"),
("Data Analyst Intern","Oasis Infobyte · Virtual. Data-focused internship with exposure to IT infrastructure and support services.","Aug 2026 – Present"),
("Campus Ambassador, E-Cell","IIT Bombay. Supported campus outreach and entrepreneurship initiatives.","Jun 2026 – Present"),
("Media & Creative Team Head","GDG on Campus. Led media and creative activities, event promotion and technical community engagement.","Jun 2025 – Present"),
("Language Intern","GLA University, Mathura. Completed an on-site language internship.","Jun 2026"),
("Desktop Support Technician","Smart Stream Technologies · Part-time. Technical support with exposure to desktop support and data engineering.","Apr – May 2026")]
EDU = [("B.Sc. Computer Science","Sri Krishna Arts and Science College (SKASC). 1st year, pursuing.","2025 – 2028"),
("12th · Commerce + Computer Science","Higher secondary education.","71.6%"),("10th","Secondary education.","62%")]
S = {"Programming":"Python,C++,JavaScript,TypeScript,DSA","AI & Data":"Generative AI,Prompt Engineering,Google Gemini,Azure AI,Data Engineering","Web":"React,Vite,Tailwind CSS,WordPress,Docker","Cloud":"Google Cloud,Supabase,PostgreSQL,MySQL/TiDB,REST APIs","Security":"Cybersecurity,Cisco Networking,Technical Support","Tools":"GitHub,VS Code,Google Workspace,Canva"}
CERT = [("Anthropic","AI Fluency Framework & Foundations","Jun 2026"),
("Google","Gen AI Apps with Gemini & Streamlit · Google Cloud Network, Data & Compute · Vertex AI Prompt Design · Generative AI · Speech & Language APIs","Oct 2025"),
("GDG","SKASC Tech Sprint","Jan 2026"),("Great Learning","WordPress with Docker",""),
("Cisco","Introduction to Cybersecurity","Oct 2024"),("HackerRank","Python (Basic)","Oct 2024")]

if __name__ == "__main__":
    hero(); falling()
    for n, t in (("projects","Top 10 Projects"),("hackathons","Hackathons & Achievements"),("experience","Experience"),("education","Education"),("skills","Technical Skills"),("certs","Certifications"),("calendar","Isometric Commit Calendar"),("skyline","GitHub Skyline 3D"),("activity","Recent Activity Charts"),("facts","Mildly Interesting Facts"),("contributors","Repository Contributors")):
        head(n, t)
    for i, p in enumerate(P): single_card(f"p{i+1:02d}", p[1], p[2], p[3], f"{i+1:02d}", i * .5)
    for i, h in enumerate(H_): single_card(f"h{i+1}", h[0], h[1], "View →", None, i * .5)
    grid("experience", EXP); grid("education", EDU); grid("certs", CERT); skills("skills", S)
    print("built")
