from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, user

app = FastAPI()

# CORS の設定
origins = [
    "http://localhost:3000",  # Reactなどのフロントエンドが動作しているURL
    "http://127.0.0.1:3000",  # ローカル開発用
    "https://netcircle.tmp.monster",    # 本番環境のドメイン
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジン
    allow_credentials=True,  # Cookieを許可する場合はTrue
    allow_methods=["*"],  # 許可するHTTPメソッド（GET, POSTなど）
    allow_headers=["*"],  # 許可するHTTPヘッダー
)

app.include_router(user.router)
app.include_router(auth.router)
