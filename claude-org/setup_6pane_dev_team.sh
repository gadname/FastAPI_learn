#!/bin/bash

# 6ペイン構成：3人の開発者特化型Claude Code組織
# Boss, PM, Frontend Dev, Backend Dev, Fullstack Dev, Test

SESSION_NAME="dev-team-6"

# 既存のセッションがある場合は削除
tmux has-session -t $SESSION_NAME 2>/dev/null && tmux kill-session -t $SESSION_NAME

# 新しいセッションを作成
tmux new-session -d -s $SESSION_NAME

# ウィンドウ名を設定
tmux rename-window -t $SESSION_NAME:0 "Dev-Team"

# 3x2のグリッドレイアウトを作成
# まず縦に3分割
tmux split-window -v -t $SESSION_NAME:0.0
tmux split-window -v -t $SESSION_NAME:0.0

# 各行を横に2分割
# 1行目を分割
tmux split-window -h -t $SESSION_NAME:0.0

# 2行目を分割  
tmux split-window -h -t $SESSION_NAME:0.2

# 3行目を分割
tmux split-window -h -t $SESSION_NAME:0.4

# 役割とアイコンの定義
declare -a roles=("Boss" "PM" "Frontend" "Backend" "Fullstack" "Test")
declare -a icons=("👑" "📋" "🎨" "⚙️" "🚀" "🧪")
declare -a descriptions=(
    "プロジェクト全体の指揮"
    "要件定義・進捗管理"
    "React/Next.js UI開発"
    "FastAPI/DB開発"
    "フロント・バック統合"
    "テスト・品質保証"
)

# ペインの配置を最適化（tiled レイアウト使用）
tmux select-layout -t $SESSION_NAME:0 tiled

# 各ペインに役割を設定
for i in {0..5}; do
    role=${roles[$i]}
    icon=${icons[$i]}
    desc=${descriptions[$i]}
    
    # ペインにタイトルを設定
    tmux send-keys -t $SESSION_NAME:0.$i "printf '\033]2;${icon} ${role}\033\\'" C-m
    
    # 役割に応じたディレクトリに移動
    case $role in
        "Boss")
            tmux send-keys -t $SESSION_NAME:0.$i "cd claude-org/boss" C-m
            ;;
        "PM")
            tmux send-keys -t $SESSION_NAME:0.$i "cd claude-org/pm" C-m
            ;;
        "Frontend")
            tmux send-keys -t $SESSION_NAME:0.$i "mkdir -p claude-org/frontend && cd claude-org/frontend" C-m
            ;;
        "Backend")
            tmux send-keys -t $SESSION_NAME:0.$i "mkdir -p claude-org/backend && cd claude-org/backend" C-m
            ;;
        "Fullstack")
            tmux send-keys -t $SESSION_NAME:0.$i "mkdir -p claude-org/fullstack && cd claude-org/fullstack" C-m
            ;;
        "Test")
            tmux send-keys -t $SESSION_NAME:0.$i "cd claude-org/test" C-m
            ;;
    esac
    
    # プロンプトとメッセージの設定
    tmux send-keys -t $SESSION_NAME:0.$i "export PS1='${icon} ${role}: '" C-m
    tmux send-keys -t $SESSION_NAME:0.$i "echo '${desc}'" C-m
    
    if [ "$role" != "Boss" ]; then
        tmux send-keys -t $SESSION_NAME:0.$i "echo '💡 Claude Codeを起動して、${role}役として待機中...'" C-m
    fi
    
    tmux send-keys -t $SESSION_NAME:0.$i "clear" C-m
done

# Bossペインにフォーカス
tmux select-pane -t $SESSION_NAME:0.0

echo "🚀 6ペイン開発チームが準備完了しました！"
echo ""
echo "📋 チーム構成（3x2レイアウト）:"
echo "  👑 Boss      📋 PM"
echo "  🎨 Frontend  ⚙️ Backend" 
echo "  🚀 Fullstack 🧪 Test"
echo ""
echo "🎯 各開発者の専門分野:"
echo "  🎨 Frontend: React, Next.js, TypeScript, CSS, UI/UX"
echo "  ⚙️ Backend:  FastAPI, Python, DB, API, サーバー"
echo "  🚀 Fullstack: フロント・バック統合, デプロイ, DevOps"
echo ""
echo "🎮 操作方法:"
echo "  Ctrl-b + 矢印キー: ペイン移動"
echo "  Ctrl-b + q: ペイン番号表示"
echo "  Ctrl-b + z: ペイン最大化/復元"
echo ""
echo "📝 次のステップ:"
echo "  1. 各開発者ペインでClaude Codeを起動"
echo "  2. Boss役から専門性に応じてタスクを分担"
echo "  3. 開発者間で連携して統合開発を進める"

# セッションにアタッチ
tmux attach-session -t $SESSION_NAME