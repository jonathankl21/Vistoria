import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Vistoria Mobile", page_icon="📦", layout="centered")

st.title("📦 Vistoria de Armários")

# ==========================================
# 1. CABEÇALHO DA VISTORIA
# ==========================================
col_a, col_b = st.columns(2)
with col_a:
    lacre = st.text_input("Número do Lacre (Obrigatório)*")
with col_b:
    data_vistoria = st.date_input("Data da Vistoria")

if 'lista_itens' not in st.session_state:
    st.session_state['lista_itens'] = []

st.divider()

# ==========================================
# 2. ÁREA DE ADIÇÃO DE MATERIAIS
# ==========================================
st.subheader("Adicionar Material Encontrado")

with st.form("form_materiais", clear_on_submit=True):
    produto = st.text_input("Nome do Produto*")
    
    col1, col2 = st.columns(2)
    with col1:
        qtd = st.number_input("Quantidade", min_value=1, step=1)
    with col2:
        valor = st.number_input("Valor Aproximado (R$)", min_value=0.0, step=1.0)
    
    btn_adicionar = st.form_submit_button("➕ Adicionar à Lista")

    if btn_adicionar:
        if not lacre or not produto:
            st.warning("⚠️ Preencha o Lacre e o Produto!")
        else:
            novo_item = {
                "Data": data_vistoria.strftime("%d/%m/%Y"),
                "Lacre": lacre,
                "Produto": produto.upper(),
                "Quantidade": qtd,
                "Valor_RS": valor
            }
            st.session_state['lista_itens'].append(novo_item)
            st.success(f"✅ {produto} adicionado ao Lacre {lacre}!")

# ==========================================
# 3. RESUMO E DOWNLOAD DO CSV
# ==========================================
if len(st.session_state['lista_itens']) > 0:
    st.divider()
    st.write("### 🛒 Resumo da Vistoria Atual:")
    
    # Transforma a memória numa Tabela de Dados
    df_final = pd.DataFrame(st.session_state['lista_itens'])
    st.dataframe(df_final, use_container_width=True, hide_index=True)

    # Converte a tabela para o formato CSV que o Excel entende (separado por ponto e vírgula)
    csv = df_final.to_csv(index=False, sep=";", encoding="utf-8-sig")

    # O Botão Mágico de Download
    st.download_button(
        label="⬇️ BAIXAR PLANILHA CSV",
        data=csv,
        file_name=f"vistoria_{datetime.now().strftime('%d%m%Y_%H%M')}.csv",
        mime="text/csv",
        type="primary",
        use_container_width=True
    )
    
    # Um botão extra caso ela queira limpar a tela para começar outro andar/corredor
    if st.button("🗑️ Limpar Tela e Começar Nova Vistoria", use_container_width=True):
        st.session_state['lista_itens'] = []
        st.rerun()