# -*- coding: utf-8 -*-
"""Builds the static Shanpar site into the parent folder (v2/).

    python _build/build.py

Content lives in _build/data.py. Every page shares the same header, mega menu
and footer from this file, so edit them here, then rebuild. The output is
plain HTML + css/style.css + js/main.js + js/catalogue.js.
"""
import json, os, re
from html import escape as esc
from urllib.parse import quote

import data as D

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ======================================================================= data
def parse(block, grade):
    rows = []
    for line in block.strip().splitlines():
        name, qual, new = [p.strip() for p in line.split("|")]
        rows.append({"name": name, "qual": qual, "new": new == "new", "grade": grade})
    return rows

def key(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())

products = {}
for row in parse(D.PHARMA, "pharma") + parse(D.ACS, "acs"):
    k = key(row["name"])
    p = products.setdefault(k, {"name": row["name"], "qual": "", "new": False, "grades": []})
    if row["qual"] and not p["qual"]:
        p["qual"] = row["qual"]
    p["new"] = p["new"] or row["new"]
    if row["grade"] not in p["grades"]:
        p["grades"].append(row["grade"])

def family_of(name):
    n = name.lower()
    for slug, _title, words, _intro in D.CATEGORIES:
        if any(w in n for w in words):
            return slug
    return "other-compounds"

def elements_of(name):
    n = name.lower() + " "
    return [sym for sym, words in D.ELEMENT_WORDS if any(w in n for w in words)]

PRODUCTS = sorted(products.values(), key=lambda p: p["name"].lower())
for p in PRODUCTS:
    p["family"] = family_of(p["name"])
    p["elements"] = elements_of(p["name"])

CATS = []
for slug, title, _w, intro in D.CATEGORIES:
    items = [p for p in PRODUCTS if p["family"] == slug]
    CATS.append({"slug": slug, "title": title, "intro": intro, "items": items})
CAT_BY_SLUG = {c["slug"]: c for c in CATS}

ELEMENTS = {}
for p in PRODUCTS:
    for s in p["elements"]:
        ELEMENTS.setdefault(s, []).append(p["name"])

N_PRODUCTS = len(PRODUCTS)
N_LISTINGS = sum(len(p["grades"]) for p in PRODUCTS)
N_NEW = sum(p["new"] for p in PRODUCTS)
N_ELEMENTS = len(ELEMENTS)
N_FAMILIES = len(CATS)
N_STAFF = sum(s + w for _d, s, w in D.STAFF)

GRADE_LABEL = {"pharma": "BP · IP · USP · NF · FCC", "acs": "Pure · ACS"}
GRADE_NAME = {"pharma": "Pharma & food grade", "acs": "Pure & ACS grade"}

# ======================================================================= shell
def nav_link(R, href, label, key_, active):
    cur = ' aria-current="page"' if key_ == active else ""
    return f'<a href="{R}{href}" class="nav-link"{cur}>{label}</a>'

def header(R, active):
    fam_links = "".join(
        f'<li><a href="{R}products/{c["slug"]}.html">{esc(c["title"])}<small>{len(c["items"])}</small></a></li>'
        for c in CATS)
    cur = ' aria-current="page"' if active == "products" else ""
    return f'''
<a class="skip" href="#main">Skip to content</a>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a href="{R}index.html" class="wordmark" aria-label="Shanpar Industries home">
      <span class="wm-name"><span class="wm-shan">Shaŋ</span> <span class="wm-par">Par</span></span>
      <span class="wm-tag">FSSC 22000 &amp; cGMP Certified</span>
    </a>

    <nav class="main-nav" id="main-nav" aria-label="Main">
      {nav_link(R, "about.html", "About", "about", active)}
      <div class="nav-item has-mega">
        <a href="{R}products.html" class="nav-link"{cur}>Products</a>
        <button class="mega-toggle" type="button" aria-expanded="false" aria-controls="mega" aria-label="Show product categories">
          <svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M2 4.5l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>
        </button>
        <div class="mega" id="mega">
          <div class="wrap mega-inner">
            <div class="mega-intro">
              <p class="kicker">Products</p>
              <p class="mega-big">{N_PRODUCTS} products in {N_FAMILIES} families</p>
              <p class="mega-sub">Pharmacopoeia, food and analytical grades of mineral salts, chelates and premixes.</p>
              <a href="{R}products.html" class="text-link">Browse the full catalogue</a>
            </div>
            <div class="mega-fam">
              <p class="label">By family</p>
              <ul>{fam_links}</ul>
            </div>
            <div class="mega-grades">
              <p class="label">By grade</p>
              <a href="{R}products.html?grade=pharma" class="mega-grade"><strong>Pharma &amp; food grade</strong><span>BP · IP · USP · NF · FCC</span></a>
              <a href="{R}products.html?grade=acs" class="mega-grade"><strong>Pure &amp; ACS grade</strong><span>Speciality chemicals</span></a>
              <a href="{R}products.html?new=1" class="mega-grade mega-new"><strong>New products</strong><span>{N_NEW} recent additions</span></a>
            </div>
          </div>
        </div>
      </div>
      {nav_link(R, "infrastructure.html", "Infrastructure", "infrastructure", active)}
      {nav_link(R, "quality.html", "Quality", "quality", active)}
      {nav_link(R, "contact.html", "Contact", "contact", active)}
      <a href="{R}contact.html" class="btn btn-ink nav-cta-mobile">Request a quote</a>
    </nav>

    <div class="header-actions">
      <a href="{R}contact.html" class="btn btn-ink">Request a quote</a>
      <button class="nav-toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu">
        <span></span><span></span>
      </button>
    </div>
  </div>
</header>'''

def footer(R):
    fams = "".join(f'<li><a href="{R}products/{c["slug"]}.html">{esc(c["title"])}</a></li>' for c in CATS[:8])
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="{R}index.html" class="wordmark">
          <span class="wm-name"><span class="wm-shan">Shaŋ</span> <span class="wm-par">Par</span></span>
          <span class="wm-tag">FSSC 22000 &amp; cGMP Certified</span>
        </a>
        <p>Shanpar Industries Pvt. Ltd.<br>Manufacturer of fine chemicals since 1982</p>
        <p class="footer-mail">info@shanpar.com<br><span class="mono">+91 265 263 8973</span></p>
      </div>
      <div class="footer-links">
        <h3>Company</h3>
        <ul>
          <li><a href="{R}about.html">About us</a></li>
          <li><a href="{R}infrastructure.html">Infrastructure</a></li>
          <li><a href="{R}quality.html">Quality</a></li>
          <li><a href="{R}contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-links">
        <h3>Products</h3>
        <ul>{fams}<li><a href="{R}products.html">All products →</a></li></ul>
      </div>
      <address>
        <h3>Regd. office &amp; Plant I</h3>
        303/5, GIDC Estate, Makarpura<br>P.B. Box 777, Vadodara 390 010<br>Gujarat, India
        <h3 class="mt">Plant II</h3>
        Survey No. 345, Nr. Gambhira Bridge<br>Village Mujpur, Ta. Padra<br>Dist. Vadodara 391 440
      </address>
      <address>
        <h3>Mumbai office</h3>
        9, Sadhana, Nanda Patkar Marg<br>Vile Parle (E), Mumbai 400 057<br><span class="mono">+91 22 2610 4226</span>
        <h3 class="mt">USA distributor</h3>
        Canton Chem, Inc., 6310, Kerne Ct.<br>Clarksville, MD 21029, USA<br><span class="mono">+1 410 531 5671</span>
      </address>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Shanpar Industries Pvt. Ltd.</p>
      <p>FSSC 22000 · cGMP · Halal · Kosher · US FDA registered</p>
    </div>
  </div>
