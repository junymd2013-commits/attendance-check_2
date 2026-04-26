import streamlit as st
import pandas as pd
import datetime

st.title("学生用：出席入力ページ")

# 名簿読み込み
try:
    meibo = pd.read_csv("meibo_1.csv", encoding="utf-8")
except:
    try:
        meibo = pd.read_csv("meibo_1.csv", encoding="cp932")
    except:
        st.error("名簿ファイル（meibo_1.csv）を読み込めませんでした。文字コードを UTF-8 または Shift-JIS にしてください。")
        st.stop()

# 学籍番号入力
student_id = st.text_input("学籍番号を入力してください")

if student_id:
    # 名簿から名前を検索
    row = meibo[meibo["id"].astype(str) == str(student_id)]

    if len(row) == 0:
        st.error("この学籍番号は名簿に存在しません。")
    else:
        student_name = row.iloc[0]["name"]
        st.success(f"{student_name} さんですね。出席ボタンを押してください。")

        # 出席ボタン
        if st.button("出席する"):

            # --- attendance.csv を読み込み（なければ作成） ---
            try:
                df = pd.read_csv("attendance.csv", encoding="utf-8")
            except:
                df = pd.DataFrame(columns=["id", "name", "time"])

            # --- 二重出席の防止 ---
            if str(student_id) in df["id"].astype(str).values:
                st.warning("この学籍番号はすでに出席済みです。")
            else:
                # 新しい出席データを追加
                new_row = pd.DataFrame({
                    "id": [student_id],
                    "name": [student_name],
                    "time": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })

                df = pd.concat([df, new_row], ignore_index=True)

                # 保存
                df.to_csv("attendance.csv", index=False, encoding="utf-8-sig")

                st.success("出席を記録しました。")
