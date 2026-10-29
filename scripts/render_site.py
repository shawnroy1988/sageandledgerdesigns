#!/usr/bin/env python3
"""Render the static Sage & Ledger Designs site from products.json."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shawnroy1988.github.io/sageandledgerdesigns"
ETSY = "https://www.etsy.com/shop/SageAndLedgerDesigns"
PINTEREST = "https://www.pinterest.com/shawnroy1988/"
SHOP_NAME = "Sage & Ledger Designs"
OG_IMAGE = f"{BASE}/brand/header.webp"

CATEGORIES = [
    (
        "Planners",
        "planners",
        "Printable pages for days, meals, habits, weddings, classrooms, and travel.",
    ),
    (
        "Excel & Sheets Templates",
        "excel-sheets",
        "Spreadsheets for budgets, debt, savings, net worth, and wedding costs.",
    ),
    (
        "Power BI",
        "power-bi",
        "Dashboard kits with sample data, DAX measures, themes, and setup guides.",
    ),
    (
        "Wall Art",
        "wall-art",
        "Printable sets in sage, terracotta, and quiet neutrals.",
    ),
    (
        "Party Printables",
        "party-printables",
        "Games, signs, cards, and paper packs for gatherings.",
    ),
    (
        "Small Business Templates",
        "small-business",
        "Bookkeeping, invoices, onboarding, resumes, and content planning.",
    ),
]

FEATURED_ORDER = ["47-smb-bookkeeping-2027", "46-christmas-party-games"]

FEATURED_COPY = {
    "47-smb-bookkeeping-2027": (
        "A 2027 small business bookkeeping spreadsheet for Excel and Google Sheets, "
        "with a profit and loss template, Etsy fees, a mileage tracker, and quarterly tax."
    ),
    "46-christmas-party-games": (
        "Twelve printable Christmas party games, including trivia, bingo, and a word scramble, "
        "in sage green for US Letter and A4."
    ),
}

GALLERY_ALT = {
    "images/47-smb-bookkeeping-2027.webp": "2027 small business bookkeeping spreadsheet on a laptop",
    "images/47-smb-bookkeeping-2027-pl.webp": "Monthly profit and loss spreadsheet preview",
    "images/47-smb-bookkeeping-2027-screenshot.webp": "Dashboard tab of the bookkeeping spreadsheet",
    "images/47-smb-bookkeeping-2027-tax.webp": "Quarterly tax set-aside spreadsheet preview",
    "images/46-christmas-party-games.webp": "Christmas party games printable preview",
    "images/46-christmas-party-games-set.webp": "Twelve Christmas party games in the bundle",
    "images/46-christmas-party-games-trivia.webp": "Christmas trivia and movie quiz pages",
    "images/46-christmas-party-games-bingo.webp": "Christmas bingo cards preview",
}


def esc(value):
    return html.escape(value, quote=True)


def price_amount(price):
    return price.replace("$", "").replace(",", "").strip()


def load_products():
    products = json.loads((ROOT / "products.json").read_text())
    by_folder = {item["folder"]: item for item in products}
    missing = [name for name in FEATURED_ORDER if name not in by_folder]
    if missing:
        raise SystemExit(f"Missing featured products: {missing}")
    for item in products:
        image = ROOT / item["image"]
        if not image.exists():
            raise SystemExit(f"Missing image for {item['folder']}: {item['image']}")
        for extra in item.get("gallery") or []:
            if not (ROOT / extra).exists():
                raise SystemExit(f"Missing gallery image: {extra}")
    return products


def slug_for(category):
    for name, slug, _blurb in CATEGORIES:
        if name == category:
            return slug
    raise SystemExit(f"Unknown category: {category}")


def head(title, description, canonical, depth, og_image=OG_IMAGE, og_type="website", extra=""):
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{esc(canonical)}">
  <meta name="theme-color" content="#7E9C8A">
  <meta property="og:site_name" content="{SHOP_NAME}">
  <meta property="og:type" content="{esc(og_type)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(og_image)}">
  <meta property="og:image:alt" content="{SHOP_NAME}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{esc(og_image)}">
  <link rel="icon" href="{prefix}favicon.ico" sizes="32x32">
  <link rel="icon" href="{prefix}brand/logo-512.png" type="image/png">
  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&amp;family=Poppins:ital,wght@0,400;0,500;0,600;1,400&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}css/styles.css">
  {extra}
</head>
"""


