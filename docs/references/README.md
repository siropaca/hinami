# 参考資料

構想段階で作ったスライドの元ファイル。編集はせず、参照用として残す。

| パス | 中身 |
|---|---|
| `slides/concept-deck/` | 事業コンセプト提案書 (16 枚) |
| `slides/design-deck/` | デザインの方向性 (8 枚) |
| `slides/*/view.html` | ブラウザで開けば全スライドを縦に並べて見られる簡易ビューア |

元ファイルの形式:

- `deck.json`: タイトル、スライドの順番 (`order`)、章立て、フォント
- `deck.css`: 全スライド共通のスタイル
- `slides/<id>.html`: 1 枚 1 ファイル。`<section>` 1 つで、1920×1080 のキャンバス
- `<x-shape>` や `<x-icon>` は元のスライドツール独自の要素。`view.html` では簡易表示になり、矢印やアイコンは正しく出ない

オンライン版 (claude.ai のアーティファクト。所有者のみ閲覧可):

- 事業コンセプト提案書: https://claude.ai/artifact/JRg5GNcNXj2hpbVMBpKpKt
- デザインの方向性: https://claude.ai/artifact/PYSNWeWn99ZucWaDkoypho
