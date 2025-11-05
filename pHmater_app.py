#インポート部分
import streamlit as st #WebアプリのGUI作製用ライブラリ
import pandas as pd #CSVファイルや表形式を扱うためのライブラリ
import os #ファイル操作やパス処理に使用
import csv #CSV読み書き用の標準ライブラリ
import io #メモリ上でファイルのようにふるまう(文字列やバイナリの操作)
import zipfile #Zip圧縮操作用(今回のコードでは未使用)

#タイトルと説明の表示
st.title("📊 pHメーターデータ自動CSV変換ツール") #Webアプリの大見出し
st.write("USB内のフォルダを選択して、`.pHdx` ファイルをCSVに変換します。") #説明文の表示

# フォルダ・ファイルをアップロード
uploaded_files = st.file_uploader( #st.file_uploader( →ファイル選択ボタンを作る
    "pHdxファイルをフォルダごと選択（複数選択可）",
    accept_multiple_files=True, #複数のファイルを同時に選択出来る
    type=["pHdx"] #拡張子の.pHdxと書いてるファイルのみ選択可能
)

#ファイルの読み込みとデータの整形
if uploaded_files:
    all_data = []
    for file in uploaded_files:
        content = file.getvalue().decode("utf-8").splitlines() #file.getvalue()→アップロードされたファイルの中身をバイト列で取得
#decode("utf-8")→UFE-8文字列に変換，splitlines()→行ごとのリストに分割
        
        reader = csv.reader(content) #CSV形式として読みこむ
        for row in reader:
            cleaned = [cell.strip() for cell in row] #前後の空白を削除
            all_data.append([file.name] + cleaned) #行データの先頭にファイル名を追加してall_dataに保存

    # DataFrameに変換
    df = pd.DataFrame(all_data) #all_dataを表形式に変換
    st.write("✅ 変換結果プレビュー：")
    st.dataframe(df.head(10)) #Webアプリ上で表形式で表示，上から10行だけ表示してプレビュー

    # CSVバイナリに変換，st.download_button(でダウンロード出来るようにする
    csv_buffer = io.StringIO() #メモリ上にファイルのようなものを作る
    df.to_csv(csv_buffer, index=False) #CSV形式で書き込み
    csv_data = csv_buffer.getvalue() #CSV文字列を取得

    # ダウンロードボタン，変換したCSVファイルをPCに保存
    st.download_button( #Web上でダウンロードボタンを作る
        label="📥 CSVとして保存", #ボタンに表示する文字
        data=csv_data,　#ダウンロードするデータ
        file_name="converted_phdx_data.csv", #保存時のファイル名
        mime="text/csv" #CSVファイルとして扱う
    )
