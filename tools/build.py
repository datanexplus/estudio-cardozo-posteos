#!/usr/bin/env python3
"""Genera las imágenes de posteos de Estudio Cardozo a partir de un lote JSON.

Uso:
    python3 tools/build.py posteos/2026-11/lote.json            # todos los posteos del lote
    python3 tools/build.py posteos/2026-11/lote.json 03-iva     # solo algunos ids

Cada imagen se guarda junto al lote como <id>.png (1080×1350 feed, 1080×1920 historia).
Requiere: pip install playwright && python3 -m playwright install chromium
"""
import html, json, sys
from pathlib import Path

from playwright.sync_api import sync_playwright

TOOLS = Path(__file__).resolve().parent
MARCA = TOOLS / "marca"
FONTS = TOOLS / "fonts"
REPO_RAW = "https://raw.githubusercontent.com/datanexplus/estudio-cardozo-posteos/main"

tokens = json.loads((MARCA / "tokens.json").read_text())


def _vars(theme):
    out = []
    for c in tokens["color"]["tokens"]:
        v = c["value"] if isinstance(c["value"], str) else c["value"].get(theme, c["value"]["light"])
        out.append(f"--{c['name']}:{v};")
    return "".join(out)


def _css():
    css = f"""
@font-face{{font-family:Newsreader;src:url({(FONTS/'newsreader-latin-opsz-normal.woff2').as_uri()}) format('woff2');font-weight:200 800;font-style:normal}}
@font-face{{font-family:Newsreader;src:url({(FONTS/'newsreader-latin-opsz-italic.woff2').as_uri()}) format('woff2');font-weight:200 800;font-style:italic}}
@font-face{{font-family:Manrope;src:url({(FONTS/'manrope-latin-wght-normal.woff2').as_uri()}) format('woff2');font-weight:200 800}}
:root,[data-theme=light]{{{_vars('light')}}}[data-theme=dark]{{{_vars('dark')}}}:root{{"""
    for fam in ("spacing", "radius"):
        for x in tokens[fam]["tokens"]:
            css += f"--{x['name']}:{x['value']};"
    for k, v in tokens["type"]["families"].items():
        css += f"--font-{k}:{v};"
    css += "}"
    for g in tokens["type"]["groups"]:
        for s in g["styles"]:
            css += (f".{s['name']}{{font-family:var(--font-{g['family']});font-size:{s['fontSize']};"
                    f"line-height:{s['lineHeight']};font-weight:{s['fontWeight']};"
                    + (f"letter-spacing:{s['letterSpacing']};" if "letterSpacing" in s else "")
                    + (f"font-style:{s['fontStyle']};" if "fontStyle" in s else "") + "}")
    css += (MARCA / "bundle.css").read_text()
    css += """body{margin:0}.ec-canvas{transform:none}
.ec-cal{list-style:none;padding:0;margin-top:var(--space-5);display:flex;flex-direction:column}
.ec-cal li{display:grid;grid-template-columns:260px 1fr;gap:var(--space-4);align-items:baseline;padding:var(--space-4) 0;border-bottom:2px solid var(--linea)}
.ec-cal .f{font-family:var(--font-sans);font-weight:800;font-size:56px;line-height:1;color:var(--oro-texto);font-variant-numeric:tabular-nums}
.ec-cal .q{display:flex;flex-direction:column;gap:4px}
"""
    return css


CSS = _css()
# Texto del lote: se escapa salvo los campos que admiten <b>…</b> (items, intro, body).
e = html.escape


def rich(s):
    return e(s).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")


def pie(texto, theme):
    iso = "isotipo-blanco" if theme == "dark" else "isotipo-oro"
    return f'<div class="ec-pie"><p class="body-fuerte">{e(texto)}</p><img src="{(MARCA/(iso+".png")).as_uri()}" alt=""></div>'


def kicker(k):
    return f'<p class="ec-kicker etiqueta"><span class="ec-rombo"></span>{e(k)}</p>'


def t_explicado(p):
    theme = p.get("theme", "light")
    lis = "".join(f"<li><span>{rich(i)}</span></li>" for i in p.get("items", []))
    intro = f'<p class="body" style="margin-top:var(--space-5);max-width:900px">{rich(p["intro"])}</p>' if p.get("intro") else ""
    return (f'<div class="ec-canvas post" data-theme="{theme}">{kicker(p["kicker"])}'
            f'<h1 class="ec-title display">{e(p["title"])}</h1>{intro}'
            f'<ul class="ec-lista body" style="margin-top:var(--space-5)">{lis}</ul>{pie(p["cta"], theme)}</div>')


