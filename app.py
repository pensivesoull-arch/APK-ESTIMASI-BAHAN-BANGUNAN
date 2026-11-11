import io
import math
import base64
from pathlib import Path
import pandas as pd
import streamlit as st
import core
import export as pdf_export

st.set_page_config(page_title="BuildEstimator", page_icon="🏗️", layout="wide")

# Tema visual Civil Engineering x anime science-adventure.
# Gambar hero berasal dari ilustrasi yang disediakan pengguna.
HERO_PATH = Path(__file__).parent / "assets" / "civil_engineering_anime_hero.jpg"
hero_b64 = base64.b64encode(HERO_PATH.read_bytes()).decode("utf-8") if HERO_PATH.exists() else ""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
  --ce-ink: #172b3a;
  --ce-navy: #102d42;
  --ce-blue: #176b87;
  --ce-cyan: #55b8cb;
  --ce-gold: #e5ad48;
  --ce-paper: #f4f1e8;
}}
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: linear-gradient(180deg, #edf5f5 0%, #f7f5ee 45%, #f1f4f2 100%); color: var(--ce-ink); }}
.block-container {{ padding-top: 1.15rem; padding-bottom: 3rem; max-width: 1500px; }}
[data-testid="stSidebar"] {{ background: linear-gradient(180deg, #102d42 0%, #173f53 100%); }}
[data-testid="stSidebar"] * {{ color: #eef7f7 !important; }}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section {{ background: rgba(255,255,255,.08); }}
.hero {{
  position: relative;
  overflow: hidden;
  min-height: 340px;
  border-radius: 22px;
  padding: 2.2rem 2.4rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: white;
  margin: .15rem 0 1.5rem 0;
  background-image: linear-gradient(90deg, rgba(7,27,43,.94) 0%, rgba(8,39,56,.78) 45%, rgba(8,39,56,.15) 100%), url("data:image/jpeg;base64,{hero_b64}");
  background-size: cover;
  background-position: center 42%;
  border: 1px solid rgba(255,255,255,.55);
  box-shadow: 0 14px 34px rgba(20,55,70,.18);
}}
.hero-kicker {{
  display: inline-block; width: fit-content; padding: .35rem .75rem;
  border: 1px solid rgba(255,255,255,.45); border-radius: 999px;
  color: #f7d58d; background: rgba(9,31,46,.45);
  font-size: .72rem; font-weight: 800; letter-spacing: .16em;
}}
.hero h1 {{
  color: #fff; font-family: 'Barlow Condensed', sans-serif;
  font-size: clamp(2.7rem, 6vw, 5.2rem); line-height: .95;
  letter-spacing: .035em; margin: .9rem 0 .55rem 0;
  text-shadow: 0 3px 18px rgba(0,0,0,.38);
}}
.hero p {{ color: #edf7f7; max-width: 670px; font-size: 1rem; line-height: 1.65; margin: 0; }}
.hero-rule {{ width: 88px; height: 5px; border-radius: 6px; background: var(--ce-gold); margin: 1rem 0; }}
.section-kicker {{
  color: #18728b; text-transform: uppercase; letter-spacing: .13em;
  font-size: .68rem; font-weight: 800; margin-bottom: -.45rem;
}}
h1, h2, h3 {{ color: #15394d; }}
h1, h2 {{ font-family: 'Barlow Condensed', sans-serif !important; letter-spacing: .015em; }}
h2 {{ font-size: 2rem !important; }}
h3 {{ font-size: 1.35rem !important; }}
div[data-testid="stMetric"] {{
  background: linear-gradient(145deg, #ffffff, #edf5f4);
  border: 1px solid #d4e3e2; padding: 15px 17px; border-radius: 15px;
  box-shadow: 0 5px 16px rgba(20,55,70,.06);
}}
div[data-testid="stMetric"] label {{ color: #527181 !important; font-weight: 700; }}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: #123c53; font-weight: 800; }}
.stButton > button, .stDownloadButton > button, button[kind="primary"] {{
  border-radius: 10px; border: 1px solid #176b87; font-weight: 700;
  transition: all .18s ease;
}}
.stButton > button[kind="primary"], button[kind="primary"] {{
  background: linear-gradient(100deg, #14536e, #1687a0); color: white;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
  border-color: #e0a63c; color: #123c53; transform: translateY(-1px);
}}
[data-baseweb="tab-list"] {{ gap: 6px; }}
button[data-baseweb="tab"] {{
  background: rgba(255,255,255,.72); border-radius: 9px 9px 0 0;
  padding: .65rem .9rem; font-weight: 700;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
  background: #dceff0; color: #12546b; border-bottom: 3px solid #e0a63c;
}}
[data-testid="stExpander"] {{ background: rgba(255,255,255,.72); border: 1px solid #d7e5e4; border-radius: 12px; }}
[data-testid="stDataFrame"], [data-testid="stDataEditor"] {{ border: 1px solid #d8e5e3; border-radius: 12px; overflow: hidden; }}
.stAlert {{ border-radius: 12px; }}
.small-note {{ color: #617b86; font-size: .82rem; }}
@media (max-width: 700px) {{
  .hero {{ min-height: 290px; padding: 1.4rem; background-position: 58% center; }}
}}
</style>
<div class="hero">
  <span class="hero-kicker">CIVIL ENGINEERING • SCIENCE • INNOVATION</span>
  <h1>BUILD ESTIMATOR</h1>
  <div class="hero-rule"></div>
  <p>Rancang, hitung, dan estimasikan kebutuhan material bangunan dengan pendekatan teknik sipil yang sistematis. Dari blueprint menuju konstruksi.</p>
</div>
""", unsafe_allow_html=True)

if "db" not in st.session_state:
    st.session_state.db = core.DB.copy()
    st.session_state.harga = core.HARGA.copy()
    st.session_state.waste = dict(core.WASTE)
    st.session_state.mode_harga = "rata-rata"
    st.session_state.P = None
    st.session_state.A = None
    st.session_state.H = None

def sync_engine():
    core.DB = st.session_state.db.copy()
    core.HARGA = st.session_state.harga.copy()
    core.WASTE = dict(st.session_state.waste)
    core.MODE_HARGA = st.session_state.mode_harga

def labelize(s):
    return str(s).replace("_"," ").capitalize()

def render_dict(d, prefix, depth=0):
    """Render dictionary input bertingkat; mengembalikan dictionary nilai terbaru."""
    result = {}
    for k, v in d.items():
        path = f"{prefix}_{k}"
        if isinstance(v, dict):
            with st.expander(labelize(k), expanded=(depth < 1)):
                result[k] = render_dict(v, path, depth+1)
        elif k == "jenis_atap":
            result[k] = st.selectbox(labelize(k), ["pelana","perisai"], index=["pelana","perisai"].index(v), key=path)
        elif isinstance(v, bool):
            result[k] = st.checkbox(labelize(k), value=v, key=path)
        elif isinstance(v, int):
            result[k] = st.number_input(labelize(k), value=int(v), step=1, min_value=0, key=path)
        elif isinstance(v, float):
            result[k] = st.number_input(labelize(k), value=float(v), step=0.1, min_value=0.0, format="%.3f", key=path)
        else:
            result[k] = st.text_input(labelize(k), value=str(v), key=path)
    return result

def make_excel():
    sync_engine()
    buf=io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        pd.DataFrame(list(st.session_state.P.items()),columns=["Data","Nilai"]).to_excel(xw,sheet_name="Identitas Proyek",index=False)
        pd.DataFrame(core.ratakan(st.session_state.A),columns=["Input","Nilai"]).to_excel(xw,sheet_name="Data Input",index=False)
        core.tabel_volume(st.session_state.H).to_excel(xw,sheet_name="Rekap Pekerjaan",index=False)
        core.tabel_detail(st.session_state.H).to_excel(xw,sheet_name="Detail Material",index=False)
        core.rekap_material(st.session_state.H).to_excel(xw,sheet_name="Rekap Material",index=False)
        st.session_state.db.to_excel(xw,sheet_name="Database Koefisien",index=False)
        pd.DataFrame(list(st.session_state.waste.items()),columns=["Material","Waste"]).to_excel(xw,sheet_name="Waste",index=False)
        st.session_state.harga.to_excel(xw,sheet_name="Harga Bahan",index=False)
    return buf.getvalue()

with st.sidebar:
    st.markdown("## 🏗️ ENGINEERING LAB")
    st.caption("BUILD ESTIMATOR • CIVIL SCIENCE EDITION")
    st.info("Koefisien awal masih berstatus asumsi prototipe. Verifikasi sebelum digunakan untuk RAB atau pelaksanaan konstruksi.")
    st.markdown("---")
    st.markdown("**Database**")
    up = st.file_uploader("Impor database Excel", type=["xlsx"], key="db_upload")
    if up is not None:
        try:
            xls=pd.ExcelFile(up)
            if "KOEFISIEN_BAHAN" in xls.sheet_names:
                newdb=pd.read_excel(up,sheet_name="KOEFISIEN_BAHAN")
                required=set(core.KOLOM_DB)
                if required.issubset(newdb.columns):
                    st.session_state.db=newdb[list(core.KOLOM_DB)].copy()
            if "HARGA" in xls.sheet_names:
                newh=pd.read_excel(up,sheet_name="HARGA")
                required={"material","spesifikasi","satuan","harga_min","harga_max","sumber"}
                if required.issubset(newh.columns):
                    st.session_state.harga=newh[list(required)].copy()
            st.success("Database berhasil dibaca. Periksa tab Database.")
        except Exception as e:
            st.error(f"Gagal membaca database: {e}")
    st.download_button("Unduh template database", data=open("data/template_database_material.xlsx","rb").read(),
                       file_name="template_database_material.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Project identity
st.header("1. Identitas proyek")
with st.form("project_form"):
    c1,c2,c3=st.columns(3)
    with c1:
        nama=st.text_input("Nama proyek",value="Rumah Contoh")
        pemilik=st.text_input("Pemilik",value="-")
        lantai=st.selectbox("Jumlah lantai",[1,2],index=1)
    with c2:
        panjang=st.number_input("Panjang bangunan (m)",min_value=0.1,value=10.0,step=.5)
        lebar=st.number_input("Lebar bangunan (m)",min_value=0.1,value=8.0,step=.5)
        tinggi1=st.number_input("Tinggi lantai 1 (m)",min_value=0.1,value=3.5,step=.1)
    with c3:
        tinggi2=st.number_input("Tinggi lantai 2 (m)",min_value=0.1,value=3.5,step=.1,disabled=(lantai==1))
        pondasi=st.selectbox("Jenis pondasi",["batu_kali","footplat"])
        dinding=st.selectbox("Jenis dinding",["bata_merah","bata_ringan"])
    c4,c5,c6=st.columns(3)
    with c4:
        rangka_atap=st.selectbox("Rangka atap",["baja_ringan","kayu"])
    with c5:
        penutup_atap=st.selectbox("Penutup atap",["genteng_keramik","spandek"])
    with c6:
        keramik=st.selectbox("Ukuran keramik",["30x30","40x40","60x60","custom"])
    ker_p=ker_l=50.0
    if keramik=="custom":
        x,y=st.columns(2)
        ker_p=x.number_input("Panjang keramik (cm)",min_value=.1,value=50.0)
        ker_l=y.number_input("Lebar keramik (cm)",min_value=.1,value=50.0)
    submitted=st.form_submit_button("Simpan identitas & buat input modul",type="primary",use_container_width=True)
if submitted:
    try:
        P={"nama":nama,"pemilik":pemilik,"lantai":lantai,"panjang":panjang,"lebar":lebar,"tinggi1":tinggi1,
           "tinggi2":tinggi2,"pondasi":pondasi,"dinding":dinding,"rangka_atap":rangka_atap,
           "penutup_atap":penutup_atap,"keramik":keramik}
        if keramik=="custom": P.update(keramik_p_cm=ker_p,keramik_l_cm=ker_l)
        st.session_state.P=core.validasi_proyek(P)
        st.session_state.A=core.default_input(st.session_state.P)
        st.session_state.H=None
        st.success("Identitas proyek tersimpan. Lanjutkan pengisian modul.")
    except Exception as e:
        st.error(str(e))

if st.session_state.P is not None:
    P=st.session_state.P
    st.divider()
    st.header("2. Input pekerjaan")
    st.caption("Nilai awal diturunkan dari identitas proyek. Periksa dan sesuaikan dengan gambar rencana serta kondisi lapangan.")
    module_names = {1:"Persiapan & Tanah",2:"Pondasi",3:"Struktur Beton",4:"Dinding",5:"Lantai",6:"Atap",7:"Finishing",8:"Utilitas"}
    tabs=st.tabs([f"{i}. {module_names[i]}" for i in range(1,9)])
    for i,tab in enumerate(tabs,1):
        with tab:
            key=f"m{i}"
            st.subheader(module_names[i])
            st.session_state.A[key]=render_dict(st.session_state.A[key],f"mod{i}")
            if st.button(f"Simpan input modul {i}",key=f"save_mod_{i}"):
                st.success(f"Input modul {i} tersimpan.")
    st.divider()
    st.header("3. Hasil estimasi")
    col1,col2=st.columns([1,3])
    with col1:
        if st.button("HITUNG SELURUH MODUL",type="primary",use_container_width=True):
            try:
                sync_engine()
                st.session_state.H=core.hitung(st.session_state.P,st.session_state.A)
                st.success("Perhitungan selesai.")
            except Exception as e:
                st.session_state.H=None
                st.error(f"Perhitungan belum berhasil: {e}")
    with col2:
        st.caption("Perhitungan menggunakan seluruh modul 1–8. Pastikan input sudah diperiksa sebelum menghitung.")
    if st.session_state.H is not None:
        H=st.session_state.H
        rec=core.rekap_material(H)
        m1,m2,m3=st.columns(3)
        m1.metric("Jumlah item pekerjaan",len(H.vol))
        m2.metric("Jenis material",len(rec))
        total=rec["biaya"].sum(min_count=1) if "biaya" in rec else None
        m3.metric("Estimasi biaya", "Belum tersedia" if pd.isna(total) else f"Rp {total:,.0f}".replace(",","."))

        t1,t2,t3=st.tabs(["Rekap pekerjaan","Detail kebutuhan","Rekap material & biaya"])
        with t1:
            st.dataframe(core.tabel_volume(H),use_container_width=True,hide_index=True)
        with t2:
            st.dataframe(core.tabel_detail(H),use_container_width=True,hide_index=True)
        with t3:
            st.dataframe(rec,use_container_width=True,hide_index=True)
            if rec["harga"].isna().all():
                st.warning("Harga bahan belum tersedia. Isi database harga agar estimasi biaya dapat dihitung.")
        d1,d2=st.columns(2)
        with d1:
            st.download_button("Unduh laporan Excel",data=make_excel(),file_name="Laporan_BuildEstimator.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",type="primary",use_container_width=True)
        with d2:
            st.download_button("Unduh laporan PDF",data=pdf_export.buat_pdf(st.session_state.P,H,rec),
                               file_name="Laporan_BuildEstimator.pdf",mime="application/pdf",use_container_width=True)

# Database editor
st.divider()
st.header("4. Pengaturan database")
dbtab,hargatab,wastetab=st.tabs(["Koefisien AHSP","Harga bahan","Waste"])
with dbtab:
    st.caption("Edit koefisien dan sumber rujukan. Jangan ubah status menjadi referensi resmi sebelum sumbernya diverifikasi.")
    edited=st.data_editor(st.session_state.db,use_container_width=True,num_rows="dynamic",key="editor_db")
    if st.button("Simpan perubahan koefisien"):
        st.session_state.db=edited.copy()
        st.success("Perubahan koefisien tersimpan pada sesi ini.")
with hargatab:
    mode=st.selectbox("Metode pemilihan harga",["min","max","rata-rata"],index=["min","max","rata-rata"].index(st.session_state.mode_harga))
    st.session_state.mode_harga=mode
    editedh=st.data_editor(st.session_state.harga,use_container_width=True,num_rows="dynamic",key="editor_harga")
    if st.button("Simpan perubahan harga"):
        st.session_state.harga=editedh.copy()
        st.success("Perubahan harga tersimpan pada sesi ini.")
with wastetab:
    wdf=pd.DataFrame([{"material":k,"waste":v} for k,v in st.session_state.waste.items()])
    editedw=st.data_editor(wdf,use_container_width=True,num_rows="dynamic",key="editor_waste")
    if st.button("Simpan perubahan waste"):
        try:
            st.session_state.waste={str(r["material"]):float(r["waste"]) for _,r in editedw.iterrows()}
            if any(v<0 for v in st.session_state.waste.values()): raise ValueError("Waste tidak boleh negatif.")
            st.success("Waste tersimpan pada sesi ini.")
        except Exception as e:
            st.error(str(e))

st.caption("BuildEstimator • Civil Engineering Science Lab — alat estimasi awal kebutuhan material. Hasil bukan pengganti gambar kerja, perhitungan struktur, survei lapangan, atau pemeriksaan tenaga ahli.")
