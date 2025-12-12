#!/usr/bin/env bash

# エラーが発生した時点で処理を停止
set -o errexit

# 1. ライブラリのインストール
pip install -r requirements.txt

# 2. 静的ファイルの収集（staticfiles へ集約）
python manage.py collectstatic --no-input

# 3. データベースのマイグレーション（本番DBへテーブル反映）
python manage.py migrate
