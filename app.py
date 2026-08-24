
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard de Óbitos - Porto Feliz", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    file_path = "óbitos_portofeliz.xlsx"
    df = pd.read_excel(file_path)
    
    # Extracting sections
    years = [int(y) for y in df.iloc[1, 1:21].values]
    
    # Sexo
    sexo_df = df.iloc[2:5, [0] + list(range(1, 22))].copy()
    sexo_df.columns = ['Categoria'] + [str(y) for y in years] + ['Total']
    
    # Local
    local_df = df.iloc[9:15, [0] + list(range(1, 22))].copy()
    local_df.columns = ['Categoria'] + [str(y) for y in years] + ['Total']
    
    # Faixa Etaria
    faixa_df = df.iloc[20:33, [0] + list(range(1, 22))].copy()
    faixa_df.columns = ['Categoria'] + [str(y) for y in years] + ['Total']
    
    # CID Capítulos
    cid_df = df.iloc[49:67, [0] + list(range(1, 22))].copy()
    cid_df.columns = ['Categoria'] + [str(y) for y in years] + ['Total']
    
    # Total ano a ano
    total_row = df.iloc[5, 1:21].values.astype(float)
    
    return years, sexo_df, local_df, faixa_df, cid_df, total_row

years, sexo_df, local_df, faixa_df, cid_df, total_row = load_data()

st.title("🏥 Dashboard Epidemiológico de Óbitos - Porto Feliz (2006-2025)")
st.markdown("Painel analítico interativo baseado nos dados oficiais de mortalidade de residentes no município.")

# Sidebar filters
st.sidebar.header("Filtros e Configurações")
selected_range = st.sidebar.slider("Selecione o Período (Anos)", min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# Filter years index
start_idx = years.index(selected_range[0])
end_idx = years.index(selected_range[1])
filtered_years = years[start_idx:end_idx+1]

# KPI metrics
col1, col2, col3, col4 = st.columns(4)
total_filtered_deaths = sum(total_row[start_idx:end_idx+1])
avg_deaths_year = total_filtered_deaths / len(filtered_years)

col1.metric("Total de Óbitos (Período)", int(total_filtered_deaths))
col2.metric("Média Anual", f"{avg_deaths_year:.1f}")
col3.metric("Ano com Maior Registro", years[start_idx + list(total_row[start_idx:end_idx+1]).index(max(total_row[start_idx:end_idx+1]))])
col4.metric("Ano com Menor Registro", years[start_idx + list(total_row[start_idx:end_idx+1]).index(min(total_row[start_idx:end_idx+1]))])

st.markdown("---")

# Row 1: Time Series Curve
st.subheader("📈 Curva de Óbitos ao Longo dos Anos")
fig, ax = plt.subplots(figsize=(10, 4))
sub_years = years[start_idx:end_idx+1]
sub_totals = total_row[start_idx:end_idx+1]
ax.plot(sub_years, sub_totals, marker='o', color='#1f77b4', linewidth=2.5)
ax.set_title(f"Evolução Temporal ({selected_range[0]} - {selected_range[1]})")
ax.set_xlabel("Ano")
ax.set_ylabel("Número de Óbitos")
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

# Row 2: Sex & Location
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("👥 Óbitos por Sexo")
    sex_totals = sexo_df.iloc[:-1, start_idx+1:end_idx+2].sum(axis=1).values
    sex_labels = sexo_df['Categoria'].values[:-1]
    
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.pie(sex_totals, labels=sex_labels, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

with col_b:
    st.subheader("📍 Local de Ocorrência")
    local_totals = local_df.iloc[:, start_idx+1:end_idx+2].sum(axis=1).values
    local_labels = local_df['Categoria'].values
    
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=local_totals, y=local_labels, palette='viridis', ax=ax3)
    ax3.set_xlabel("Total de Óbitos")
    ax3.set_ylabel("")
    st.pyplot(fig3)

# Row 3: Age Groups
st.subheader("👶👵 Óbitos por Faixa Etária")
faixa_totals = faixa_df.iloc[:-1, start_idx+1:end_idx+2].sum(axis=1).values
faixa_labels = faixa_df['Categoria'].values[:-1]

fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.barplot(x=faixa_labels, y=faixa_totals, palette='mako', ax=ax4)
plt.xticks(rotation=45)
ax4.set_xlabel("Faixa Etária")
ax4.set_ylabel("Total de Óbitos")
st.pyplot(fig4)

# Row 4: CID Chapters
st.subheader("🔬 Principais Causas (Capítulos CID-10)")
cid_totals = cid_df.iloc[:, start_idx+1:end_idx+2].sum(axis=1).values
cid_labels = [c[:35] for c in cid_df['Categoria'].values]

# Sort by totals descending for better visual
sorted_indices = cid_totals.argsort()[::-1]
sorted_totals = cid_totals[sorted_indices]
sorted_labels = [cid_labels[i] for i in sorted_indices]

fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.barplot(x=sorted_totals[:10], y=sorted_labels[:10], palette='rocket', ax=ax5)
ax5.set_xlabel("Total de Óbitos")
ax5.set_ylabel("")
st.pyplot(fig5)
