"""HTML + theme CSS -> print-grade PDF via WeasyPrint."""

from __future__ import annotations

from pathlib import Path

import weasyprint


def render_pdf(
    html: str,
    css: str,
    out_path: str | Path,
    *,
    pdf_ua: bool = True,
    base_url: str | Path | None = None,
) -> int:
    """Render HTML+CSS to PDF. Returns number of pages."""
    stylesheet = weasyprint.CSS(string=css)
    document = weasyprint.HTML(string=html, base_url=str(base_url) if base_url else None).render(
        stylesheets=[stylesheet]
    )
    options = {"pdf_variant": "pdf/ua-1"} if pdf_ua else {}
    document.write_pdf(str(out_path), **options)
    return len(document.pages)


def compress_pdf(path: str | Path, max_side: int = 2000, quality: int = 88) -> int:
    """Re-encode embedded raster images: downscale over-large ones and re-encode.

    Returns bytes saved (0 when there is nothing to compress). Keeps the file
    untouched when the re-encoded image is not smaller than the original.
    """
    import io

    import pymupdf
    from PIL import Image

    src = Path(path)
    before = src.stat().st_size
    doc = pymupdf.open(src)
    changed = 0
    seen: set[int] = set()
    for pno in range(doc.page_count):
        for img in doc.get_page_images(pno, full=True):
            xref = img[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                info = doc.extract_image(xref)
                im = Image.open(io.BytesIO(info["image"]))
                im.load()
            except Exception:
                continue
            w, h = im.size
            oversized = max(w, h) > max_side or w * h > 4_000_000
            if not oversized and info["ext"].lower() in ("jpeg", "jpg"):
                continue
            if oversized:
                im.thumbnail((max_side, max_side), Image.LANCZOS)
            if "A" in im.mode:
                buf = io.BytesIO()
                im.save(buf, "PNG", optimize=True)
                new_bytes: bytes = buf.getvalue()
                filt = "[/FlateDecode]"
            else:
                buf = io.BytesIO()
                im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
                new_bytes = buf.getvalue()
                filt = "[/DCTDecode]"
            if len(new_bytes) >= len(info["image"]):
                continue
            doc.update_stream(xref, new_bytes, compress=0)
            doc.xref_set_key(xref, "Filter", filt)
            if filt == "[/DCTDecode]":
                doc.xref_set_key(xref, "ColorSpace", "/DeviceRGB")
            doc.xref_set_key(xref, "DecodeParms", "<< >>")
            doc.xref_set_key(xref, "Width", str(im.width))
            doc.xref_set_key(xref, "Height", str(im.height))
            changed += 1
    if not changed:
        doc.close()
        return 0
    tmp = src.with_suffix(".imprint-compress.pdf")
    doc.save(str(tmp), garbage=3, deflate=True)
    doc.close()
    saved = before - tmp.stat().st_size
    if saved > 0:
        tmp.replace(src)
    else:
        tmp.unlink(missing_ok=True)
    return max(saved, 0)