def organization_ld():
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SHOP_NAME,
        "url": BASE + "/",
        "logo": BASE + "/brand/logo-512.png",
        "sameAs": [ETSY, PINTEREST],
    }
    return json.dumps(data, indent=2)


def json_ld_block(*objects):
    blocks = []
    for obj in objects:
        if obj is None:
            continue
        if isinstance(obj, str):
            payload = obj
        else:
            payload = json.dumps(obj, indent=2)
        blocks.append(f'<script type="application/ld+json">\n{payload}\n</script>')
    return "\n".join(blocks)


def header(depth, current):
    prefix = "../" * depth
    home = prefix + "index.html"
    shop = prefix + "shop.html"
    about = prefix + "about.html"

    def current_attr(name):
        return ' aria-current="page"' if current == name else ""

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{home}">
      <img src="{prefix}brand/logo.webp" alt="" width="1000" height="1000">
      <span>Sage &amp; Ledger Designs</span>
    </a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="site-nav" aria-label="Primary">
      <a href="{shop}"{current_attr("shop")}>Shop</a>
      <a href="{home}#featured">Featured</a>
      <a href="{about}"{current_attr("about")}>About</a>
      <a href="{home}#free-printable">Free printable</a>
      <a href="{PINTEREST}" target="_blank" rel="noopener">Pinterest<span class="visually-hidden"> (opens in a new tab)</span></a>
      <a class="btn btn-ink btn-small" href="{ETSY}" target="_blank" rel="noopener">Shop on Etsy<span class="visually-hidden"> (opens in a new tab)</span></a>
    </nav>
  </div>
</header>
"""


def footer(depth):
    prefix = "../" * depth
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="{prefix}brand/logo.webp" alt="" width="1000" height="1000">
      <div>
        <strong>Sage &amp; Ledger Designs</strong>
        <p>Digital planners, templates, and prints. Checkout is on Etsy.</p>
      </div>
    </div>
    <nav class="footer-nav" aria-label="Footer">
      <a href="{prefix}shop.html">Shop</a>
      <a href="{prefix}about.html">About</a>
      <a href="{ETSY}" target="_blank" rel="noopener">Etsy shop<span class="visually-hidden"> (opens in a new tab)</span></a>
      <a href="{PINTEREST}" target="_blank" rel="noopener">Pinterest<span class="visually-hidden"> (opens in a new tab)</span></a>
    </nav>
    <p class="legal">© 2026 Sage &amp; Ledger Designs. Listing prices are shown as published on Etsy.</p>
  </div>
</footer>
<script src="{prefix}js/site.js"></script>
"""


def new_tab():
    return '<span class="visually-hidden"> (opens in a new tab)</span>'


def gallery_html(item, depth, gallery_name):
    prefix = "../" * depth
    images = item.get("gallery") or [item["image"]]
    if len(images) == 1:
        alt = GALLERY_ALT.get(images[0], item["short_title"] + " preview")
        return f"""<div class="gallery gallery-single">
  <div class="gallery-stage">
    <img class="slide" src="{prefix}{esc(images[0])}" alt="{esc(alt)}" width="1200" height="900">
  </div>
</div>"""

    radios = []
    slides = []
    thumbs = []
    for index, image in enumerate(images):
        input_id = f"{gallery_name}-{index}"
        alt = GALLERY_ALT.get(image, f"{item['short_title']} preview {index + 1}")
        checked = " checked" if index == 0 else ""
        radios.append(
            f'<input class="gallery-radio" type="radio" name="{esc(gallery_name)}" id="{esc(input_id)}"{checked}>'
        )
        loading = "eager" if index == 0 else "lazy"
        slides.append(
            f'<img class="slide" src="{prefix}{esc(image)}" alt="{esc(alt)}" width="1200" height="900" loading="{loading}" decoding="async">'
        )
        thumbs.append(
            f"""<label for="{esc(input_id)}">
        <img src="{prefix}{esc(image)}" alt="" width="1200" height="900" loading="lazy" decoding="async">
        <span class="visually-hidden">{esc(alt)}</span>
      </label>"""
        )
    return f"""<div class="gallery">
  {chr(10).join(radios)}
  <div class="gallery-stage">
    {chr(10).join(slides)}
  </div>
  <div class="gallery-thumbs" role="group" aria-label="More previews of {esc(item['short_title'])}">
    {chr(10).join(thumbs)}
  </div>
</div>"""


