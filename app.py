import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador de Planilhas", layout="wide")

st.title("📊 Comparador de Planilhas")
st.write("Faça upload de duas planilhas e compare os dados facilmente.")

# Upload dos arquivos
file1 = st.file_uploader("📁 Upload da Planilha 1", type=["xlsx", "csv"])
file2 = st.file_uploader("📁 Upload da Planilha 2", type=["xlsx", "csv"])

def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if file1 and file2:
    df1 = load_file(file1)
    df2 = load_file(file2)

    st.subheader("🔍 Pré-visualização dos dados")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Planilha 1")
        st.dataframe(df1.head())

    with col2:
        st.write("Planilha 2")
        st.dataframe(df2.head())

    # Colunas em comum
    st.subheader("⚙️ Configuração")
    colunas = list(set(df1.columns).intersection(set(df2.columns)))

    if not colunas:
        st.error("❌ As planilhas não possuem colunas em comum.")
    else:
        chave = st.selectbox("Selecione a coluna chave (ex: CNPJ)", colunas)

        if st.button("🚀 Comparar"):
            df1[chave] = df1[chave].astype(str)
            df2[chave] = df2[chave].astype(str)

            novos = df2[~df2[chave].isin(df1[chave])]
            existentes = df2[df2[chave].isin(df1[chave])]
            removidos = df1[~df1[chave].isin(df2[chave])]

            # Diferenças
            merged = df1.merge(df2, on=chave, how="inner", suffixes=("_old", "_new"))

            diferencas = pd.DataFrame()

            for col in df1.columns:
                if col != chave and col in df2.columns:
                    diff = merged[merged[f"{col}_old"] != merged[f"{col}_new"]]
                    if not diff.empty:
                        diferencas = pd.concat([diferencas, diff])

            st.success("✅ Comparação concluída!")

            st.subheader("🆕 Novos registros")
            st.dataframe(novos)

            st.subheader("🔁 Registros existentes")
            st.dataframe(existentes)

            st.subheader("❌ Registros removidos")
            st.dataframe(removidos)

            st.subheader("⚠️ Diferenças encontradas")
            st.dataframe(diferencas)

            # Download
            def convert_df(df):
                return df.to_csv(index=False).encode("utf-8")

            st.subheader("⬇️ Baixar resultados")

            st.download_button("Download Novos", convert_df(novos), "novos.csv", "text/csv")
            st.download_button("Download Existentes", convert_df(existentes), "existentes.csv", "text/csv")
            st.download_button("Download Removidos", convert_df(removidos), "removidos.csv", "text/csv")
            st.download_button("Download Diferenças", convert_df(diferencas), "diferencas.csv", "text/csv")