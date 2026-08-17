# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:21:43 2026

@author: Merve Nisa
"""

import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Finansal Asistan", page_icon="📈")

# Yahoo Finance engellemesin diye veriyi 15 dk aklında tutan hafıza modülü
@st.cache_data(ttl=900) 
def anlik_fiyat_getir(borsa_kodu):
    return yf.Ticker(borsa_kodu).history(period="1d")['Close'].iloc[-1]

st.title("💸 Merhaba! Ben Senin Finansal Asistanınım")
st.subheader("Yatırım dünyasını karmaşık terimler olmadan, en basit haliyle keşfet.")

isim = st.text_input("Sana nasıl hitap etmemi istersin?")

if isim:
    st.success(f"Hoş geldin {isim}! Bugün finansal özgürlüğün için harika bir adım attın.")
    
    st.divider()
    st.header("🤖 Akıllı Robo-Danışman (Bütçe Botu)")
    st.info("Veriler Yahoo Finance üzerinden çekilmektedir. (Sunucu yorulmasın diye 15 dakikada bir güncellenir)")
    
    portfoy = {
        "🎒 Öğrenci İşi (Düşük Bütçe & Yenilikçi)": {
            "🚀 Dogecoin (USD)": "DOGE-USD",
            "🏦 Yapı Kredi (BIST)": "YKBNK.IS",
            "🛒 Şok Marketler (BIST)": "SOKM.IS",
            "📱 Turkcell (BIST)": "TCELL.IS"
        },
        "🟢 Az Riskli (Güvenli Limanlar)": {
            "🟡 Altın Fonu (BIST)": "GLDTR.IS", 
            "🏢 Koç Holding (BIST)": "KCHOL.IS",
            "🛡️ Akbank (BIST)": "AKBNK.IS"
        },
        "🟡 Orta Riskli (Global Şirketler)": {
            "🍏 Apple Hisse (USD)": "AAPL",
            "💻 Microsoft Hisse (USD)": "MSFT",
            "✈️ THY (BIST)": "THYAO.IS"
        },
        "🔴 Yüksek Riskli (Kripto & Teknoloji)": {
            "🪙 Bitcoin (USD)": "BTC-USD",
            "🤖 NVIDIA Hisse (USD)": "NVDA",
            "⚡ Tesla Hisse (USD)": "TSLA"
        }
    }
    
    secilen_risk = st.selectbox("1. Lütfen Risk Profilini Seç:", options=list(portfoy.keys()))
    butce = st.number_input("2. Yatırım Bütçeni Gir (TL):", min_value=500, value=1000, step=100)
    
    if st.button("🚀 Botu Çalıştır ve Parayı Dağıt"):
        
        with st.spinner('Piyasalar analiz ediliyor, cüzdanın hesaplanıyor...'):
            
            try:
                usd_try_kuru = anlik_fiyat_getir("TRY=X")
                
                secilen_varliklar = portfoy[secilen_risk]
                varlik_basina_butce = butce / len(secilen_varliklar)
                
                harcanan_toplam = 0
                grafik_isimleri = []
                grafik_degerleri = []
                alinan_adetler = []
                
                for varlik_adi, borsa_kodu in secilen_varliklar.items():
                    anlik_fiyat = anlik_fiyat_getir(borsa_kodu)
                    
                    if "USD" in varlik_adi:
                        fiyat_tl = anlik_fiyat * usd_try_kuru
                    else:
                        fiyat_tl = anlik_fiyat
                        
                    if fiyat_tl > 0:
                        alinabilir_adet = int(varlik_basina_butce // fiyat_tl)
                    else:
                        alinabilir_adet = 0
                        
                    yatirim_tutari = alinabilir_adet * fiyat_tl
                    harcanan_toplam += yatirim_tutari
                    
                    if alinabilir_adet > 0:
                        grafik_isimleri.append(varlik_adi)
                        grafik_degerleri.append(yatirim_tutari)
                        alinan_adetler.append(alinabilir_adet)  
                
                kalan_nakit = butce - harcanan_toplam
                
                if harcanan_toplam == 0:
                    st.error("⚠️ Girdiğiniz bütçe, bu risk profilindeki varlıkların adet fiyatları için yetersiz kaldı! Lütfen bütçenizi artırın ya da 'Öğrenci İşi' profilini seçin.")
                else:
                    st.success("Analiz tamamlandı! İşte senin için oluşturduğum portföy:")
                    
                    st.subheader("👛 Yatırım Cüzdanın")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="📊 Sepete Harcanan Tutar", value=f"{harcanan_toplam:,.2f} ₺")
                    with col2:
                        st.metric(label="💵 Cüzdanda Kalan Nakit", value=f"{kalan_nakit:,.2f} ₺")    
                    
                    fig = px.pie(values=grafik_degerleri, names=grafik_isimleri, title="Sadece Yatırım Yapılan Varlıkların Dağılımı", hole=0.4)
                    fig.update_traces(hovertemplate="<b>%{label}</b><br>Yatırım Tutarı: %{value:,.2f} ₺<extra></extra>")
                    st.plotly_chart(fig)
                    
                    st.subheader("🛒 Alınan Hisseler Özeti")
                    for i in range(len(alinan_adetler)):
                        st.write(f"- **{alinan_adetler[i]} Adet** {grafik_isimleri[i]} *(Tutar: {grafik_degerleri[i]:,.2f} ₺)*")

                    st.divider()
                    st.header("📊 Portföy Sağlık ve Çeşitlilik Analizi")
                    
                    toplam_varlik_sayisi = len(grafik_isimleri)
                    cesitlilik_puani = min(toplam_varlik_sayisi * 25, 100)
                    
                    if "Öğrenci" in secilen_risk or "Yüksek" in secilen_risk:
                        karakter = "Agresif / Büyüme Odaklı 🚀"
                        onerilen_vade = "Uzun Vade (3+ Yıl)"
                    elif "Az Riskli" in secilen_risk:
                        karakter = "Defansif / Güvenli Liman 🛡️"
                        onerilen_vade = "Kısa / Orta Vade"
                    else:
                        karakter = "Dengeli / Melez Sepet ⚖️"
                        onerilen_vade = "Orta Vade (1-3 Yıl)"

                    # Yazıların kesilmesini önleyen şık yan yana görünüm
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric(label="🎯 Çeşitlilik Skoru", value=f"{cesitlilik_puani} / 100")
                    with col_b:
                        st.markdown("**Sektörel Karakter:**")
                        st.success(karakter)
                    with col_c:
                        st.markdown("**Önerilen Vade:**")
                        st.success(onerilen_vade)

                    st.warning("""
                    ⚖️ **Yasal Uyarı (Compliance Notu):** 
                    Bu uygulamada sunulan varlık dağılımı ve analizler yalnızca finansal okuryazarlığı artırma ve algoritmik modelleme amacıyla hazırlanmıştır. 
                    Hiçbir şekilde yatırım tavsiyesi (YTD) niteliği taşımaz. Yatırım kararı almadan önce lisanslı bir aracı kurumdan danışmanlık almanız önerilir.
                    """)
                    
                    st.divider()
                    st.subheader("👨‍💻 Geliştirici (API) Görünümü")

                    api_yaniti = {
                        "kullanici_profili": secilen_risk,
                        "toplam_butce_tl": butce,
                        "hesap_ozeti": {
                            "harcanan_tutar_tl": round(harcanan_toplam, 2),
                            "cuzdanda_kalan_nakit_tl": round(kalan_nakit, 2)
                        },
                        "alinan_varliklar": []
                    }

                    for i in range(len(alinan_adetler)):
                        api_yaniti["alinan_varliklar"].append({
                            "varlik_adi": grafik_isimleri[i],
                            "adet": alinan_adetler[i],
                            "toplam_deger_tl": round(grafik_degerleri[i], 2)
                        })

                    st.json(api_yaniti)
            
            except Exception as e:
                st.error("🚨 Yahoo Finance sunucuları şu an çok yoğun olduğu için isteğinize yanıt veremiyor. Lütfen 5-10 dakika bekleyip tekrar deneyin.")
                    
   
