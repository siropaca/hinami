# デザインの道具

画面イメージ・ロゴ・スライドを画像にして確かめるための道具。デザインの資料を直したときに、スライドの画像を同じ手順で作り直せるように置いている。

## 要るもの

- Node 24 以上 (リポジトリと同じ)
- Playwright と Chromium。リポジトリの依存には入れていない (入れるかは別に決める)。クラウドの作業環境には最初から入っている。手元で使うときは、リポジトリの外で入れる
- 画面イメージの写真 (Unsplash) と書体 (Google Fonts) はネットから読むので、つながっている環境で動かす

## 道具

| ファイル          | 中身                                                                      |
| ----------------- | ------------------------------------------------------------------------- |
| `shoot.js`        | HTML の要素を画像にする。倍率、透過、WebP、余白の切り詰めを選べる         |
| `preview-deck.js` | スライドを手元で画像にし、余白 (128px) からはみ出す箱を一覧にする         |
| `logo-shots.html` | ロゴのスライド用の画像を撮るためのページ (`../logo/` の SVG を並べている) |

## スライドの画像を作り直す

画面イメージ (`../screens/index.html`) を直したとき。影の余白ごと載せるので、切り詰めない。

```bash
node docs/design/tools/shoot.js docs/design/screens/index.html docs/design/deck/img --transparent --webp home-light home-dark detail-light calendar-light ranking-dark achievements-light saved-dark camera
```

印の画像。1 つずつ切り詰める。

```bash
node docs/design/tools/shoot.js docs/design/screens/index.html docs/design/deck/img --transparent --webp --trim stamp-ink stamp-kind stamp-shop stamp-land stamp-off
```

ロゴ (`../logo/`) を直したとき。先に `../logo/build.py` で SVG を書き出し直してから撮る。

```bash
node docs/design/tools/shoot.js docs/design/tools/logo-shots.html docs/design/deck/img --transparent --webp --trim --prefix logo-
```

`logo-explored.webp` (検討して外した形) は、作り直さない記録の画像。

## スライドを手元で確かめる

```bash
node docs/design/tools/preview-deck.js /tmp/hinami-deck
```

各スライドを `slide-<id>.png` に書き出し、余白からはみ出す箱を一覧にする。スライドの形式に合わせて、段落の既定の余白を消し、表の罫を引いて表示する。見た目はアーティファクトの表示に近いが、行の折り返しなどは少し違うことがある。

## アーティファクトに上げ直す

スライドの画像は、アーティファクトに上げた画像 (`/_blob/<id>`) を指している。画像を作り直したら、次の順で差し替える。

1. 作り直した画像をアーティファクトに上げる (Artifact ツールの `asset: true`)
2. 返ってきた番号で、スライドの `src` を差し替える
3. [`../deck/blobs.json`](../deck/blobs.json) の番号とファイル名の対応を直す (`preview-deck.js` が使う)
4. 直したスライドを公開し直す ([`../deck/README.md`](../deck/README.md))
