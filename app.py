import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="NöroGenetik Türkiye | NeuroGenetics Türkiye",
    page_icon="🧬",
    layout="wide",
)

with st.sidebar:
  dil = st.radio(
      "🌐 Dil / Language:",
      ["🇹🇷 Türkçe", "🇬🇧 English"],
      horizontal=True,
  )
  tr = dil == "🇹🇷 Türkçe"
  st.divider()
  st.title("🧬 NöroGenetik Türkiye" if tr else "🧬 NeuroGenetics Türkiye")
  st.caption(
      "Nadir Nörogenetik Hastalıklar Biyoinformatik Platformu"
      if tr
      else "Open-Source Rare Neurogenetic Bioinformatics Platform"
  )
  st.divider()
  st.metric(
      label="Kapsanan İnsan Geni" if tr else "Indexed Human Genes",
      value="20.000+",
      delta="HGNC / NCBI",
  )
  st.metric(
      label="Klinik Veri Kaynağı" if tr else "Clinical Data Source",
      value="NIH v2 API",
      delta="Gerçek Zamanlı" if tr else "Real-Time",
  )
  st.divider()
  st.markdown("### 👩‍🔬 Kurucu & İletişim" if tr else "### 👩‍🔬 Founder & Contact")
  st.markdown(
      "**Deniz İnci Tarma**\n\n"
      "CoLab International Science Community\n\n"
      "📧 denizinci.tarma@gmail.com\n\n"
      "📞 +90 530 447 73 33\n\n"
      "🔗 [GitHub](https://github.com)"
  )
