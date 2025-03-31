import streamlit as st

# Título de la aplicación
st.title("Demo: Automatización Inteligente de Procesamiento de Documentos para TCS")

# Subtítulo
st.markdown("""
Esta aplicación permite subir un documento (PDF o imagen) y procesarlo utilizando **Azure AI** y **DeepSeek**.
""")

# Widget para subir archivos
uploaded_file = st.file_uploader("Sube un documento (PDF o imagen)", type=["pdf", "png", "jpg", "jpeg"])

# Verificar si se ha subido un archivo
if uploaded_file is not None:
    # Mostrar el nombre del archivo
    st.success(f"Archivo subido: {uploaded_file.name}")

    # Mostrar el contenido del archivo (si es una imagen)
    if uploaded_file.type.startswith("image"):
        st.image(uploaded_file, caption="Documento subido", use_column_width=True)
    elif uploaded_file.type == "application/pdf":
        st.write("**PDF subido**. Puedes procesarlo haciendo clic en el botón de abajo.")

    # Botón para procesar el documento
    if st.button("Procesar Documento"):
        with st.spinner("Procesando el documento..."):
            # Aquí irá la lógica para procesar el documento con Azure y DeepSeek
            st.success("¡Documento procesado con éxito!")
            # Mostrar resultados (esto lo completaremos en los siguientes pasos)
            st.write("Resultados del procesamiento:")
            st.json({"campo1": "valor1", "campo2": "valor2"})  # Ejemplo de resultados