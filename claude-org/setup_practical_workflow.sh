#!/bin/bash

# 実践的なClaude Code組織運営のワークフロー
# 複数のClaude Codeセッションを使った実際の開発フロー

SESSION_NAME="claude-org"

# 既存のセッションがある場合は削除
tmux has-session -t $SESSION_NAME 2>/dev/null && tmux kill-session -t $SESSION_NAME

# 新しいセッションを作成
tmux new-session -d -s $SESSION_NAME

# ウィンドウ名を設定
tmux rename-window -t $SESSION_NAME:0 "AI-Organization"

# 4つのペインを作成（2x2構成）
# 上段を左右に分割
tmux split-window -h -t $SESSION_NAME:0.0

# 左上を上下に分割
tmux split-window -v -t $SESSION_NAME:0.0

# 右上を上下に分割
tmux split-window -v -t $SESSION_NAME:0.1

# 各ペインの設定
declare -a roles=("Boss" "PM" "Dev" "Test")
declare -a icons=("👑" "📋" "💻" "🧪")
declare -a colors=("Boss" "PM" "Dev" "Test")

# 各ペインに役割を設定
for i in {0..3}; do
    role=${roles[$i]}
    icon=${icons[$i]}
    
    # ペインにタイトルを設定
    tmux send-keys -t $SESSION_NAME:0.$i "printf '\033]2;${icon} ${role}\033\\'" C-m
    
    # 対応するディレクトリに移動
    tmux send-keys -t $SESSION_NAME:0.$i "cd claude-org" C-m
    
    # 役割に応じた初期化
    case $role in
        "Boss")
            tmux send-keys -t $SESSION_NAME:0.$i "export PS1='${icon} ${role}: '" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '🎯 プロジェクト全体の指揮を執ります'" C-m
            ;;
        "PM")
            tmux send-keys -t $SESSION_NAME:0.$i "export PS1='${icon} ${role}: '" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '📊 要件定義と進捗管理を担当します'" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '💡 Claude Codeを起動して、PM役として待機中...'" C-m
            ;;
        "Dev")
            tmux send-keys -t $SESSION_NAME:0.$i "export PS1='${icon} ${role}: '" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '⚙️ 実装とコーディングを担当します'" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '🔍 必要に応じてWeb検索も実行します'" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '💡 Claude Codeを起動して、Dev役として待機中...'" C-m
            ;;
        "Test")
            tmux send-keys -t $SESSION_NAME:0.$i "export PS1='${icon} ${role}: '" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '🔬 テストとバグ発見を担当します'" C-m
            tmux send-keys -t $SESSION_NAME:0.$i "echo '💡 Claude Codeを起動して、Test役として待機中...'" C-m
            ;;
    esac
    
    tmux send-keys -t $SESSION_NAME:0.$i "clear" C-m
done

# レイアウトを調整
tmux select-layout -t $SESSION_NAME:0 tiled

# Bossペインにフォーカス
tmux select-pane -t $SESSION_NAME:0.0

echo "🚀 Claude Code組織が準備完了しました！"
echo ""
echo "📋 ペイン構成:"
echo "  👑 Boss  (左上): あなたが指揮を執る"
echo "  📋 PM    (右上): プロジェクト管理"
echo "  💻 Dev   (左下): 開発・実装"
echo "  🧪 Test  (右下): テスト・品質保証"
echo ""
echo "🎮 操作方法:"
echo "  Ctrl-b + 矢印キー: ペイン移動"
echo "  Ctrl-b + q: ペイン番号表示"
echo "  Ctrl-b + z: ペイン最大化/復元"
echo ""
echo "📝 次のステップ:"
echo "  1. 各ペインでClaude Codeを起動"
echo "  2. Boss役からPM役に指示を出す"
echo "  3. 各役割間で連携して作業を進める"

# セッションにアタッチ
tmux attach-session -t $SESSION_NAME