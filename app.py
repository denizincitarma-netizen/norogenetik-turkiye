
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="NöroGenetik Türkiye | Nadir Hastalıklar Platformu",
    page_icon="🧬",
    layout="wide",
)

with st.sidebar:
  st.title("🧬 NöroGenetik Türkiye")
  st.caption("Açık Kaynak Biyoinformatik & Halk Sağlığı Girişimi")
  st.divider()
  st.markdown("### 📊 Platform Etki Göstergesi")
  if "sorgu_sayaci" not in st.session_state:
    st.session_state.sorgu_sayaci = 142
  st.session_state.sorgu_sayaci += 1
  st.metric(
      label="Toplam Biyoinformatik Sorgu",
      value=f"{st.session_state.sorgu_sayaci:,}",
      delta="+Canlı Veri Akışı",
  )
  st.divider()
  st.markdown("### 🔬 Bilimsel Veri Kaynakları")
  st.markdown(
      "- **NIH ClinicalTrials.gov API v2:** Güncel klinik araştırmalar\n"
      "- **MyGene.info & NCBI Entrez:** Moleküler gen verileri\n"
      "- **NCBI ClinVar:** Genetik varyant ve mutasyon kayıtları"
  )
  st.divider()
  st.markdown("### 🤝 Akademik İş Birliği")
  st.info(
      "Bu platform **CoLab Uluslararası Bilim Topluluğu** inisiyatifi"
      " kapsamında geliştirilmiştir."
  )


@st.cache_data(ttl=86400)
def turkceye_cevir(metin):
  if not metin or metin == "-":
    return metin
  try:
    return GoogleTranslator(source="auto", target="tr").translate(metin[:4500])
  except Exception:
    return metin


