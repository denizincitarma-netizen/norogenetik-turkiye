
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="NöroGenetik Türkiye | Biyoinformatik & Klinik Araştırma Platformu",
    page_icon="🧬",
    layout="wide",
)

with st.sidebar:
  st.title("🧬 NöroGenetik Türkiye")
  st.caption(
      "Nadir Nörogenetik Hastalıklar Biyoinformatik ve Klinik Araştırma"
      " Erişim Platformu"
  )
  st.divider()
  st.markdown("### 📡 Sistem Altyapısı")
  st.metric(label="Kapsanan İnsan Geni", value="20.000+", delta="HGNC / NCBI")
  st.metric(
      label="Klinik Veri Kaynağı", value="NIH v2 API", delta="Gerçek Zamanlı"
  )
  st.divider()
  st.markdown("### 👩‍🔬 Kurucu & İletişim")
  st.markdown(
      "**Deniz İnci Tarma**\n\n"
      "CoLab Uluslararası Bilim Topluluğu İnisiyatifi\n\n"
      "📧 [denizinci.tarma@gmail.com](mailto:denizinci.tarma@gmail.com)\n\n"
      "📞 +90 530 447 73 33\n\n"
      "🔗 [GitHub Açık Kaynak Deposu](https://github.com)"
  )
  st.divider()
  st.caption("Sürüm: v1.0 (Açık Erişim) | MIT Lisansı")

