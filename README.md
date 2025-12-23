
# SalesDataRobotVer2

## 概要
このロボットは、RobotSpareBin Industriesの注文サイトに対して、CSVの注文データをもとに自動で注文処理を行います。  
注文ごとに **レシートPDF** と **スクリーンショット画像** を生成し、最後に **PDFをZIPアーカイブ** にまとめます。  
Sema4.ai「Automation Certification Level II - Python」コースの課題として作成しました。

## 機能
- ダウンロードした CSV ファイルから orders データを読み込み
- orders レコード毎に、Robot Order ウェブサイトにデータを入力して注文を実行
- 各注文の **HTMLレシート** を **PDF** に変換
- 各注文の **スクリーンショット** を取得
- スクリーンショットを **PDFレシートに追記（埋め込み）**
- すべての PDF を **ZIP** (`output/output_pdfs.zip`) にまとめる

## 生成されるファイルと出力先
- `output/receipts/receipt_<Order number>.pdf` : レシート PDF
- `output/images/img_<Order number>.png` : スクリーンショット
- `output/output_pdfs.zip` : レシート PDF をまとめた ZIP

## 実行の流れ（内部処理）
1. `https://robotsparebinindustries.com/orders.csv` をダウンロード
2. CSV をテーブルとして読み込み（RPA.Tables）
3. 各行のデータでフォームを入力し、注文を送信（robocorp.browser）
4. レシートHTMLを PDF に変換（RPA.PDF）
5. スクリーンショットを撮影し、PDFに追加（RPA.PDF）
6. 全レシートPDFを ZIP でアーカイブ（RPA.Archive）

## 必要環境
- Python（Robocorp の conda 環境を使用）
- Robocorp ランタイム（`robot.yaml` / `conda.yaml` に定義）
- 依存ライブラリ：  
  - `robocorp.browser`  
  - `RPA.HTTP` / `RPA.Tables` / `RPA.PDF` / `RPA.Archive`

## セットアップ & 実行方法
> ※ Robocorp の rcc（または VS Code の Robocorp 拡張機能）を利用して実行する構成です。

1. リポジトリをクローン
   ```bash
   git clone https://github.com/megumi-python/SalesDataRobotVer2.git
   cd SalesDataRobotVer2