HASTALIK_VERITABANI = {
    "Dravet Sendromu (Dravet Syndrome)": {
        "gen": "SCN1A",
        "ingilizce_ad": "Dravet Syndrome",
        "kalitim_tr": "Otozomal Dominant (De novo)",
        "kalitim_en": "Autosomal Dominant (De novo)",
        "ozet_tr": "Yaşamın ilk yılında başlayan, ilaca dirençli nöbetlerle seyreden ve %80+ oranında SCN1A gen mutasyonlarından kaynaklanan nadir epilepsi sendromudur.",
        "ozet_en": "A rare drug-resistant genetic epilepsy beginning in infancy, caused in >80% of cases by SCN1A sodium channel gene mutations.",
        "dernekler": "• [Epilepsi ve Yaşam Derneği](https://epilepsiveyasam.org.tr)\n• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
    },
    "Rett Sendromu (Rett Syndrome)": {
        "gen": "MECP2",
        "ingilizce_ad": "Rett Syndrome",
        "kalitim_tr": "X'e Bağlı Dominant",
        "kalitim_en": "X-Linked Dominant",
        "ozet_tr": "Çoğunlukla kız çocuklarında görülen ve X kromozomu üzerindeki MECP2 genindeki değişimlerden kaynaklanan nörogelişimsel bir bozukluktur.",
        "ozet_en": "A rare neurodevelopmental disorder primarily affecting females, caused by mutations in the X-linked MECP2 gene.",
        "dernekler": "• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
    },
    "Spinal Müsküler Atrofi (SMA)": {
        "gen": "SMN1",
        "ingilizce_ad": "Spinal Muscular Atrophy",
        "kalitim_tr": "Otozomal Resesif",
        "kalitim_en": "Autosomal Recessive",
        "ozet_tr": "Omurilikteki motor sinir hücrelerinin kaybına bağlı ilerleyici kas güçsüzlüğüne yol açan SMN1 geni kaynaklı kalıtsal nöromüsküler hastalıktır.",
        "ozet_en": "An inherited neuromuscular disorder causing progressive muscle weakness due to SMN1 gene deletions or mutations.",
        "dernekler": "• [SMA Benimle Yürü Derneği](https://smabenimleyuru.org.tr)\n• [KASDER](https://kasder.org.tr)\n• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)",
    },
    "Frajil X Sendromu (Fragile X Syndrome)": {
        "gen": "FMR1",
        "ingilizce_ad": "Fragile X Syndrome",
        "kalitim_tr": "X'e Bağlı",
        "kalitim_en": "X-Linked",
        "ozet_tr": "FMR1 genindeki CGG tekrar artışı sonucu FMRP proteininin sentezlenememesiyle oluşan kalıtsal nörogelişimsel durumdur.",
        "ozet_en": "An inherited neurodevelopmental condition caused by CGG repeat expansion in the FMR1 gene.",
        "dernekler": "• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
    },
    "Tuberoz Skleroz Kompleksi (TSC)": {
        "gen": "TSC1",
        "ingilizce_ad": "Tuberous Sclerosis",
        "kalitim_tr": "Otozomal Dominant",
        "kalitim_en": "Autosomal Dominant",
        "ozet_tr": "TSC1 veya TSC2 genlerindeki mutasyonlar sonucu beyin ve diğer organlarda iyi huylu hamartomlar ve epilepsiyle seyreden genetik sendromdur.",
        "ozet_en": "A genetic disorder caused by TSC1 or TSC2 mutations, leading to benign hamartomas and epilepsy.",
        "dernekler": "• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
    },
    "Angelman Sendromu (Angelman Syndrome)": {
        "gen": "UBE3A",
        "ingilizce_ad": "Angelman Syndrome",
        "kalitim_tr": "Genomik İmprinting (15q11)",
        "kalitim_en": "Genomic Imprinting (15q11)",
        "ozet_tr": "15. kromozomdaki maternal UBE3A geninin işlev kaybından kaynaklanan gelişimsel gecikme ve ataksi ile seyreden nörogenetik durumdur.",
        "ozet_en": "A neurogenetic disorder caused by maternal UBE3A loss of function on chromosome 15.",
        "dernekler": "• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
    },
    "Duchenne Musküler Distrofi (DMD)": {
        "gen": "DMD",
        "ingilizce_ad": "Duchenne Muscular Dystrophy",
        "kalitim_tr": "X'e Bağlı Resesif",
        "kalitim_en": "X-Linked Recessive",
        "ozet_tr": "Distrofin proteinini kodlayan DMD genindeki mutasyonlar nedeniyle erken çocuklukta başlayan ilerleyici kas yıkımıyla seyreder.",
        "ozet_en": "An X-linked recessive disorder caused by DMD gene mutations leading to progressive muscle degeneration.",
        "dernekler": "• [DMD Aileleri Derneği](https://dmd.org.tr)\n• [KASDER](https://kasder.org.tr)\n• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)",
    },
    "Huntington Hastalığı (Huntington Disease)": {
        "gen": "HTT",
        "ingilizce_ad": "Huntington Disease",
        "kalitim_tr": "Otozomal Dominant",
        "kalitim_en": "Autosomal Dominant",
        "ozet_tr": "HTT genindeki CAG tekrar genişlemesine bağlı olarak beyindeki sinir hücrelerinin ilerleyici yıkımına yol açan kalıtsal hastalıktır.",
        "ozet_en": "An autosomal dominant neurodegenerative disorder caused by CAG repeat expansion in the HTT gene.",
        "dernekler": "• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
    },
    "Nörofibromatozis Tip 1 (NF1)": {
        "gen": "NF1",
        "ingilizce_ad": "Neurofibromatosis Type 1",
        "kalitim_tr": "Otozomal Dominant",
        "kalitim_en": "Autosomal Dominant",
        "ozet_tr": "NF1 tümör baskılayıcı genindeki mutasyonlar sonucu ciltte sütlü kahve lekeleri ve nörofibromlarla seyreden genetik durumdur.",
        "ozet_en": "An autosomal dominant disorder caused by NF1 mutations, marked by café-au-lait macules and neurofibromas.",
        "dernekler": "• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
    },
    "CDKL5 Eksikliği Bozukluğu (CDKL5)": {
        "gen": "CDKL5",
        "ingilizce_ad": "CDKL5 Deficiency Disorder",
        "kalitim_tr": "X'e Bağlı Dominant",
        "kalitim_en": "X-Linked Dominant",
        "ozet_tr": "CDKL5 genindeki patojenik varyantlar sonucu yaşamın ilk haftalarında başlayan dirençli epileptik ensefalopati ile seyreden nadir durumdur.",
        "ozet_en": "An X-linked developmental and epileptic encephalopathy caused by pathogenic variants in CDKL5.",
        "dernekler": "• [Nadir Hastalıklar Ağı](https://nadirhastaliklaragi.org.tr)\n• [Nadir Hastalıklar Federasyonu](https://nadir.org.tr)",
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
          "tam_ad": h.get("name", "N/A"),
          "kromozom": h.get("map_location", "Unknown"),
          "gen_tipi": h.get("type_of_gene", "-"),
          "omim": omim_id if omim_id else "-",
          "ncbi_ozet": h.get("summary", "No summary available."),
          "clinvar_url": f"{cv_base}?term={temiz_gen}%5Bgene%5D",
      }
  except Exception:
    pass
  return None


@st.cache_data(ttl=3600)
def klinik_arastirmalari_getir(arama_terimi, sadece_turkiye=False):
  url = "https://" + "clinicaltrials.gov/api/v2/studies"
  study_base = "https://" + "clinicaltrials.gov/study/"
  params = {"query.term": arama_terimi, "filter.overallStatus": "RECRUITING", "pageSize": 20}
  if sadece_turkiye:
    params["query.locn"] = "Turkey"
  try:
    veri = requests.get(url, params=params, timeout=10).json()
    calismalar = []
    for study in veri.get("studies", []):
      protokol = study.get("protocolSection", {})
      kimlik = protokol.get("identificationModule", {})
      tasarim = protokol.get("designModule", {})
      konumlar = protokol.get("contactsLocationsModule", {}).get("locations", [])
      ulkeler = list(set([loc.get("country", "") for loc in konumlar if loc.get("country")]))
      calismalar.append({
          "NCT ID": kimlik.get("nctId", "-"),
          "Study Title": kimlik.get("briefTitle", "-"),
          "Phase": ", ".join(tasarim.get("phases", ["Not Specified"])),
          "Countries": ", ".join(ulkeler[:4]) if ulkeler else "N/A",
          "Official Link": f"{study_base}{kimlik.get('nctId', '')}",
      })
    return pd.DataFrame(calismalar)
  except Exception:
    return pd.DataFrame()


st.title("🧬 NöroGenetik Türkiye" if tr else "🧬 NeuroGenetics Türkiye")
st.markdown(
    "**Nadir Nörogenetik Hastalıklar Biyoinformatik ve Küresel Klinik Araştırma Platformu**"
    if tr
    else "**Open-Access Bioinformatics & Clinical Trial Platform for Rare Neurogenetic Disorders**"
)

tab_sorgu, tab_metodoloji, tab_hakkinda = st.tabs([
    "🔍 Gen & Klinik Araştırma Sorgulama" if tr else "🔍 Gene & Clinical Trial Search",
    "🔬 Bilimsel Metodoloji" if tr else "🔬 Scientific Methodology",
    "⚖️ Tıbbi Sorumluluk & İletişim" if tr else "⚖️ Medical Disclaimer & Contact",
])

with tab_sorgu:
  st.warning(
      "⚠️ **Tıbbi Bilgilendirme Uyarısı:** Bu platform yalnızca bilimsel bilgilendirme amaçlıdır; tıbbi tanı veya tedavi yerine geçmez."
      if tr
      else "⚠️ **Medical Disclaimer:** For scientific educational purposes only; does not replace medical diagnosis or treatment."
  )
  arama_modu = st.radio(
      "Sorgulama Modu:" if tr else "Query Mode:",
      [
          "🇹🇷 Klinik Rehber (10 Temel Hastalık)" if tr else "📋 Curated Clinical Guide (10 Disorders)",
          "🌍 Küresel İnsan Genomu Arama (20.000+ Gen)" if tr else "🌍 Global Human Genome Search (20,000+ Genes)",
      ],
      horizontal=True,
  )
  rapor_baslik = ""
  rapor_ozet = ""

  if "10" in arama_modu:
    col1, col2 = st.columns(2)
    with col1:
      filtre = st.radio(
          "Arama Kriteri:" if tr else "Filter By:",
          ["Hastalık Adına Göre", "Gen Sembolüne Göre"] if tr else ["By Disease", "By Gene"],
      )
    with col2:
      if "Hastalık" in filtre or "Disease" in filtre:
        secilen = st.selectbox("Hastalık Seçiniz:" if tr else "Select Disorder:", list(HASTALIK_VERITABANI.keys()))
      else:
        gen_map = {f"{v['gen']} — {k}": k for k, v in HASTALIK_VERITABANI.items()}
        secilen = gen_map[st.selectbox("Gen Seçiniz:" if tr else "Select Gene:", list(gen_map.keys()))]
    bilgi = HASTALIK_VERITABANI[secilen]
    aktif_gen = bilgi["gen"]
    aktif_sorgu = bilgi["ingilizce_ad"]
    rapor_baslik = secilen
    rapor_ozet = bilgi["ozet_tr"] if tr else bilgi["ozet_en"]
    st.markdown(f"### 📋 {secilen}")
    c1, c2, c3 = st.columns(3)
    c1.metric("İlişkili Gen" if tr else "Associated Gene", aktif_gen)
    c2.metric("Kalıtım Modeli" if tr else "Inheritance", bilgi["kalitim_tr"] if tr else bilgi["kalitim_en"])
    with c3:
      st.info(("**Hasta Dayanışma Ağları:**\n\n" if tr else "**Patient Networks:**\n\n") + bilgi["dernekler"])
    st.success(rapor_ozet)
  else:
    col_a, col_b = st.columns(2)
    with col_a:
      serbest_gen = st.text_input("HGNC Gen Sembolü:" if tr else "HGNC Gene Symbol:", value="FOXG1").strip().upper()
    with col_b:
      serbest_hastalik = st.text_input("Araştırma Terimi (İngilizce):" if tr else "Query Term:", value=serbest_gen).strip()
    aktif_gen = serbest_gen
    aktif_sorgu = serbest_hastalik if serbest_hastalik else serbest_gen
    rapor_baslik = f"Gene Query: {aktif_gen}"

  st.divider()
  st.markdown(f"#### 🔬 Moleküler Gen Profili: `{aktif_gen}`")
  gen_bilgi = gen_detaylarini_getir(aktif_gen)
  if gen_bilgi:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Sitogenetik Konum" if tr else "Location", gen_bilgi["kromozom"])
    m2.metric("OMIM No" if tr else "OMIM ID", gen_bilgi["omim"])
    m3.metric("Gen Biyotip" if tr else "Biotype", gen_bilgi["gen_tipi"])
    m4.link_button("🧬 NCBI ClinVar", gen_bilgi["clinvar_url"], use_container_width=True)
    st.info(f"**NCBI RefSeq Summary ({gen_bilgi['tam_ad']}):**\n\n{gen_bilgi['ncbi_ozet']}")
    if not rapor_ozet:
      rapor_ozet = gen_bilgi["ncbi_ozet"]

  st.divider()
  st.markdown(f"#### 🌍 Aktif Klinik Araştırmalar (Recruiting): `{aktif_sorgu}`")
  with st.expander("ℹ️ Klinik Araştırma Fazları Rehberi" if tr else "ℹ️ Clinical Trial Phases Guide"):
    st.markdown(
        "- **Faz 1:** Güvenlik ve doz aralığı testi.\n- **Faz 2:** Etkinlik ve yan etki incelemesi.\n- **Faz 3:** Çok merkezli üstünlük doğrulaması."
        if tr
        else "- **Phase 1:** Safety & dosage testing.\n- **Phase 2:** Efficacy & side effects.\n- **Phase 3:** Multicenter effectiveness confirmation."
    )
  sadece_tr = st.checkbox("🇹🇷 Yalnızca Türkiye Merkezli Çalışmalar" if tr else "🇹🇷 Filter Only Trials in Türkiye")
  df = klinik_arastirmalari_getir(aktif_sorgu, sadece_turkiye=sadece_tr)
  if not df.empty:
    st.dataframe(df, column_config={"Official Link": st.column_config.LinkColumn("NIH Kaydı" if tr else "NIH Record")}, use_container_width=True, hide_index=True)
    nct_listesi = ", ".join(df["NCT ID"].tolist()[:5])
  else:
    nct_listesi = "None"
    st.info("Aktif çalışma bulunamadı." if tr else "No active trials found.")

  st.divider()
  rapor_metni = f"NOROGENETIK TURKIYE OZET RAPORU\nKonu: {rapor_baslik}\nGen: {aktif_gen}\nOzet: {rapor_ozet}\nNIH NCT Kodlari: {nct_listesi}\nKaynak: https://streamlit.app\n"
  st.download_button(
      label="📄 Hekim Görüşmesi İçin Özet Raporu İndir (.txt)" if tr else "📄 Download Summary Report (.txt)",
      data=rapor_metni,
      file_name=f"NoroGenetik_{aktif_gen}_Rapor.txt",
      mime="text/plain",
  )

with tab_metodoloji:
  st.header("🔬 Bilimsel Metodoloji" if tr else "🔬 Scientific Methodology")
  st.markdown("1. **MyGene.info & NCBI Entrez:** HGNC gen ve kromozom verileri.\n2. **NCBI ClinVar:** Patojenik varyant kayıtları.\n3. **NIH ClinicalTrials.gov API v2:** Güncel klinik araştırmalar.")

with tab_hakkinda:
  st.header("⚖️ Tıbbi Sorumluluk & İletişim" if tr else "⚖️ Medical Disclaimer & Contact")
  st.markdown(
      "- **Kurucu / Founder:** Deniz İnci Tarma (CoLab International Science Community)\n"
      "- **E-Posta / Email:** denizinci.tarma@gmail.com\n"
      "- **Telefon / Phone:** +90 530 447 73 33\n"
      "- **GitHub:** https://github.com"
  )

st.caption("© 2026 NöroGenetik Türkiye | Deniz İnci Tarma — CoLab International Science Community")


