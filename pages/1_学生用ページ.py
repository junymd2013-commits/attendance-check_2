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
    row = meibo[meibo["id"].astype(str) == str(student_id)]

    if len(row) == 0:
        st.error("この学籍番号は名簿に存在しません。")
    else:
        student_name = row.iloc[0]["name"]
        st.success(f"{student_name} さんですね。出席ボタンを押してください。")

        if st.button("出席する"):

            # attendance.csv 読み込み
            try:
                df = pd.read_csv("attendance.csv", encoding="utf-8-sig")
            except:
                df = pd.DataFrame(columns=["id", "name", "time"])

            # 今日の日付
            today = datetime.date.today().isoformat()

            # 今日の出席だけ抽出
            df_today = df[df["time"].str.startswith(today)]

            # 二重出席の防止（今日のみ）
            if str(student_id) in df_today["id"].astype(str).values:
                st.warning("今日はすでに出席済みです。")
            else:
                new_row = pd.DataFrame({
                    "id": [student_id],
                    "name": [student_name],
                    "time": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })

                df = pd.concat([df, new_row], ignore_index=True)

                # 保存（文字化けしない）
                df.to_csv("attendance.csv", index=False, encoding="utf-8-sig")

                st.success("出席を記録しました。")