def card_html(item, depth):
    prefix = "../" * depth
    search = " ".join([item["short_title"], item["title"], item["category"], item["price"]])
    return f"""<article class="card" data-product data-category="{esc(item['category'])}" data-search="{esc(search)}">
  <a class="card-main" href="{esc(item['etsy_url'])}" target="_blank" rel="noopener">
    <span class="card-media">
      <img src="{prefix}{esc(item['image'])}" alt="" width="1200" height="900" loading="lazy" decoding="async">
    </span>
    <div class="card-body">
      <span class="pill">{esc(item['category'])}</span>
      <h3>{esc(item['short_title'])}</h3>
      <span class="price-row">
        <span class="price">{esc(item['price'])}</span>
        <span class="etsy-cta">Shop on Etsy{new_tab()}</span>
      </span>
    </div>
  </a>
  <a class="details-link" href="{prefix}products/{esc(item['folder'])}.html">Details<span class="visually-hidden"> for {esc(item['short_title'])}</span></a>
</article>"""


def itemlist_ld(products, name, url):
    elements = []
    for index, item in enumerate(products, start=1):
        elements.append(
            {
                "@type": "ListItem",
                "position": index,
                "url": item["etsy_url"],
                "name": item["short_title"],
                "item": {
                    "@type": "Product",
                    "name": item["title"],
                    "image": f"{BASE}/{item['image']}",
                    "brand": {"@type": "Brand", "name": SHOP_NAME},
                    "offers": {
                        "@type": "Offer",
                        "url": item["etsy_url"],
                        "priceCurrency": "USD",
                        "price": price_amount(item["price"]),
                    },
                },
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "url": url,
        "numberOfItems": len(products),
        "itemListElement": elements,
    }


def product_ld(item):
    images = item.get("gallery") or [item["image"]]
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": item["title"],
        "image": [f"{BASE}/{image}" for image in images],
        "description": item["title"],
        "brand": {"@type": "Brand", "name": SHOP_NAME},
        "category": item["category"],
        "offers": {
            "@type": "Offer",
            "url": item["etsy_url"],
            "priceCurrency": "USD",
            "price": price_amount(item["price"]),
            "availability": "https://schema.org/InStock",
        },
    }


def breadcrumb_ld(item):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Shop", "item": BASE + "/shop.html"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": item["category"],
                "item": BASE + "/shop.html#" + slug_for(item["category"]),
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": item["short_title"],
                "item": BASE + "/products/" + item["folder"] + ".html",
            },
        ],
    }


def page(title, description, canonical, depth, current, main, ld_objects, og_image=OG_IMAGE, og_type="website"):
    extra = json_ld_block(organization_ld(), *ld_objects)
    return (
        head(title, description, canonical, depth, og_image=og_image, og_type=og_type, extra=extra)
        + "<body>\n"
        + header(depth, current)
        + "<main id=\"main\">\n"
        + main
        + "</main>\n"
        + footer(depth)
        + "</body>\n</html>\n"
    )


