// Build a local preview of the design deck, render each slide to PNG, and list boxes that cross the margins.
//
// Usage:
//   node docs/design/tools/preview-deck.js <out dir>
//
// Images on the slides point to files uploaded to the artifact (/_blob/<id>).
// docs/design/deck/blobs.json maps each id to a file in docs/design/deck/img/.
// The slide format drops default margins and draws its own table rules; the preview copies that.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import path from 'node:path'

const require = createRequire(import.meta.url)
const { chromium } = require('playwright')

const outDir = process.argv[2]
if (!outDir) {
  console.error('usage: node preview-deck.js <out dir>')
  process.exit(1)
}
const deckDir = path.resolve(
  path.dirname(new URL(import.meta.url).pathname),
  '../deck',
)
const deck = JSON.parse(
  readFileSync(path.join(deckDir, 'project/deck.json'), 'utf8'),
)
const css = readFileSync(path.join(deckDir, 'project/deck.css'), 'utf8')
const blobs = JSON.parse(readFileSync(path.join(deckDir, 'blobs.json'), 'utf8'))

let body = ''
for (const id of deck.order) {
  let html = readFileSync(
    path.join(deckDir, `project/slides/${id}.html`),
    'utf8',
  )
  html = html.replace(/\/_blob\/([0-9a-f]{32})/g, (m, blob) =>
    blobs[blob] ? `file://${path.join(deckDir, 'img', blobs[blob])}` : m,
  )
  body += html
}
const links = Object.values(deck.faces)
  .map((f) => `<link rel="stylesheet" href="${f.href}">`)
  .join('')
const reset = `
body { margin: 0; counter-reset: page; background: #888; }
section { width: 1920px; height: 1080px; position: relative; box-sizing: border-box; overflow: hidden; margin: 0 0 20px; }
aside { display: none; }
p, h1, h2, h3, ul, ol, table { margin: 0; }
table { border-collapse: collapse; width: 100%; }
td, th { padding: .35em .6em; text-align: left; vertical-align: top; border-top: 1px solid rgba(128, 128, 128, .35); }
* { animation: none !important; }`
mkdirSync(outDir, { recursive: true })
const file = path.join(outDir, 'deck-preview.html')
writeFileSync(
  file,
  `<!doctype html><html lang="ja"><head><meta charset="utf-8">${links}<style>${css}\n${reset}</style></head><body>${body}</body></html>`,
)

const browser = await chromium.launch()
const tab = await browser.newPage({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 0.5,
})
await tab.goto(`file://${file}`, { waitUntil: 'networkidle' })
await tab.evaluate(() => document.fonts.ready)
await tab.waitForTimeout(600)

// Boxes past the 128 px margins (the footer row is allowed below).
const report = await tab.$$eval('section', (sections) =>
  sections.map((sec) => {
    const r0 = sec.getBoundingClientRect()
    const bad = []
    for (const el of sec.querySelectorAll('*')) {
      if (el.closest('.foot') || el.tagName === 'ASIDE') continue
      const r = el.getBoundingClientRect()
      if (!r.width) continue
      const right = r.right - r0.left
      const bottom = r.bottom - r0.top
      if (right > 1796 || bottom > 956)
        bad.push(
          `${el.tagName}.${el.className} ${Math.round(right)}x${Math.round(bottom)}`,
        )
    }
    return `${sec.id}: ${bad.slice(0, 4).join(' | ') || 'ok'}`
  }),
)
console.log(report.join('\n'))
for (const id of deck.order) {
  await tab
    .locator(`#${id}`)
    .screenshot({ path: path.join(outDir, `slide-${id}.png`) })
}
console.log('wrote slide images to', outDir)
await browser.close()
