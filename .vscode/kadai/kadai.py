import os
from openai import OpenAI

# APIキーを環境変数から設定（環境変数が設定されていない場合のエラーハンドリング）
try:
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    print("OpenAI APIクライアントを初期化しました。")
except KeyError:
    print("警告: OPENAI_API_KEY環境変数が設定されていません。")
    # 一時的な対処: 直接APIキーを入力
    api_key = input("OpenAI APIキーを入力してください: ").strip()
    if not api_key:
        print("APIキーが入力されませんでした。プログラムを終了します。")
        exit(1)
    try:
        client = OpenAI(api_key=api_key)
        print("OpenAI APIクライアントを初期化しました。")
    except Exception as e:
        print(f"APIキーが無効です: {e}")
        exit(1)
except Exception as e:
    print(f"OpenAIクライアントの初期化でエラーが発生しました: {e}")
    exit(1)

# システムプロンプト
messages = [
    {"role": "system", "content": "あなたは健康に関する専門家です。ユーザーの質問に回答してください。"}
]

total_tokens = 0

while True:
    user_input = input("質問を入力してください（終了の場合は'quit'と入力）：")
    if user_input.strip().lower() == "quit":
        print("対話を終了します。")
        break

    messages.append({"role": "user", "content": user_input})

    # Chat API 呼び出し
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    result = completion.choices[0].message.content
    print("アシスタント：", result)

    messages.append({"role": "assistant", "content": result})

    # トークン数の加算と表示
    usage = completion.usage
    current_tokens = usage.total_tokens
    total_tokens += current_tokens
    print(f"今回のトークン数: {current_tokens}, 合計トークン数: {total_tokens}")
    print("-" * 50)

print(f"総トークン数: {total_tokens}")