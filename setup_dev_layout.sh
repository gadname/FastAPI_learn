#!/bin/bash

# Claude Code組織化のための3ペイン構成tmuxセッション
# セッション名: dev
# 構成: エディタ領域（左）、AI対話領域（右上）、コマンド実行領域（右下）

SESSION_NAME="dev"

# 既存のセッションがある場合は削除
tmux has-session -t $SESSION_NAME 2>/dev/null && tmux kill-session -t $SESSION_NAME

# 新しいセッションを作成
tmux new-session -d -s $SESSION_NAME

# ウィンドウ名を設定
tmux rename-window -t $SESSION_NAME:0 "Claude-Dev"

# 右側を縦に分割（AI対話領域とコマンド実行領域）
tmux split-window -h -t $SESSION_NAME:0.0

# 右側を横に分割
tmux split-window -v -t $SESSION_NAME:0.1

# 各ペインのサイズを調整
# 左のペインを60%に設定
tmux resize-pane -t $SESSION_NAME:0.0 -x 60%

# 右上のペインを60%に設定
tmux resize-pane -t $SESSION_NAME:0.1 -y 60%

# 各ペインに移動してタイトル設定とディレクトリ移動
# ペイン0: エディタ領域
tmux send-keys -t $SESSION_NAME:0.0 "printf '\033]2;Editor\033\\'" C-m
tmux send-keys -t $SESSION_NAME:0.0 "export PS1='(📝 Editor) \$ '" C-m
tmux send-keys -t $SESSION_NAME:0.0 "clear" C-m

# ペイン1: AI対話領域
tmux send-keys -t $SESSION_NAME:0.1 "printf '\033]2;AI-Chat\033\\'" C-m
tmux send-keys -t $SESSION_NAME:0.1 "export PS1='(🤖 AI) \$ '" C-m
tmux send-keys -t $SESSION_NAME:0.1 "clear" C-m

# ペイン2: コマンド実行領域
tmux send-keys -t $SESSION_NAME:0.2 "printf '\033]2;Commands\033\\'" C-m
tmux send-keys -t $SESSION_NAME:0.2 "export PS1='(⚡ CMD) \$ '" C-m
tmux send-keys -t $SESSION_NAME:0.2 "clear" C-m

# エディタ領域にフォーカス
tmux select-pane -t $SESSION_NAME:0.0

# セッションにアタッチ
tmux attach-session -t $SESSION_NAME

echo "Claude Code開発環境が構築されました！"
echo "構成:"
echo "  📝 Editor (左)    : コード編集"
echo "  🤖 AI-Chat (右上) : AI対話"
echo "  ⚡ CMD (右下)     : コマンド実行"