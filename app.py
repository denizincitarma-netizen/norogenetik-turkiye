import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="NöroGenetik Türkiye", page_icon="🧬", layout="wide")

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
        "gen": "TSC1 / TSC2",
        "ingilizce_ad": "Tuberous Sclerosis",
        "ozet": "Tuberoz Skleroz, hücre büyümesini kontrol eden TSC1 veya TSC2 genlerindeki mutasyonlar sonucu iyi huylu tümörlere ve sıklıkla epilepsiye yol açan genetik bir durumdur.",
        "dernek": "Nadir Hastalıklar Ağı",
    },
}

@st.cache_data(ttl=3600)
def klinik_arastirmalari_getir(ingilizce_hastalik_adi):
    url = "https://clinicaltrials.gov"
    params = {"query.cond": ingilizce_hastalik_adi, "filter.overallStatus": "RECRUITING", "pageSize": 10}
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
                "Ülkeler": ", ".join(ulkeler[:4]) if ulkeler else "Bilgi Yok",
                "Link": f"https://clinicaltrials.gov{kimlik.get('nctId', '')}",
            })
        return pd.DataFrame(calismalar)
    except Exception:
        return pd.DataFrame()

st.title("🧬 NöroGenetik Türkiye")
st.subheader("Nadir Nörogenetik Hastalıklar Bilgi ve Klinik Araştırma Erişim Platformu")
st.warning("⚠️ Bu platform yalnızca bilgilendirme amaçlıdır; tıbbi tanı veya tedavi yerine geçmez.")

col1, col2 = st.columns(2)
with col1:
    arama_turu = st.radio("Arama Yöntemi:", ["Hastalık Adına Göre", "Gen Koduna Göre"])
with col2:
    if arama_turu == "Hastalık Adına Göre":
        secilen_hastalik = st.selectbox("Hastalık Seçiniz:", list(HASTALIK_VERITABANI.keys()))
    else:
        gen_map = {f"{v['gen']} ({k})": k for k, v in HASTALIK_VERITABANI.items()}
        secilen_hastalik = gen_map[st.selectbox("Gen Kodu Seçiniz:", list(gen_map.keys()))]

bilgi = HASTALIK_VERITABANI[secilen_hastalik]
st.markdown(f"### 📋 {secilen_hastalik}")
c1, c2, c3 = st.columns(3)
c1.metric("Sorumlu Gen", bilgi["gen"])
c2.metric("Uluslararası Adı", bilgi["ingilizce_ad"])
c3.info(f"**Hasta Ağı:** {bilgi['dernek']}")
st.success(bilgi["ozet"])

st.markdown(f"#### 🌍 Güncel Klinik Araştırmalar ({bilgi['ingilizce_ad']})")
df = klinik_arastirmalari_getir(bilgi["ingilizce_ad"])
if not df.empty:
    st.dataframe(df, column_config={"Link": st.column_config.LinkColumn("İncele")}, use_container_width=True, hide_index=True)
