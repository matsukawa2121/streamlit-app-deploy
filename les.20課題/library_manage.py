books = []
members = []
borrow_records = []

# ユーティリティ関数

def find_book(book_id):
    return next((book for book in books if book["book_id"] == book_id), None)

def find_member(member_id):
    return next((member for member in members if member["member_id"] == member_id), None)

def add_book(book_id, title, author, copies):
    if find_book(book_id):
        print(f"図書ID「{book_id}」の本は既に存在します。")
        return
    books.append({
        "book_id": book_id,
        "title": title,
        "author": author,
        "copies": copies,
        "available_copies": copies
    })
    print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")

def list_books():
    if not books:
        print("現在、登録されている図書はありません。")
        return
    print("--- 図書一覧 ---")
    for book in books:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")

def search_book(book_id):
    book = find_book(book_id)
    if book:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")
    else:
        print(f"図書ID「{book_id}」の本は存在しません。")

def add_member(member_id, name):
    if find_member(member_id):
        print(f"会員ID「{member_id}」の会員は既に存在します。")
        return
    members.append({"member_id": member_id, "name": name})
    print(f"会員「{name}」（ID: {member_id}）を追加しました。")

def list_members():
    if not members:
        print("現在、登録されている会員はいません。")
        return
    print("--- 会員一覧 ---")
    for member in members:
        print(f"ID: {member['member_id']}, 名前: {member['name']}")

def borrow_book(book_id, member_id):
    book = find_book(book_id)
    if not book:
        print(f"図書ID「{book_id}」の本は存在しません。")
        return
    member = find_member(member_id)
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return
    if book["available_copies"] <= 0:
        print(f"図書「{book['title']}」は現在貸出可能な冊数がありません。")
        return
    record_count = sum(1 for record in borrow_records if record["member_id"] == member_id and not record["returned"])
    if record_count >= 5:
        print("貸出可能数は5冊までです。")
        return
    borrow_records.append({
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": "2024-11-24",
        "due_date": "2024-12-01",
        "returned": False
    })
    print(f"図書「{book['title']}」を会員「{member['name']}」に貸し出しました。\n返却期限: 2024-12-01")
    book["available_copies"] -= 1

def list_borrowed_books():
    print("--- 貸出中の図書一覧 ---")
    borrow_count = 0
    for record in borrow_records:
        if not record["returned"]:
            book = find_book(record["book_id"])
            member = find_member(record["member_id"])
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}")
            borrow_count += 1
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

def return_book(book_id, member_id):
    record = next((r for r in borrow_records if r["book_id"] == book_id and r["member_id"] == member_id and not r["returned"]), None)
    if not record:
        print(f"図書ID「{book_id}」本を会員ID「{member_id}」の会員は借りていません。")
        return
    record["returned"] = True
    book = find_book(book_id)
    if book:
        book["available_copies"] += 1
        print(f"図書「{book['title']}」が返却されました。")
    else:
        print(f"図書ID「{book_id}」の本は存在しません。")

def calculate_fines():
    print("--- 延滞料金一覧 ---")
    borrow_count = 0
    for record in borrow_records:
        if not record["returned"]:
            book = find_book(record["book_id"])
            member = find_member(record["member_id"])
            due_date = "2024-12-01"
            today = "2024-12-24"
            overdue_days = max((int(today[-2:]) - int(due_date[-2:])), 0)
            fine = overdue_days * 100
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 延滞料金: {fine}円")
            borrow_count += 1
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

def show_member_borrow_history(member_id):
    member = find_member(member_id)
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return
    print(f"--- 会員『{member['name']}』（ID: {member_id}）の貸出履歴 ---")
    history_count = 0
    for record in borrow_records:
        if record["member_id"] == member_id:
            book = find_book(record["book_id"])
            book_title = book["title"] if book else "不明"
            status = "返却済み" if record["returned"] else "貸出中"
            print(f"図書: {book_title}（ID: {record['book_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}, 状態: {status}")
            history_count += 1
    if history_count == 0:
        print("この会員の貸出履歴はありません。")

def main():
    while True:
        print("図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 会員の貸出履歴を表示")
        print("11: 終了")
        try:
            choice = int(input("操作を選択してください（1-11）: "))
            if choice == 1:
                book_id = input("図書IDを入力してください: ").strip()
                title = input("タイトルを入力してください: ").strip()
                author = input("著者名を入力してください: ").strip()
                try:
                    copies = int(input("冊数を入力してください: "))
                except ValueError:
                    print("冊数は数字で入力してください。")
                    continue
                add_book(book_id, title, author, copies)
            elif choice == 2:
                list_books()
            elif choice == 3:
                book_id = input("検索する図書IDを入力してください: ").strip()
                search_book(book_id)
            elif choice == 4:
                member_id = input("会員IDを入力してください: ").strip()
                name = input("名前を入力してください: ").strip()
                add_member(member_id, name)
            elif choice == 5:
                list_members()
            elif choice == 6:
                book_id = input("貸し出す図書IDを入力してください: ").strip()
                member_id = input("会員IDを入力してください: ").strip()
                borrow_book(book_id, member_id)
            elif choice == 7:
                list_borrowed_books()
            elif choice == 8:
                book_id = input("返却する図書IDを入力してください: ").strip()
                member_id = input("会員IDを入力してください: ").strip()
                return_book(book_id, member_id)
            elif choice == 9:
                calculate_fines()
            elif choice == 10:
                member_id = input("履歴を表示する会員IDを入力してください: ").strip()
                show_member_borrow_history(member_id)
            elif choice == 11:
                print("図書館管理システムを終了します。")
                break
            else:
                print("無効な選択です。1-11の数字を入力してください。")
        except ValueError as e:
            print(f"入力エラー: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

main()