def render_home(products):
    by_folder = {item["folder"]: item for item in products}
    featured = [by_folder[name] for name in FEATURED_ORDER]
    counts = {}
    for item in products:
        counts[item["category"]] = counts.get(item["category"], 0) + 1

    features = []
    for index, item in enumerate(featured):
        flip = " feature-flip" if index == 1 else ""
        features.append(
            f"""<article class="feature{flip}">
  <div class="feature-gallery">
    {gallery_html(item, 0, "featured-" + item["folder"])}
  </div>
  <div class="feature-copy">
    <p class="eyebrow">{esc(item["category"])}</p>
    <h3>{esc(item["short_title"])}</h3>
    <p class="price">{esc(item["price"])}</p>
    <p class="listing">{esc(FEATURED_COPY[item["folder"]])}</p>
    <div class="feature-actions">
      <a class="btn btn-ink" href="{esc(item["etsy_url"])}" target="_blank" rel="noopener">Shop on Etsy{new_tab()}</a>
      <a class="details-link" href="products/{esc(item["folder"])}.html">Listing details</a>
    </div>
  </div>
</article>"""
        )

    tiles = []
    for name, slug, blurb in CATEGORIES:
        noun = "listing" if counts[name] == 1 else "listings"
        tiles.append(
            f"""<a class="cat-tile" href="shop.html#{esc(slug)}">
  <span class="cat-count">{counts[name]} {noun}</span>
  <h3>{esc(name)}</h3>
  <p>{esc(blurb)}</p>
</a>"""
        )

    hero_links = [
        by_folder["47-smb-bookkeeping-2027"],
        by_folder["05-botanical-wall-art"],
        by_folder["02-excel-budget"],
    ]
    collage = []
    for index, item in enumerate(hero_links):
        loading = "eager" if index == 0 else "lazy"
        priority = ' fetchpriority="high"' if index == 0 else ""
        collage.append(
            f"""<a href="{esc(item["etsy_url"])}" target="_blank" rel="noopener">
  <img src="{esc(item["image"])}" alt="{esc(item["short_title"])}. Shop on Etsy." width="1200" height="900" loading="{loading}" decoding="async"{priority}>
</a>"""
        )

    signup = """<section class="section" id="free-printable">
  <div class="wrap">
    <div class="signup">
      <div>
        <p class="eyebrow">Free printable</p>
        <h2>A free budget printable</h2>
        <p class="lede">A one-page budget sheet for the mailing list.</p>
        <p>The list is not connected yet. Until it is, the button opens the Etsy shop, where the budget planners and spreadsheets are.</p>
      </div>
      <!--
        Kit form slot (#kit-signup, data-kit-form="free-budget-printable").
        When Kit is connected, paste the Kit embed inside #kit-signup
        and remove the .kit-signup-fallback block. Keep this section heading.
      -->
      <div id="kit-signup" class="kit-signup" data-kit-form="free-budget-printable">
        <div class="kit-signup-fallback">
          <div class="kit-field" aria-hidden="true"><span>Email address</span><span class="soon">Soon</span></div>
          <a class="btn btn-ink" href="https://www.etsy.com/shop/SageAndLedgerDesigns" target="_blank" rel="noopener">Visit the Etsy shop<span class="visually-hidden"> (opens in a new tab)</span></a>
          <p class="form-note">No email is collected on this page. This button opens the shop.</p>
        </div>
      </div>
    </div>
  </div>
</section>"""

    main = f"""<section class="hero wrap">
  <div class="hero-copy">
    <p class="eyebrow">Planners · Templates · Prints</p>
    <h1>Sage &amp; Ledger Designs</h1>
    <p class="lede">Calm, simple tools for your money, your time and your home.</p>
    <p>Digital planners, spreadsheets, dashboard kits, and printable art from the Etsy shop SageAndLedgerDesigns. {len(products)} listings, with the real price and photo on every card.</p>
    <div class="hero-actions">
      <a class="btn btn-ink" href="shop.html">Shop the collection</a>
      <a class="btn btn-ghost" href="{ETSY}" target="_blank" rel="noopener">Shop on Etsy{new_tab()}</a>
    </div>
  </div>
  <div class="hero-collage">
    {chr(10).join(collage)}
  </div>
</section>
<section class="section" id="featured">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Featured</p>
        <h2>Start here</h2>
      </div>
      <p>Two listings from the shop, with the preview photos from each one.</p>
    </div>
    <div class="feature-list">
      {chr(10).join(features)}
    </div>
  </div>
</section>
<section class="section" id="categories">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">The collection</p>
        <h2>Browse by category</h2>
      </div>
    </div>
    <div class="cat-grid">
      {chr(10).join(tiles)}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">How it works</p>
        <h2>Choose it. Buy it on Etsy.</h2>
      </div>
    </div>
    <div class="steps">
      <article class="step"><span>01</span><h3>Pick a listing</h3><p>Planners, spreadsheets, dashboard kits, wall art, and party printables.</p></article>
      <article class="step"><span>02</span><h3>Open it on Etsy</h3><p>Every card goes to that exact listing. Checkout stays on Etsy.</p></article>
      <article class="step"><span>03</span><h3>Download the files</h3><p>Delivery happens through Etsy after purchase.</p></article>
    </div>
  </div>
</section>
{signup}
"""
    title = "Sage & Ledger Designs | Planners, Templates & Prints"
    description = (
        "Calm digital downloads from Sage & Ledger Designs: printable planners, Excel templates, "
        "Power BI kits, wall art, and party printables. Shop the listings on Etsy."
    )
    featured_list = itemlist_ld(featured, "Featured listings", BASE + "/#featured")
    return page(title, description, BASE + "/", 0, "home", main, [featured_list])