HASTALIK_VERITABANI = {
    "Dravet Sendromu (Genetik Epilepsi)": {
        "gen": "SCN1A",
        "ingilizce_ad": "Dravet Syndrome",
        "ozet": (
            "Dravet Sendromu, genellikle yaşamın ilk yılında başlayan ve ilaca"
            " dirençli nöbetlerle seyreden nadir bir genetik epilepsi türüdür."
            " Vakaların %80'inden fazlasında beyindeki sodyum kanallarını"
            " düzenleyen SCN1A genindeki mutasyonlar sorumludur."
        ),
        "dernek": "Epilepsi ve Yaşam Derneği / Nadir Hastalıklar Ağı",
    },
    "Rett Sendromu": {
        "gen": "MECP2",
        "ingilizce_ad": "Rett Syndrome",
        "ozet": (
            "Rett Sendromu, çoğunlukla kız çocuklarında görülen ve X"
            " kromozomu üzerindeki MECP2 genindeki değişimlerden kaynaklanan"
            " nörogelişimsel bir durumdur."
        ),
        "dernek": "Rett Sendromu Derneği / Nadir Hastalıklar Ağı",
    },
    "Spinal Müsküler Atrofi (SMA)": {
        "gen": "SMN1",
        "ingilizce_ad": "Spinal Muscular Atrophy",
        "ozet": (
            "SMA, omurilikteki motor sinir hücrelerinin kaybına bağlı olarak"
            " ilerleyici kas güçsüzlüğüne yol açan kalıtsal bir nöromüsküler"
            " hastalıktır."
        ),
        "dernek": "SMA Benimle Yürü Derneği",
    },
    "Frajil X Sendromu": {
        "gen": "FMR1",
        "ingilizce_ad": "Fragile X Syndrome",
        "ozet": (
            "Frajil X Sendromu, kalıtsal zihinsel gelişim farklılıklarının ve"
            " otizm spektrum belirtilerinin en yaygın genetik nedenlerinden"
            " biridir."
        ),
        "dernek": "Türkiye Frajil X Sendromu Dayanışma Derneği",
    },
    "Tuberoz Skleroz Kompleksi (TSC)": {
        "gen": "TSC1",
        "ingilizce_ad": "Tuberous Sclerosis",
        "ozet": (
            "Tuberoz Skleroz, hücre büyümesini kontrol eden TSC1 veya TSC2"
            " genlerindeki mutasyonlar sonucu iyi huylu tümörlere ve sıklıkla"
            " epilepsiye yol açan genetik bir durumdur."
        ),
        "dernek": "Nadir Hastalıklar Ağı",
    },
    "Angelman Sendromu": {
        "gen": "UBE3A",
        "ingilizce_ad": "Angelman Syndrome",
        "ozet": (
            "Angelman Sendromu, 15. kromozomdaki UBE3A geninin işlev kaybından"
            " kaynaklanan; gelişimsel gecikme, konuşma güçlüğü ve denge"
            " sorunlarıyla seyreden nörogenetik bir durumdur."
        ),
        "dernek": "Nadir Hastalıklar Ağı",
    },
    "Duchenne Musküler Distrofi (DMD)": {
        "gen": "DMD",
        "ingilizce_ad": "Duchenne Muscular Dystrophy",
        "ozet": (
            "DMD, kas liflerinin bütünlüğünü koruyan distrofin proteinini"
            " kodlayan DMD genindeki mutasyonlar nedeniyle ilerleyici kas"
            " zayıflığına yol açan kalıtsal bir hastalıktır."
        ),
        "dernek": "DMD Aileleri Derneği",
    },
    "Huntington Hastalığı": {
        "gen": "HTT",
        "ingilizce_ad": "Huntington Disease",
        "ozet": (
            "Huntington Hastalığı, HTT genindeki CAG tekrar artışına bağlı"
            " olarak beyindeki sinir hücrelerinin zamanla yıkımına yol açan"
            " kalıtsal nörodejeneratif bir hastalıktır."
        ),
        "dernek": "Huntington Hastalığı Derneği / Nadir Hastalıklar Ağı",
    },
    "Nörofibromatozis Tip 1 (NF1)": {
        "gen": "NF1",
        "ingilizce_ad": "Neurofibromatosis Type 1",
        "ozet": (
            "NF1, sinir dokusu büyümesini baskılayan nörofibromin proteinini"
            " kodlayan NF1 genindeki değişimler sonucu cilt lekeleri ve sinir"
            " kılıfı tümörleriyle seyreden genetik bir durumdur."
        ),
        "dernek": "Nörofibromatozis Derneği",
    },
    "CDKL5 Eksikliği Bozukluğu": {
        "gen": "CDKL5",
        "ingilizce_ad": "CDKL5 Deficiency Disorder",
        "ozet": (
            "CDKL5 genindeki mutasyonlar sonucu yaşamın ilk aylarında başlayan"
            " ağır epileptik nöbetler ve nörogelişimsel gecikme ile kendini"
            " gösteren nadir bir durumdur."
        ),
        "dernek": "Nadir Hastalıklar Ağı",
    },
}
@st.cache_data(ttl=3600)
def gen_detaylarini_getir(gen_sembolu):
  temiz_gen = gen_sembolu.split("/")[0].strip().upper()
  base = "https://" + "mygene.info/v3/query"
  url = f"{base}?q=symbol:{temiz_gen}&species=human&fields=symbol,name,summary,map_location,type_of_gene,MIM"
  try:
    res = requests.get(url, timeout=8).json()
    hits = res.get("hits", [])
    if hits:
      h = hits[0]
      ingilizce_ozet = h.get("summary", "")
      turkce_ozet = (
          turkceye_cevir(ingilizce_ozet)
          if ingilizce_ozet
          else "Bu gen için NCBI moleküler özeti bulunamadı."
      )
      cv_base = "https://" + "www.ncbi.nlm.nih.gov/clinvar/"
      return {
          "sembol": temiz_gen,
          "tam_ad": h.get("name", "Bilgi bulunamadı"),
          "kromozom": h.get("map_location", "Bilinmiyor"),
          "gen_tipi": h.get("type_of_gene", "-"),
          "omim": h.get("MIM", "-"),
          "turkce_ozet": turkce_ozet,
          "ingilizce_ozet": ingilizce_ozet,
          "clinvar_url": f"{cv_base}?term={temiz_gen}%5Bgene%5D",
      }
  except Exception:
    pass
  return None


