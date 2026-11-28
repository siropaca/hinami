# AGENTS.md — HINAMI

HINAMI (日次 / ひなみ) は、口にする食と飲みを 1 品ずつ記録する個人向けスマホアプリ。覚えておきたい一皿だけでも、口にするすべてでも残せ、究極は自分の好みを誰よりも知っていて記憶している記録帳になる。
このファイルは入口と最低限のルールだけを示す。詳細は `docs/` にある。

## 現在地

- 構想段階を終え、リポジトリを整備した段階。アプリのコードはまだない
- UX (画面に出す要素と流れ) は、ワイヤーフレームの画面遷移図で一通り決めた ([`docs/ux/`](docs/ux/recording.md))。見た目は、このあとのデザインのフェーズで決める ([`docs/design/direction.md`](docs/design/direction.md))
- デザインは、方向性 (世界観「日々の帳面」。明暗 2 つの紙面、墨・生成り・金・朱の 4 色、OS のヒラギノ)、ロゴ「皿と箸」、デザイントークン、ブランドの金を決めた ([`docs/design/`](docs/design/README.md))
- 6 つの視点のレビューを受け、作り手の判断を反映した ([`docs/reviews/2026-11-27-review.md`](docs/reviews/2026-11-27-review.md))
- 最先端の事例と手法を調べ、3 つの施策 (撮ったら残る、どの品も名前まで残る、記録が好みを語る) を採った ([`docs/research/2026-11-28/README.md`](docs/research/2026-11-28/README.md))
- サービスの本質の論点を詰めた: 記録の単位 (品と写真、写真なし。[`docs/ux/recording.md`](docs/ux/recording.md))、そのときの気持ちと比べる ([`docs/ux/compare.md`](docs/ux/compare.md))、長く使うほど返るもの ([`docs/ux/memory.md`](docs/ux/memory.md))、記録にためるもの ([`docs/data.md`](docs/data.md))。次は、技術の確認に進む ([`docs/open-questions.md`](docs/open-questions.md) の「技術」)
- 最初の関門 (PHASE 1): 作り手自身が 4 週間使い、このまま使い続けたいと思えること。数えずに、作り手の手応えで決める。友だちの機能まで入れ、家族とも使う。Expo のアプリを TestFlight で使う ([ADR-0002](docs/adr/0002-phase1-on-testflight.md))

## ドキュメントマップ

| 知りたいこと                                          | 場所                                                   |
| ----------------------------------------------------- | ------------------------------------------------------ |
| 何を作るか (コンセプト・前提・収益・進め方)           | [`docs/concept.md`](docs/concept.md)                   |
| 事業コンセプト提案書 (スライド)                       | [`docs/concept-deck/`](docs/concept-deck/README.md)    |
| 画面の流れ (UX)。入口は「記録の流れ」                 | [`docs/ux/recording.md`](docs/ux/recording.md)         |
| 続けたくなる仕組み (実績)                             | [`docs/ux/achievements.md`](docs/ux/achievements.md)   |
| 気持ちと比べる (ランキング)                           | [`docs/ux/compare.md`](docs/ux/compare.md)             |
| 種類の一覧                                            | [`docs/ux/kinds.md`](docs/ux/kinds.md)                 |
| 最初のチュートリアルとアカウント                      | [`docs/ux/onboarding.md`](docs/ux/onboarding.md)       |
| 画面の構成 (タブとホーム)                             | [`docs/ux/navigation.md`](docs/ux/navigation.md)       |
| お知らせと設定                                        | [`docs/ux/settings.md`](docs/ux/settings.md)           |
| 記録のタブ (履歴と検索)                               | [`docs/ux/history.md`](docs/ux/history.md)             |
| 記録が好みを語る (好みの分析と次に試すもの)           | [`docs/ux/taste.md`](docs/ux/taste.md)                 |
| 長く使うほど返るもの (前にも、アルバム、毎年の楽しみ) | [`docs/ux/memory.md`](docs/ux/memory.md)               |
| 記録にためるもの (データの原則と同意)                 | [`docs/data.md`](docs/data.md)                         |
| つながる (SNS)                                        | [`docs/ux/connect.md`](docs/ux/connect.md)             |
| デザインの入口 (決めたこと、資料の地図)               | [`docs/design/README.md`](docs/design/README.md)       |
| デザインの方向性 (考え方と理由)                       | [`docs/design/direction.md`](docs/design/direction.md) |
| デザイントークン (色、文字、余白などの値)             | [`docs/design/tokens.md`](docs/design/tokens.md)       |
| ロゴ (シンボル、セット、アイコン)                     | [`docs/design/logo/`](docs/design/logo/README.md)      |
| 判断待ち・未確認のこと                                | [`docs/open-questions.md`](docs/open-questions.md)     |
| 外部の目でのレビューの記録                            | [`docs/reviews/`](docs/reviews/2026-11-27-review.md)   |
| 最先端の事例と手法の調査                              | [`docs/research/`](docs/research/2026-11-28/README.md) |
| 意思決定の理由 (ADR)                                  | [`docs/adr/index.md`](docs/adr/index.md)               |
| 構想段階の経緯                                        | [`docs/concept-history.md`](docs/concept-history.md)   |
| 構想段階のスライド (参照専用)                         | [`docs/references/`](docs/references/README.md)        |

