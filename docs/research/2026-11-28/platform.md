# 調査: iOS の新しい仕組みと AI の最新の手法 (2026-11-28)

エージェントが Web で調べた報告。数字や仕様は出典のものを写しただけで、一次情報はまだ確かめていない。iOS 27 と WWDC26 の内容の多くは、技術のレビューで一次情報に照らした (下の「レビューで確かめたこと」)。施策の候補は調査担当の意見で、決まりではない。まとめは [`README.md`](README.md)。

前提 (報告より): 最新の OS は iOS 27 (2026-09-14 公開)。Expo は iOS 27 に対応した SDK 58 (2026-10) が最新。

## レビューで確かめたこと (2026-11-28)

技術のレビュー (別のエージェント) で、Apple と Expo の一次情報に照らした結果。

- **合っていた**:
  - iOS 27 の端末のモデルの画像入力 (`Attachment`)。対応端末 (iPhone 15 Pro、16 以降、Air、Duo。8〜14GB の空きが要る)
  - PCC を開発者が使えること (通信が要る。文脈 32K。TestFlight で試せる。将来は有料の枠ができる)
  - Claude と Gemini に同じ API で差し替えられること
  - `expo-ai` (アルファ版)、`expo-widgets` (SDK 56 で安定版)、`expo-app-intents` (アルファ版)
  - LockedCameraCapture の制約 (通信も App Group も使えない。申請の要る entitlement はない。`expo-apple-targets` は対応していない)
  - Place ID は保存の制限を受けない
  - PhotosPicker は埋め込めて、許可が要らない
- **違っていた・補足**:
  - 端末のモデルの文脈長「4K 前後」は iOS 26 の値。WWDC26 の例では 8192。実行時に `contextSize` で取る
  - PCC を無料で使うには、Small Business Program に加えて、初回のダウンロードが 200 万未満であることと、申請して受ける entitlement が要る
  - Journaling Suggestions の entitlement は Xcode で付けられ、申請制ではない。ただし、写真の候補で渡るのは画像と日時だけで、位置がない
  - Place ID は 1 つの店に複数付くことがある。別の ID (alternateIdentifiers) を見て重複を除く
  - Live Activity は、動くのが 8 時間まで、そのあとロック画面に最長 4 時間残る。「8 時間」と「12 時間」はどちらも正しい
  - Live Activity のデータは 4KB まで
