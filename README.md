# Sage & Ledger Designs

Catalog site for the Etsy shop [SageAndLedgerDesigns](https://www.etsy.com/shop/SageAndLedgerDesigns). It is plain static HTML, CSS, and JavaScript. Open `index.html` in a browser, or from this folder run:

```bash
python3 -m http.server
```

Live site: https://shawnroy1988.github.io/sageandledgerdesigns/

## Pages

- `index.html` — home, featured listings, categories, free-printable slot
- `shop.html` — all 47 listings, with category tabs and search
- `about.html` — what the shop sells and how buying works
- `products/*.html` — one page per listing
- `sitemap.xml`, `robots.txt`, `.nojekyll`

Prices, titles, photos, and Etsy URLs come from `products.json`. Product cards open the matching Etsy listing in a new tab.

## Free printable / Kit

The home page has a signup slot, `#kit-signup` (`data-kit-form="free-budget-printable"`). No email provider is connected, so the button currently opens the Etsy shop and the page does not collect addresses.

When Kit is ready, paste the Kit embed inside `#kit-signup` and remove the `.kit-signup-fallback` block. The heading above the slot can stay.

## Regenerating HTML

After editing `products.json`:

```bash
python3 scripts/render_site.py
```

The published site does not need that step.
