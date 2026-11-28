# 事業コンセプト提案書 (改訂版)

HINAMI の事業コンセプトを、スライド 20 枚 (付録 1 枚を含む) にまとめたもの。2026-11-28 に、UX の決定、6 つの視点のレビュー、最先端の事例と手法の調査から採った 3 つの施策を反映して書き直した。構想段階の版は [`../references/slides/concept-deck/`](../references/slides/concept-deck/) に残している。

- オンライン版 (claude.ai のアーティファクト。所有者のみ閲覧可): https://claude.ai/artifact/FevqCwUA1VGmWV7FGanJuT
- 構想段階の版のアーティファクトは、別のもの (https://claude.ai/artifact/JRg5GNcNXj2hpbVMBpKpKt) としてそのまま残している
- 中身の正は [`../concept.md`](../concept.md) と [`../ux/`](../ux/recording.md)。決まりが変わったら、提案書も直す

## ファイル

| パス                       | 中身                                                       |
| -------------------------- | ---------------------------------------------------------- |
| `project/deck.json`        | タイトル、スライドの順番、章立て、書体                     |
| `project/deck.css`         | 全スライド共通のスタイル (構想段階の版と同じ)              |
| `project/slides/<id>.html` | 1 枚 1 ファイル。1920×1080 のキャンバス                    |
| `view.html`                | 手元で確かめるための簡易ビューア。矢印や図形は正しく出ない |

## 手元で見る

`.claude/launch.json` の `concept-deck` を起動し、`http://127.0.0.1:4174/view.html` を開く。

## 直して公開する

ここのファイルを直し、アーティファクトに公開し直す (Artifact ツールで、`root` をこのフォルダにする)。公開した版とここのファイルをそろえておく。