- **確かめられなかった**: PCC が画像を受けるか。1 日の上限の数値。撮影の拡張で位置を取れるか。日本の飲食店の MapKit の網羅度
- **出典**: [WWDC26 #241](https://developer.apple.com/videos/play/wwdc2026/241)、[画像の入力](https://developer.apple.com/documentation/foundationmodels/analyzing-images-with-multimodal-prompting)、[対応端末](https://support.apple.com/en-us/121115)、[PCC](https://developer.apple.com/private-cloud-compute/)、[LockedCameraCapture](https://developer.apple.com/documentation/lockedcameracapture/creating-a-camera-experience-for-the-lock-screen)、[Journaling Suggestions の写真](https://developer.apple.com/documentation/journalingsuggestions/journalingsuggestion/photo)、[Place ID](https://developer.apple.com/documentation/mapkit/identifying-unique-locations-with-place-ids)、[Live Activities](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities)、[Expo SDK 58](https://expo.dev/changelog/sdk-58)、[iPhone の機種の割合 (MMD 研究所)](https://www.watch.impress.co.jp/docs/news/2141787.html)

## 項目ごとの要点

### 1. Foundation Models (端末で動く LLM)

- iOS 27 で、端末のモデルが画像を受けられるようになった。構造化した出力 (@Generable) と tool calling が使え、Vision の OCR・バーコードを読むツールも標準で付く
- 日本語は Apple Intelligence の対応言語。動くのは iPhone 15 Pro、16 以降など。端末モデルの文脈長は 4K 前後
- iOS 27 で、Apple のサーバー (Private Cloud Compute、PCC) で動く大きいモデルが加わった。Small Business Program の開発者は無料で使える。申請が要り、利用者ごとに 1 日の上限がある
- 同じ API のまま、モデルを Claude や Gemini に差し替えられる
- Expo: `expo-ai` (アルファ版) が画像入力・構造化出力・tool calling を扱える。PCC は Expo Modules で自作する
- 未確認: PCC が画像を受けるか。食の判定の精度。1 日の上限の数値
- 出典: [WWDC26 #241](https://developer.apple.com/videos/play/wwdc2026/241)、[WWDC26 #319](https://developer.apple.com/videos/play/wwdc2026/319)、[PCC](https://developer.apple.com/private-cloud-compute/)、[Expo AI](https://docs.expo.dev/versions/unversioned/sdk/ai)

### 2. Vision・VisionKit・Visual Intelligence

- Vision の文字認識は、日本語の横書きなら実用になる。縦書きは公式の記載がなく、読めないという報告が多い
- Visual Intelligence (iOS 26〜) では、アプリが検索結果を返せる。カメラの画像を受け取り、結果をタップするとアプリが開く
- 意見: 酒瓶にカメラを向けたとき「前に飲んだ記録」を返す使い方ができる
- Expo: ほぼ Swift で書く
- 出典: [フォーラム](https://developer.apple.com/forums/thread/772972)、[WWDC26 #297](https://developer.apple.com/videos/play/wwdc2026/297)

### 3. Journaling Suggestions

- iOS 17.2 以降、実機だけ。entitlement (`com.apple.developer.journal.allow`) が要る
- 候補は OS が端末の中で作り、選んだものだけがアプリに渡る。候補は写真・Live Photo・場所・運動・曲など。アプリから種類を絞る引数はない
- OS は定期的に振り返りの通知を出す。タップすると、設定で選んだ 1 つのアプリが開く (Apple のジャーナルと取り合いになる)
- 日本: ジャーナル App は日本の App Store にある。API の地域の制限は見つからなかった (未確認)
- Expo: 既存のモジュールはない。Expo Modules で包む
- 出典: [Apple](https://developer.apple.com/documentation/journalingsuggestions)、[通知から受け取る](https://developer.apple.com/documentation/journalingsuggestions/receiving-journaling-suggestions-from-system-notifications)

### 4. ロック画面のカメラ、コントロール、App Intents、Siri、Spotlight

- 撮影の拡張 (LockedCameraCapture) は、コントロールセンター・ロック画面・アクションボタンのコントロールから開く。Camera Control に出すにもこの拡張が要る
- 拡張の制約: ネットワークを使えない。App Group も使えない。開いてすぐファインダーを出さないと終了させられる。撮ったものは、拡張を閉じたときにアプリへコピーされる。位置情報を使えるかは記載がない
- iOS 27 の App Intents では、記録を schema で登録すると、Spotlight の意味の検索と Siri AI に載る。Siri AI は英語のベータで始まった
- Expo: `expo-apple-targets` はコントロールを作れるが、撮影の拡張は Swift で自作する。`expo-app-intents` (アルファ版) は Spotlight への登録などに対応
- 出典: [WWDC24 #10204](https://developer.apple.com/videos/play/wwdc2024/10204)、[HIG](https://developer.apple.com/design/human-interface-guidelines/camera-control)、[Expo App Intents](https://docs.expo.dev/versions/latest/sdk/app-intents/)

### 5. ウィジェット、Live Activities

- ボタンを押せるウィジェットは iOS 17 から。Live Activity はロック画面に最長 12 時間出せる (journaling.md の報告では「最長 8 時間」。動いている時間と、終わったあとに残る時間の違いと思われる。未確認)
- Expo: `expo-widgets` が SDK 56 で安定版。ウィジェットと Live Activity を作れる
- 出典: [Expo Widgets](https://docs.expo.dev/versions/latest/sdk/widgets/)

### 6. MapKit と Apple Maps

- 店の検索は、飲食の種類 (restaurant、cafe、bakery、brewery、winery、distillery、nightlife) に絞れる
- 店の ID (Place ID) は保存の制限を受けない。期限なく保存でき、他のアプリとも共有でき、サーバーからも引ける
- Apple Maps Server API と MapKit JS は、1 チームで 1 日 25,000 回まで無料。端末の MapKit には、料金と上限の公式の記載がない
- Apple マップの「訪れた場所」をアプリが受け取る公開 API は見当たらない
- Expo: `expo-maps` は地図を出すだけ。店の検索は Expo Modules で包む
- 未確認: 日本の飲食店の網羅度
- 出典: [Place ID](https://developer.apple.com/documentation/mapkit/identifying-unique-locations-with-place-ids)

### 7. 写真まわり

- PhotosPicker は別のプロセスで動き、写真へのアクセスの許可なしで使える。iOS 17 から、アプリの画面に埋め込める
- 選んだ写真には、位置などの情報が既定で付く。利用者は外せる
- Expo: `expo-image-picker` は画面を覆う形だけ。カメラで撮った写真の EXIF には GPS が入らないと明記されている
- 出典: [WWDC23 #10107](https://developer.apple.com/videos/play/wwdc2023/10107)、[Expo ImagePicker](https://docs.expo.dev/versions/latest/sdk/imagepicker/)

### 8. 外部の多モーダル AI

- 報告された料金 (入力 / 出力の 100 万トークンあたり): Gemini 3.5 Flash-Lite $0.30 / $2.50、Gemini 3.8 Flash $0.75 / $3.75、Claude Haiku 5.5 $0.10 / $0.50。Gemini の有料枠は、送ったデータを製品の改善に使わない。いずれも未確認で、選ぶ前に各社の料金表で確かめる
- 縦書きの日本語は、多モーダルの LLM でも横書きより精度が落ちる ([arXiv 2511.15059](https://arxiv.org/abs/2511.15059))
- Jev の画像入力は、1.14 (2026-10) でも実験の扱い (二次情報)
- 未確認: 食の判定と酒ラベルの読み取りでの各社の実力と遅延。実際の写真 50 枚程度で比べる必要がある
- 意見 (最新の型): まず端末で判定し、足りないときだけ同意を取って外部に送る

### 9. その他

- Core AI (iOS 27): 自前のモデルを端末で動かせる
- Evaluations (iOS 27): AI の判定の質を測り続けられる
- App Store の審査ガイドライン 5.1.2(i): 第三者の AI に個人データを送るには、開示と許可が要る。PCC が「第三者」に当たるかは未確認

## 施策の候補 (調査担当の意見)

- **A. 判定を「端末 → PCC → 外部」の段階にする**: 種類の判定はまず端末のモデルで、画像と OCR を使い、種類の一覧から選ばせる。足りなければ PCC、それでも足りないときだけ同意を取って外部へ。写真を外に出さないのが既定になり、電波がなくても種類が付く。Jev は見直しの対象になる
- **B. 酒ラベルは「端末の OCR → LLM で整える」**: 端末で文字を拾い、銘柄・蔵・種別に整える。縦書きや毛筆は外部に回す。今の UX どおり、メモの候補として出す
- **C. Journaling Suggestions で記録漏れを拾う**: 「最近の食事から」の入り口から候補の一覧を出す。OS の振り返りの通知の開き先にも登録する。候補を食に絞れない。食の記録アプリに entitlement が認められるかは未確認
- **D. 写真の選択を画面に埋め込む**: 許可の要らない PhotosPicker を記録の画面に埋め込み、最近の写真を見せる。「記録済みの写真を外して見せる」決まりは、埋め込みでは制御できない見込み
- **E. 撮影の入り口を OS に置き、食事中は Live Activity を出す**: ロック中に撮り、解除してから確認カードへ。種類の判定と店の推定は解除してから。撮影の拡張は Swift の別ターゲットで難しい
- **F. 店は MapKit の Place ID で持つ**: 撮った位置の近くを飲食に絞って検索し、Place ID を記録に保存する。サーバーと姉妹アプリでも同じ ID を使う。Google Places の規約と費用の課題を避けられる。日本の網羅度は未検証