HASTALIK_VERITABANI = {
    "Dravet Sendromu (Genetik Epilepsi)": {
        "gen": "SCN1A",
        "ingilizce_ad": "Dravet Syndrome",
        "kalitim": "Otozomal Dominant (Çoğunlukla de novo)",
        "ozet": (
            "Dravet Sendromu, genellikle yaşamın ilk yılında başlayan ve ilaca"
            " dirençli nöbetlerle seyreden nadir bir genetik epilepsi türüdür."
            " Vakaların %80'inden fazlasında beyindeki voltaj kapılı sodyum"
            " kanallarını kodlayan SCN1A genindeki patojenik varyantlar"
            " sorumludur."
        ),
        "dernek": "Epilepsi ve Yaşam Derneği / Nadir Hastalıklar Ağı",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
    "Rett Sendromu": {
        "gen": "MECP2",
        "ingilizce_ad": "Rett Syndrome",
        "kalitim": "X'e Bağlı Dominant",
        "ozet": (
            "Rett Sendromu, çoğunlukla kız çocuklarında görülen ve X"
            " kromozomu üzerindeki MECP2 genindeki değişimlerden kaynaklanan"
            " nörogelişimsel bir bozukluktur. Sinir hücreleri arasındaki"
            " sinaptik iletişimi ve gen ekspresyonunu düzenleyen MeCP2"
            " proteinini etkiler."
        ),
        "dernek": "Rett Sendromu Derneği / Nadir Hastalıklar Ağı",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
    "Spinal Müsküler Atrofi (SMA)": {
        "gen": "SMN1",
        "ingilizce_ad": "Spinal Muscular Atrophy",
        "kalitim": "Otozomal Resesif",
        "ozet": (
            "SMA, omurilikteki ön boynuz motor sinir hücrelerinin kaybına bağlı"
            " olarak ilerleyici kas güçsüzlüğüne yol açan kalıtsal bir"
            " nöromüsküler hastalıktır. SMN1 genindeki delesyon veya mutasyonlar"
            " sonucu SMN proteini üretilemez."
        ),
        "dernek": "SMA Benimle Yürü Derneği",
        "dernek_url": "https://smabenimleyuru.org.tr",
    },
    "Frajil X Sendromu": {
        "gen": "FMR1",
        "ingilizce_ad": "Fragile X Syndrome",
        "kalitim": "X'e Bağlı",
        "ozet": (
            "Frajil X Sendromu, kalıtsal zihinsel gelişim farklılıklarının ve"
            " otizm spektrum belirtilerinin en sık tek gen nedenidir. X"
            " kromozomundaki FMR1 geninde CGG üçlü nükleotid tekrar artışıyla"
            " FMRP proteininin sentezi baskılanır."
        ),
        "dernek": "Türkiye Frajil X Sendromu Dayanışma Derneği",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
    "Tuberoz Skleroz Kompleksi (TSC)": {
        "gen": "TSC1",
        "ingilizce_ad": "Tuberous Sclerosis",
        "kalitim": "Otozomal Dominant",
        "ozet": (
            "Tuberoz Skleroz, mTOR yolağını baskılayan TSC1 (hamartin) veya"
            " TSC2 (tuberin) genlerindeki mutasyonlar sonucu beyin, cilt,"
            " böbrek ve kalpte iyi huylu hamartomlarla seyreden genetik bir"
            " sendromdur."
        ),
        "dernek": "Nadir Hastalıklar Ağı",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
    "Angelman Sendromu": {
        "gen": "UBE3A",
        "ingilizce_ad": "Angelman Syndrome",
        "kalitim": "Genomik İmprinting (15q11-q13)",
        "ozet": (
            "Angelman Sendromu, 15. kromozomdaki maternal UBE3A geninin işlev"
            " kaybından kaynaklanan; ağır gelişimsel gecikme, konuşma yokluğu"
            " ve ataksi ile karakterize nörogenetik bir durumdur."
        ),
        "dernek": "Nadir Hastalıklar Ağı",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
    "Duchenne Musküler Distrofi (DMD)": {
        "gen": "DMD",
        "ingilizce_ad": "Duchenne Muscular Dystrophy",
        "kalitim": "X'e Bağlı Resesif",
        "ozet": (
            "DMD, kas hücresi zarının mekanik bütünlüğünü koruyan distrofin"
            " proteinini kodlayan DMD genindeki mutasyonlar nedeniyle erken"
            " çocuklukta başlayan ilerleyici kas yıkımıyla seyreder."
        ),
        "dernek": "DMD Aileleri Derneği",
        "dernek_url": "https://dmd.org.tr",
    },
    "Huntington Hastalığı": {
        "gen": "HTT",
        "ingilizce_ad": "Huntington Disease",
        "kalitim": "Otozomal Dominant",
        "ozet": (
            "Huntington Hastalığı, HTT genindeki CAG tekrar genişlemesine"
            " bağlı olarak striatumdaki nöronların ilerleyici dejenerasyonuna"
            " yol açan kalıtsal bir nörodejeneratif hastalıktır."
        ),
        "dernek": "Huntington Hastalığı Derneği / Nadir Hastalıklar Ağı",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
    "Nörofibromatozis Tip 1 (NF1)": {
        "gen": "NF1",
        "ingilizce_ad": "Neurofibromatosis Type 1",
        "kalitim": "Otozomal Dominant",
        "ozet": (
            "NF1, RAS sinyal yolağını düzenleyen nörofibromin tümör baskılayıcı"
            " proteinini kodlayan NF1 genindeki mutasyonlar sonucu ciltte sütlü"
            " kahve lekeleri ve nörofibromlarla seyreder."
        ),
        "dernek": "Nörofibromatozis Derneği",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
    "CDKL5 Eksikliği Bozukluğu": {
        "gen": "CDKL5",
        "ingilizce_ad": "CDKL5 Deficiency Disorder",
        "kalitim": "X'e Bağlı Dominant",
        "ozet": (
            "CDKL5 genindeki patojenik varyantlar sonucu yaşamın ilk"
            " haftalarında başlayan dirençli epileptik ensefalopati ve ağır"
            " nörogelişimsel gecikme ile kendini gösteren nadir bir durumdur."
        ),
        "dernek": "Nadir Hastalıklar Ağı",
        "dernek_url": "https://nadirhastaliklaragi.org.tr",
    },
}
@st.cache_data(ttl=3600)
def gen_detaylarini_getir(gen_sembolu):
  temiz_gen = gen_sembolu.strip().upper()
  base = "https://" + "mygene.info/v3/query"
  url = f"{base}?q=symbol:{temiz_gen}&species=human&fields=symbol,name,summary,map_location,type_of_gene,MIM"
  try:
    res = requests.get(url, timeout=8).json()
    hits = res.get("hits", [])
    if hits:
      h = next(iter(hits))
      cv_base = "https://" + "www.ncbi.nlm.nih.gov/clinvar/"
      omim_id = str(h.get("MIM", ""))
      return {
          "sembol": temiz_gen,
          "tam_ad": h.get("name", "Bilgi bulunamadı"),
          "kromozom": h.get("map_location", "Bilinmiyor"),
          "gen_tipi": h.get("type_of_gene", "-"),
          "omim": omim_id if omim_id else "-",
          "ncbi_ozet": h.get("summary", "NCBI moleküler özeti mevcut değil."),
          "clinvar_url": f"{cv_base}?term={temiz_gen}%5Bgene%5D",
      }
  except Exception:
    pass
  return None


@st.cache_data(ttl=3600)
def klinik_arastirmalari_getir(arama_terimi, sadece_turkiye=False):
  url = "https://" + "clinicaltrials.gov/api/v2/studies"
  study_base = "https://" + "clinicaltrials.gov/study/"
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
      konumlar = protokol.get("contactsLocationsModule", {}).get(
          "locations", []
      )
      ulkeler = list(
          set([loc.get("country", "") for loc in konumlar if loc.get("country")])
      )
      calismalar.append({
          "Kayıt No (NCT)": kimlik.get("nctId", "-"),
          "Klinik Araştırma Başlığı": kimlik.get("briefTitle", "-"),
          "Çalışma Fazı": ", ".join(tasarim.get("phases", ["Belirtilmemiş"])),
          "Katılımcı Ülkeler": (
              ", ".join(ulkeler[:4]) + ("..." if len(ulkeler) > 4 else "")
              if ulkeler
              else "Bilgi Yok"
          ),
          "Resmi Kayıt": f"{study_base}{kimlik.get('nctId', '')}",
      })
    return pd.DataFrame(calismalar)
  except Exception:
    return pd.DataFrame()


st.title("🧬 NöroGenetik Türkiye")
st.markdown(
    "**Nadir Nörogenetik Hastalıklar İçin Açık Erişimli Biyoinformatik ve"
    " Küresel Klinik Araştırma Eşleştirme Platformu**"
)

tab_sorgu, tab_metodoloji, tab_hakkinda = st.tabs([
    "🔍 Gen & Klinik Araştırma Sorgulama",
    "🔬 Bilimsel Metodoloji & API Mimarisi",
    "⚖️ Tıbbi Sorumluluk & İletişim",
])

with tab_sorgu:
  st.warning(
      "⚠️ **Tıbbi Bilgilendirme Uyarısı:** Bu platform yalnızca bilimsel"
      " farkındalık ve eğitim amaçlıdır; tıbbi tanı, genetik danışmanlık veya"
      " tedavi önerisi yerine geçmez."
  )

  arama_modu = st.radio(
      "Sorgulama Modu:",
      [
          "🇹🇷 Türkçe Klinik Rehber (Öncelikli 10 Nörogenetik Hastalık)",
          "🌍 Küresel İnsan Genomu & Hastalık Arama (20.000+ Gen — NCBI / NIH)",
      ],
      horizontal=True,
  )

  if "Türkçe Klinik" in arama_modu:
    col1, col2 = st.columns(2)
    with col1:
      filtre = st.radio(
          "Arama Kriteri:", ["Hastalık Adına Göre", "Gen Sembolüne Göre"]
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
    c1.metric("İlişkili Gen", aktif_gen)
    c2.metric("Kalıtım Modeli", bilgi["kalitim"])
    with c3:
      st.info(f"**Hasta Dayanışma Ağı:**\n[{bilgi['dernek']}]({bilgi['dernek_url']})")
    st.success(f"**Klinik ve Moleküler Özet:** {bilgi['ozet']}")
  else:
    st.info(
        "💡 HGNC standartlarına uygun herhangi bir insan gen sembolünü (örn:"
        " `SYNGAP1`, `FOXG1`, `CACNA1A`, `GRIN2A`, `KCNQ2`) veya İngilizce"
        " hastalık adını (örn: `Ataxia`, `ALS`, `Batten Disease`) yazarak canlı"
        " veri çekebilirsiniz."
    )
    col_a, col_b = st.columns(2)
    with col_a:
      serbest_gen = (
          st.text_input("HGNC Gen Sembolü (Örn: FOXG1):", value="FOXG1")
          .strip()
          .upper()
      )
    with col_b:
      serbest_hastalik = st.text_input(
          "Klinik Araştırma Sorgu Terimi (İngilizce):", value=serbest_gen
      ).strip()
    aktif_gen = serbest_gen
    aktif_sorgu = serbest_hastalik if serbest_hastalik else serbest_gen

  st.divider()
  st.markdown(
      f"#### 🔬 Moleküler Gen Profili & Varyant Kayıtları: `{aktif_gen}`"
  )
  gen_bilgi = gen_detaylarini_getir(aktif_gen)
  if gen_bilgi:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Sitogenetik Konum", gen_bilgi["kromozom"])
    m2.metric("OMIM Kayıt No", gen_bilgi["omim"])
    m3.metric("Gen Biyotip", gen_bilgi["gen_tipi"])
    m4.link_button(
        "🧬 NCBI ClinVar Varyantları",
        gen_bilgi["clinvar_url"],
        use_container_width=True,
    )
    st.info(
        f"**Resmi NCBI RefSeq Moleküler Fonksiyon Özeti ({gen_bilgi['tam_ad']}):**\n\n{gen_bilgi['ncbi_ozet']}"
    )
  else:
    st.caption("Bu terim için doğrudan tekil gen eşleşmesi bulunamadı.")

  st.divider()
  st.markdown(f"#### 🌍 Aktif Klinik Araştırmalar (Recruiting): `{aktif_sorgu}`")

  with st.expander("ℹ️ Hasta Yakınları İçin Klinik Araştırma Fazları Rehberi"):
    st.markdown(
        "- **Faz 1 (Phase 1):** Tedavinin güvenliği ve doğru doz aralığı küçük bir grupta test edilir.\n"
        "- **Faz 2 (Phase 2):** Tedavinin etkinliği ve yan etkileri daha geniş bir hasta grubunda incelenir.\n"
        "- **Faz 3 (Phase 3):** Tedavinin mevcut standart yöntemlere göre üstünlüğü çok merkezli olarak doğrulanır."
    )

  sadece_tr = st.checkbox(
      "🇹🇷 Yalnızca Türkiye Merkezli Çalışmaları Filtrele"
  )

  with st.spinner("NIH ClinicalTrials.gov v2 API üzerinden canlı veriler alınıyor..."):
    df = klinik_arastirmalari_getir(aktif_sorgu, sadece_turkiye=sadece_tr)

  if not df.empty:
    st.write(
        f"Şu an hasta kabul eden (Recruiting) **{len(df)}** klinik çalışma"
        " listeleniyor:"
    )
    st.dataframe(
        df,
        column_config={
            "Resmi Kayıt": st.column_config.LinkColumn("NIH Kaydını Aç")
        },
        use_container_width=True,
        hide_index=True,
    )
  else:
    if sadece_tr:
      st.warning(
          "Bu gen/hastalık için şu an Türkiye'de aktif (Recruiting) çalışma"
          " kaydı bulunmamaktadır. Küresel çalışmaları görmek için filtreyi"
          " kaldırabilirsiniz."
      )
    else:
      st.info("Bu sorgu için aktif klinik çalışma bulunamadı.")

with tab_metodoloji:
  st.header("🔬 Bilimsel Metodoloji ve Veri Mimarisi")
  st.markdown("""
    **NöroGenetik Türkiye**, statik metinler yerine uluslararası biyoinformatik veri tabanlarının resmi REST API servislerini gerçek zamanlı sorgulayan modüler bir mimari üzerine inşa edilmiştir:
    
    1. **Genomik ve Sitogenetik Veri Katmanı (MyGene.info & NCBI Entrez):** Kullanıcı tarafından seçilen veya girilen HGNC gen sembolleri, *Homo sapiens* referans genomu üzerinden sorgulanarak kromozom lokasyonu, gen biyotipleri, OMIM referans numaraları ve RefSeq özetleri anlık çekilir.
    2. **Klinik Varyant Yönlendirmesi (NCBI ClinVar):** Her gen sorgusu, ilgili genin patojenik ve klinik önemi belirsiz (VUS) varyantlarının incelenebilmesi için doğrudan NCBI ClinVar veri tabanına bağlanır.
    3. **Klinik Araştırma Eşleştirme Motoru (NIH ClinicalTrials.gov API v2):** Amerikan Ulusal Sağlık Enstitüsü'nün resmi v2 arayüzü üzerinden yalnızca durumu `RECRUITING` (aktif hasta kabul eden) olan faz çalışmaları filtrelenir.
    """)

with tab_hakkinda:
  st.header("⚖️ Tıbbi Sorumluluk Reddi, Proje Vizyonu ve İletişim")
  st.markdown("""
    ### Amaç ve Kapsam
    Nadir nörogenetik hastalıklar alanında tanı alan bireylerin ve ailelerin, genetik raporlarında yer alan bilimsel terimleri anlaşılır bir dille kavramalarını sağlamak ve dünyadaki güncel klinik araştırmalara erişim bariyerini azaltmak amacıyla geliştirilmiştir.
    
    ### Tıbbi Sorumluluk Reddi (Disclaimer)
    - Bu platformda sunulan hiçbir bilgi **tıbbi tanı, teşhis, genetik danışmanlık veya tedavi tavsiyesi niteliği taşımaz**.
    - Klinik araştırma uygunluk kriterleri hekim değerlendirmesi gerektirir; hastaların mevcut tedavilerini doktor onayı olmadan değiştirmemeleri esastır.
    
    ### Geliştirici ve Akademik İletişim
    - **Kurucu & Geliştirici:** Deniz İnci Tarma (CoLab Uluslararası Bilim Topluluğu)
    - **E-Posta:** [denizinci.tarma@gmail.com](mailto:denizinci.tarma@gmail.com)
    - **Telefon:** +90 530 447 73 33
    - **Açık Kaynak Deposu:** [://github.com](https://://github.com)
    """)

st.divider()
st.caption(
    "© 2026 NöroGenetik Türkiye | Açık Kaynak Biyoinformatik Platformu — Deniz"
    " İnci Tarma (CoLab Bilim Topluluğu İnisiyatifi)"
)