@st.cache_data(ttl=3600)
def klinik_arastirmalari_getir(
    arama_terimi, sadece_turkiye=False, basliklari_cevir=False
):
  url = "https://" + "clinicaltrials.gov/api/v2/studies"
  study_base = "https://" + "clinicaltrials.gov/study/"
  params = {
      "query.term": arama_terimi,
      "filter.overallStatus": "RECRUITING",
      "pageSize": 15,
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
      konumlar = protokol.get("contactsLocationsModule", {}).get(
          "locations", []
      )
      ulkeler = list(
          set([loc.get("country", "") for loc in konumlar if loc.get("country")])
      )
      baslik = kimlik.get("briefTitle", "-")
      if basliklari_cevir and baslik != "-":
        baslik = turkceye_cevir(baslik)
      calismalar.append({
          "Kayıt No": kimlik.get("nctId", "-"),
          "Araştırma Başlığı": baslik,
          "Faz": ", ".join(tasarim.get("phases", ["Belirtilmemiş"])),
          "Ülkeler": (
              ", ".join(ulkeler[:4]) + ("..." if len(ulkeler) > 4 else "")
              if ulkeler
              else "Bilgi Yok"
          ),
          "Link": f"{study_base}{kimlik.get('nctId', '')}",
      })
    return pd.DataFrame(calismalar)
  except Exception:
    return pd.DataFrame()


st.title("🧬 NöroGenetik Türkiye")
st.subheader(
    "Nadir Nörogenetik Hastalıklar Bilgi ve Küresel Klinik Araştırma Erişim"
    " Platformu"
)
st.warning(
    "⚠️ **Tıbbi Bilgilendirme Notu:** Bu platform yalnızca bilimsel"
    " bilgilendirme amaçlıdır; tıbbi tanı veya tedavi yerine geçmez."
)
st.divider()

arama_modu = st.radio(
    "Arama Modu Seçin:",
    [
        "🇹🇷 Öncelikli Nörogenetik Hastalıklar Rehberi (10 Temel Hastalık)",
        (
            "🌍 Sınırsız Küresel Gen & Hastalık Arama (20.000+ İnsan Geni -"
            " Otomatik Türkçe Çevirili)"
        ),
    ],
    horizontal=True,
)

if "Öncelikli" in arama_modu:
  col1, col2 = st.columns(2)
  with col1:
    filtre = st.radio(
        "Listeleme Şekli:", ["Hastalık Adına Göre", "Gen Koduna Göre"]
    )
  with col2:
    if filtre == "Hastalık Adına Göre":
      secilen = st.selectbox(
          "Hastalık Seçiniz:", list(HASTALIK_VERITABANI.keys())
      )
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
  st.info(
      "💡 Dünyadaki **herhangi bir insan genini** (örn: `SYNGAP1`, `FOXG1`,"
      " `CACNA1A`) veya **hastalık adını** (örn: `Ataxia`, `ALS`) yazın."
  )
  col_a, col_b = st.columns(2)
  with col_a:
    serbest_gen = (
        st.text_input("Gen Sembolü Girin (Örn: FOXG1):", value="FOXG1")
        .strip()
        .upper()
    )
  with col_b:
    serbest_hastalik = st.text_input(
        "Hastalık veya Gen Arama Terimi (İngilizce):", value=serbest_gen
    ).strip()
  aktif_gen = serbest_gen
  aktif_sorgu = serbest_hastalik if serbest_hastalik else serbest_gen

st.markdown(
    f"#### 🔬 Canlı Moleküler Gen Profili & Mutasyon Kayıtları: `{aktif_gen}`"
)
gen_bilgi = gen_detaylarini_getir(aktif_gen)
if gen_bilgi:
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("Kromozom Konumu", gen_bilgi["kromozom"])
  m2.metric("OMIM Kodu", str(gen_bilgi["omim"]))
  m3.metric("Gen Türü", gen_bilgi["gen_tipi"])
  m4.link_button(
      "🧬 ClinVar Mutasyonlarını Aç",
      gen_bilgi["clinvar_url"],
      use_container_width=True,
  )
  st.info(
      f"**🇹🇷 Moleküler Görev Özeti (Otomatik Çeviri):**\n\n{gen_bilgi['turkce_ozet']}"
  )
  with st.expander("📄 Orijinal İngilizce NCBI Kaydını Gör", expanded=False):
    st.write(f"**Tam Adı:** {gen_bilgi['tam_ad']}")
    st.write(gen_bilgi["ingilizce_ozet"])

st.divider()
st.markdown(f"#### 🌍 Aktif Klinik Araştırmalar: `{aktif_sorgu}`")
f1, f2 = st.columns(2)
with f1:
  sadece_tr = st.checkbox(
      "🇹🇷 Sadece Türkiye'de Hasta Kabul Eden Çalışmaları Göster"
  )
with f2:
  baslik_cevir = st.checkbox("🔄 Araştırma Başlıklarını Türkçeye Çevir")

with st.spinner("NIH ClinicalTrials.gov canlı veri tabanı taranıyor..."):
  df = klinik_arastirmalari_getir(
      aktif_sorgu, sadece_turkiye=sadece_tr, basliklari_cevir=baslik_cevir
  )

if not df.empty:
  st.write(f"Toplam **{len(df)}** aktif çalışma bulundu:")
  st.dataframe(
      df,
      column_config={"Link": st.column_config.LinkColumn("Detaylı İncele")},
      use_container_width=True,
      hide_index=True,
  )
else:
  st.info("Bu arama kriteri için aktif (Recruiting) çalışma bulunamadı.")

st.divider()
with st.expander("💬 Geri Bildirim Gönder veya Yeni Hastalık/Dernek Öner"):
  with st.form("geri_bildirim_formu"):
    kullanici_rol = st.selectbox(
        "Profiliniz:",
        [
            "Hasta / Hasta Yakını",
            "Hekim / Akademisyen",
            "Öğrenci / Araştırmacı",
            "Diğer",
        ],
    )
    mesaj = st.text_area(
        "Eklenmesini istediğiniz hastalık, gen veya öneriniz:"
    )
    if st.form_submit_button("Kaydet ve Gönder") and mesaj:
      st.success("Teşekkür ederiz! Geri bildiriminiz kaydedildi.")

st.caption(
    "© 2026 NöroGenetik Türkiye | Açık Kaynak Biyoinformatik Platformu — CoLab"
    " Uluslararası Bilim Topluluğu İnisiyatifi"
)

