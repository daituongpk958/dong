import time
import os
import pandas as pd
import geopandas as gpd


import streamlit as st
global dataframe1

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






def upload():
    uploaded_files = st.file_uploader("Choose a GML file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
         bytes_data = uploaded_file.read()
         st.write("filename:", uploaded_file.name)

def main():
    global df
    st.title("KIỂM TRA CSDL_GML")
    def convert_df(c):
        return c.to_csv().encode('utf-8-sig')
    def chayhuy(b):
        for j in b:

            st.write("Đang kiểm tra ", str(j))


            try:
                    # PATH = 'D:/intersection.SHP'
                    # if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
                    # os.remove('D:/intersection.SHP')

                    data_temp = gpd.read_file(j)
                    print(data_temp.iloc[2, 1])
                    data_overlaps = gpd.GeoDataFrame(crs=data_temp.crs)
                    data_temp["ID"] = data_temp.index + 1
                    print(data_temp.shape[0])
                    for index, row in data_temp.iterrows():
                        try:
                            print(index)
                            data_temp1 = data_temp.loc[data_temp.ID != row.ID,]
                            # check if intersection occured
                            overlaps = data_temp1[data_temp1.geometry.overlaps(row.geometry)]['ID'].tolist()
                            if len(overlaps) > 0:

                                temp_list = []
                                # compare the area with threshold
                                for i in overlaps:

                                    temp_area = gpd.overlay(data_temp.loc[data_temp.ID == i,], data_temp
                                                            .loc[data_temp.ID == row.ID,], how='intersection')
                                    temp_area = temp_area.loc[temp_area.geometry.area >= 0.00000000000000001]
                                    if temp_area.shape[0] > 0:
                                        data_overlaps = gpd.GeoDataFrame(
                                            pd.concat([temp_area, data_overlaps], ignore_index=True), crs=data_temp.crs)
                                        # data_overlaps.to_file(os.path.dirname(j) + "/" + c.split(".")[0] + ".SHP")
                                        # k = gpd.read_file(os.path.dirname(j) + "/" + c.split(".")[0] + ".SHP")

                        except:
                            index = index + 1
                    if data_overlaps.shape[0] != 0:
                        data_overlaps['dien tich chong lan'] = round(data_overlaps.area, 13)
                        columns = ['maXa_1', 'soHieuToBanDo_1', 'soThuTuThua_1', 'maLoaiDat_1', 'dienTich_1',
                                   'maXa_2', 'soHieuToBanDo_2', 'soThuTuThua_2', 'maLoaiDat_2', 'dienTich_2',
                                   'dien tich chong lan', 'geometry']
                        data_overlaps = pd.DataFrame(data_overlaps, columns=columns)
                        data_overlaps = gpd.GeoDataFrame(data_overlaps)
                        print(data_overlaps)
                        # k.drop_duplicates(subset = ['dien tich chong lan'])
                        data = df.loc[df['Mã Xã'] == int(data_temp.iloc[0, 1])]
                        #with pd.ExcelWriter(os.path.dirname(j) + "/" + str(data.iloc[0, 0]) + ".xlsx") as writer:data_overlaps.to_excel(writer)
                        csv = convert_df(data_overlaps)
                        st.download_button(
                            "Press to Download: " + str(data.iloc[0, 0]),
                            csv,
                            str(data.iloc[0, 0]) + ".csv",
                            "text/csv",
                            key='download-csv'
                        )
                        # filename_read = 'os.path.dirname(j) + "/" + c.split(".")[0] + ".xlsx"'
                        # wb = xw.Book(filename_read)
                        # sht = wb.sheets[0]
            except:
                    pass
    def intersection(a):
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

                            csv = convert_df(pf)
                            st.download_button(
                                "Press to Download: "+str(data.iloc[0, 0]) + '-' + str(data1.iloc[0, 0]),
                                csv,
                                str(data.iloc[0, 0]) + '-' + str(data1.iloc[0, 0])+".csv",
                                "text/csv",
                                key='download-csv'
                            )
                            #with pd.ExcelWriter(str(data.iloc[0, 0]) + '-' + str(data1.iloc[0, 0]) + ".xlsx") as writer:
                                #pf.to_excel(writer)
                            #with open(str(data.iloc[0, 0]) + '-' + str(data1.iloc[0, 0]) + ".xlsx", "rb") as file:
                                #st.download_button(
                                    #label="tải file tiếp biên:",
                                     #data=file,
                                    #file_name=str(data.iloc[0, 0]) + '-' + str(data1.iloc[0, 0]) + ".xlsx",
                                    #mime="xlsx")

                except:
                    pass




    menu = ["Kiểm tra tiếp biên GML thửa đất","Kiểm tra tiếp biên các GML trong đơn vị hành chính","DocumentFiles","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    maxa = st.file_uploader("Choose a file")
    if maxa is not None:
        global df
        # To read file as bytes:
        dataframe1 = pd.read_excel(maxa)
        st.dataframe(dataframe1)
        df = dataframe1
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
        #st.subheader("Image")

        uploaded_files = st.file_uploader("Choose a GML file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)

            with open(os.path.join(uploaded_file.name), "wb") as f:
                f.write((uploaded_file).getbuffer())
            st.success("File uploaded thành công")
            data.append(uploaded_file.name)

        intersection(data)
    elif choice == "Kiểm tra tiếp biên các GML trong đơn vị hành chính":
        data = []

        # root = tk.Tk()
        # root.withdraw()
        # Make folder picker dialog appear on top of other windows
        # root.wm_attributes('-topmost', 1)
        # Folder picker button
        # st.title('Kiểm tra tiếp biên giữa các đơn vị hành chính')
        # st.write('Please select a folder:')
        # clicked = st.button('Folder Picker')
        # if clicked:
        # dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
        # intersection(dirname)
        # st.subheader("Image")

        uploaded_files = st.file_uploader("Choose a GML file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)

            with open(os.path.join(uploaded_file.name), "wb") as f:
                f.write((uploaded_file).getbuffer())
            st.success("File uploaded thành công")
            data.append(uploaded_file.name)

        chayhuy(data)

    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles")
if __name__ == "__main__":
    main()