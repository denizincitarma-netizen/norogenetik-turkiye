import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="NöroGenetik Türkiye", page_icon="🧬", layout="wide")

# Hazır Türkçe Rehber İçeren Öncelikli Hastalıklar
HASTALIK_VERITABANI = {
    "Dravet Sendromu (Genetik Epilepsi)": {
        "gen": "SCN1A",
        "ingilizce_ad": "Dravet Syndrome",
        "ozet": "Dravet Sendromu, genellikle yaşamın ilk yılında başlayan ve ilaca dirençli nöbetlerle seyreden nadir bir genetik epilepsi türüdür. Vakaların %80'inden fazlasında beyindeki sodyum kanallarını düzenleyen SCN1A genindeki mutasyonlar sorumludur.",
        "dernek": "Epilepsi ve Yaşam Derneği / Nadir Hastalıklar Ağı",
    },
    "Rett Sendromu": {
        "gen": "MECP2",
        "ingilizce_ad": "Rett Syndrome",
        "ozet": "Rett Sendromu, çoğunlukla kız çocuklarında görülen ve X kromozomu üzerindeki MECP2 genindeki değişimlerden kaynaklanan nörogelişimsel bir durumdur.",
        "dernek": "Rett Sendromu Derneği / Nadir Hastalıklar Ağı",
    },
    "Spinal Müsküler Atrofi (SMA)": {
        "gen": "SMN1",
        "ingilizce_ad": "Spinal Muscular Atrophy",
        "ozet": "SMA, omurilikteki motor sinir hücrelerinin kaybına bağlı olarak ilerleyici kas güçsüzlüğüne yol açan kalıtsal bir nöromüsküler hastalıktır.",
        "dernek": "SMA Benimle Yürü Derneği",
    },
    "Frajil X Sendromu": {
        "gen": "FMR1",
        "ingilizce_ad": "Fragile X Syndrome",
        "ozet": "Frajil X Sendromu, kalıtsal zihinsel gelişim farklılıklarının ve otizm spektrum belirtilerinin en yaygın genetik nedenlerinden biridir.",
        "dernek": "Türkiye Frajil X Sendromu Dayanışma Derneği",
    },
    "Tuberoz Skleroz Kompleksi (TSC)": {
        "gen": "TSC1",
        "ingilizce_ad": "Tuberous Sclerosis",
        "ozet": "Tuberoz Skleroz, hücre büyümesini kontrol eden TSC1 veya TSC2 genlerindeki mutasyonlar sonucu iyi huylu tümörlere ve sıklıkla epilepsiye yol açan genetik bir durumdur.",
        "dernek": "Nadir Hastalıklar Ağı",
    },
    "Angelman Sendromu": {
        "gen": "UBE3A",
        "ingilizce_ad": "Angelman Syndrome",
        "ozet": "Angelman Sendromu, 15. kromozomdaki UBE3A geninin işlev kaybından kaynaklanan; gelişimsel gecikme, konuşma güçlüğü, denge sorunları ve sık gülümseme ile karakterize nörogenetik bir durumdur.",
        "dernek": "Nadir Hastalıklar Ağı",
    },
    "Duchenne Musküler Distrofi (DMD)": {
        "gen": "DMD",
        "ingilizce_ad": "Duchenne Muscular Dystrophy",
        "ozet": "DMD, kas liflerinin bütünlüğünü koruyan distrofin proteinini kodlayan DMD genindeki mutasyonlar nedeniyle ilerleyici kas zayıflığına yol açan X'e bağlı kalıtsal bir hastalıktır.",
        "dernek": "DMD Aileleri Derneği",
    },
    "Huntington Hastalığı": {
        "gen": "HTT",
        "ingilizce_ad": "Huntington Disease",
        "ozet": "Huntington Hastalığı, HTT genindeki CAG tekrar artışına bağlı olarak beyindeki sinir hücrelerinin zamanla yıkımına yol açan kalıtsal nörodejeneratif bir hastalıktır.",
        "dernek": "Huntington Hastalığı Derneği / Nadir Hastalıklar Ağı",
    },
    "Nörofibromatozis Tip 1 (NF1)": {
        "gen": "NF1",
        "ingilizce_ad": "Neurofibromatosis Type 1",
        "ozet": "NF1, sinir dokusu büyümesini baskılayan nörofibromin proteinini kodlayan NF1 genindeki değişimler sonucu cilt lekeleri ve sinir kılıfı tümörleriyle seyreden genetik bir durumdur.",
        "dernek": "Nörofibromatozis Derneği",
    },
    "CDKL5 Eksikliği Bozukluğu": {
        "gen": "CDKL5",
        "ingilizce_ad": "CDKL5 Deficiency Disorder",
        "ozet": "CDKL5 genindeki mutasyonlar sonucu yaşamın ilk aylarında başlayan ağır epileptik nöbetler ve nörogelişimsel gecikme ile kendini gösteren nadir bir durumdur.",
        "dernek": "Nadir Hastalıklar Ağı",
    },
}