def render_shop(products):
    grouped = {name: [] for name, _slug, _blurb in CATEGORIES}
    for item in products:
        grouped[item["category"]].append(item)

    sections = []
    for name, slug, blurb in CATEGORIES:
        cards = "\n".join(card_html(item, 0) for item in grouped[name])
        sections.append(
            f"""<section class="category-block" id="{esc(slug)}" data-category-section>
  <h2>{esc(name)}</h2>
  <p class="category-blurb">{esc(blurb)}</p>
  <div class="grid">
    {cards}
  </div>
</section>"""
        )

    chips = ['<button class="chip" type="button" data-filter="all" data-slug="all" aria-pressed="true">All</button>']
    for name, slug, _blurb in CATEGORIES:
        chips.append(
            f'<button class="chip" type="button" data-filter="{esc(name)}" data-slug="{esc(slug)}" aria-pressed="false">{esc(name)}</button>'
        )

    main = f"""<section class="shop-intro wrap">
  <p class="eyebrow">The shop</p>
  <h1>All listings</h1>
  <p class="lede">Real photos. Real prices. Each card opens its Etsy listing.</p>
</section>
<div class="shop-tools" data-shop>
  <div class="wrap">
    <form role="search" action="shop.html">
      <label class="search-label" for="product-search">Search listings</label>
      <input class="search-input" id="product-search" data-search type="search" name="q" placeholder="Search planners, budgets, prints" autocomplete="off">
    </form>
    <div class="filters" role="group" aria-label="Filter by category">
      {chr(10).join(chips)}
    </div>
    <p class="result-count" data-count aria-live="polite"></p>
  </div>
</div>
<div class="wrap">
  {chr(10).join(sections)}
  <p class="empty" data-empty hidden>No listings match that search.</p>
</div>
"""
    title = "Shop all listings | Sage & Ledger Designs"
    description = (
        f"Browse {len(products)} Sage & Ledger Designs listings: planners, Excel templates, "
        "Power BI kits, wall art, party printables, and small business templates. Each card links to Etsy."
    )
    return page(
        title,
        description,
        BASE + "/shop.html",
        0,
        "shop",
        main,
        [itemlist_ld(products, "Sage & Ledger Designs listings", BASE + "/shop.html")],
    )


def render_about(products):
    counts = {}
    for item in products:
        counts[item["category"]] = counts.get(item["category"], 0) + 1
    items = []
    for name, slug, blurb in CATEGORIES:
        items.append(
            f"""<a href="shop.html#{esc(slug)}">
  <h3>{esc(name)}</h3>
  <p>{counts[name]} listings. {esc(blurb)}</p>
</a>"""
        )
    main = f"""<section class="about-hero wrap">
  <p class="eyebrow">About</p>
  <h1>A quiet shop for practical files.</h1>
  <div class="prose">
    <p class="lede">Sage &amp; Ledger Designs is an Etsy shop of digital downloads for money, time, and home.</p>
    <p>The collection covers printable planners, Excel and Google Sheets templates, Power BI dashboard kits, wall art, party printables, and small business files. The palette stays in sage, sand, and terracotta.</p>
    <p>This site is a catalog. The Etsy listing is where you buy, and where the file details for that item live.</p>
  </div>
  <figure class="banner">
    <img src="brand/header.webp" alt="Sage and Ledger Designs. Planners, templates, and prints. Calm, simple tools for your money, your time and your home." width="1500" height="500">
  </figure>
</section>
<section class="section wrap">
  <h2>What you’ll find</h2>
  <div class="about-list">
    {chr(10).join(items)}
  </div>
</section>
<section class="section wrap">
  <div class="prose">
    <h2>Buying a download</h2>
    <p>Pick a listing here, then open it on Etsy. Checkout and delivery stay on Etsy. Questions about a file belong on that listing, where the shop can answer them.</p>
    <p><a class="btn btn-ink" href="{ETSY}" target="_blank" rel="noopener">Visit the Etsy shop{new_tab()}</a></p>
    <h2>Pinterest</h2>
    <p>More of the collection is pinned on <a href="{PINTEREST}" target="_blank" rel="noopener">Pinterest{new_tab()}</a>.</p>
  </div>
</section>
"""
    title = "About the shop | Sage & Ledger Designs"
    description = (
        "Sage & Ledger Designs makes calm digital downloads for home and small-business organization. "
        "Browse the catalog, then buy on Etsy."
    )
    return page(title, description, BASE + "/about.html", 0, "about", main, [])


