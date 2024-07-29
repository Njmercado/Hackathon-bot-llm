import time
import streamlit as st
from streamlit_chat import message
from rag.Chat import Chat
from nlp.NLP import NLP

st.set_page_config(page_title="Chatbot")

def display_messages():
  # st.subheader("Chat")
  for i, (msg, is_user) in enumerate(st.session_state["messages"]):
    message(msg, is_user=is_user, key=str(i))
  st.session_state["thinking_spinner"] = st.empty()


def process_input():
  if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
    user_text = st.session_state["user_input"].strip()
    with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
      agent_text = st.session_state["assistant"].ask(user_text)

    does_not_know = agent_text.split('.')[0] == "I don't know"

    st.session_state["messages"].append((user_text, True))
    if does_not_know:
      nlp_agent_text = NLP.ask(user_text)

      for text in nlp_agent_text:
        st.session_state["messages"].append(("NLP..." + text, False))
    else:
      st.session_state["messages"].append(("LLM..." + agent_text, False))


def read_and_save_file():
  # st.session_state["assistant"].ingest(file_path='./data/Precios_Medicamentos_20240728.csv', file_type='csv')
  # time.sleep(10)
  # st.session_state["assistant"].ingest(file_path='./data/Clicsalud_-_Term_metro_de_Precios_de_Medicamentos_20240727.csv', file_type='csv')
  # time.sleep(10)
  # st.session_state["assistant"].ingest(file_path='./data/EVENTOS_ADVERSOS_DE_MEDICAMENTOS_2019.csv', file_type='csv')
  # time.sleep(10)
  # st.session_state["assistant"].ingest(file_path='./data/LISTADO_DE_MEDICAMENTOS_EN_VENTA_LIBRE_20240728.csv', file_type='csv')
  # time.sleep(10)
  # st.session_state["assistant"].ingest(file_path='./data/resolucion-0371-de-2009.pdf', file_type='pdf')
  st.session_state["assistant"].ingest(file_path='./data/prueba.txt', file_type='txt')
  return

def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = Chat()

    st.header("Chatbot de inventario")

    read_and_save_file()

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)

if __name__ == "__main__":
    page()