# Canlı MyGene.info Biyoinformatik API Fonksiyonu
@st.cache_data(ttl=3600)
def gen_detaylarini_getir(gen_sembolu):
    temiz_gen = gen_sembolu.split("/")[0].strip().upper()
    url = f"https://mygene.info:{temiz_gen}&species=human&fields=symbol,name,summary,map_location,type_of_gene,MIM"
    try:
        res = requests.get(url, timeout=8).json()
        hits = res.get("hits", [])
        if hits:
            h = hits[0]
            return {
                "tam_ad": h.get("name", "Bilgi bulunamadı"),
                "kromozom": h.get("map_location", "Bilinmiyor"),
                "gen_tipi": h.get("type_of_gene", "-"),
                "omim": h.get("MIM", "-"),
                "ncbi_ozet": h.get("summary", "NCBI moleküler özeti mevcut değil."),
            }
    except Exception:
        pass
    return None

# Canlı ClinicalTrials.gov API Fonksiyonu
@st.cache_data(ttl=3600)
def klinik_arastirmalari_getir(arama_terimi, sadece_turkiye=False):
    url = "https://clinicaltrials.gov"
    params = {
        "query.term": arama_terimi,
        "filter.overallStatus": "RECRUITING",
        "pageSize": 20,
    }
    if sadece_turkiye:
        params["query.locn"] = "Turkey"
    try:
        response = requests.get(url, params=params, timeout=10)
        veri = response.json()
        calismalar = []
        for study in veri.get("studies", []):
            protokol = study.get("protocolSection", {})
            kimlik = protokol.get("identificationModule", {})
            tasarim = protokol.get("designModule", {})
            konumlar = protokol.get("contactsLocationsModule", {}).get("locations", [])
            ulkeler = list(set([loc.get("country", "") for loc in konumlar if loc.get("country")]))
            calismalar.append({
                "Kayıt No": kimlik.get("nctId", "-"),
                "Araştırma Başlığı": kimlik.get("briefTitle", "-"),
                "Faz": ", ".join(tasarim.get("phases", ["Belirtilmemiş"])),
                "Ülkeler": ", ".join(ulkeler[:4]) + ("..." if len(ulkeler) > 4 else "") if ulkeler else "Bilgi Yok",
                "Link": f"https://clinicaltrials.gov{kimlik.get('nctId', '')}",
            })
        return pd.DataFrame(calismalar)
    except Exception:
        return pd.DataFrame()

# --- ARAYÜZ ---
st.title("🧬 NöroGenetik Türkiye")
st.subheader("Nadir Nörogenetik Hastalıklar Bilgi ve Küresel Klinik Araştırma Erişim Platformu")
st.warning("⚠️ **Tıbbi Bilgilendirme Notu:** Bu platform yalnızca bilimsel bilgilendirme amaçlıdır; tıbbi tanı veya tedavi yerine geçmez. Sonuçlarınızı mutlaka Tıbbi Genetik veya Çocuk Nörolojisi uzmanınızla değerlendiriniz.")

st.divider()

arama_modu = st.radio(
    "Arama Modu Seçin:",
    [
        "🇹🇷 Türkçe Rehberli Hastalık & Gen Listesi (10 Temel Hastalık)",
        "🌍 Sınırsız Küresel Gen / Hastalık Arama (Tüm İnsan Genomu - MyGene & NIH)",
    ],
    horizontal=True,
)

