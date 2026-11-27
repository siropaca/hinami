# 0002. PHASE 1 は Expo のアプリを TestFlight で使う

- 状態: 採用
- 日付: 2026-11-27

## 背景

PHASE 1 では、作り手が 4 週間、覚えておきたい食をすべて記録する。そのあと、家族や知り合いに使ってもらう限定テストを挟む ([`../concept.md`](../concept.md))。

2026-11-27 のレビューで、web のプロトタイプでは PHASE 1 の記録ができないと指摘された ([`../reviews/2026-11-27-review.md`](../reviews/2026-11-27-review.md))。

- 写真の位置、端末への保存、オフライン、通知が、web では取れないか不安定
- iOS Safari は、選んだ写真の位置情報を消す場合がある ([WebKit bug 257534](https://bugs.webkit.org/show_bug.cgi?id=257534))。写真から店を出す流れを試せない

## 決定

- PHASE 1 で使い込むのは、Expo のアプリ ([ADR-0001](0001-monorepo-and-stack.md) のネイティブアプリ) にする
- 作り手の iPhone には TestFlight で入れる。限定テストの人にも TestFlight で配る

## 結果

- PHASE 1 から、本番と同じ写真・位置・通知の扱いで記録を試せる
- web (Vite + React) のプロトタイプを残すかは、技術の確認のときに決める
- 作り手以外に TestFlight で配るときは、Apple のベータ版の審査 (外部テスト) を通す