def render_product(item, products):
    related = [other for other in products if other["category"] == item["category"] and other["folder"] != item["folder"]][:3]
    related_html = "\n".join(card_html(other, 1) for other in related)
    slug = slug_for(item["category"])
    canonical = f"{BASE}/products/{item['folder']}.html"
    og_image = f"{BASE}/{item['image']}"
    main = f"""<div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb">
    <a href="../index.html">Home</a>
    <span aria-hidden="true">/</span>
    <a href="../shop.html">Shop</a>
    <span aria-hidden="true">/</span>
    <a href="../shop.html#{esc(slug)}">{esc(item["category"])}</a>
    <span aria-hidden="true">/</span>
    <span aria-current="page">{esc(item["short_title"])}</span>
  </nav>
  <article class="product">
    {gallery_html(item, 1, "product-" + item["folder"])}
    <div class="product-info">
      <p class="eyebrow">{esc(item["category"])}</p>
      <h1>{esc(item["short_title"])}</h1>
      <p class="price">{esc(item["price"])}</p>
      <p class="listing">{esc(item["title"])}</p>
      <a class="btn btn-ink" href="{esc(item["etsy_url"])}" target="_blank" rel="noopener">Shop on Etsy{new_tab()}</a>
      <p class="fine">Purchase and download happen on Etsy. The price and title here match that listing.</p>
    </div>
  </article>
  <section class="section">
    <div class="section-head">
      <h2>More in {esc(item["category"])}</h2>
      <a href="../shop.html#{esc(slug)}">See the category</a>
    </div>
    <div class="grid">
      {related_html}
    </div>
  </section>
</div>
"""
    title = f"{item['short_title']} | Sage & Ledger Designs"
    description = f"{item['title']} Price {item['price']} on Etsy."
    if len(description) > 170:
        description = item["title"][:157].rstrip() + "..."
    return page(
        title,
        description,
        canonical,
        1,
        "product",
        main,
        [product_ld(item), breadcrumb_ld(item)],
        og_image=og_image,
        og_type="product",
    )


def render_404():
    title = "Page not found | Sage & Ledger Designs"
    description = "That page is not on the Sage & Ledger Designs catalog."
    main = """<section class="wrap page-404">
  <p class="eyebrow">404</p>
  <h1>That page isn’t here.</h1>
  <p class="lede">The catalog is still one click away.</p>
  <div class="hero-actions">
    <a class="btn btn-ink" href="index.html">Back home</a>
    <a class="btn btn-ghost" href="shop.html">Browse the shop</a>
  </div>
</section>
"""
    extra = json_ld_block(organization_ld())
    html_doc = head(title, description, BASE + "/404.html", 0, extra=extra)
    html_doc = html_doc.replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="noindex">')
    return html_doc + "<body>\n" + header(0, "") + '<main id="main">\n' + main + "</main>\n" + footer(0) + "</body>\n</html>\n"


def render_sitemap(products):
    urls = [
        BASE + "/",
        BASE + "/shop.html",
        BASE + "/about.html",
    ]
    urls.extend(f"{BASE}/products/{item['folder']}.html" for item in products)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{esc(url)}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    products = load_products()
    (ROOT / "index.html").write_text(render_home(products))
    (ROOT / "shop.html").write_text(render_shop(products))
    (ROOT / "about.html").write_text(render_about(products))
    (ROOT / "404.html").write_text(render_404())
    product_dir = ROOT / "products"
    product_dir.mkdir(exist_ok=True)
    for item in products:
        (product_dir / f"{item['folder']}.html").write_text(render_product(item, products))
    (ROOT / "sitemap.xml").write_text(render_sitemap(products))
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://shawnroy1988.github.io/sageandledgerdesigns/sitemap.xml\n"
    )
    (ROOT / ".nojekyll").write_text("")
    print(f"Rendered {len(products)} products and site pages.")


if __name__ == "__main__":
    main()
