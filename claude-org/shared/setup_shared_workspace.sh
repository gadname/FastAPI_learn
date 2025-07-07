#!/bin/bash

# 開発者間の協調作業用共有ワークスペース作成

echo "🤝 協調作業用共有ワークスペースを構築中..."

# 共有ディレクトリ構造を作成
mkdir -p claude-org/shared/{requests,responses,specs,issues,status,plans,instructions}

# テンプレートファイルを作成
cat > claude-org/shared/requests/template.md << 'EOF'
# 質問・依頼テンプレート

## 質問者: [役割名]
## 宛先: [役割名]  
## 日時: $(date)
## 緊急度: [高/中/低]

## 質問・依頼内容
[具体的な内容を記載]

## 背景・理由
[なぜこの質問/依頼が必要なのか]

## 期待する回答・対応
[どのような形で回答してほしいか]

## 期限
[いつまでに必要か]

---
回答は shared/responses/[対応するファイル名] に記載してください。
EOF

cat > claude-org/shared/responses/template.md << 'EOF'
# 回答・対応テンプレート

## 回答者: [役割名]
## 宛先: [役割名]
## 日時: $(date)

## 回答・対応内容
[具体的な回答を記載]

## 関連ファイル・リソース
[参考となるファイルやURL]

## 追加の注意事項
[実装時の注意点など]

## フォローアップ
[追加で必要な作業があれば]
EOF

cat > claude-org/shared/status/template.md << 'EOF'
# 進捗状況テンプレート

## 担当者: [役割名]
## 更新日時: $(date)

## 完了したタスク
- [ ] タスク1
- [ ] タスク2

## 進行中のタスク
- [ ] タスク1 (進捗: XX%)
- [ ] タスク2 (進捗: XX%)

## 次のタスク
- [ ] タスク1
- [ ] タスク2

## ブロッカー・課題
[進捗を妨げている問題があれば]

## 他の開発者への依頼
[協力が必要な事項があれば]
EOF

# 初期ファイルを作成
echo "# 開発者間協調ログ

## $(date)
協調作業用ワークスペースを構築しました。

## 使用方法
1. 質問・依頼: shared/requests/ にファイル作成
2. 回答・対応: shared/responses/ にファイル作成  
3. 進捗共有: shared/status/ に状況更新
4. 仕様書: shared/specs/ に技術仕様
5. 問題報告: shared/issues/ に課題記録

## ファイル命名規則
- requests: [送信者]_to_[受信者]_[番号].md
- responses: [受信者]_to_[送信者]_[番号].md
- 例: frontend_to_backend_001.md

" > claude-org/shared/collaboration_log.md

echo "✅ 共有ワークスペースが構築されました！"
echo ""
echo "📁 ディレクトリ構成:"
echo "  shared/requests/     - 質問・依頼ファイル"
echo "  shared/responses/    - 回答・対応ファイル"
echo "  shared/specs/        - 技術仕様書"
echo "  shared/issues/       - 問題・課題報告"
echo "  shared/status/       - 進捗状況"
echo "  shared/plans/        - 計画・予定"
echo "  shared/instructions/ - Boss役からの指示"
echo ""
echo "📝 使用開始:"
echo "  1. テンプレートファイルを参考に情報共有"
echo "  2. ファイル名は [送信者]_to_[受信者]_[番号].md"
echo "  3. 定期的に shared/collaboration_log.md を更新"