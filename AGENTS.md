# AGENTS.md — HINAMI

HINAMI (日次 / ひなみ) は、食と飲みの「覚えておきたい体験」を 1 品ずつ記録する個人向けスマホアプリ。
このファイルは入口と最低限のルールだけを示す。詳細は `docs/` にある。

## 現在地

- 構想段階を終え、リポジトリを整備した段階。アプリのコードはまだない
- 見た目のデザイン ([`docs/design/direction.md`](docs/design/direction.md)) の前に、ワイヤーフレームの画面遷移図で UX を詰めている ([`docs/ux/`](docs/ux/recording.md))。「ホームからいつもの記録」の流れ、続けたくなる仕組み (実績) の最初の一覧、比べる (ランキング)、履歴と検索、つながる (SNS)、画面の構成 (タブとホーム)、実績とマップのタブ、最初のチュートリアルとアカウント、種類の一覧の持ち方と作り方、食事の詳細に出す要素、お知らせと設定まで決めた
- 最初の関門 (PHASE 1): 作り手自身が 4 週間、覚えておきたい食をすべて記録できること

## ドキュメントマップ

| 知りたいこと                                | 場所                                                   |
| ------------------------------------------- | ------------------------------------------------------ |
| 何を作るか (コンセプト・前提・収益・進め方) | [`docs/concept.md`](docs/concept.md)                   |
| 画面の流れ (UX)                             | [`docs/ux/`](docs/ux/recording.md)                     |
| 続けたくなる仕組み (実績)                   | [`docs/ux/achievements.md`](docs/ux/achievements.md)   |
| 比べる (ランキング)                         | [`docs/ux/compare.md`](docs/ux/compare.md)             |
| 種類の一覧                                  | [`docs/ux/kinds.md`](docs/ux/kinds.md)                 |
| 最初のチュートリアルとアカウント            | [`docs/ux/onboarding.md`](docs/ux/onboarding.md)       |
| 画面の構成 (タブとホーム)                   | [`docs/ux/navigation.md`](docs/ux/navigation.md)       |
| お知らせと設定                              | [`docs/ux/settings.md`](docs/ux/settings.md)           |
| 記録のタブ (履歴と検索)                     | [`docs/ux/history.md`](docs/ux/history.md)             |
| つながる (SNS)                              | [`docs/ux/connect.md`](docs/ux/connect.md)             |
| デザインの方向性                            | [`docs/design/direction.md`](docs/design/direction.md) |
| 判断待ち・未確認のこと                      | [`docs/open-questions.md`](docs/open-questions.md)     |
| 外部の目でのレビューの記録                  | [`docs/reviews/`](docs/reviews/2026-11-27-review.md)   |
| 意思決定の理由 (ADR)                        | [`docs/adr/index.md`](docs/adr/index.md)               |
| 構想段階の経緯                              | [`docs/history.md`](docs/history.md)                   |
| 構想段階のスライド (参照専用)               | [`docs/references/`](docs/references/README.md)        |

## ディレクトリ構成 (pnpm workspace)

| ディレクトリ | 中身                                                                              |
| ------------ | --------------------------------------------------------------------------------- |
| `apps/`      | アプリ。web (Vite + React、プロトタイプ) とネイティブ (Expo) を置く予定           |
| `packages/`  | web とネイティブで共有するライブラリ (デザイントークン、型、ドメインロジックなど) |
| `docs/`      | 設計ドキュメント                                                                  |

## コマンド

| コマンド     | 内容                                             |
| ------------ | ------------------------------------------------ |
| `task setup` | ツール (mise) と依存を入れ、git hooks を設定する |
| `task check` | lint とフォーマットを検査する                    |
| `task fix`   | lint とフォーマットを自動修正する                |

## 最低限のルール

- 回答・説明・ドキュメントは日本語。コード内の識別子・コメントは英語
- TypeScript は strict で `any` を避ける
- 新規依存パッケージの追加は事前に確認する
- 決定事項が変わったら、該当する `docs/` を同じ変更で更新する。判断待ちが決まったら [`docs/open-questions.md`](docs/open-questions.md) から消す
- 作業中に作り手から指摘されたことはドキュメントに残す。プロジェクト全般に当てはまることは本ファイルか `docs/`、作り手個人の進め方の好みは `CLAUDE.local.md` (git 管理外) に書く

## 提案物・ドキュメントのルール

- 成果物に作り手の名前を書かない。他人に見せても不自然でない書き方にし、本人は「作り手」と呼ぶ
- 提案は結論を先に、1 枚 1 メッセージ、図解と画面イメージ中心、文章は簡潔にする
- 平易・明快に書く。ポップ・幼稚な表現は NG
- 案は数を並べない。全条件を満たし、別の目でレビューを通した案だけを 3 案以内で出す
- 名前などのアイデア出しは、スライドにせずチャットのテキストで出す
- 作り手が出した例を前提に格上げしない
- UX (ワイヤーフレーム) では、画面に出す要素と流れだけを決める。写真の大きさ、配置、並べ方などの見た目は、デザインのフェーズで決める
