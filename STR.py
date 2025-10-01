import streamlit as st
import geopandas as gpd
import tempfile, zipfile, os
import leafmap.foliumap as leafmap
import pandas as pd
st.set_page_config(page_title="Hệ thống kiểm tra GML", page_icon="🌍", layout="wide")

# ================== CSS ẢNH NỀN ==================
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1502920514313-52581002a659");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.7);
        z-index: 0;
    }
    .block-container {
        position: relative;
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.title("🌍 Hệ thống Kiểm soát dữ liệu")
st.markdown("### 🚀 Ứng dụng hỗ trợ kiểm tra dữ liệu bản đồ hành chính")

# ================== SIDEBAR ==================
menu = ["🔎 Kiểm tra dữ liệu kiểm kê 2024",
        "🗂️ Kiểm tra tiếp biên GML trong đơn vị hành chính",
        "📁 Document Files",
        "ℹ️ About"]

choice = st.sidebar.radio("Menu:", menu)

if choice == menu[0]:
    st.subheader("🔎 Kiểm tra dữ liệu kiểm kê 2024")
    st.info("👉 Upload đủ các file `.shp`, `.dbf`, `.shx`, `.prj` để kiểm tra")

    uploaded_files = st.file_uploader(
        "Tải shapefile (có thể chọn nhiều shapefile cùng lúc)",
        type=["shp", "dbf", "shx", "prj"],
        accept_multiple_files=True
    )

    if uploaded_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Lưu tất cả file vào thư mục tạm
            for file in uploaded_files:
                file_path = os.path.join(tmpdir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

            # Tìm tất cả file .shp trong thư mục
            shp_files = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]

            if not shp_files:
                st.error("❌ Không tìm thấy file `.shp` nào")
            else:
                m = leafmap.Map(google_map="SATELLITE")
                all_gdfs = []

                for shp in shp_files:
                    shp_path = os.path.join(tmpdir, shp)
                    try:
                        gdf = gpd.read_file(shp_path)

                        # CRS VN2000 Cao Bằng (105°45′)
                        proj4 = (
                            "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 "
                            "+x_0=500000 +y_0=0 +ellps=WGS84 "
                            "+towgs84=-191.90441429,-39.30318279,-111.45032835,"
                            "-0.00928836,-0.01975479,0.00427372,0.252906278 "
                            "+units=m +no_defs"
                        )

                        if gdf.crs is None:
                            gdf = gdf.set_crs(proj4).to_crs(epsg=4326)
                        else:
                            gdf = gdf.to_crs(epsg=4326)

                        gdf = gdf[gdf.is_valid]
                        all_gdfs.append(gdf)

                        layer_name = shp.replace(".shp", "")
                        m.add_gdf(gdf, layer_name=layer_name, info_mode=None)

                        st.success(f"✅ Đọc thành công: {shp}, số đối tượng: {len(gdf)}")

                    except Exception as e:
                        st.error(f"❌ Lỗi khi đọc {shp}: {e}")

                # ===== 🔎 Tìm & Zoom theo thuộc tính =====
                if uploaded_files:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        # Lưu tất cả file vào thư mục tạm
                        for file in uploaded_files:
                            file_path = os.path.join(tmpdir, file.name)
                            with open(file_path, "wb") as f:
                                f.write(file.getbuffer())

                        # Tìm tất cả file .shp trong thư mục
                        shp_files = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]

                        if not shp_files:
                            st.error("❌ Không tìm thấy file `.shp` nào")
                        else:
                            m = leafmap.Map(google_map="SATELLITE")
                            all_gdfs = []

                            for shp in shp_files:
                                shp_path = os.path.join(tmpdir, shp)
                                try:
                                    gdf = gpd.read_file(shp_path)

                                    # CRS VN2000 Cao Bằng (105°45′)
                                    proj4 = (
                                        "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 "
                                        "+x_0=500000 +y_0=0 +ellps=WGS84 "
                                        "+towgs84=-191.90441429,-39.30318279,-111.45032835,"
                                        "-0.00928836,-0.01975479,0.00427372,0.252906278 "
                                        "+units=m +no_defs"
                                    )

                                    if gdf.crs is None:
                                        gdf = gdf.set_crs(proj4).to_crs(epsg=4326)
                                    else:
                                        gdf = gdf.to_crs(epsg=4326)

                                    gdf = gdf[gdf.is_valid]
                                    all_gdfs.append(gdf)

                                    layer_name = shp.replace(".shp", "")
                                    m.add_gdf(gdf, layer_name=layer_name, info_mode=None)

                                    st.success(f"✅ Đọc thành công: {shp}, số đối tượng: {len(gdf)}")

                                except Exception as e:
                                    st.error(f"❌ Lỗi khi đọc {shp}: {e}")

                            # ===== 🔎 Tìm & Zoom theo thuộc tính =====
                            if all_gdfs:
                                combined = pd.concat(all_gdfs, ignore_index=True)

                                st.subheader("🔎 Tìm và zoom tới thửa đất")

                                # --- Combobox chọn trường ---
                                field_name = st.selectbox(
                                    "Chọn trường dữ liệu để tìm:",
                                    options=[c for c in combined.columns if c != "geometry"]
                                )

                                # --- Input nhập giá trị ---
                                search_value = st.text_input("Nhập giá trị cần tìm:")

                                if search_value:
                                    target = combined[combined[field_name].astype(str) == search_value]

                                    if not target.empty:
                                        # Style thửa được tìm thấy (đỏ, viền đen, trong suốt)
                                        style_red = lambda x: {
                                            "color": "black",  # viền đen
                                            "weight": 2,
                                            "fillColor": "red",  # tô đỏ
                                            "fillOpacity": 0.6
                                        }

                                        # Thêm lớp highlight riêng
                                        m.add_gdf(
                                            target,
                                            layer_name=f"🔴 {field_name}={search_value}",
                                            style_function=style_red,
                                            info_mode=None
                                        )

                                        # Zoom đúng vào thửa tìm được
                                        m.zoom_to_gdf(target)
                                        st.success(f"✅ Đã zoom và highlight {field_name} = {search_value}")
                                    else:
                                        st.warning(f"⚠️ Không tìm thấy {field_name} = {search_value}")

                            m.to_streamlit(height=600)




elif choice == menu[1]:
    st.subheader("🗂️ Kiểm tra tiếp biên GML trong đơn vị hành chính")
    st.warning("⚠️ Chức năng đang phát triển...")

elif choice == menu[2]:
    st.subheader("📁 Document Files")
    st.write("Danh sách tài liệu, hướng dẫn sử dụng...")

else:
    st.subheader("ℹ️ About")
    st.write("Ứng dụng demo bằng **Streamlit**, hỗ trợ xử lý GML, bản đồ...")

# ================== FOOTER ==================
st.markdown("---")
st.markdown("💡 *Phát triển bởi Kim Dong | Streamlit + Python*")
