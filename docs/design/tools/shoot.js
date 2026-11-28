// Render elements of an HTML page to image files with Playwright.
//
// Usage:
//   node docs/design/tools/shoot.js <page.html> <out dir> [options] [id ...]
//
// Options:
//   --scale <n>      device scale factor (default 2)
//   --transparent    keep the page background out of the image
//   --webp           write WebP (encoded in the browser) instead of PNG
//   --trim           crop to the visible content (needs --transparent)
//   --prefix <text>  prefix for the file names (the element id follows)
//
// Without ids, every element with the class "shot" is rendered.

import { mkdirSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import path from 'node:path'

const require = createRequire(import.meta.url)
const { chromium } = require('playwright')

const args = process.argv.slice(2)
const positional = []
const opts = {
  scale: 2,
  transparent: false,
  webp: false,
  trim: false,
  prefix: '',
}
for (let i = 0; i < args.length; i++) {
  const a = args[i]
  if (a === '--scale') opts.scale = Number(args[++i])
  else if (a === '--prefix') opts.prefix = args[++i]
  else if (a === '--transparent') opts.transparent = true
  else if (a === '--webp') opts.webp = true
  else if (a === '--trim') opts.trim = true
  else positional.push(a)
}
const [page, outDir, ...ids] = positional
if (!page || !outDir) {
  console.error('usage: node shoot.js <page.html> <out dir> [options] [id ...]')
  process.exit(1)
}

// Re-encode a PNG in the browser: optional crop to non-transparent pixels, optional WebP.
async function encode(tab, png) {
  const dataUrl = await tab.evaluate(
    async ({ b64, webp, trim }) => {
      const img = new Image()
      img.src = `data:image/png;base64,${b64}`
      await img.decode()
      let [x0, y0, x1, y1] = [0, 0, img.width, img.height]
      const full = document.createElement('canvas')
      full.width = img.width
      full.height = img.height
      const fctx = full.getContext('2d')
      fctx.drawImage(img, 0, 0)
      if (trim) {
        const px = fctx.getImageData(0, 0, img.width, img.height).data
        ;[x0, y0, x1, y1] = [img.width, img.height, 0, 0]
        for (let y = 0; y < img.height; y++) {
          for (let x = 0; x < img.width; x++) {
            if (px[(y * img.width + x) * 4 + 3] > 8) {
              if (x < x0) x0 = x
              if (y < y0) y0 = y
              if (x + 1 > x1) x1 = x + 1
              if (y + 1 > y1) y1 = y + 1
            }
          }
        }
      }
      const out = document.createElement('canvas')
      out.width = x1 - x0
      out.height = y1 - y0
      out
        .getContext('2d')
        .drawImage(
          full,
          x0,
          y0,
          out.width,
          out.height,
          0,
          0,
          out.width,
          out.height,
        )
      return out.toDataURL(webp ? 'image/webp' : 'image/png', 0.9)
    },
    { b64: png.toString('base64'), webp: opts.webp, trim: opts.trim },
  )
  return Buffer.from(dataUrl.split(',')[1], 'base64')
}

const browser = await chromium.launch()
const tab = await browser.newPage({
  viewport: { width: 1800, height: 1200 },
  deviceScaleFactor: opts.scale,
})
await tab.goto(`file://${path.resolve(page)}`, { waitUntil: 'networkidle' })
await tab.evaluate(() => document.fonts.ready)
if (opts.transparent)
  await tab.addStyleTag({
    content: 'html, body { background: transparent !important; }',
  })
await tab.waitForTimeout(500)

const targets = ids.length
  ? ids
  : await tab.$$eval('.shot', (els) => els.map((e) => e.id))
mkdirSync(outDir, { recursive: true })
for (const id of targets) {
  const png = await tab
    .locator(`#${id}`)
    .screenshot({ omitBackground: opts.transparent })
  const buf = opts.webp || opts.trim ? await encode(tab, png) : png
  const file = path.join(
    outDir,
    `${opts.prefix}${id}.${opts.webp ? 'webp' : 'png'}`,
  )
  writeFileSync(file, buf)
  console.log('wrote', file)
}
await browser.close()