## ディレクトリ構成 (pnpm workspace)

| ディレクトリ | 中身                                                                                                                                                      |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `apps/`      | アプリ。ネイティブ (Expo) を置く予定。web (Vite + React) のプロトタイプを残すかは、技術の確認で決める ([ADR-0002](docs/adr/0002-phase1-on-testflight.md)) |
| `packages/`  | web とネイティブで共有するライブラリ (デザイントークン、型、ドメインロジックなど)                                                                         |
| `docs/`      | 設計ドキュメント                                                                                                                                          |

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

## 提案の姿勢

作り手は、記録アプリにイノベーションを起こす、今までにない質の高いアプリを目指している ([`docs/concept.md`](docs/concept.md))。

- 作り手の意思を尊重しつつ、アプリの質を上げる施策を自分から提案する。頼まれるのを待たない
- 最新の手法 (OS の新しい仕組み、AI など) や、世の中の成功事例を調べて取り入れる。出典を添える
- 作り手の案や、過去に決めたことより良いと考えるときは、「こちらのほうが良いのでは」と出す。作り手も意思が固まっていないことがある
- 特定の種類に寄せない。酒を飲まない人も、ワイン・ウイスキー・日本酒などが好きな人も、同じ厚さの価値を受け取れる設計にする ([`docs/concept.md`](docs/concept.md))。レビューの利用者役は 1 人にせず、好みの違う人を入れる
- 提案も下の「提案物・ドキュメントのルール」に従う (結論を先に、別の目でレビューを通した案だけを 3 案以内)
- 提案しても、論点を次へ進めるかどうかは作り手が決める

## アプリの中の言葉

- 利用者に伝える言葉 (トースト、ヒント、空の画面の案内、確認、通知、実績の条件、好みのことば) は、いつもユーザーフレンドリーにする。です・ます調で、やわらかく書く
- 体言止めにしない。冷たく、AI が書いたように聞こえるため (作り手の判断。2026-11-28)
- ボタン、見出し、タブ、欄の名前のような短いラベルと、実績の名前 (題名として使う) は、この限りではない
- ワイヤーフレームの言葉は仮だが、仮の言葉もこの決まりで書く

## 提案物・ドキュメントのルール

- 成果物に作り手の名前を書かない。他人に見せても不自然でない書き方にし、本人は「作り手」と呼ぶ
- 提案は結論を先に、1 枚 1 メッセージ、図解と画面イメージ中心、文章は簡潔にする
- 平易・明快に書く。ポップ・幼稚な表現は NG
- 案は数を並べない。全条件を満たし、別の目でレビューを通した案だけを 3 案以内で出す
- 名前などのアイデア出しは、スライドにせずチャットのテキストで出す
- 作り手が出した例を前提に格上げしない
- あとで調整しうるもの (実績の中身や言葉など) は、具体の言葉より、方針と理由を残す。具体の言葉は「今の案」として添える
- UX (ワイヤーフレーム) では、画面に出す要素と流れだけを決める。写真の大きさ、配置、並べ方などの見た目は、デザインのフェーズで決める
