import time
import os
import pandas as pd
import geopandas as gpd

import tkinter as tk
from tkinter import filedialog
import pathlib
import streamlit as st
#st.write('Daysdau')
#st.title('Daysdau')
#st.header('Daysdau')
#st.caption('Daysdau')
#st.text('Daysdau')
#st.code('Daysdau')

#ten = st.text_input("nhap vao ten ban")
#st.write(ten)


#text_download = 'Tep tin tai ve'
#st.download_button("Download",text_download)
#with st.spinner("Đang chạy"):

    #st.download_button(
            #label = "tai_file",
            #data = "Phường Hương Văn-Phường Tứ Hạ.xlsx",
            #file_name = "Phường Hương Văn-Phường Tứ Hạ.xlsx",
            #mime ="xlsx/xlsx"
        #)
    #time.sleep(1)
def intersection(a):
    df = pd.read_excel("DonViHanhChinhTemplate.xls")
    for j in a:
        st.write("Đang kiểm tra ", str(j))
        for k in a:
            try:
                if j != k:
                    g1 = gpd.read_file(j)
                    g2 = gpd.read_file(k)
                    inter = gpd.overlay(g1, g2, how='intersection')

                    inter['dien tich chong lan'] = inter.area
                    columns = ['maXa_1', 'soHieuToBanDo_1', 'soThuTuThua_1', 'maLoaiDat_1', 'dienTich_1',
                               'maXa_2', 'soHieuToBanDo_2', 'soThuTuThua_2', 'maLoaiDat_2', 'dienTich_2',
                               'dien tich chong lan', 'geometry']
                    pf = pd.DataFrame(inter, columns=columns)

                    if pf.shape[0] != 0:
                        data = df.loc[df['Mã Xã'] == int(g1.iloc[0, 1])]
                        print(data.iloc[0, 0])
                        data1 = df.loc[df['Mã Xã'] == int(g2.iloc[0, 1])]
                        pf = pf.loc[pf['dien tich chong lan'] >= 0.0000000000000000000001]
                        pf.loc[pf['maXa_1'] == int(g1.iloc[0, 1]), 'maXa_1'] = str(data.iloc[0, 0])
                        pf.loc[pf['maXa_2'] == int(g2.iloc[0, 1]), 'maXa_2'] = str(data1.iloc[0, 0])

                        with pd.ExcelWriter(str(data.iloc[0, 0]) + '-' + str(
                                data1.iloc[0, 0]) + ".xlsx") as writer:
                                    pf.to_excel(writer)
                        with open(str(data.iloc[0, 0]) + '-' + str(data1.iloc[0, 0]) + ".xlsx", "rb") as file:
                            st.download_button(
                                label="tải file tiếp biên:",
                                data=file,
                                file_name=str(data.iloc[0, 0]) + '-' + str(data1.iloc[0, 0]) + ".xlsx",
                                mime="xlsx")
            except:
                pass




def upload():
    uploaded_files = st.file_uploader("Choose a GML file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
         bytes_data = uploaded_file.read()
         st.write("filename:", uploaded_file.name)

def main():

    st.title("KIỂM TRA CSDL_GML")

    menu = ["Kiểm tra tiếp biên GML thửa đất","Dataset","DocumentFiles","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Kiểm tra tiếp biên GML thửa đất":
        data = []
        #root = tk.Tk()
        #root.withdraw()
        # Make folder picker dialog appear on top of other windows
        #root.wm_attributes('-topmost', 1)
        # Folder picker button
        #st.title('Kiểm tra tiếp biên giữa các đơn vị hành chính')
        #st.write('Please select a folder:')
        #clicked = st.button('Folder Picker')
        #if clicked:
            #dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
            #intersection(dirname)
        st.subheader("Image")

        uploaded_files = st.file_uploader("Choose a GML file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)

            with open(os.path.join(uploaded_file.name), "wb") as f:
                f.write((uploaded_file).getbuffer())
            st.success("File uploaded thành công")
            data.append(uploaded_file.name)
        intersection(data)
    elif choice == "Dataset":
        st.subheader("Dataset")

    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles")
if __name__ == "__main__":
    main()