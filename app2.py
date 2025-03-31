import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import requests

# Configuración de Azure Form Recognizer
AZURE_KEY = "CMuZd8vvpEQ0oHiSxSpqNOXK7sGKPMRNAdMroeyClByXE6MMZUfuJQQJ99BCACYeBjFXJ3w3AAALACOGtCSP"  # Reemplaza con tu clave
AZURE_ENDPOINT = "https://aonformrecognizer.cognitiveservices.azure.com/"  # Reemplaza con tu endpoint

# Configuración de DeepSeek (ejemplo - ajusta según tu API)
DEEPSEEK_KEY = "sk-e32d54b4d5904572b62630276a08d807"
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/process"

# Título de la aplicación
st.title("📑 Automatización Inteligente de Documentos")
st.markdown("""
Procesa documentos con **Azure AI** y potencia los resultados con **DeepSeek**!
""")

# Función para Azure Form Recognizer
def analyze_document(file):
    try:
        document_analysis_client = DocumentAnalysisClient(
            endpoint=AZURE_ENDPOINT,
            credential=AzureKeyCredential(AZURE_KEY)
        )
        
        file_bytes = file.read()
        poller = document_analysis_client.begin_analyze_document(
            model_id="prebuilt-document",
            document=file_bytes
        )
        return poller.result()
    except Exception as e:
        st.error(f"Error en Azure: {str(e)}")
        return None

# Función para DeepSeek (ejemplo)
def call_deepseek(text, task="summarize"):
    try:
        headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}"}
        data = {"text": text, "task": task}
        response = requests.post(DEEPSEEK_ENDPOINT, json=data, headers=headers)
        return response.json()
    except Exception as e:
        st.error(f"Error en DeepSeek: {str(e)}")
        return {"error": str(e)}

# Widget para subir archivos
uploaded_file = st.file_uploader("Sube un documento (PDF o imagen)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Mostrar preview
    if uploaded_file.type.startswith("image"):
        st.image(uploaded_file, caption="Documento subido", use_column_width=True)
    else:
        st.write(f"📤 Archivo subido: {uploaded_file.name}")

    # Botón de procesamiento
    if st.button("🚀 Procesar Documento"):
        with st.spinner("Analizando con Azure AI..."):
            azure_result = analyze_document(uploaded_file)
            
        if azure_result:
            # Extraer datos de Azure
            extracted_text = azure_result.content
            key_values = {kv.key.content: kv.value.content for kv in azure_result.key_value_pairs}
            
            with st.spinner("Potenciando con DeepSeek..."):
                deepseek_result = call_deepseek(extracted_text, task="summarize")
            
            # Mostrar resultados
            st.success("✅ Procesamiento completado!")
            
            # Sección en columnas
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📄 Texto Extraído")
                st.expander("Ver texto completo").write(extracted_text[:2000] + "...")  # Limita a 2000 caracteres

                st.subheader("🔍 Campos Clave")
                st.json(key_values)
                
                # Ejemplo: Gráfico si hay total
                if "total" in key_values:
                    try:
                        total = float(key_values["total"].replace("$", "").strip())
                        st.metric(label="💰 Total Identificado", value=f"${total:.2f}")
                    except:
                        pass

            with col2:
                st.subheader("✨ DeepSeek Insights")
                
                if "summary" in deepseek_result:
                    st.success("📝 Resumen Automático")
                    st.write(deepseek_result["summary"])
                
                if "entities" in deepseek_result:  # Ejemplo para entidades
                    st.success("🔎 Entidades Detectadas")
                    st.write(deepseek_result["entities"])
                
                # Espacio para más resultados de DeepSeek
                st.json(deepseek_result)  # Muestra todos los resultados

# Notas al pie
st.markdown("---")
st.caption("Demo creado con ❤️ usando Azure AI y DeepSeek")