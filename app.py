import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CrypDGAFinance · Calculadora Fiscal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Premium Dark AI Look
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 40%, #0a0f1a 100%);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hero header */
    .hero-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d2ff, #7b2ff7, #00d2ff);
        background-size: 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        letter-spacing: -1px;
        margin: 0;
    }
    @keyframes shimmer {
        0% { background-position: 0% }
        100% { background-position: 200% }
    }
    .hero-sub {
        color: rgba(255,255,255,0.45);
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* Badge pill */
    .badge {
        display: inline-block;
        background: linear-gradient(90deg, rgba(0,210,255,0.15), rgba(123,47,247,0.15));
        border: 1px solid rgba(0,210,255,0.3);
        color: #00d2ff;
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    /* Section cards */
    .section-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-desc {
        color: rgba(255,255,255,0.4);
        font-size: 0.85rem;
        margin-bottom: 1.2rem;
        margin-top: 0;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.5rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 210, 255, 0.15) !important;
    }
    div[data-testid="metric-container"] label {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }

    /* Positive / negative metric delta colors */
    div[data-testid="stMetricDelta"] svg { display: none; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff, #7b2ff7) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important;
    }

    /* Download button */
    .stDownloadButton > button {
        background: rgba(0, 210, 255, 0.1) !important;
        color: #00d2ff !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(0, 210, 255, 0.2) !important;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.3) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02) !important;
        border: 2px dashed rgba(0, 210, 255, 0.25) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        transition: border-color 0.3s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0, 210, 255, 0.5) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        color: rgba(255,255,255,0.8) !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderContent {
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.06) !important;
        margin: 2rem 0 !important;
    }

    /* Result highlight card */
    .result-highlight {
        background: linear-gradient(135deg, rgba(0,210,255,0.08), rgba(123,47,247,0.08));
        border: 1px solid rgba(0,210,255,0.2);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
        text-align: center;
    }
    .result-highlight h2 {
        color: #00d2ff !important;
        -webkit-text-fill-color: #00d2ff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0.2rem 0;
    }
    .result-highlight p {
        color: rgba(255,255,255,0.5);
        margin: 0;
        font-size: 0.9rem;
    }

    /* Tag badges */
    .tag-futuros { color: #00d2ff; background: rgba(0,210,255,0.1); padding: 2px 10px; border-radius: 20px; font-size:0.78rem; font-weight:600; }
    .tag-capitalflow { color: #a78bfa; background: rgba(167,139,250,0.1); padding: 2px 10px; border-radius: 20px; font-size:0.78rem; font-weight:600; }
    .tag-retiradas { color: #34d399; background: rgba(52,211,153,0.1); padding: 2px 10px; border-radius: 20px; font-size:0.78rem; font-weight:600; }
    .tag-spot { color: #facc15; background: rgba(250,204,21,0.1); padding: 2px 10px; border-radius: 20px; font-size:0.78rem; font-weight:600; }
    .tag-error { color: #f87171; background: rgba(248,113,113,0.1); padding: 2px 10px; border-radius: 20px; font-size:0.78rem; font-weight:600; }

    /* IRPF table */
    .irpf-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.9rem;
        color: rgba(255,255,255,0.75);
    }
    .irpf-row:last-child { border-bottom: none; }
    .irpf-highlight {
        color: #fbbf24;
        font-weight: 600;
    }

    /* Dataframe fix */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    [data-testid="stDataFrameResizable"] { border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 10px !important; }

    /* Input fields */
    .stNumberInput input, .stTextInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    .stDateInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }

    /* Success / error / info */
    .stAlert { border-radius: 10px !important; }

    /* Spinner */
    .stSpinner > div { border-top-color: #00d2ff !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: rgba(255,255,255,0.5) !important;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0,210,255,0.2), rgba(123,47,247,0.2)) !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS — Data Processing
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# AI ENGINE — Google Gemini Integration
# ─────────────────────────────────────────────

def get_gemini_client():
    api_key = st.session_state.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    
    system_instruction = (
        "Actúa como un Perito Contable Fiscal experto en la legislación española de criptomonedas. "
        "Tu objetivo es ayudar a procesar ficheros Excel de exchanges (MEXC) para calcular ganancias y pérdidas patrimoniales. "
        "Eres preciso, técnico y capaz de limpiar datos 'sucios' o mal formateados."
    )
    
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

def ai_detect_columns(df_headers, filename):
    """Usa Gemini para identificar qué columnas mapear a nuestro modelo tax."""
    model = get_gemini_client()
    if not model:
        return None
    
    prompt = f"""
    Analiza las cabeceras de este archivo Excel de MEXC llamado '{filename}':
    {df_headers}
    
    Identifica qué columnas corresponden a:
    1. 'pnl_bruto': Ganancia o pérdida cerrada (ej: 'Closing PNL', 'Realized PNL').
    2. 'comisiones': Comisiones de trading o retiro (ej: 'Trading Fee', 'Fee').
    3. 'funding': Pagos por financiación (ej: 'Amount' cuando el tipo es 'Funding').
    4. 'direccion_retiro': Dirección de destino de la cripto.
    5. 'monto': Cantidad de la transacción.
    
    Responde ÚNICAMENTE con un JSON válido con este formato:
    {{
        "tipo_archivo": "Futuros | Spot | Capital Flow | Retiradas | Desconocido",
        "mapeo": {{
            "pnl": "nombre_columna_original o null",
            "fee": "nombre_columna_original o null",
            "funding": "nombre_columna_original o null",
            "address": "nombre_columna_original o null",
            "amount": "nombre_columna_original o null"
        }}
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpiar posible markdown del JSON
        json_str = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_str)
    except Exception as e:
        st.error(f"Error en AI Detect: {e}")
        return None

def ai_fix_data(dirty_val, error_msg):
    """Self-healing: Si falla la limpieza estándar, Gemini lo arregla."""
    model = get_gemini_client()
    if not model:
        return None
    
    prompt = f"""
    El valor '{dirty_val}' causó el siguiente error al intentar convertirlo a float: '{error_msg}'.
    Por favor, devuélveme ÚNICAMENTE el valor numérico limpio como un float (ej: 1250.50).
    No añadas texto, solo el número.
    """
    
    try:
        response = model.generate_content(prompt)
        return float(response.text.strip())
    except:
        return None

XAMAN_ADDRESS = 'rUgqSQfdtxwii14t7mj2Fq2JUpF4xg29fm'

def clean_numeric(val) -> float:
    """Convierte valores numéricos con fallback a AI Self-Healing."""
    if pd.isna(val):
        return 0.0
    
    original_val = val
    if isinstance(val, str):
        val = val.replace(',', '').replace(' ', '').replace('USDT', '').replace('€', '').strip()
        try:
            return float(val)
        except ValueError as e:
            # Fallback a AI si el usuario tiene la API Key
            if st.session_state.get("gemini_api_key"):
                fixed = ai_fix_data(original_val, str(e))
                if fixed is not None:
                    return fixed
            return 0.0
    try:
        return float(val)
    except (ValueError, TypeError) as e:
        if st.session_state.get("gemini_api_key"):
            fixed = ai_fix_data(original_val, str(e))
            if fixed is not None:
                return fixed
        return 0.0


def identify_and_process_excel(file) -> dict:
    """Abre el .xlsx y usa Gemini para clasificación dinámica."""
    try:
        df = pd.read_excel(file, engine='openpyxl')
        columns = df.columns.tolist()
        
        # Intentar detección por AI si hay API Key
        ai_config = None
        if st.session_state.get("gemini_api_key"):
            with st.status("🤖 AI analizando esquema...", expanded=False):
                ai_config = ai_detect_columns(columns, file.name)
        
        if ai_config and ai_config['tipo_archivo'] != "Desconocido":
            return process_with_ai_config(df, file.name, ai_config)
        
        # Fallback a reglas fijas si no hay AI o falla
        if 'Closing PNL' in columns:
            return process_futures(df, file.name)
        elif 'Fund Type' in columns:
            return process_capital_flow(df, file.name)
        elif 'Withdrawal Address' in columns:
            return process_withdrawals(df, file.name)
        elif 'Transaction Type' in columns and 'Direction' in columns:
            return process_spot(df, file.name)
        else:
            return {
                "type": "Desconocido",
                "filename": file.name,
                "error": f"No se pudo clasificar. Cabeceras encontradas: {', '.join(columns[:8])}..."
            }
    except Exception as e:
        return {"type": "Error", "filename": file.name, "error": str(e)}

def process_with_ai_config(df, filename, config):
    """Procesador genérico basado en el mapeo de Gemini."""
    tipo = config['tipo_archivo']
    mapeo = config['mapeo']
    
    pnl = 0.0
    fees = 0.0
    
    if mapeo.get('pnl') in df.columns:
        df['PNL_Clean'] = df[mapeo['pnl']].apply(clean_numeric)
        pnl = df['PNL_Clean'].sum()
        
    if mapeo.get('fee') in df.columns:
        df['Fee_Clean'] = df[mapeo['fee']].apply(clean_numeric)
        fees = df['Fee_Clean'].sum()
    
    # Lógica específica por tipo para detalles
    details = f"IA detectó tipo: **{tipo}**\n"
    if pnl != 0: details += f"PNL detectado: **{pnl:,.2f}**\n"
    if fees != 0: details += f"Fees detectados: **{fees:,.2f}**\n"
    
    # Mapeo interno para que el resto de la app funcione
    if tipo == "Futuros":
        return {"type": "Futuros", "filename": filename, "gross_profit": pnl, "trading_fees": fees, "rows": len(df), "details": details}
    elif tipo == "Spot":
        return {"type": "Spot", "filename": filename, "spot_pnl": pnl, "spot_fees": fees, "rows": len(df), "details": details}
    elif tipo == "Capital Flow":
        return {"type": "Capital Flow", "filename": filename, "funding_fees": pnl if pnl != 0 else fees, "rows": len(df), "details": details}
    elif tipo == "Retiradas":
        # Verificación de Xaman en retiradas
        xaman_transfers = []
        addr_col = mapeo.get('address')
        amt_col = mapeo.get('amount')
        if addr_col in df.columns and amt_col in df.columns:
            xaman_df = df[df[addr_col] == XAMAN_ADDRESS].copy()
            for _, row in xaman_df.iterrows():
                xaman_transfers.append({
                    "Fecha": "N/A",
                    "Importe (USDT)": clean_numeric(row[amt_col]),
                    "Dirección": XAMAN_ADDRESS,
                    "Tipo": "Transferencia Interna (IA Verified)"
                })
        return {"type": "Retiradas", "filename": filename, "withdrawal_fees": fees, "xaman_transfers": xaman_transfers, "rows": len(df), "details": details}
    
    return {"type": tipo, "filename": filename, "details": details, "rows": len(df)}


def process_futures(df: pd.DataFrame, filename: str) -> dict:
    gross_profit = 0.0
    trading_fees = 0.0

    if 'Closing PNL' in df.columns:
        df['Closing PNL'] = df['Closing PNL'].apply(clean_numeric)
        gross_profit = df['Closing PNL'].sum()

    if 'Trading Fee' in df.columns:
        df['Trading Fee'] = df['Trading Fee'].apply(clean_numeric)
        trading_fees = df['Trading Fee'].sum()

    return {
        "type": "Futuros",
        "filename": filename,
        "gross_profit": gross_profit,
        "trading_fees": trading_fees,
        "rows": len(df),
        "details": f"Closing PNL (bruto): **{gross_profit:,.2f} USDT**\nTrading Fees: **{trading_fees:,.2f} USDT**"
    }


def process_capital_flow(df: pd.DataFrame, filename: str) -> dict:
    funding_fees = 0.0

    if 'Fund Type' in df.columns and 'Amount' in df.columns:
        funding_df = df[df['Fund Type'].str.contains('funding', case=False, na=False)].copy()
        funding_df['Amount'] = funding_df['Amount'].apply(clean_numeric)
        funding_fees = funding_df['Amount'].sum()

    return {
        "type": "Capital Flow",
        "filename": filename,
        "funding_fees": funding_fees,
        "rows": len(df),
        "details": f"Funding Fees neto: **{funding_fees:,.2f} USDT**"
    }


def process_spot(df: pd.DataFrame, filename: str) -> dict:
    """Procesa el Spot Account Statement de MEXC.
    Identifica fees pagados y calcula el volumen total de compras/ventas.
    """
    fees_total = 0.0
    total_buy_qty = 0.0
    total_sell_qty = 0.0
    spot_pnl = 0.0  # Intentamos calcular si hay columna de Amount/Total

    # Limpiamos columnas numéricas clave
    for col in ['Quantity', 'Amount', 'Fee', 'Price', 'Total']:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric)

    # También puede llamarse 'Transaction Fee' o 'Trading Fee'
    for fee_col in ['Fee', 'Transaction Fee', 'Trading Fee']:
        if fee_col in df.columns:
            fees_total += df[fee_col].apply(clean_numeric).abs().sum()
            break

    # Separar compras y ventas por Direction
    if 'Direction' in df.columns and 'Quantity' in df.columns:
        buys = df[df['Direction'].str.strip().str.lower() == 'buy']
        sells = df[df['Direction'].str.strip().str.lower() == 'sell']
        total_buy_qty = buys['Quantity'].sum()
        total_sell_qty = sells['Quantity'].sum()

    # Si hay columna 'Total' o 'Amount' en USDT → intentamos PNL aproximado
    if 'Total' in df.columns:
        df['Total_Clean'] = df['Total'].apply(clean_numeric)
        if 'Direction' in df.columns:
            ventas_total = df[df['Direction'].str.strip().str.lower() == 'sell']['Total_Clean'].sum()
            compras_total = df[df['Direction'].str.strip().str.lower() == 'buy']['Total_Clean'].sum()
            spot_pnl = ventas_total - compras_total
    elif 'Amount' in df.columns:
        df['Amount_Clean'] = df['Amount'].apply(clean_numeric)
        if 'Direction' in df.columns:
            ventas_total = df[df['Direction'].str.strip().str.lower() == 'sell']['Amount_Clean'].sum()
            compras_total = df[df['Direction'].str.strip().str.lower() == 'buy']['Amount_Clean'].sum()
            spot_pnl = ventas_total - compras_total

    # Tipos de transacción disponibles
    tx_types = df['Transaction Type'].unique().tolist() if 'Transaction Type' in df.columns else []

    return {
        "type": "Spot",
        "filename": filename,
        "spot_fees": fees_total,
        "spot_pnl": spot_pnl,
        "compras_total": compras_total if 'compras_total' in locals() else 0.0,
        "ventas_total": ventas_total if 'ventas_total' in locals() else 0.0,
        "total_buy_qty": total_buy_qty,
        "total_sell_qty": total_sell_qty,
        "tx_types": tx_types,
        "rows": len(df),
        "details": (
            f"📊 Tipos de transacción: **{', '.join(str(t) for t in tx_types[:5])}**\n"
            f"📈 Qty Comprada: **{total_buy_qty:,.4f}** | Qty Vendida: **{total_sell_qty:,.4f}**\n"
            f"💸 Fees Spot: **{fees_total:,.4f}**\n"
            f"📋 PNL estimado (ventas - compras): **{spot_pnl:,.2f} USDT**\n"
            f"⚠️ *El Spot Statement refleja movimientos internos. Revisa si hay ganancias realizadas.*"
        )
    }


def process_withdrawals(df: pd.DataFrame, filename: str) -> dict:
    withdrawal_fees = 0.0
    xaman_transfers = []

    if 'Trading Fee' in df.columns:
        df['Trading Fee'] = df['Trading Fee'].apply(clean_numeric)
        withdrawal_fees = df['Trading Fee'].sum()
    elif 'Fee' in df.columns:
        df['Fee'] = df['Fee'].apply(clean_numeric)
        withdrawal_fees = df['Fee'].sum()

    if 'Withdrawal Address' in df.columns and 'Amount' in df.columns:
        xaman_df = df[df['Withdrawal Address'] == XAMAN_ADDRESS].copy()
        if not xaman_df.empty:
            xaman_df['Amount_Clean'] = xaman_df['Amount'].apply(clean_numeric)
            for _, row in xaman_df.iterrows():
                xaman_transfers.append({
                    "Fecha": row.get('Time', row.get('Date', 'N/A')),
                    "Importe (USDT)": row['Amount_Clean'],
                    "Dirección": XAMAN_ADDRESS,
                    "Tipo": "Transferencia Interna (No tributable)"
                })

    return {
        "type": "Retiradas",
        "filename": filename,
        "withdrawal_fees": withdrawal_fees,
        "xaman_transfers": xaman_transfers,
        "rows": len(df),
        "details": f"Comisiones retirada: **{withdrawal_fees:,.2f} USDT**\nTransferencias a Xaman: **{len(xaman_transfers)}**"
    }


# ─────────────────────────────────────────────
# IRPF SPAIN — Tramos 2024
# ─────────────────────────────────────────────

def calcular_irpf(ganancia: float) -> dict:
    """Calcula el IRPF estimado sobre ganancias patrimoniales según tramos 2024."""
    if ganancia <= 0:
        return {"impuesto": 0.0, "desglose": [], "tipo_efectivo": 0.0}

    tramos = [
        (6000,   0.19),
        (44000,  0.21),
        (150000, 0.23),
        (float('inf'), 0.28),
    ]

    impuesto = 0.0
    base_restante = ganancia
    desglose = []
    limite_anterior = 0

    for limite, tipo in tramos:
        if base_restante <= 0:
            break
        tramo_size = limite - limite_anterior
        en_este_tramo = min(base_restante, tramo_size)
        impuesto_tramo = en_este_tramo * tipo
        impuesto += impuesto_tramo
        desglose.append({
            "Tramo": f"Hasta {limite:,.0f} €" if limite != float('inf') else "Más de 150.000 €",
            "Base en tramo": en_este_tramo,
            "Tipo": f"{tipo*100:.0f}%",
            "Cuota": impuesto_tramo
        })
        base_restante -= en_este_tramo
        limite_anterior = limite

    tipo_efectivo = (impuesto / ganancia) * 100 if ganancia > 0 else 0

    return {
        "impuesto": impuesto,
        "desglose": desglose,
        "tipo_efectivo": tipo_efectivo
    }


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if 'fiat_deposits' not in st.session_state:
    st.session_state.fiat_deposits = []
if 'delete_idx' not in st.session_state:
    st.session_state.delete_idx = None


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", width=100)
    
    with st.expander("⚙️ Configuración AI", expanded=False):
        st.markdown("---")
        api_key_input = st.text_input(
            "Gemini API Key", 
            type="password", 
            value=st.session_state.get("gemini_api_key", ""),
            help="Obtén tu clave en Google AI Studio"
        )
        if api_key_input:
            st.session_state.gemini_api_key = api_key_input
            st.success("API Key cargada")
        
        st.info("💡 Si has configurado la clave en los Secrets de Streamlit o .env, la app la detectará automáticamente.")

st.markdown("""
<div class="hero-header">
    <div class="badge">⚡ IA-DRIVEN · FISCALIDAD CRIPTO</div>
    <h1 class="hero-title">CrypDGAFinance</h1>
    <p class="hero-sub">Calculadora fiscal inteligente para criptomonedas en España · Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📂  Importar & Calcular", "🏦  Depósitos Fiat", "📊  Análisis & IRPF"])

# ════════════════════════════════════════════
# TAB 1: IMPORT & CALCULATE
# ════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📂 Archivos Excel de MEXC</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Compatible con: Futuros (Closing PNL), Capital Flow (Funding), Retiradas (Withdrawal). Puedes subir múltiples archivos a la vez.</p>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Arrastra o selecciona tus archivos .xlsx de MEXC",
        type="xlsx",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_files:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">⚙️ Procesando archivos...</p>', unsafe_allow_html=True)

        total_gross_profit    = 0.0
        total_trading_fees    = 0.0
        total_funding_fees    = 0.0
        total_withdrawal_fees  = 0.0
        total_spot_fees       = 0.0
        total_spot_pnl        = 0.0
        total_spot_compras    = 0.0
        total_spot_ventas     = 0.0
        all_xaman_transfers   = []
        results_data          = []
        file_summary_rows     = []

        for file in uploaded_files:
            with st.spinner(f'Analizando `{file.name}`...'):
                result = identify_and_process_excel(file)

            results_data.append(result)

            tipo = result['type']
            has_error = "error" in result

            if not has_error:
                if tipo == "Futuros":
                    total_gross_profit  += result.get('gross_profit', 0)
                    total_trading_fees  += result.get('trading_fees', 0)
                elif tipo == "Capital Flow":
                    total_funding_fees  += result.get('funding_fees', 0)
                elif tipo == "Retiradas":
                    total_withdrawal_fees += result.get('withdrawal_fees', 0)
                    all_xaman_transfers.extend(result.get('xaman_transfers', []))
                elif tipo == "Spot":
                    total_spot_fees += result.get('spot_fees', 0)
                    total_spot_pnl  += result.get('spot_pnl', 0)
                    total_spot_compras += result.get('compras_total', 0)
                    total_spot_ventas  += result.get('ventas_total', 0)

                tag_class = {
                    "Futuros": "tag-futuros",
                    "Capital Flow": "tag-capitalflow",
                    "Retiradas": "tag-retiradas",
                    "Spot": "tag-spot"
                }.get(tipo, "tag-error")

                with st.expander(f"**{file.name}**", expanded=False):
                    col_t, col_r = st.columns([3, 1])
                    with col_t:
                        st.markdown(f'<span class="{tag_class}">{tipo}</span>', unsafe_allow_html=True)
                        st.markdown(result.get('details', ''))
                    with col_r:
                        st.metric("Registros", result.get('rows', '—'))

                    if result.get('xaman_transfers'):
                        st.warning(f"⚠️ {len(result['xaman_transfers'])} transferencias internas a Xaman detectadas (no tributables)")
                        st.dataframe(pd.DataFrame(result['xaman_transfers']), use_container_width=True)

                    if tipo == "Spot" and result.get('tx_types'):
                        st.info(f"📌 Tipos de transacción detectados: `{'`, `'.join(str(t) for t in result['tx_types'])}`")

                file_summary_rows.append({
                    "Archivo": file.name,
                    "Tipo": tipo,
                    "Registros": result.get('rows', 0)
                })
            else:
                st.error(f"❌ Error en `{file.name}`: {result['error']}")

        st.markdown('</div>', unsafe_allow_html=True)

        # ── CÁLCULO FISCAL FINAL ──────────────────────────
        st.markdown("---")
        st.markdown('<p class="section-title">🧮 Resultado Fiscal para Hacienda</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Según la normativa española de tributación de criptomonedas (IRPF — Ganancias y Pérdidas Patrimoniales)</p>', unsafe_allow_html=True)

        deductible_trading  = -abs(total_trading_fees) if total_trading_fees != 0 else 0.0
        deductible_withdraw = -abs(total_withdrawal_fees) if total_withdrawal_fees != 0 else 0.0
        deductible_spot     = -abs(total_spot_fees) if total_spot_fees != 0 else 0.0
        net_funding         = total_funding_fees

        gastos_deducibles = deductible_trading + deductible_withdraw + deductible_spot
        if net_funding < 0:
            gastos_deducibles += net_funding
            net_funding_profit = 0.0
        else:
            net_funding_profit = net_funding

        beneficio_bruto  = total_gross_profit + net_funding_profit + total_spot_pnl
        resultado_neto   = beneficio_bruto + gastos_deducibles

        # ── DATOS PARA CASILLAS HACIENDA ──────────────────
        # Agrupación por lotes para Casillas 1800-1814
        # Transmisión: Ventas Spot + Ganancias Futuros/Funding
        # Adquisición: Compras Spot + Comisiones + Pérdidas Futuros/Funding
        
        val_transmision = (total_spot_ventas + 
                           max(total_gross_profit, 0) + 
                           max(total_funding_fees, 0))
        
        val_adquisicion = (total_spot_compras + 
                           abs(min(total_gross_profit, 0)) + 
                           abs(min(total_funding_fees, 0)) + 
                           abs(total_trading_fees) + 
                           abs(total_spot_fees) + 
                           abs(total_withdrawal_fees))
        
        # Base de coste fiat
        total_fiat = sum(d["Importe (€)"] for d in st.session_state.fiat_deposits)
        ganancia_sobre_base = resultado_neto - total_fiat if total_fiat > 0 else resultado_neto

        # Metrics row 1
        col1, col2, col3, col_extra = st.columns(4)
        col1.metric("📈 Futures PNL", f"{total_gross_profit:,.2f} USDT")
        col2.metric("📊 Spot PNL Est.", f"{total_spot_pnl:,.2f} USDT")
        col3.metric("💸 Funding Neto", f"{net_funding:,.2f} USDT")
        col_extra.metric("💰 Beneficio Bruto", f"{beneficio_bruto:,.2f} USDT")

        st.markdown("")

        # Metrics row 2
        col4, col5, col6, col_s = st.columns(4)
        col4.metric("🔻 Futures Fees", f"{deductible_trading:,.2f} USDT")
        col5.metric("🔻 Spot Fees", f"{deductible_spot:,.2f} USDT")
        col6.metric("🔻 Withdraw Fees", f"{deductible_withdraw:,.2f} USDT")
        col_s.metric("📋 Total Gastos", f"{gastos_deducibles:,.2f} USDT")

        st.markdown("")

        # RESULTADO FINAL HIGHLIGHT
        color = "#00d2ff" if resultado_neto >= 0 else "#f87171"
        emoji = "🟢" if resultado_neto >= 0 else "🔴"
        st.markdown(f"""
        <div class="result-highlight">
            <p>Resultado Neto Final para la Casilla de Hacienda {emoji}</p>
            <h2 style="color:{color}; -webkit-text-fill-color:{color}">{resultado_neto:,.2f} USDT</h2>
            {"<p>Base de Coste Fiat: <strong>" + f"{total_fiat:,.2f} €</strong> → Ganancia real estimada: <strong>" + f"{ganancia_sobre_base:,.2f} USDT</strong></p>" if total_fiat > 0 else ""}
        </div>
        """, unsafe_allow_html=True)

        if all_xaman_transfers:
            with st.expander(f"🔄 {len(all_xaman_transfers)} Transferencias Internas a Xaman (No Tributables)", expanded=False):
                st.dataframe(pd.DataFrame(all_xaman_transfers), use_container_width=True)

        # ── DESCARGA CSV ──────────────────────────────────
        st.markdown("---")
        st.markdown('<p class="section-title">💾 Descargar Resumen</p>', unsafe_allow_html=True)

        summary_dict = {
            "Concepto": [
                "Valor de Adquisición Total (Compras + Comisiones + Pérdidas)",
                "Valor de Transmisión Total (Ventas + Ganancias)",
                "Resultado Neto Final (Casilla Hacienda)",
                "Futures PNL Bruto",
                "Spot PNL Estimado",
                "Funding Fees Neto",
                "Total Gastos Deducibles",
                "Base de Coste Fiat (€)",
                "Ganancia sobre Base de Coste"
            ],
            "Valor (USDT / €)": [
                val_adquisicion,
                val_transmision,
                resultado_neto,
                total_gross_profit,
                total_spot_pnl,
                net_funding,
                gastos_deducibles,
                total_fiat,
                ganancia_sobre_base
            ]
        }
        summary_df = pd.DataFrame(summary_dict)
        csv = summary_df.to_csv(index=False).encode('utf-8')

        col_dl1, col_dl2, _ = st.columns([1, 1, 2])
        with col_dl1:
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name=f'resumen_fiscal_mexc_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
            )
        with col_dl2:
            # Excel download
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                summary_df.to_excel(writer, sheet_name='Resumen Fiscal', index=False)
                if all_xaman_transfers:
                    pd.DataFrame(all_xaman_transfers).to_excel(writer, sheet_name='Xaman (Internas)', index=False)
            st.download_button(
                label="⬇️ Descargar Excel",
                data=excel_buffer.getvalue(),
                file_name=f'resumen_fiscal_mexc_{datetime.now().strftime("%Y%m%d")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

        # Store for Tab 3
        st.session_state['calc_results'] = {
            "total_gross_profit": total_gross_profit,
            "total_spot_pnl": total_spot_pnl,
            "net_funding": net_funding,
            "beneficio_bruto": beneficio_bruto,
            "deductible_trading": deductible_trading,
            "deductible_spot": deductible_spot,
            "deductible_withdraw": deductible_withdraw,
            "gastos_deducibles": gastos_deducibles,
            "resultado_neto": resultado_neto,
            "val_adquisicion": val_adquisicion,
            "val_transmision": val_transmision,
            "total_fiat": total_fiat,
            "ganancia_sobre_base": ganancia_sobre_base
        }
    else:
        st.markdown("""
        <div style="text-align:center; padding: 3rem; color: rgba(255,255,255,0.25);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📂</div>
            <p style="font-size:1rem;">Sube tus archivos .xlsx de MEXC para comenzar el análisis</p>
            <p style="font-size:0.8rem;">Futuros · Capital Flow · Retiradas</p>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2: DEPÓSITOS FIAT
# ════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">🏦 Depósitos de Fondos Fiat (Base de Coste)</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Añade manualmente los depósitos realizados desde Wise u otras cuentas bancarias. Esta información se usa para calcular tu ganancia real sobre la inversión inicial.</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        deposit_date = st.date_input("📅 Fecha del Depósito", key="dep_date")
    with col2:
        deposit_amount = st.number_input("💶 Importe en Euros (€)", min_value=0.0, step=50.0, format="%.2f", key="dep_amount")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Añadir", use_container_width=True):
            if deposit_amount > 0:
                st.session_state.fiat_deposits.append({
                    "Fecha": deposit_date.strftime("%Y-%m-%d"),
                    "Importe (€)": deposit_amount
                })
                st.success(f"✅ Depósito de {deposit_amount:,.2f} € añadido")
                st.rerun()
            else:
                st.warning("El importe debe ser mayor que 0")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.fiat_deposits:
        fiat_df = pd.DataFrame(st.session_state.fiat_deposits)
        total_fiat = fiat_df["Importe (€)"].sum()

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total Depósitos (Base de Coste)", f"{total_fiat:,.2f} €")
        col_m2.metric("Número de Depósitos", len(st.session_state.fiat_deposits))

        st.markdown("")
        st.markdown('<p class="section-title">📋 Lista de Depósitos</p>', unsafe_allow_html=True)

        for i, dep in enumerate(st.session_state.fiat_deposits):
            col_d, col_a, col_del = st.columns([2, 2, 1])
            with col_d:
                st.markdown(f"<span style='color:rgba(255,255,255,0.6); font-size:0.9rem'>📅 {dep['Fecha']}</span>", unsafe_allow_html=True)
            with col_a:
                st.markdown(f"<span style='color:#00d2ff; font-weight:600; font-size:0.95rem'>💶 {dep['Importe (€)']:,.2f} €</span>", unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_{i}", help="Eliminar este depósito"):
                    st.session_state.fiat_deposits.pop(i)
                    st.rerun()

        st.markdown("")
        col_clear, _ = st.columns([1, 3])
        with col_clear:
            if st.button("🗑️ Limpiar todos los depósitos"):
                st.session_state.fiat_deposits = []
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding: 2.5rem; color: rgba(255,255,255,0.25);">
            <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">💶</div>
            <p style="font-size:0.95rem;">Aún no has añadido depósitos fiat.<br>Añade tus transferencias de Wise para calcular tu Base de Coste real.</p>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 3: ANÁLISIS & IRPF
# ════════════════════════════════════════════
with tab3:
    results = st.session_state.get('calc_results', None)

    if results:
        # DATA FOR TAX FORM
        st.markdown('<p class="section-title">🏠 Resumen para el Formulario de la Renta (Casillas 1800-1814)</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Copia estos valores en el apartado de Ganancias y Pérdidas Patrimoniales de la AEAT.</p>', unsafe_allow_html=True)
        
        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            st.markdown(f"""
            <div style="background: rgba(0,210,255,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0,210,255,0.2); text-align: center;">
                <p style="color:rgba(255,255,255,0.5); font-size:0.8rem; margin:0;">VALOR DE ADQUISICIÓN</p>
                <h3 style="color:#ffffff; margin:0.5rem 0;">{results['val_adquisicion']:,.2f} €</h3>
                <p style="font-size:0.7rem; color:rgba(255,255,255,0.3);">(Compras + Comisiones + Pérdidas)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_h2:
            st.markdown(f"""
            <div style="background: rgba(0,210,255,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0,210,255,0.2); text-align: center;">
                <p style="color:rgba(255,255,255,0.5); font-size:0.8rem; margin:0;">VALOR DE TRANSMISIÓN</p>
                <h3 style="color:#ffffff; margin:0.5rem 0;">{results['val_transmision']:,.2f} €</h3>
                <p style="font-size:0.7rem; color:rgba(255,255,255,0.3);">(Ventas + Ganancias)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_h3:
            emoji = "🟢" if results['resultado_neto'] >= 0 else "🔴"
            color = "#34d399" if results['resultado_neto'] >= 0 else "#f87171"
            st.markdown(f"""
            <div style="background: rgba({ '52,211,153' if results['resultado_neto'] >= 0 else '248,113,113' },0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid {color}; text-align: center;">
                <p style="color:rgba(255,255,255,0.5); font-size:0.8rem; margin:0;">RESULTADO NETO {emoji}</p>
                <h3 style="color:{color}; margin:0.5rem 0;">{results['resultado_neto']:,.2f} €</h3>
                <p style="font-size:0.7rem; color:rgba(255,255,255,0.3);">(Diferencia fiscal final)</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # PIE CHART
        st.markdown('<p class="section-title">📊 Composición del Resultado</p>', unsafe_allow_html=True)

        labels = ["Futures PNL", "Spot PNL", "Funding (si +)", "Futures Fees", "Spot Fees", "Withdraw Fees"]
        values = [
            max(results["total_gross_profit"], 0),
            max(results["total_spot_pnl"], 0),
            max(results["net_funding"], 0),
            abs(results["deductible_trading"]),
            abs(results["deductible_spot"]),
            abs(results["deductible_withdraw"])
        ]
        colors = ["#00d2ff", "#facc15", "#a78bfa", "#f87171", "#fbbf24", "#34d399"]

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color='rgba(0,0,0,0)', width=0)),
            textfont=dict(family="Inter", size=13),
        )])
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
            annotations=[dict(
                text=f"<b>{results['resultado_neto']:,.0f}</b><br>USDT neto",
                x=0.5, y=0.5,
                font=dict(size=16, color='white', family='Inter'),
                showarrow=False
            )]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # BAR CHART — waterfall style
        st.markdown('<p class="section-title">📉 Desglose Waterfall</p>', unsafe_allow_html=True)

        bar_labels = ["Futures PNL", "Spot PNL", "+ Funding", "- Fut. Fees", "- Spot Fees", "- Ret. Fees", "= Neto Final"]
        bar_values = [
            results["total_gross_profit"],
            results["total_spot_pnl"],
            results["net_funding"],
            results["deductible_trading"],
            results["deductible_spot"],
            results["deductible_withdraw"],
            results["resultado_neto"]
        ]
        bar_colors = [
            "#00d2ff" if v >= 0 else "#f87171"
            for v in bar_values
        ]

        fig_bar = go.Figure(go.Bar(
            x=bar_labels,
            y=bar_values,
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{v:,.2f}" for v in bar_values],
            textposition='outside',
            textfont=dict(color='white', size=11),
        ))
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='rgba(255,255,255,0.6)', family='Inter'),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=True, zerolinecolor='rgba(255,255,255,0.15)'),
            margin=dict(t=30, b=10, l=10, r=10),
            height=300,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # IRPF CALCULATION
        st.markdown("---")
        st.markdown('<p class="section-title">🇪🇸 Estimación IRPF — Tramos 2024</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Cálculo estimado del impuesto a pagar en la declaración de la Renta sobre las ganancias patrimoniales de criptomonedas.</p>', unsafe_allow_html=True)

        ganancia_base = max(results["resultado_neto"], 0)

        col_irpf1, col_irpf2 = st.columns([2, 1])
        with col_irpf1:
            ganancia_irpf = st.number_input(
                "Ganancia patrimonial a calcular (USDT ≈ €)",
                value=float(f"{ganancia_base:.2f}"),
                min_value=0.0,
                step=100.0,
                format="%.2f",
                help="Por defecto usa el Resultado Neto Final. Ajusta según el tipo de cambio real USDT/EUR."
            )

        irpf = calcular_irpf(ganancia_irpf)

        col_i1, col_i2, col_i3 = st.columns(3)
        col_i1.metric("Base Imponible", f"{ganancia_irpf:,.2f} €")
        col_i2.metric("💸 Impuesto Estimado", f"{irpf['impuesto']:,.2f} €")
        col_i3.metric("📊 Tipo Efectivo", f"{irpf['tipo_efectivo']:.2f}%")

        if irpf['desglose']:
            st.markdown("")
            st.markdown('<p class="section-title">Desglose por Tramos</p>', unsafe_allow_html=True)
            tramos_df = pd.DataFrame(irpf['desglose'])
            tramos_df["Base en tramo"] = tramos_df["Base en tramo"].apply(lambda x: f"{x:,.2f} €")
            tramos_df["Cuota"] = tramos_df["Cuota"].apply(lambda x: f"{x:,.2f} €")
            st.dataframe(tramos_df, use_container_width=True, hide_index=True)

            neto_tras_irpf = ganancia_irpf - irpf['impuesto']
            st.markdown(f"""
            <div class="result-highlight" style="margin-top:1rem;">
                <p>Neto estimado tras IRPF</p>
                <h2 style="color:#34d399; -webkit-text-fill-color:#34d399">{neto_tras_irpf:,.2f} €</h2>
                <p>Después de pagar {irpf['impuesto']:,.2f} € al fisco ({irpf['tipo_efectivo']:.2f}% efectivo)</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding: 3rem; color: rgba(255,255,255,0.25);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <p style="font-size:1rem;">Importa tus archivos en la pestaña <strong>Importar & Calcular</strong> para ver el análisis aquí.</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:rgba(255,255,255,0.2); font-size:0.78rem; padding-bottom:1rem;">
    CrypDGAFinance · Calculadora Fiscal Cripto IA-Driven · Solo orientativo, no constituye asesoramiento fiscal.
</div>
""", unsafe_allow_html=True)
