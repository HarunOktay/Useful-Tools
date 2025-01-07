import streamlit as st
import pandas as pd
from urllib.parse import urlparse
import plotly.express as px
from datetime import datetime

def load_data():
    df = pd.read_csv('HistoryName.csv')
    df['Visit Datetime'] = pd.to_datetime(df['Visit Datetime'])
    return df

def get_base_domain(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        parsed = urlparse(url)
        return parsed.netloc.split('.')[-2] + '.' + parsed.netloc.split('.')[-1]
    except:
        return url

def analyze_visits(df, top_n, start_date, end_date, selected_sites=None):
    df['Base_Domain'] = df['URL'].apply(get_base_domain)
    
    # Tarih filtresi uygula
    mask = (df['Visit Datetime'].dt.date >= start_date) & (df['Visit Datetime'].dt.date <= end_date)
    df_filtered = df.loc[mask]
    
    # Site bazlı filtreleme
    if selected_sites:
        df_filtered = df_filtered[df_filtered['Base_Domain'].isin(selected_sites)]
    
    visit_counts = df_filtered['Base_Domain'].value_counts().head(top_n)
    return visit_counts, df_filtered

def main():
    st.title('Firefox Geçmişi Detaylı Analizi')
    
    try:
        # Veriyi yükle
        df = load_data()
        
        # Tarih aralığı hesapla
        min_date = df['Visit Datetime'].dt.date.min()
        max_date = df['Visit Datetime'].dt.date.max()
        
        # Sidebar ayarları
        st.sidebar.header('Analiz Ayarları')
        
        # Tarih seçimi
        st.sidebar.subheader('Tarih Aralığı')
        start_date = st.sidebar.date_input('Başlangıç Tarihi', min_date)
        end_date = st.sidebar.date_input('Bitiş Tarihi', max_date)
        
        # Site sayısı seçimi
        top_n = st.sidebar.slider('Gösterilecek Site Sayısı', 5, 50, 10)
        
        # Site seçimi için tüm siteleri al
        all_sites = df['URL'].apply(get_base_domain).unique()
        selected_sites = st.sidebar.multiselect(
            'Analiz Edilecek Siteleri Seçin',
            options=all_sites,
            default=None
        )
        
        # Analizi yap
        visit_counts, filtered_df = analyze_visits(df, top_n, start_date, end_date, selected_sites)
        
        # Görselleştirmeler
        st.header('Ziyaret Analizi')
        
        # Tab oluştur
        tab1, tab2, tab3 = st.tabs(["Site Bazlı Analiz", "Zaman Serisi Analizi", "Detaylı Veriler"])
        
        with tab1:
            # Bar chart
            fig1 = px.bar(
                x=visit_counts.index,
                y=visit_counts.values,
                labels={'x': 'Website', 'y': 'Ziyaret Sayısı'},
                title=f'En Çok Ziyaret Edilen Siteler ({start_date} - {end_date})'
            )
            st.plotly_chart(fig1)
        
        with tab2:
            # Zaman serisi grafiği
            if selected_sites:
                # Seçili siteler için zaman serisi
                time_series_data = filtered_df.groupby([
                    filtered_df['Visit Datetime'].dt.date, 
                    'Base_Domain'
                ]).size().reset_index(name='count')
                
                fig2 = px.line(
                    time_series_data,
                    x='Visit Datetime',
                    y='count',
                    color='Base_Domain',
                    title='Günlük Site Ziyaret Sayıları',
                    labels={'Visit Datetime': 'Tarih', 'count': 'Ziyaret Sayısı'}
                )
            else:
                # Tüm siteler için toplam zaman serisi
                daily_visits = filtered_df.groupby(
                    filtered_df['Visit Datetime'].dt.date
                ).size()
                
                fig2 = px.line(
                    x=daily_visits.index,
                    y=daily_visits.values,
                    title='Günlük Toplam Ziyaret Sayısı',
                    labels={'x': 'Tarih', 'y': 'Ziyaret Sayısı'}
                )
            
            st.plotly_chart(fig2)
        
        with tab3:
            st.subheader('Detaylı Ziyaret Verileri')
            visit_df = pd.DataFrame({
                'Site': visit_counts.index,
                'Ziyaret Sayısı': visit_counts.values
            })
            st.dataframe(visit_df)
            
    except Exception as e:
        st.error(f'Bir hata oluştu: {str(e)}')

if __name__ == '__main__':
    main()