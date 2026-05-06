# VOICEBOX Search Demo

Static in-browser search for monthly DCSA / Voice of Industry newsletters, intended for GitHub Pages hosting.

Live site: https://4l3xv33.github.io/voicebox-search/

The site uses `lunr.min.js` in the browser and a generated `documents.js` file as its local search index. Each search result links to the corresponding PDF in `voi_newsletters/`.

## Files

- `index.html`: the static search UI
- `lunr.min.js`: Lunr client-side search library
- `documents.js`: generated search data consumed by the page
- `voi_newsletters.tar`: source archive of newsletter PDFs
- `voi_newsletters/`: extracted newsletter PDFs served by the site
- `scripts/build_documents.py`: extracts PDF text and rebuilds `documents.js`

## Rebuild The Search Index

Requirements:

- `python3`
- `pdftotext` (from Poppler)

Run:

```bash
python3 scripts/build_documents.py
```

That script:

1. Extracts `voi_newsletters.tar`
2. Reads each PDF with `pdftotext -layout`
3. Generates `documents.js` with filename, title, link, and searchable text

## Notes

- Search is entirely client-side.
- The index includes newsletter titles, filenames, and extracted PDF text.
- The site is intended to be published as a static GitHub Pages site.
- If you replace or update the PDF archive, rerun `python3 scripts/build_documents.py`.
