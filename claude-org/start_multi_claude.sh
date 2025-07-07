#!/bin/bash

# 複数のClaude Codeセッションを立ち上げるスクリプト
# 各ペインで異なる役割のClaude Codeを起動

SESSION_NAME="dev"

echo "Claude Code組織を立ち上げ中..."

# ペイン0（Editor）: Boss役 - あなたがメインで操作
tmux send-keys -t $SESSION_NAME:0.0 "cd claude-org/boss" C-m
tmux send-keys -t $SESSION_NAME:0.0 "echo 'Boss役：プロジェクト全体の指揮を取ります'" C-m

# ペイン1（AI-Chat）: PM役 - プロダクトマネージャー
tmux send-keys -t $SESSION_NAME:0.1 "cd claude-org/pm" C-m
tmux send-keys -t $SESSION_NAME:0.1 "echo 'PM役：要件定義とタスク管理を行います'" C-m
tmux send-keys -t $SESSION_NAME:0.1 "echo 'Claude Codeを起動してPM役として待機中...'" C-m

# ペイン2（Commands）: Dev役 - 開発者
tmux send-keys -t $SESSION_NAME:0.2 "cd claude-org/dev" C-m
tmux send-keys -t $SESSION_NAME:0.2 "echo 'Dev役：実装とコーディングを行います'" C-m
tmux send-keys -t $SESSION_NAME:0.2 "echo 'Claude Codeを起動してDev役として待機中...'" C-m

echo "✅ 各ペインでClaude Code組織の準備が完了しました"
echo ""
echo "次のステップ："
echo "1. 各ペインでClaude Codeセッションを開始"
echo "2. Boss役（あなた）からPM役に指示を出す"
echo "3. PM役からDev役に指示を出す"
echo ""
echo "tmuxペイン移動: Ctrl-b + 矢印キー"
echo "ペイン番号表示: Ctrl-b + q"