def t_dato(p):
    fuente = f'<p class="chico ec-muted" style="margin-top:var(--space-3)">{e(p["fuente"])}</p>' if p.get("fuente") else ""
    return (f'<div class="ec-canvas post" data-theme="light">{kicker(p["kicker"])}'
            f'<h1 class="ec-title display">{e(p["title"])}</h1>'
            f'<div class="ec-dato" style="margin-top:var(--space-5)"><span class="cifra">{e(p["cifra"])}</span>'
            f'<span class="h2" style="padding-bottom:24px">{e(p.get("unidad", ""))}</span></div>'
            f'<p class="body" style="margin-top:var(--space-5)">{rich(p["body"])}</p>{fuente}{pie(p["cta"], "light")}</div>')


def t_calendario(p):
    rows = "".join(
        f'<li><span class="f">{e(r["fecha"])}</span><span class="q"><span class="body-fuerte">{e(r["que"])}</span>'
        + (f'<span class="chico ec-muted">{e(r["detalle"])}</span>' if r.get("detalle") else "")
        + "</span></li>" for r in p["rows"][:6])
    nota = f'<p class="chico ec-muted" style="margin-top:var(--space-4)">{e(p["nota"])}</p>' if p.get("nota") else ""
    return (f'<div class="ec-canvas post" data-theme="light">{kicker(p["kicker"])}'
            f'<h1 class="ec-title h1">{e(p["title"])}</h1><ul class="ec-cal">{rows}</ul>{nota}{pie(p["cta"], "light")}</div>')


def t_novedad(p):
    lis = "".join(f"<li><span>{rich(i)}</span></li>" for i in p.get("items", []))
    fuente = f'<p class="chico ec-muted" style="margin-top:var(--space-5)">{e(p["fuente"])}</p>' if p.get("fuente") else ""
    return (f'<div class="ec-canvas post" data-theme="light"><div class="ec-bloque-noche" data-theme="dark">{kicker(p["kicker"])}'
            f'<h1 class="ec-title display">{e(p["title"])}</h1></div>'
            f'<ul class="ec-lista body" style="margin-top:var(--space-6)">{lis}</ul>{fuente}{pie(p["cta"], "light")}</div>')


def t_historia(p):
    return (f'<div class="ec-canvas story" data-theme="dark" style="align-items:center;justify-content:center;text-align:center;gap:var(--space-6)">'
            f'<img src="{(MARCA/"logo-completo-blanco.png").as_uri()}" style="width:600px;height:auto" alt="">'
            f'<p class="h1" style="max-width:860px">{e(p.get("frase", "Tu estudio contable de confianza, siempre a un mensaje de distancia."))}</p>'
            f'<span class="ec-wa body-fuerte">Escribinos por WhatsApp</span>'
            f'<p class="chico ec-muted">Fray Santa María de Oro 985, Cipolletti<br>Lunes a viernes de 9 a 15 h</p></div>')


TEMPLATES = {"explicado": t_explicado, "dato": t_dato, "calendario": t_calendario,
             "novedad": t_novedad, "historia": t_historia}


def main():
    lote_path = Path(sys.argv[1]).resolve()
    only = set(sys.argv[2:])
    lote = json.loads(lote_path.read_text())
    out_dir = lote_path.parent
    rel = out_dir.relative_to(TOOLS.parent).as_posix()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for p in lote["posteos"]:
            if only and p["id"] not in only:
                continue
            story = p["template"] == "historia"
            w, h = (1080, 1920) if story else (1080, 1350)
            doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{TEMPLATES[p["template"]](p)}</body></html>'
            tmp = out_dir / f".{p['id']}.html"
            tmp.write_text(doc)
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(tmp.as_uri())
            page.wait_for_timeout(500)
            page.screenshot(path=str(out_dir / f"{p['id']}.png"))
            page.close()
            tmp.unlink()
            print(f"{p['id']}.png  →  {REPO_RAW}/{rel}/{p['id']}.png")
        browser.close()


if __name__ == "__main__":
    main()
