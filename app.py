# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:21:43 2026

@author: Merve Nisa
"""

import streamlit as st 
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Finansal Asistan",page_icon="📈")

st.title("💸 Merhaba! Ben Senin Finansal Asistanınım")
st.subheader("Yatırım dünyasını karmaşık terimler olmadan, en basit haliyle keşfet.")

isim = st.text_input("Sana nasıl hitap etmemi istersin?")

if isim:
    st.success(f"Hoş geldin {isim}! Bugün finansal özgürlüğün için harika bir adım attın. Çok yakında burası canlı verilerle dolacak!")
    
    st.divider()
    st.header("🌍 Canlı Piyasa Ekranı")
    st.info("Veriler Yahoo Finance üzerinden anlık çekilmektedir...")
    
    portfoy = {
        "🎒 Öğrenci İşi (Düşük Bütçe & Yenilikçi)": {
            "🚀 Dogecoin (USD)": "DOGE-USD", # Adet fiyatı çok ucuz kripto
            "🏦 Yapı Kredi (BIST)": "YKBNK.IS", # Adet fiyatı uygun banka hissesi
            "🛒 Şok Marketler (BIST)": "SOKM.IS", # Hızlı tüketim, uygun fiyat
            "📱 Turkcell (BIST)": "TCELL.IS" # Teknoloji ve iletişim
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
    
    secilen_risk=st.selectbox("1. Lütfen Risk Profilini Seç:",options=list(portfoy.keys()))
    butce=st.number_input("2. Yatırım Bütçeni Gir (TL):", min_value=500, value=1000, step=100)
    
    if st.button("🚀 Botu Çalıştır ve Parayı Dağıt") :
        
        with st.spinner('Piyasalar analiz ediliyor, cüzdanın hesaplanıyor...'):
            
            usd_try_kuru= yf.Ticker("TRY=X").history(period="1d")['Close'].iloc[-1]
            
            secilen_varliklar= portfoy[secilen_risk]
            varlik_basina_butce= butce / len(secilen_varliklar)
            
            harcanan_toplam=0
            grafik_isimleri=[]
            grafik_degerleri=[]
            alinan_adetler=[]
            
            for varlik_adi,borsa_kodu in secilen_varliklar.items():
                anlik_fiyat = yf.Ticker(borsa_kodu).history(period="1d")['Close'].iloc[-1]
                
                if "USD" in varlik_adi:
                    fiyat_tl = anlik_fiyat * usd_try_kuru
                    
                else:
                    fiyat_tl = anlik_fiyat
                    
                if fiyat_tl>0:
                    alinabilir_adet= int(varlik_basina_butce // fiyat_tl)
                else:
                    alinabilir_adet=0
                    
                yatirim_tutari = alinabilir_adet * fiyat_tl
                harcanan_toplam += yatirim_tutari
                
                if alinabilir_adet >0:
                    grafik_isimleri.append(varlik_adi)
                    grafik_degerleri.append(yatirim_tutari)
                    alinan_adetler.append(alinabilir_adet)  
            kalan_nakit=butce - harcanan_toplam
            
            st.success("Analiz tamamlandı! İşte senin için oluşturduğum portföy:")
            
            st.subheader("👛 Yatırım Cüzdanın")
            col1,col2 = st.columns(2)
            with col1:
                st.metric(label="📊 Sepete Harcanan Tutar", value=f"{harcanan_toplam:,.2f} ₺")
            with col2:
                # Cüzdanda kalan nakit artık o kocaman grafik yerine burada asil bir şekilde duruyor
                st.metric(label="💵 Cüzdanda Kalan Nakit", value=f"{kalan_nakit:,.2f} ₺")    
            
            fig = px.pie(values=grafik_degerleri, names=grafik_isimleri, title="Sadece Yatırım Yapılan Varlıkların Dağılımı", hole=0.4)
            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>Yatırım Tutarı: %{value:,.2f} ₺<extra></extra>"
            )
            
            # (Mevcut kodun)
            st.plotly_chart(fig)
           
            
            st.subheader("🛒 Alınan Hisseler Özeti")
            for i in range(len(alinan_adetler)):
                st.write(f"- **{alinan_adetler[i]} Adet** {grafik_isimleri[i]} *(Tutar: {grafik_degerleri[i]:,.2f} ₺)*")
            # ... (Mevcut grafik ve özet kodlarının hemen altına bunu ekle) ...

            st.divider()
            st.subheader("👨‍💻 Geliştirici (API) Görünümü")
            st.info("Eğer bu kod gerçek bir bankanın sunucusunda çalışsaydı, müşterinin telefonuna (mobil uygulamaya) arka planda şu ham veriyi gönderecekti:")

            # Yazdığımız algoritmanın sonucunu gerçek bir API JSON formatına çeviriyoruz
            api_yaniti = {
                "kullanici_profili": secilen_risk,
                "toplam_butce_tl": butce,
                "hesap_ozeti": {
                    "harcanan_tutar_tl": round(harcanan_toplam, 2),
                    "cuzdanda_kalan_nakit_tl": round(kalan_nakit, 2)
                },
                "alinan_varliklar": []
            }

            # Sepetteki ürünleri API listemize ekliyoruz
            for i in range(len(alinan_adetler)):
                api_yaniti["alinan_varliklar"].append({
                    "varlik_adi": grafik_isimleri[i],
                    "adet": alinan_adetler[i],
                    "toplam_deger_tl": round(grafik_degerleri[i], 2)
                })

            # Streamlit'in muazzam özelliği: JSON formatını ekranda profesyonelce gösterir
            st.json(api_yaniti)        
                    
   