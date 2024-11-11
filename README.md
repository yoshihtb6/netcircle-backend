# netcircle-backend環境構築
## 参考サイト
(https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/f1b6fc)

## 前提条件
[windows開発環境](https://github.com/yoshihtb6/netcircle-frontend?tab=readme-ov-file#windows%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83)の1,2,3,5が完了しているものとします。

1. gitでソースコードのclone

   `$ git clone git@github.com:yoshihtb6/netcircle-backend.git`

2. fastAPIのインストール

   プロジェクトルートディレクトリ(/netcircle-backend/)に移動して下記コマンドを実行する。

   `$ docker-compose run --entrypoint "poetry install --no-root" demo-app`

4. dockerコンテナの立ち上げ

   プロジェクトルートディレクトリ(/netcircle-backend/)に移動して下記コマンドを実行する。
   
   初回↓
   `$ docker compose up -d --build `

   2回目以降
   `$ docker compose up -d`

   ブラウザに`localhost:8000/docs`と入力する。

5. migtationの実行

   プロジェクトルートディレクトリ(/netcircle-backend/)に移動して下記コマンドを実行する。

   `$ docker compose exec demo-app poetry run python -m api.migrate_db`

以上です。
