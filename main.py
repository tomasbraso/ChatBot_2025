import streamlit as st
import groq

altura_chat = 300
MODELOS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

def configurar_pagina():

    st.set_page_config(page_title="Chatbot de tomi", page_icon= "🚗")

    st.title("Chatbot de tomi")

    st.sidebar.title("Seleccion de modelos")

    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)

    return elegirModelo

def crear_usuario():
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key = clave_secreta)

def configurar_modelo(cliente, modelo_elegido, promt_usuario):
    return cliente.chat.completions.create(
        model = modelo_elegido, 
        messages = [{"role" : "user", "content" : promt_usuario}],
        stream = True
        )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol,contenido,avatar):
    st.session_state.mensajes.append({"role" : rol, "content" : contenido, "avatar" : avatar})


def mostrar_historial():
    for mensaje in st.session_state.mensajes: 
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])

def area_chat():
    contenedor = st.container (height=altura_chat, border=True)
    with contenedor:
        mostrar_historial()

def generar_respuesta(respuesta_en_web):
    respuesta_web = ""
    for frase in respuesta_en_web:
        if frase.choices[0].delta.content:
            respuesta_web += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_web

def main():
    modelo_usuario = configurar_pagina()

    cliente_usuario = crear_usuario()

    inicializar_estado()

    area_chat()

    prompt_usuario = st.chat_input("Escribi tu prompt: ")

    if prompt_usuario:
        actualizar_historial("user", prompt_usuario, "😲")
        respuesta_bot = configurar_modelo(cliente_usuario, modelo_usuario,prompt_usuario)
        if respuesta_bot:
            with st.chat_message("assistant"):
                respuesta_in_web = st.write_stream(generar_respuesta(respuesta_bot)) 
        actualizar_historial("assistant", respuesta_in_web, "🤖")
        st.rerun()

if __name__ == "__main__":
    main()