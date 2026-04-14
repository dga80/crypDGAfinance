# CrypDGAFinance 💎

Calculadora fiscal inteligente para criptomonedas (MEXC) diseñada para facilitar la declaración de la Renta en España.

## 🚀 Características

- **IA-Driven**: Utiliza Google Gemini para la detección dinámica de archivos y auto-curación de datos.
- **Soporte MEXC**: Procesa automáticamente archivos de Futuros, Spot, Capital Flow y Retiradas.
- **Cálculo de IRPF**: Estimación automática según los tramos de 2024.
- **Gráficos Interactivos**: Visualiza tus ganancias y pérdidas con Plotly.
- **Exportación**: Descarga tus resultados en CSV y Excel.

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/dga80/crypDGAfinance.git
   cd crypDGAfinance
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

## ⚙️ Configuración AI

Obtén tu API Key gratuita en [Google AI Studio](https://aistudio.google.com/) e introdúcela en la barra lateral de la aplicación para activar las funciones inteligentes.