if "Türkçe Rehberli" in arama_modu:
    col1, col2 = st.columns([1, 2])
    with col1:
        filtre = st.radio("Listeleme Şekli:", ["Hastalık Adına Göre", "Gen Koduna Göre"])
    with col2:
        if filtre == "Hastalık Adına Göre":
            secilen = st.selectbox("Hastalık Seçiniz:", list(HASTALIK_VERITABANI.keys()))
        else:
            gen_map = {f"{v['gen']} — {k}": k for k, v in HASTALIK_VERITABANI.items()}
            secilen = gen_map[st.selectbox("Gen Seçiniz:", list(gen_map.keys()))]

    bilgi = HASTALIK_VERITABANI[secilen]
    aktif_gen = bilgi["gen"]
    aktif_sorgu = bilgi["ingilizce_ad"]

    st.markdown(f"### 📋 {secilen}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sorumlu Gen", aktif_gen)
    c2.metric("Uluslararası Tıbbi Adı", aktif_sorgu)
    c3.info(f"**Hasta Dayanışma Ağı:**\n{bilgi['dernek']}")
    st.success(bilgi["ozet"])

else:
    st.info("💡 Dünyadaki **herhangi bir insan genini** (örneğin: `SYNGAP1`, `FOXG1`, `CACNA1A`, `GRIN2A`, `KCNQ2`) veya **İngilizce hastalık adını** (örneğin: `Ataxia`, `ALS`, `Charcot-Marie-Tooth`) yazarak canlı moleküler veri ve klinik deneyleri sorgulayabilirsiniz.")
    col_a, col_b = st.columns(2)
    with col_a:
        serbest_gen = st.text_input("Gen Sembolü Girin (Örn: SYNGAP1):", value="SYNGAP1").strip().upper()
    with col_b:
        serbest_hastalik = st.text_input("İngilizce Hastalık veya Gen Arama Terimi:", value=serbest_gen).strip()
    aktif_gen = serbest_gen
    aktif_sorgu = serbest_hastalik if serbest_hastalik else serbest_gen

# Canlı Moleküler Veri Kartı (MyGene.info)
st.markdown(f"#### 🔬 Canlı Moleküler Gen Profili: `{aktif_gen}` (NCBI / MyGene.info)")
gen_bilgi = gen_detaylarini_getir(aktif_gen)
if gen_bilgi:
    m1, m2, m3 = st.columns(3)
    m1.metric("Kromozom Konumu", gen_bilgi["kromozom"])
    m2.metric("OMIM Kodu", str(gen_bilgi["omim"]))
    m3.metric("Gen Türü", gen_bilgi["gen_tipi"])
    with st.expander(f"🧬 {aktif_gen} Resmi Moleküler Fonksiyon Özeti (İngilizce - NCBI)", expanded=False):
        st.write(f"**Tam Adı:** {gen_bilgi['tam_ad']}")
        st.write(gen_bilgi["ncbi_ozet"])
else:
    st.caption("Bu terim için doğrudan tekil gen eşleşmesi bulunamadı veya genel hastalık araması yapılıyor.")

st.divider()

# Klinik Araştırmalar ve Türkiye Filtresi
st.markdown(f"#### 🌍 Aktif Klinik Araştırmalar: `{aktif_sorgu}`")
sadece_tr = st.checkbox("🇹🇷 Sadece Türkiye'de Hasta Kabul Eden Çalışmaları Göster")

with st.spinner("NIH ClinicalTrials.gov canlı veri tabanı taranıyor..."):
    df = klinik_arastirmalari_getir(aktif_sorgu, sadece_turkiye=sadece_tr)

if not df.empty:
    st.write(f"Toplam **{len(df)}** aktif (hasta kabul eden) çalışma bulundu:")
    st.dataframe(df, column_config={"Link": st.column_config.LinkColumn("Detaylı İncele")}, use_container_width=True, hide_index=True)
else:
    if sadece_tr:
        st.warning("Bu hastalık/gen için şu an Türkiye merkezli aktif (Recruiting) çalışma görünmüyor. Yukarıdaki kutucuğun işaretini kaldırarak Avrupa ve ABD'deki çalışmaları görebilirsiniz.")
    else:
        st.info("Bu arama terimi için şu an hasta kabul eden (Recruiting) çalışma bulunamadı.")

st.divider()
st.caption("Açık Kaynak Biyoinformatik Platformu | CoLab Uluslararası Bilim Topluluğu İnisiyatifi")