</footer>'''

def page(filename, title, desc, body, active="", R="", scripts=("main",)):
    js = ""
    if "catalogue" in scripts:
        js += f'<script src="{R}js/catalogue.js"></script>\n'
    js += f'<script src="{R}js/main.js"></script>'
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{R}css/style.css">
</head>
<body class="page-{active or 'home'}">
{header(R, active)}
<main id="main">
{body}
{cta(R)}
</main>
{footer(R)}
{js}
</body>
</html>
'''
    path = os.path.join(OUT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", filename)

def cta(R):
    return f'''
<section class="cta">
  <div class="wrap cta-inner">
    <h2>Tell us the product, grade and quantity.</h2>
    <div class="cta-side">
      <p>Our sales team will get back to you with specifications and pricing.</p>
      <dl>
        <div><dt>Email</dt><dd>info@shanpar.com</dd></div>
        <div><dt>Phone</dt><dd>+91 265 263 8973</dd></div>
        <div><dt>USA</dt><dd>+1 410 531 5671</dd></div>
      </dl>
      <a href="{R}contact.html" class="btn btn-white">Send an enquiry <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>'''

def page_hero(kicker, h1, lede, crumbs, R, aside="", cls=""):
    bc = "".join(f'<li><a href="{R}{h}">{esc(t)}</a></li>' for t, h in crumbs)
    return f'''
<section class="page-hero {cls}">
  <div class="wrap page-hero-inner">
    <div class="ph-text">
      <ol class="crumbs" aria-label="Breadcrumb"><li><a href="{R}index.html">Home</a></li>{bc}</ol>
      <p class="kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p class="ph-lede">{lede}</p>
    </div>
    {aside}
  </div>
</section>'''

def sec_head(kicker, h2, text, id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'''<div class="sec-head"><div><p class="kicker">{kicker}</p><h2{i}>{h2}</h2></div><p>{text}</p></div>'''

# ======================================================================= pieces
def product_rows(items, R, show_family=True):
    rows = []
    for p in items:
        fam = CAT_BY_SLUG[p["family"]]
        grades = "".join(f'<span class="g g-{g}">{GRADE_LABEL[g]}</span>' for g in ("pharma", "acs") if g in p["grades"])
        new = '<span class="badge-new">New</span>' if p["new"] else ""
        qual = f' <em>{esc(p["qual"])}</em>' if p["qual"] else ""
        fam_cell = f'<td class="c-fam"><a href="{R}products/{fam["slug"]}.html">{esc(fam["title"])}</a></td>' if show_family else ""
        enquire = f'{R}contact.html?product={quote(p["name"])}'
        rows.append(
            f'<tr data-name="{esc(p["name"].lower())}" data-family="{p["family"]}" data-grades="{" ".join(p["grades"])}" data-new="{1 if p["new"] else 0}">'
            f'<th scope="row"><span class="p-name">{esc(p["name"])}{qual}</span>{new}</th>'
            f'{fam_cell}<td class="c-grade">{grades}</td>'
            f'<td class="c-act"><a href="{enquire}" class="row-link">Enquire <span aria-hidden="true">→</span></a></td></tr>')
    head_fam = '<th scope="col">Family</th>' if show_family else ""
    return f'''<div class="ptable-wrap"><table class="products-table">
<thead><tr><th scope="col">Product</th>{head_fam}<th scope="col">Grades</th><th scope="col"><span class="sr">Enquire</span></th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>'''

def cust_list(names):
    return '<ul class="clients">' + "".join(f"<li>{esc(n)}</li>" for n in names) + "</ul>"

WATER = '''
<div class="water" role="img" aria-label="Bore-well water at 5,000 litres per hour passes through RO-1, HSRO and EDI to give 2.0 cubic metres per hour of purified water, stored in a 2,000 litre tank and circulated through an SS 316 loop to user points and back.">
  <div class="w-node w-source"><span class="w-val">5,000<small>L/hr</small></span><span class="w-name">Bore well</span></div>
  <div class="w-pipe"></div>
  <div class="w-node w-stage"><span class="w-name">RO-1</span><span class="w-sub">Reverse osmosis</span></div>
  <div class="w-pipe"></div>
  <div class="w-node w-stage"><span class="w-name">HSRO</span><span class="w-sub">Hot-sanitisable RO</span></div>
  <div class="w-pipe"></div>
  <div class="w-node w-stage"><span class="w-name">EDI</span><span class="w-sub">Electrodeionisation</span></div>
  <div class="w-pipe"></div>
  <div class="w-node w-out"><span class="w-val">2.0<small>m³/hr</small></span><span class="w-name">Purified water</span></div>
  <div class="w-pipe"></div>
  <div class="w-node w-tank"><span class="w-val">2,000<small>L</small></span><span class="w-name">Distribution tank</span></div>
  <div class="w-loop"><span>SS 316 loop to user points</span></div>
</div>'''

# ======================================================================= HOME
def build_home():
    R = ""
    ticker_names = ["Calcium Gluconate", "Zinc Citrate", "Ferrous Bisglycinate", "Magnesium Aspartate",
                    "Sodium Selenite", "Chromium Picolinate", "Copper Gluconate", "Ferric Pyrophosphate"]
    tick = "".join(f'<span{" class=\"o\"" if i % 2 else ""}>{n}</span>' for i, n in enumerate(ticker_names))
    photo_steps = [s for s in D.PROCESS if s[2]][:6]
    step_no = {s[0]: i + 1 for i, s in enumerate(D.PROCESS)}
    steps = "".join(f'''<li>
        <figure><img src="images/{img}" alt="" loading="lazy"></figure>
        <span class="step-no">Stage {step_no[name]:02d} of 12</span>
        <h3>{name}</h3><p>{note}</p></li>''' for name, note, img in photo_steps)
    lines = [
        ("APIs &amp; Nutraceuticals", "Mineral salts and chelates made to pharmacopoeia monographs. DMF available for selected products.", ["BP", "IP", "USP", "NF"], "products.html?grade=pharma"),
        ("Mineral Fortifiers", "Calcium, iron, zinc and magnesium salts for fortified foods and beverages.", ["FCC", "Food grade"], "products.html?grade=pharma"),
        ("Mineral Premixes", "Trace-mineral triturations such as sodium selenite 1% in maltodextrin and chromium 0.2%.", ["1% premix", "0.2% premix"], "products/mineral-premixes.html"),
        ("Speciality Chemicals", "Peroxides, strontium, bismuth, vanadium and other compounds for industrial and lab use.", ["Pure", "ACS"], "products.html?grade=acs"),
    ]
    seg = "".join(f'''<li><a href="{href}">
        <h3>{t}</h3><p>{d}</p><span class="tags">{"".join(f"<b>{x}</b>" for x in tags)}</span>
        <span class="seg-arrow" aria-hidden="true">→</span></a></li>''' for t, d, tags, href in lines)

    slides_html = "".join(
        f'<figure class="slide{' is-active' if i == 0 else ''}" data-caption="{esc(cap)}">'
        f'<img src="images/{f}" alt="{esc(alt)}" style="object-position:{pos}"{'' if i == 0 else ' loading="lazy"'}></figure>'
        for i, (f, cap, alt, pos) in enumerate(D.HERO_SLIDES))
    body = f'''
<section class="hero" aria-roledescription="carousel" aria-label="Inside Shanpar">
  <div class="hero-media">
    {slides_html}
  </div>
  <div class="wrap hero-text">
    <p class="eyebrow">Shanpar Industries &nbsp;/&nbsp; Vadodara, India &nbsp;/&nbsp; Est. 1982</p>
    <h1>Mineral salts <span class="h1-accent">made to monograph.</span></h1>
    <p class="hero-lede">Gluconates, citrates, glycinates and {N_PRODUCTS - 3} more products in BP, IP, USP, NF, FCC and ACS grades, for pharmaceutical, nutraceutical and food brands in over 40 countries.</p>
    <div class="hero-buttons">
      <a href="products.html" class="btn btn-white">Explore products <span aria-hidden="true">→</span></a>
      <a href="contact.html" class="btn btn-ghost">Request a sample</a>
    </div>
  </div>
  <div class="wrap hero-bar">
    <p class="media-caption" aria-live="polite"><span class="media-count">01 / {len(D.HERO_SLIDES):02d}</span> <span class="media-text">{D.HERO_SLIDES[0][1]}</span></p>
    <div class="media-dots" role="tablist" aria-label="Choose photo">
      {"".join(f'<button role="tab" aria-selected="{str(i == 0).lower()}" aria-label="Photo {i + 1}"><i></i></button>' for i in range(len(D.HERO_SLIDES)))}
    </div>
  </div>
</section>

<section class="hero-stats-band">
  <div class="wrap">
    <dl class="hero-stats">
      <div><dt>1982</dt><dd>Founded in Vadodara</dd></div>
      <div><dt><span data-count="40">40</span>+</dt><dd>Export countries</dd></div>
      <div><dt><span data-count="{N_PRODUCTS}">{N_PRODUCTS}</span></dt><dd>Products in the catalogue</dd></div>
      <div><dt><span data-count="{N_ELEMENTS}">{N_ELEMENTS}</span></dt><dd>Elements we work with</dd></div>
    </dl>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{tick}{tick}</div></div>

<section class="section about-home">
  <div class="wrap">
    <p class="kicker">About Shanpar</p>
    <p class="statement">We began in 1982 making <em>mineral gluconates</em>. Four decades later we manufacture minerals and speciality chemicals for food, beverage, cosmetic and pharmaceutical companies worldwide.</p>
    <ol class="timeline">
      <li><span class="tl-year">1982</span><span class="tl-dot" aria-hidden="true"></span><p><strong>Founded in Vadodara</strong>Started as a mineral gluconate manufacturer at GIDC Makarpura.</p></li>
      <li><span class="tl-year">2016</span><span class="tl-dot" aria-hidden="true"></span><p><strong>Plant II goes live at Mujpur</strong>Built to FSSAI, FSSC 22000, cGMP and ICH Q7A guidelines.</p></li>
      <li><span class="tl-year">Today</span><span class="tl-dot" aria-hidden="true"></span><p><strong>{N_PRODUCTS} products, 40+ countries</strong>With an office in Mumbai and a distributor in the USA.</p></li>
    </ol>
    <a href="about.html" class="text-link">More about us</a>
  </div>
</section>

<section class="section elements" id="elements">
  <div class="wrap">
    {sec_head("Product range", "Our periodic table", f"We supply salts, chelates and premixes of {N_ELEMENTS} elements. The darker the tile, the more products we make with it. Select an element to see the full list.")}
    <div class="ptable" id="ptable"><div class="ptable-panel" id="ptable-panel" aria-live="polite"></div></div>
    <div class="ptable-legend">
      <span class="label">Products per element</span>
      <ol><li><i class="lv1"></i>1</li><li><i class="lv2"></i>2–3</li><li><i class="lv3"></i>4–7</li><li><i class="lv4"></i>8–14</li><li><i class="lv5"></i>15+</li></ol>
      <a href="products.html" class="text-link">Full catalogue</a>
    </div>
  </div>
</section>

<section class="section segments-sec">
  <div class="wrap">
    {sec_head("Markets", "Four product lines", "Each line is made to the grade your market asks for, from pharmacopoeia monographs to food chemical codex and analytical reagent specs.")}
    <ul class="seg-list">{seg}</ul>
  </div>
</section>

<section class="section process">
  <div class="wrap">
    {sec_head("Manufacturing", "How a batch moves through Plant II", "Six of the twelve stages in our general process flow, photographed on the shop floor. Material moves one way through the plant, with separate entries for people and materials.")}
    <ol class="steps">{steps}</ol>
    <a href="infrastructure.html#process" class="text-link steps-link">See all 12 stages</a>
  </div>
</section>

<section class="section glance">
  <div class="wrap">
    {sec_head("Infrastructure", "Plant II at a glance", "Our Mujpur site sits 30 km from Vadodara airport, with its own purified water system, steam, compressed air and HEPA-filtered air handling.")}
    <dl class="glance-grid">
      <div><dt>11,891<small>m²</small></dt><dd>Total site area</dd></div>
      <div><dt>4,263<small>m²</small></dt><dd>Built-up area</dd></div>
      <div><dt>2.0<small>m³/hr</small></dt><dd>Purified water, RO + HSRO + EDI</dd></div>
      <div><dt>2 × 2,000<small>kg/hr</small></dt><dd>Boiler capacity for indirect heating</dd></div>
      <div><dt>250<small>kVA</small></dt><dd>HT power, continuous process licence</dd></div>
      <div><dt>HEPA</dt><dd>Terminal filters in drying, blending and packing areas</dd></div>
    </dl>
    <a href="infrastructure.html" class="text-link">Explore our infrastructure</a>
  </div>
</section>

<section class="section quality-home">
  <div class="wrap">
    {sec_head("Quality", "Certified, audited, tested", "Every procedure meets FSSC 22000 and cGMP standards, and products are made under a HACCP programme. National and international health agencies inspect the plant.")}
    <ul class="certs">
      <li class="c-big"><strong>FSSC<br>22000</strong><span>Food safety system certification</span></li>
      <li class="c-big"><strong>cGMP</strong><span>Schedule M good manufacturing practice</span></li>
      <li><strong>US FDA</strong><span>Registered for food exports to the US</span></li>
      <li><strong>FSSAI</strong><span>Central licence</span></li>
      <li><strong>SMETA</strong><span>4-pillar ethical trade audit</span></li>
      <li><strong>DMF</strong><span>Available for selected APIs</span></li>
      <li><strong>Halal</strong><span>Certified</span></li>
      <li><strong>Kosher</strong><span>Certified</span></li>
    </ul>
    <a href="quality.html" class="text-link">Quality systems and licences</a>
  </div>
</section>

<section class="section customers">
  <div class="wrap">
    {sec_head("Customers", "Supplying global brands", "Multinational and leading Indian companies in pharma, nutrition and food buy from us.")}
    {cust_list(D.CUSTOMERS[:20])}
  </div>
</section>'''
    page("index.html", "Shanpar Industries | Mineral Salts & Speciality Chemicals since 1982",
         f"Shanpar Industries, Vadodara: {N_PRODUCTS} mineral salts, chelates and premixes in BP, IP, USP, NF, FCC and ACS grades. FSSC 22000 and cGMP certified. Exporting to 40+ countries since 1982.",
         body, "", R, scripts=("catalogue", "main"))

# ======================================================================= ABOUT
def build_about():
    R = ""
    people = "".join(f'''<li>
      <span class="pp-years">{yrs}<small>{"+" if yrs >= 30 else ""} yrs</small></span>
      <h3>{esc(n)}</h3><p class="pp-role">{esc(role)}</p>
      <p class="pp-note">{esc(q + " · ") if q else ""}{esc(note)}</p></li>''' for n, role, q, yrs, note in D.PEOPLE)
    mx = max(s + w for _d, s, w in D.STAFF)
    bars = "".join(f'''<li data-tip="{esc(d)}: {s} management/staff, {w} workmen">
      <span class="sb-label">{esc(d)}</span>
      <span class="sb-track"><span class="sb-bar" style="--total:{(s + w) / mx * 100:.2f}%;--f:{s / (s + w) * 100:.2f}%">
        <i class="sb-s"></i><i class="sb-w"></i></span><span class="sb-total">{s + w}</span></span></li>''' for d, s, w in D.STAFF)
    vision = "".join(f"<li>{esc(v)}</li>" for v in D.VISION)
    tot_s = sum(s for _d, s, _w in D.STAFF); tot_w = sum(w for _d, _s, w in D.STAFF)
    aside = '<figure class="ph-media"><img src="images/plant-exterior.jpg" alt="Shanpar Plant II building, Mujpur" style="object-position:62% 50%"><figcaption>Plant II, Mujpur</figcaption></figure>'
    body = page_hero("About us", "Four decades of mineral chemistry.",
        "Shanpar Industries Pvt. Ltd. was founded in Vadodara in 1982 as a mineral gluconate manufacturer. Promoted by Mr. B. N. Patel, we make nutraceuticals, speciality chemicals and bulk drugs for domestic and export markets.",
        [("About us", "about.html")], R, aside) + f'''

<section class="facts-band">
  <div class="wrap">
    <dl class="facts">
      <div><dt>1982</dt><dd>Established, Unit I at Makarpura, Vadodara</dd></div>
      <div><dt>2015</dt><dd>Unit II established at Mujpur, Vadodara</dd></div>
      <div><dt>40+</dt><dd>Countries we export to</dd></div>
      <div><dt>{N_STAFF}</dt><dd>People across both plants and offices</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Corporate profile", "Experience and innovation", "Three decades after our founding, we had established ourselves as a quality manufacturer of minerals and speciality chemicals for the food, beverage, cosmetic and pharmaceutical industries. Our products are accepted worldwide and exported to more than 40 countries.")}
    <div class="pillars">
      <article><h3>Commitment</h3><p>All procedures meet stringent FSSC 22000 and cGMP standards, and products are manufactured under a HACCP programme. Shanpar is recognised as a GMP manufacturer and upgrades its facility regularly to maintain cGMP standards.</p></article>
      <article><h3>Competence</h3><p>We support customers with cross-functional teams of technocrats. Innovation and flexibility drive our development work, and our experience with customised granules and powders turns your problems into value-added solutions.</p></article>
      <article><h3>Logistics</h3><p>Our trained customer service team handles orders with professional accuracy, so they are executed just in time, every time.</p></article>
      <article><h3>Environment &amp; safety</h3><p>We use operating procedures that protect the environment while improving public health and safety, and we reduce our impact by conserving raw materials and energy and recycling waste.</p></article>
    </div>
  </div>
</section>

<section class="section vision">
  <div class="wrap vision-inner">
    <div>
      <p class="kicker">Our vision</p>
      <h2>Grow as partners of multinationals.</h2>
      <p class="vision-sign">B. N. Patel<span>Managing Director</span></p>
    </div>
    <ol class="vision-list">{vision}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Key personnel", "The people behind the plant", "Our leadership brings more than 170 combined years of experience in organic chemistry, bulk drugs, quality and manufacturing.")}
    <ul class="people">{people}</ul>
  </div>
</section>

<section class="section team">
  <div class="wrap">
    {sec_head("Employee strength", f"{N_STAFF} people, {tot_s + 0} in management and staff", f"{tot_s} management and staff members and {tot_w} workmen. Manufacturing and packing is our largest team; the quality unit is our largest staff function.")}
    <div class="staff-chart" id="staff-chart">
      <div class="sc-legend"><span><i class="sb-s"></i>Management / staff</span><span><i class="sb-w"></i>Workmen</span></div>
      <ul class="sc-bars">{bars}</ul>
      <div class="sc-tip" id="sc-tip" hidden></div>
    </div>
    <details class="sc-table">
      <summary>View as table</summary>
      <table><thead><tr><th scope="col">Department</th><th scope="col">Management / staff</th><th scope="col">Workmen</th></tr></thead>
      <tbody>{"".join(f"<tr><th scope='row'>{esc(d)}</th><td>{s}</td><td>{w}</td></tr>" for d, s, w in D.STAFF)}
      <tr class="tot"><th scope="row">Total</th><td>{tot_s}</td><td>{tot_w}</td></tr></tbody></table>
    </details>
  </div>
</section>

<section class="section customers">
  <div class="wrap">
    {sec_head("Customers", "Who we supply", "We serve multinational and leading Indian companies in pharmaceuticals, nutrition and food.")}
    {cust_list(D.CUSTOMERS)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Policies", "How we work", "Our documented policies cover ethics, people, safety and product integrity.")}
    <ul class="chips">{"".join(f"<li>{esc(p)}</li>" for p in D.POLICIES)}</ul>
  </div>
</section>'''
    page("about.html", "About Us | Shanpar Industries",
         "Shanpar Industries was founded in Vadodara in 1982 as a mineral gluconate manufacturer. Company profile, vision, key personnel and customers.",
         body, "about", R)

# ======================================================================= INFRASTRUCTURE
def build_infra():
    R = ""
    flow = []
    for i, (name, note, _img) in enumerate(D.PROCESS, 1):
        side = ""
        if name == "Raw material": side = '<span class="pf-side pf-in">+ Process water</span>'
        if name == "Filtration": side = '<span class="pf-side pf-out">Reject residue</span>'
        if name == "Evaporation": side = '<span class="pf-side pf-out">Water rejects</span>'
        if name == "Packing": side = '<span class="pf-side pf-in">QC approval</span>'
        flow.append(f'<li><span class="pf-no">{i:02d}</span><h3>{name}</h3><p>{note}</p>{side}</li>')
    gallery = [("production.jpg", "Reaction and charging area"), ("centrifuge.jpg", "Centrifuge"),
               ("fbd.jpg", "Fluid bed dryer"), ("sifter.jpg", "Vibro sifter"),
               ("hero-blending.jpg", "Blending room"), ("hero-sifting.jpg", "Sifting room"),
               ("gowning.jpg", "Gowning room"), ("hero-corridor.jpg", "Clean corridor"),
               ("hero-warehouse.jpg", "Raw material warehouse")]
    gal = "".join(f'<figure><img src="images/{f}" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for f, c in gallery)
    aside = '<figure class="ph-media"><img src="images/plant-exterior.jpg" alt="Shanpar Plant II building at Mujpur" style="object-position:62% 50%"><figcaption>Front side entry, Plant II</figcaption></figure>'
    body = page_hero("Infrastructure", "Plant II, Mujpur.",
        "Our main manufacturing site, 30 km from Vadodara airport. It was built to FSSAI, FSSC 22000, cGMP and ICH Q7A guidelines and has been in operation since January 2016.",
        [("Infrastructure", "infrastructure.html")], R, aside) + f'''

<section class="facts-band">
  <div class="wrap">
    <dl class="facts">
      <div><dt>11,891<small>m²</small></dt><dd>Total site area</dd></div>
      <div><dt>4,263<small>m²</small></dt><dd>Built-up area</dd></div>
      <div><dt>30<small>km</small></dt><dd>From Vadodara airport</dd></div>
      <div><dt>2016</dt><dd>In operation since January</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Plant layout", "Two floors, one direction of flow", "The plant is designed for unidirectional material flow, with segregated entries for people and materials. Each floor is zoned by function. Schematic, not to scale.")}
    <div class="floorplan">
      <div class="fp-floor">
        <p class="fp-name"><span>First floor</span></p>
        <div class="fp-zones">
          <div class="z z-q" style="--w:1.1">QA</div>
          <div class="z z-s" style="--w:1.6">FG store</div>
          <div class="z z-s" style="--w:1.2">PM store</div>
          <div class="z z-u" style="--w:1">Utility</div>
          <div class="z z-m" style="--w:2.4">Reaction area</div>
        </div>
      </div>
      <div class="fp-floor">
        <p class="fp-name"><span>Ground floor</span></p>
        <div class="fp-zones">
          <div class="z z-q" style="--w:1.1">QC</div>
          <div class="z z-s" style="--w:1.6">FG store</div>
          <div class="z z-m" style="--w:3">Manufacturing area</div>
          <div class="z z-s" style="--w:1.6">RM store</div>
        </div>
      </div>
      <div class="fp-flow" aria-hidden="true"><span>Material flow</span></div>
      <ul class="fp-key">
        <li><i class="z-m"></i>Manufacturing</li><li><i class="z-s"></i>Stores</li><li><i class="z-q"></i>Quality</li><li><i class="z-u"></i>Utility</li>
      </ul>
    </div>
  </div>
</section>

<section class="section process-flow" id="process">
  <div class="wrap">
    {sec_head("Process", "General process flow", "Every product follows the same twelve controlled stages, from raw material to dispatch. Nothing is packed until QC has approved the batch.")}
    <ol class="pflow">{"".join(flow)}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Utilities", "Purified water system", "Bore-well water, tested and accepted, is purified through RO-1, HSRO and EDI. The HSRO, HSEDI and distribution loop are sanitised by hot-water circulation.")}
    {WATER}
    <div class="utils">
      <article><span class="u-val">250<small>kVA</small></span><h3>Power</h3><p>HT connection from the GEB grid, with a continuous process industry licence for uninterrupted supply from Gujarat State.</p></article>
      <article><span class="u-val">2 × 2,000<small>kg/hr</small></span><h3>Boilers</h3><p>Two boilers. Steam is used for indirect heating.</p></article>
      <article><span class="u-val">100<small>CFM</small></span><h3>Air compressor</h3><p>7 kg/cm² with 5 micron filters. Compressed air drives pneumatic operations and utilities.</p></article>
      <article><span class="u-val">2,000<small>L</small></span><h3>Water storage</h3><p>Distribution tank at room temperature with an SS 316 loop to user points and back.</p></article>
    </div>
  </div>
</section>

<section class="section air">
  <div class="wrap">
    {sec_head("Air handling", "Clean air where the product is open", "Each area where product is exposed has its own filtered air system.")}
    <div class="air-table">
      <div class="at-row at-head"><span>Area</span><span>System</span><span>Terminal filter</span></div>
      <div class="at-row"><span>Centrifuge and dryer area</span><span>AHU</span><span class="hepa">HEPA</span></div>
      <div class="at-row"><span>Blending and packing area</span><span>HVAC</span><span class="hepa">HEPA</span></div>
      <div class="at-row"><span>Sampling and dispensing rooms</span><span>RLAF (reverse laminar air flow)</span><span>—</span></div>
      <div class="at-row"><span>Microbiology laboratory</span><span>HVAC, bio safety cabinet and LAF</span><span class="hepa">HEPA</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("On the shop floor", "Equipment and clean areas", "Photographed at Plant II.")}
    <div class="gallery">{gal}</div>
  </div>
</section>

<section class="section ehs">
  <div class="wrap">
    {sec_head("Environment, health &amp; safety", "Monitored, measured, drilled", "We follow GPCB, EICL and NECL regulations and monitor our emissions, effluent and workplace continuously.")}
    <ul class="ehs-grid">
      <li><h3>Stack monitoring</h3><p>At the scrubber and boiler.</p></li>
      <li><h3>Air monitoring</h3><p>Ambient and workplace air.</p></li>
      <li><h3>Noise monitoring</h3><p>Across the plant.</p></li>
      <li><h3>ETP water analysis</h3><p>Effluent treatment plant water is tested.</p></li>
      <li><h3>Equipment safety testing</h3><p>For safety at the workplace.</p></li>
      <li><h3>Fire safety</h3><p>Extinguishers placed where required, with an emergency alarm system.</p></li>
      <li><h3>Mock drills</h3><p>Fire and emergency mock drill training.</p></li>
      <li><h3>Pollution-free setting</h3><p>The plant sits in pollution-free surroundings.</p></li>
    </ul>
  </div>
</section>

<section class="section units">
  <div class="wrap">
    {sec_head("Locations", "Two manufacturing units", "Both units are in Vadodara district, Gujarat.")}
    <div class="unit-cards">
      <article><p class="label">Unit I · Est. 1982</p><h3>Makarpura</h3><p>Corporate office and manufacturing facility.<br>303/5, GIDC Estate, Makarpura, Vadodara 390 010</p></article>
      <article><p class="label">Unit II · Est. 2015</p><h3>Mujpur</h3><p>Main manufacturing plant, 11,891 m² site.<br>Survey No. 345, Nr. Gambhira Bridge, Village Mujpur, Ta. Padra, Dist. Vadodara 391 440</p></article>
    </div>
  </div>
</section>'''
    page("infrastructure.html", "Infrastructure | Shanpar Industries",
         "Shanpar Plant II at Mujpur, Vadodara: 11,891 m² site, purified water system, HEPA air handling, boilers and a 12-stage process flow built to FSSC 22000, cGMP and ICH Q7A.",
         body, "infrastructure", R)

# ======================================================================= QUALITY
def build_quality():
    R = ""
    qa = ["Validation and qualification", "FSMS procedure", "Change control", "Risk analysis", "Documentation control",
          "Deviation control", "Vendor management", "Annual product review", "Labelling control", "Failure investigation",
          "Self inspection", "Market complaint review", "Product recall",
          "Training: orientation, on-the-job, cGMP and food safety"]
    qc = ["Analytical testing of RM, PM, intermediates and finished products", "Preparing and updating test specifications",
          "Updating and upgrading QC SOPs", "Calibration and qualification of instruments", "Out-of-specification handling",
          "Training of personnel", "Analytical method validation", "Working standard preparation and maintenance",
          "Product stability studies"]
    food = ["Systematic monitoring of work procedures, from receipt of incoming material to dispatch of finished goods.",
            "Eliminating physical, chemical and microbiological contamination, or reducing it to acceptable levels.",
            "Meeting all statutory and regulatory requirements for food safety and a quality culture.",
            "Managing internal and external communication.",
            "Keeping high standards of hygiene in plant, machinery and personnel.",
            "Building awareness of the food safety system among employees, suppliers and customers.",
            "Strict adherence to the food safety system and its continual improvement."]
    labs = [("SGS India Private Limited", "", "Plot 21, Sector 3, IMT Manesar, Gurugram, Haryana 122 050"),
            ("Gujarat Test Lab Pvt. Ltd.", "Lic. GTL/20 · FSSAI approved", "F-16-17 & E17, Madhavpura Market, Sahibaug, Ahmedabad 380 004"),
            ("Choksi Laboratories Ltd.", "Lic. GTL-14", "829 GIDC, Makarpura, Vadodara 390 010"),
            ("Baroda Analytical Services", "Lic. GTL/37/32", "78/2/3 GIDC, Makarpura, Vadodara 390 010"),
            ("Bee Pharmo Labs Pvt. Ltd.", "", "C-2, Hatkesh Udyog Nagar, Mira Bhayander Road, Mira Road (E), Thane 401 107")]
    licences = [
        ("Drug Licence", "G/25/2111", "Valid to 09 Jul 2030"),
        ("FSSAI Central Licence", "10714024000269", "Valid to 16 Jun 2029"),
        ("FSSC 22000", "Food safety system certification", "Valid to 11 Dec 2027"),
        ("GMP certificate", "Schedule M", ""),
        ("GLP certificate", "Good laboratory practice", ""),
        ("SMETA", "4-pillar ethical trade audit", "Approved"),
        ("US FDA", "Registered for food product export to the US", "Registered"),
        ("Kosher &amp; Halal", "Products certified", "Certified"),
    ]
    lic = "".join(f'<div class="lic-row"><strong>{n}</strong><span class="mono">{d}</span><span class="lic-valid">{v}</span></div>' for n, d, v in licences)
    aside = '''<div class="ph-certs"><figure><img src="images/cert-fssc.jpg" alt="FSSC 22000 certificate of registration"></figure><figure><img src="images/cert-kosher.jpg" alt="Star-K Kosher certificate"></figure></div>'''
    body = page_hero("Quality", "Quality you can audit.",
        "Our quality policy ensures that quality systems and procedures are followed, so every product meets its specifications for quality, purity, efficacy and safety.",
        [("Quality", "quality.html")], R, aside, "ph-quality") + f'''

<section class="section">
  <div class="wrap">
    {sec_head("Licences &amp; certifications", "Regulatory approvals", "Our plant is inspected by international and national health agencies. Certificates are available on request.")}
    <div class="lic">{lic}</div>
    <div class="free-from"><span class="label">Our products are</span><ul class="chips"><li>Allergen free</li><li>BSE / TSE free</li><li>Melamine free</li><li>GMO free</li></ul></div>
  </div>
</section>

<section class="section policy">
  <div class="wrap policy-inner">
    <div>
      <p class="kicker">Food safety &amp; quality policy</p>
      <h2>Safe, hazard-free food ingredients and nutrients.</h2>
      <p class="policy-sign">B. N. Patel<span>Authorised signatory</span></p>
    </div>
    <ol class="vision-list">{"".join(f"<li>{esc(x)}</li>" for x in food)}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Quality unit", "Assurance and control", "Our quality unit has 21 people across QA and QC, working separately from production.")}
    <div class="qa-qc">
      <article><p class="qq-count">{len(qa)}<small>functions</small></p><h3>Quality assurance</h3><ul>{"".join(f"<li>{esc(x)}</li>" for x in qa)}</ul></article>
      <article><p class="qq-count">{len(qc)}<small>functions</small></p><h3>Quality control</h3><ul>{"".join(f"<li>{esc(x)}</li>" for x in qc)}</ul></article>
    </div>
  </div>
</section>

<section class="section lab">
  <div class="wrap">
    {sec_head("Laboratory", "An independent QC section", "Separate from the production area, staffed by qualified and trained analysts.")}
    <ul class="lab-grid">
      <li><h3>Segregated sections</h3><p>Instrumentation and chemical analysis, with a separate microbiology section on the first floor.</p></li>
      <li><h3>Calibration</h3><p>Calibration and qualification of instruments carried out in-house.</p></li>
      <li><h3>Written procedures</h3><p>For solvents, reagents, reference and working standards, cultures and media, and retain samples.</p></li>
      <li><h3>Stability studies</h3><p>For all process validation batches, then one batch of each product every year.</p></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Validation master plan", "Validated before it ships", "The validation master plan sets out every validation activity. Requalification runs at defined intervals, and revalidation follows any change in equipment, critical process steps, specifications, active or primary packaging material.")}
    <ol class="vmp">
      <li><span>Equipment</span>qualification</li>
      <li><span>Manufacturing process</span>validation</li>
      <li><span>Utilities</span>qualification (water system, AHU)</li>
      <li><span>Analytical method</span>validation</li>
      <li><span>Cleaning</span>validation</li>
    </ol>
  </div>
</section>

<section class="section labs-sec">
  <div class="wrap">
    {sec_head("Testing contractors", "Independent laboratories", "Government FDCA and FSSAI approved laboratories we work with for third-party testing.")}
    <ul class="lab-cards">{"".join(f'<li><h3>{esc(n)}</h3>{f"<p class=\"lab-lic\">{esc(l)}</p>" if l else ""}<p>{esc(a)}</p></li>' for n, l, a in labs)}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("Policies", "Documented and enforced", "Our quality and food safety systems are backed by these company policies.")}
    <ul class="chips">{"".join(f"<li>{esc(p)}</li>" for p in D.POLICIES)}</ul>
  </div>
</section>'''
    page("quality.html", "Quality & Certifications | Shanpar Industries",
         "FSSC 22000, cGMP (Schedule M), FSSAI, drug licence, US FDA registration, Kosher and Halal. Shanpar quality assurance, quality control, validation and testing.",
         body, "quality", R)

# ======================================================================= PRODUCTS
def family_cards(R, current=""):
    out = []
    for c in CATS:
        cur = ' aria-current="page"' if c["slug"] == current else ""
        els = sorted({s for p in c["items"] for s in p["elements"]})
        out.append(f'''<li><a href="{R}products/{c["slug"]}.html"{cur}>
          <span class="fc-count">{len(c["items"])}</span>
          <h3>{esc(c["title"])}</h3>
          <span class="fc-els">{" ".join(els[:7])}{" …" if len(els) > 7 else ""}</span></a></li>''')
    return "".join(out)

def build_products():
    R = ""
    aside = f'''<dl class="ph-stats">
      <div><dt>{N_PRODUCTS}</dt><dd>Products</dd></div>
      <div><dt>{N_FAMILIES}</dt><dd>Families</dd></div>
      <div><dt>{N_ELEMENTS}</dt><dd>Elements</dd></div>
      <div><dt>{N_NEW}</dt><dd>New</dd></div></dl>'''
    fam_opts = "".join(f'<option value="{c["slug"]}">{esc(c["title"])} ({len(c["items"])})</option>' for c in CATS)
    body = page_hero("Products", "Product catalogue",
        f"{N_PRODUCTS} mineral salts, chelates, premixes and speciality chemicals. Most are made to BP, IP, USP, NF and FCC monographs; speciality chemicals are supplied in Pure and ACS grades.",
        [("Products", "products.html")], R, aside) + f'''

<section class="section families-sec">
  <div class="wrap">
    {sec_head("Browse by family", "Product families", "Each family page lists every grade we make, with its available specifications.")}
    <ul class="fam-cards">{family_cards(R)}</ul>
  </div>
</section>

<section class="section catalogue" id="catalogue">
  <div class="wrap">
    {sec_head("Full list", "Find a product", "Search by name or filter by grade and family. Send an enquiry from any row.")}
    <form class="filters" id="filters" role="search" onsubmit="return false">
      <div class="f-search">
        <label for="f-q" class="sr">Search products</label>
        <input id="f-q" type="search" placeholder="Search, e.g. zinc or gluconate" autocomplete="off">
      </div>
      <div class="f-seg" role="radiogroup" aria-label="Grade">
        <label><input type="radio" name="grade" value="" checked><span>All grades</span></label>
        <label><input type="radio" name="grade" value="pharma"><span>BP · IP · USP · NF · FCC</span></label>
        <label><input type="radio" name="grade" value="acs"><span>Pure · ACS</span></label>
      </div>
      <div class="f-row">
        <label for="f-fam" class="sr">Family</label>
        <select id="f-fam"><option value="">All families</option>{fam_opts}</select>
        <label class="f-check"><input type="checkbox" id="f-new"><span>New only</span></label>
      </div>
    </form>
    <p class="f-count" id="f-count" aria-live="polite">Showing {N_PRODUCTS} of {N_PRODUCTS} products</p>
    {product_rows(PRODUCTS, R)}
    <p class="f-empty" id="f-empty" hidden>No products match. Try another search, or <a href="contact.html">ask us</a>: we also develop custom grades.</p>
  </div>
</section>

<section class="section custom">
  <div class="wrap custom-inner">
    <div><p class="kicker">Custom development</p><h2>Need a particular particle size or granule?</h2></div>
    <p>Our experience in developing customised granules and powders lets us turn your formulation problem into a value-added solution. Tell us your target specification.</p>
  </div>
</section>'''
    page("products.html", "Products | Shanpar Industries",
         f"Catalogue of {N_PRODUCTS} mineral salts, chelates, premixes and speciality chemicals in BP, IP, USP, NF, FCC, Pure and ACS grades from Shanpar Industries.",
         body, "products", R)

def build_categories():
    R = "../"
    for i, c in enumerate(CATS):
        els = sorted({s for p in c["items"] for s in p["elements"]})
        tiles = "".join(f'<li><span>{s}</span><small>{D.ELEMENT_NAMES[s]}</small></li>' for s in els)
        n_ph = sum("pharma" in p["grades"] for p in c["items"])
        n_acs = sum("acs" in p["grades"] for p in c["items"])
        n_new = sum(p["new"] for p in c["items"])
        aside = f'''<dl class="ph-stats">
          <div><dt>{len(c["items"])}</dt><dd>Products</dd></div>
          <div><dt>{n_ph}</dt><dd>Pharma / food grade</dd></div>
          <div><dt>{n_acs}</dt><dd>Pure / ACS grade</dd></div>
          {f"<div><dt>{n_new}</dt><dd>New</dd></div>" if n_new else ""}</dl>'''
        prev_c = CATS[i - 1]; next_c = CATS[(i + 1) % len(CATS)]
        side = "".join(f'<li><a href="{x["slug"]}.html"{" aria-current=\"page\"" if x is c else ""}>{esc(x["title"])}<small>{len(x["items"])}</small></a></li>' for x in CATS)
        body = page_hero("Product family", esc(c["title"]), esc(c["intro"]),
            [("Products", "products.html"), (c["title"], f'products/{c["slug"]}.html')], R, aside, "ph-cat") + f'''

<section class="section cat">
  <div class="wrap cat-inner">
    <aside class="cat-side">
      <p class="label">Families</p>
      <ul>{side}</ul>
      <a href="../products.html" class="text-link">All products</a>
    </aside>
    <div class="cat-main">
      {f'<div class="cat-els"><p class="label">Elements in this family</p><ul class="el-tiles">{tiles}</ul></div>' if tiles else ""}
      {product_rows(c["items"], R, show_family=False)}
      <div class="grade-note">
        <div><strong>BP · IP · USP · NF · FCC</strong><p>British, Indian and United States Pharmacopoeia, National Formulary and Food Chemicals Codex grades for pharmaceutical, nutraceutical and food use.</p></div>
        <div><strong>Pure · ACS</strong><p>Pure and American Chemical Society reagent grades for speciality, industrial and laboratory use.</p></div>
      </div>
      <nav class="cat-pager" aria-label="Other families">
        <a href="{prev_c["slug"]}.html"><span class="label">Previous</span>{esc(prev_c["title"])}</a>
        <a href="{next_c["slug"]}.html"><span class="label">Next</span>{esc(next_c["title"])}</a>
      </nav>
    </div>
  </div>
</section>'''
        names = ", ".join(p["name"] for p in c["items"][:6])
        page(f'products/{c["slug"]}.html', f'{c["title"]} | Shanpar Industries',
             f'{c["title"]} from Shanpar Industries: {names}. Available in pharmacopoeia, food and ACS grades.',
             body, "products", R)

# ======================================================================= CONTACT
def build_contact():
    R = ""
    offices = [
        ("Regd. office &amp; Plant I", "Makarpura, Vadodara", "303/5, GIDC Estate, Makarpura<br>P.B. Box 777, Vadodara 390 010<br>Gujarat, India",
         [("Phone", "+91 265 263 8973 / 74 / 75 / 76"), ("Mobile", "+91 97234 64973, 98240 21461"), ("Fax", "+91 265 263 3702"), ("Email", "info@shanpar.com")],
         "Shanpar Industries GIDC Makarpura Vadodara"),
        ("Plant II", "Mujpur, Vadodara", "Survey No. 345, Nr. Gambhira Bridge<br>Village Mujpur, Ta. Padra<br>Dist. Vadodara 391 440, Gujarat, India",
         [], "Gambhira Bridge Mujpur Padra Vadodara"),
        ("Mumbai office", "Vile Parle (East)", "9, Sadhana, Nanda Patkar Marg<br>Vile Parle (E), Mumbai 400 057<br>Maharashtra, India",
         [("Phone", "+91 22 2610 4226"), ("Fax", "+91 22 2617 1532"), ("Email", "mumbai@shanpar.com")],
         "Nanda Patkar Marg Vile Parle East Mumbai 400057"),
        ("USA distributor", "Canton Chem, Inc.", "6310, Kerne Ct.<br>Clarksville, MD 21029<br>USA",
         [("Phone", "+1 410 531 5671"), ("Fax", "+1 410 531 5736"), ("Email", "apatel@cantonchem.com")],
         "6310 Kerne Ct Clarksville MD 21029"),
    ]
    cards = "".join(f'''<article class="office">
      <p class="label">{t}</p><h3>{sub}</h3><address>{addr}</address>
      {"<dl>" + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in lines) + "</dl>" if lines else ""}
      <a class="text-link" href="https://www.google.com/maps/search/?api=1&amp;query={quote(q)}" target="_blank" rel="noopener">Open in Google Maps</a>
    </article>''' for t, sub, addr, lines, q in offices)
    body = page_hero("Contact", "Talk to our sales team.",
        "Send us the product, grade and quantity you need. For orders in the USA, contact our distributor, Canton Chem, Inc.",
        [("Contact", "contact.html")], R) + f'''

<section class="section contact-sec">
  <div class="wrap contact-inner">
    <form class="enquiry" id="enquiry-form" novalidate>
      <h2>Product enquiry</h2>
      <div class="fg two">
        <div><label for="e-product">Product</label><input id="e-product" name="product" list="product-list" placeholder="e.g. Zinc gluconate" required>
          <datalist id="product-list">{"".join(f'<option value="{esc(p["name"])}">' for p in PRODUCTS)}</datalist></div>
        <div><label for="e-grade">Grade</label><select id="e-grade" name="grade">
          <option value="">Not sure</option><option>BP</option><option>IP</option><option>USP</option><option>NF</option><option>FCC</option><option>Pure</option><option>ACS</option></select></div>
      </div>
      <div class="fg two">
        <div><label for="e-qty">Quantity</label><input id="e-qty" name="quantity" placeholder="e.g. 500 kg per month"></div>
        <div><label for="e-country">Country</label><input id="e-country" name="country" autocomplete="country-name"></div>
      </div>
      <div class="fg two">
        <div><label for="e-name">Your name</label><input id="e-name" name="name" autocomplete="name" required></div>
        <div><label for="e-company">Company</label><input id="e-company" name="company" autocomplete="organization"></div>
      </div>
      <div class="fg two">
        <div><label for="e-email">Email</label><input id="e-email" name="email" type="email" autocomplete="email" required></div>
        <div><label for="e-phone">Phone</label><input id="e-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <div class="fg"><label for="e-msg">Message</label><textarea id="e-msg" name="message" rows="5" placeholder="Specification, documents needed (CoA, TDS, MSDS), packing, delivery"></textarea></div>
      <p class="form-error" id="form-error" hidden></p>
      <button type="submit" class="btn btn-indigo">Send enquiry <span aria-hidden="true">→</span></button>
      <p class="form-note">This opens your email app with the enquiry filled in, addressed to info@shanpar.com.</p>
    </form>
    <aside class="contact-direct">
      <p class="label">Direct</p>
      <p class="cd-big">info@shanpar.com</p>
      <p class="cd-big mono">+91 265 263 8973</p>
      <p class="cd-note">Monday to Saturday, Indian Standard Time.</p>
    </aside>
  </div>
</section>

<section class="section offices-sec">
  <div class="wrap">
    {sec_head("Offices", "Where to find us", "Two plants in Vadodara, a sales office in Mumbai and a distributor in the USA.")}
    <div class="offices">{cards}</div>
  </div>
</section>'''
    page("contact.html", "Contact | Shanpar Industries",
         "Contact Shanpar Industries: Vadodara head office and plants, Mumbai office and US distributor Canton Chem. Send a product enquiry.",
         body, "contact", R)

# ======================================================================= JS data
def build_catalogue_js():
    z = {}
    order = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La".split()
    for i, s in enumerate(order): z[s] = i + 1
    for i, s in enumerate("Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn".split()): z[s] = 72 + i
    els = {s: {"name": D.ELEMENT_NAMES[s], "z": z[s], "products": names} for s, names in ELEMENTS.items()}
    js = "/* Generated by _build/build.py from the company brochure. Do not edit by hand. */\n"
    js += "window.SHANPAR = " + json.dumps({"elements": els}, ensure_ascii=False, separators=(",", ":")) + ";\n"
    with open(os.path.join(OUT, "js", "catalogue.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    print("wrote js/catalogue.js")

if __name__ == "__main__":
    build_catalogue_js()
    build_home(); build_about(); build_infra(); build_quality()
    build_products(); build_categories(); build_contact()
    print(f"\n{N_PRODUCTS} products ({N_LISTINGS} grade listings), {N_NEW} new, {N_ELEMENTS} elements, {N_FAMILIES} families")
    for c in CATS: print(f'  {c["title"]:30s} {len(c["items"])}')
