import streamlit as st
import pandas as pd

st.title("教員用：出席一覧確認ページ")

# --- パスワード保護 ---
password = st.text_input("パスワードを入力してください", type="password")
if password != "teacher123":   # ← パスワードは自由に変更可能
    st.stop()

# --- attendance.csv の読み込み ---
try:
    df = pd.read_csv("attendance.csv", encoding="utf-8")
except:
    df = pd.DataFrame(columns=["id", "name", "time"])
    st.warning("attendance.csv が存在しないため、空の一覧を表示します。")

# --- 出席一覧の表示 ---
st.subheader("出席一覧（ID順）")

if len(df) == 0:
    st.info("まだ出席データがありません。")
else:
    df_sorted = df.sort_values("id")
    st.dataframe(df_sorted, use_container_width=True)

# --- ダウンロードボタン ---
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="出席一覧をダウンロード (attendance.csv)",
    data=csv,
    file_name="attendance.csv",
    mime="text/csv"
)
