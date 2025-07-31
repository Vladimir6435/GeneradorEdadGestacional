import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

months_map = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
    "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

def build_date(dia, mes_str, ano):
    mes = months_map.get(mes_str, 0)
    if mes == 0 or dia < 1 or dia > 31 or ano < 2020 or ano > 2050:
        return None, "Error: Datos de fecha inválidos o año parece ser equivocado."
    try:
        return f"{dia:02d}/{mes:02d}/{ano}", None
    except ValueError:
        return None, "Error: Fecha inválida."

def calcular_edad_gestacional(fecha_ultima_regla, fecha_actual=None):
    try:
        fur = datetime.strptime(fecha_ultima_regla, '%d/%m/%Y')
        if fecha_actual is None:
            hoy = datetime.now()
        else:
            hoy = datetime.strptime(fecha_actual, '%d/%m/%Y')
        
        diferencia = hoy - fur
        dias_totales = diferencia.days
        
        if dias_totales < 0:
            return 0, 0, "Error: La fecha de última regla no puede ser futura", None
        if dias_totales > 310:
            return 0, 0, "Error: La edad gestacional parece excesiva", None
        
        semanas = dias_totales // 7
        dias = dias_totales % 7
        fpp = fur + timedelta(days=280)
        fpp_str = fpp.strftime('%d/%m/%Y')
        
        mensaje = f"Edad gestacional: {semanas} semanas y {dias} días\nFecha probable de parto: {fpp_str}"
        return semanas, dias, mensaje, fpp_str
    
    except ValueError:
        return 0, 0, "Error: Formato de fecha inválido. Use DD/MM/YYYY", None

def calcular_desde_ultrasonido(fecha_ultrasonido, semanas_ultra, dias_ultra, fecha_actual=None):
    try:
        if not (0 <= dias_ultra <= 6):
            return 0, 0, "Error: Los días deben estar entre 0 y 6", None
        
        ultra = datetime.strptime(fecha_ultrasonido, '%d/%m/%Y')
        if fecha_actual is None:
            hoy = datetime.now()
        else:
            hoy = datetime.strptime(fecha_actual, '%d/%m/%Y')
        
        diferencia = hoy - ultra
        dias_pasados = diferencia.days
        
        if dias_pasados < 0:
            return 0, 0, "Error: La fecha del ultrasonido no puede ser futura", None
        
        dias_totales = (semanas_ultra * 7) + dias_ultra + dias_pasados
        
        if dias_totales > 310:
            return 0, 0, "Error: La edad gestacional parece excesiva", None
        
        semanas = dias_totales // 7
        dias = dias_totales % 7
        dias_restantes = 280 - dias_totales
        fpp = hoy + timedelta(days=dias_restantes)
        fpp_str = fpp.strftime('%d/%m/%Y')
        
        mensaje = f"Edad gestacional actual: {semanas} semanas y {dias} días\nFecha probable de parto: {fpp_str}"
        return semanas, dias, mensaje, fpp_str
    
    except ValueError:
        return 0, 0, "Error: Formato de fecha inválido. Use DD/MM/YYYY", None

def calcular_desde_fpp(fecha_probable_parto, fecha_actual=None):
    try:
        fpp = datetime.strptime(fecha_probable_parto, '%d/%m/%Y')
        if fecha_actual is None:
            hoy = datetime.now()
        else:
            hoy = datetime.strptime(fecha_actual, '%d/%m/%Y')
        
        diferencia = fpp - hoy
        dias_restantes = diferencia.days
        
        if dias_restantes < 0:
            return 0, 0, "Error: La fecha probable de parto ya ha pasado", None
        
        dias_totales = 280 - dias_restantes
        
        if dias_totales < 0 or dias_totales > 310:
            return 0, 0, "Error: La edad gestacional parece inválida", None
        
        semanas = dias_totales // 7
        dias = dias_totales % 7
        fpp_str = fpp.strftime('%d/%m/%Y')
        mensaje = f"Edad gestacional actual: {semanas} semanas y {dias} días\nFecha probable de parto: {fpp_str}"
        return semanas, dias, mensaje, fpp_str
    
    except ValueError:
        return 0, 0, "Error: Formato de fecha inválido. Use DD/MM/YYYY", None

def calcular_desde_manual(semanas_manual, dias_manual, fecha_actual=None):
    try:
        if not (0 <= dias_manual <= 6):
            return 0, 0, "Error: Los días deben estar entre 0 y 6", None
        
        if semanas_manual < 0 or (semanas_manual * 7 + dias_manual) > 310:
            return 0, 0, "Error: La edad gestacional parece inválida", None
        
        if fecha_actual is None:
            hoy = datetime.now()
        else:
            hoy = datetime.strptime(fecha_actual, '%d/%m/%Y')
        
        dias_totales = (semanas_manual * 7) + dias_manual
        dias_restantes = 280 - dias_totales
        fpp = hoy + timedelta(days=dias_restantes)
        fpp_str = fpp.strftime('%d/%m/%Y')
        
        mensaje = f"Edad gestacional actual: {semanas_manual} semanas y {dias_manual} días\nFecha probable de parto: {fpp_str}"
        return semanas_manual, dias_manual, mensaje, fpp_str
    
    except ValueError:
        return 0, 0, "Error: Formato de fecha inválido. Use DD/MM/YYYY", None

def generar_hitos(semanas, dias, hoy):
    current_total = semanas * 7 + dias
    hitos = []
    
    target_1 = 11 * 7 + 0
    if current_total > target_1:
        edad = "1. Semana 11"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_1 = target_1 - current_total
        fecha_1 = hoy + timedelta(days=days_to_1)
        fecha_1_str = fecha_1.strftime('%d/%m/%Y')
        edad = "1. Semana 11"
        detalles = f"{fecha_1_str}\nfavor realizar los laboratorios de primer trimestre PaPP-a, HCG Libre, PLGF, TSH, T4L y T3L"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    start_2 = 12 * 7 + 0
    end_2 = 13 * 7 + 6
    if current_total > end_2:
        edad = "2. Semana 12 a semana 13 y 6 días"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_start_2 = start_2 - current_total
        start_date_2 = hoy + timedelta(days=days_to_start_2)
        start_2_str = start_date_2.strftime('%d/%m/%Y')
        days_to_end_2 = end_2 - current_total
        end_date_2 = hoy + timedelta(days=days_to_end_2)
        end_2_str = end_date_2.strftime('%d/%m/%Y')
        edad = "2. Semana 12 a semana 13 y 6 días"
        detalles = f"desde {start_2_str} hasta {end_2_str}\ntamízaje de Primer Trimestre, recuerde llevar resultados de exámenes solicitados, favor no cambie la fecha de esta cita"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    start_3 = 22 * 7 + 0
    end_3 = 24 * 7 + 6
    if current_total > end_3:
        edad = "3. Semana 22 a semana 24 y 6 días"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_start_3 = start_3 - current_total
        start_date_3 = hoy + timedelta(days=days_to_start_3)
        start_3_str = start_date_3.strftime('%d/%m/%Y')
        days_to_end_3 = end_3 - current_total
        end_date_3 = hoy + timedelta(days=days_to_end_3)
        end_3_str = end_date_3.strftime('%d/%m/%Y')
        edad = "3. Semana 22 a semana 24 y 6 días"
        detalles = f"desde {start_3_str} hasta {end_3_str}\ntamízaje de Anatómico y de Cardiopatía congénita, favor no perder esta cita"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    start_4 = 34 * 7 + 0
    end_4 = 35 * 7 + 6
    if current_total > end_4:
        edad = "4. Semana 34 a 35 semanas y 6 días"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_start_4 = start_4 - current_total
        start_date_4 = hoy + timedelta(days=days_to_start_4)
        start_4_str = start_date_4.strftime('%d/%m/%Y')
        days_to_end_4 = end_4 - current_total
        end_date_4 = hoy + timedelta(days=days_to_end_4)
        end_4_str = end_date_4.strftime('%d/%m/%Y')
        edad = "4. Semana 34 a 35 semanas y 6 días"
        detalles = f"desde {start_4_str} hasta {end_4_str}\nControl de crecimiento fetal"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    target_5 = 37 * 7 + 0
    if current_total > target_5:
        edad = "5. Semana 37"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_5 = target_5 - current_total
        fecha_5 = hoy + timedelta(days=days_to_5)
        fecha_5_str = fecha_5.strftime('%d/%m/%Y')
        day_5 = days_of_week[fecha_5.weekday()]
        edad = "5. Semana 37"
        detalles = f"{fecha_5_str}\nque es {day_5}"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    target_6 = 39 * 7 + 0
    if current_total > target_6:
        edad = "6. Semana 39"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_6 = target_6 - current_total
        fecha_6 = hoy + timedelta(days=days_to_6)
        fecha_6_str = fecha_6.strftime('%d/%m/%Y')
        day_6 = days_of_week[fecha_6.weekday()]
        edad = "6. Semana 39"
        detalles = f"{fecha_6_str}\nque es {day_6}"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    target_7 = 40 * 7 + 0
    if current_total > target_7:
        edad = "7. Semana 40"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_7 = target_7 - current_total
        fecha_7 = hoy + timedelta(days=days_to_7)
        fecha_7_str = fecha_7.strftime('%d/%m/%Y')
        day_7 = days_of_week[fecha_7.weekday()]
        edad = "7. Semana 40"
        detalles = f"{fecha_7_str}\nque es {day_7}\nanotar fecha probable de parto"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    target_8 = 41 * 7 + 0
    if current_total > target_8:
        edad = "8. Semana 41"
        detalles = "ya se superó esta edad gestacional"
    else:
        days_to_8 = target_8 - current_total
        fecha_8 = hoy + timedelta(days=days_to_8)
        fecha_8_str = fecha_8.strftime('%d/%m/%Y')
        edad = "8. Semana 41"
        detalles = f"{fecha_8_str}"
    hitos.append({"Edad Gestacional": edad, "Detalles": detalles})
    
    return hitos

def main():
    st.set_page_config(page_title="Calculadora de Edad Gestacional", page_icon="👶", layout="centered")
    
    # Aplicar paleta de colores azul
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #e6f0fa;
        }
        .stButton>button {
            background-color: #1e90ff;
            color: white;
            border: 2px solid #1e90ff;
        }
        .stButton>button:hover {
            background-color: #104e8b;
            border: 2px solid #104e8b;
        }
        .stRadio>label {
            color: #1e90ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Calculadora de Edad Gestacional - Consulta de Alto Riesgo Hospital de Liberia")
    st.markdown("Selecciona un método para calcular la edad gestacional y obtener las fechas de hitos clave del embarazo.")
    
    # Inicializar estado de sesión
    if 'calculated' not in st.session_state:
        st.session_state.calculated = False
        st.session_state.mensaje = ""
        st.session_state.hitos = []
        st.session_state.dia_fur = 1
        st.session_state.mes_fur = "Enero"
        st.session_state.ano_fur = 2025
        st.session_state.dia_ultra = 1
        st.session_state.mes_ultra = "Enero"
        st.session_state.ano_ultra = 2025
        st.session_state.dia_fpp = 1
        st.session_state.mes_fpp = "Enero"
        st.session_state.ano_fpp = 2025
    
    if not st.session_state.calculated:
        # Selección con radio buttons para más elegancia
        option = st.radio(
            "Método de cálculo",
            [
                "1. A partir de la fecha de última regla",
                "2. A partir de un ultrasonido previo",
                "3. A partir de la fecha probable de parto",
                "4. Introducción de edad gestacional manual"
            ],
            horizontal=False
        )
        
        semanas, dias, mensaje, fpp_str = 0, 0, "", None
        hoy = datetime.now()
        
        if option.startswith("1"):
            st.subheader("Fecha de última regla")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.dia_fur = st.selectbox("Día", list(range(1, 32)), key="dia_fur", index=st.session_state.dia_fur-1)
            with col2:
                st.session_state.mes_fur = st.selectbox("Mes", list(months_map.keys()), key="mes_fur", index=list(months_map.keys()).index(st.session_state.mes_fur))
            with col3:
                st.session_state.ano_fur = st.selectbox("Año", list(range(2020, 2051)), key="ano_fur", index=st.session_state.ano_fur-2020)
            
            if st.button("Calcular", key="calcular_1"):
                fecha_ultima_regla, error = build_date(st.session_state.dia_fur, st.session_state.mes_fur, st.session_state.ano_fur)
                if error:
                    st.error(error)
                elif fecha_ultima_regla:
                    semanas, dias, mensaje, fpp_str = calcular_edad_gestacional(fecha_ultima_regla)
                    if "Error" in mensaje:
                        st.error(mensaje)
                    else:
                        st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                        st.session_state.mensaje = mensaje
                        st.session_state.calculated = True
                else:
                    st.error("Por favor, seleccione una fecha válida.")
        
        elif option.startswith("2"):
            st.subheader("Fecha del ultrasonido")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.dia_ultra = st.selectbox("Día", list(range(1, 32)), key="dia_ultra", index=st.session_state.dia_ultra-1)
            with col2:
                st.session_state.mes_ultra = st.selectbox("Mes", list(months_map.keys()), key="mes_ultra", index=list(months_map.keys()).index(st.session_state.mes_ultra))
            with col3:
                st.session_state.ano_ultra = st.selectbox("Año", list(range(2020, 2051)), key="ano_ultra", index=st.session_state.ano_ultra-2020)
            
            semanas_ultra = st.number_input("Semanas de edad gestacional en el ultrasonido (número entero)", min_value=0, step=1, key="semanas_ultra")
            dias_ultra = st.number_input("Días de edad gestacional en el ultrasonido (0 a 6)", min_value=0, max_value=6, step=1, key="dias_ultra")
            
            if st.button("Calcular", key="calcular_2"):
                fecha_ultrasonido, error = build_date(st.session_state.dia_ultra, st.session_state.mes_ultra, st.session_state.ano_ultra)
                if error:
                    st.error(error)
                elif fecha_ultrasonido:
                    semanas, dias, mensaje, fpp_str = calcular_desde_ultrasonido(fecha_ultrasonido, semanas_ultra, dias_ultra)
                    if "Error" in mensaje:
                        st.error(mensaje)
                    else:
                        st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                        st.session_state.mensaje = mensaje
                        st.session_state.calculated = True
                else:
                    st.error("Por favor, seleccione una fecha válida.")
        
        elif option.startswith("3"):
            st.subheader("Fecha probable de parto")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.dia_fpp = st.selectbox("Día", list(range(1, 32)), key="dia_fpp", index=st.session_state.dia_fpp-1)
            with col2:
                st.session_state.mes_fpp = st.selectbox("Mes", list(months_map.keys()), key="mes_fpp", index=list(months_map.keys()).index(st.session_state.mes_fpp))
            with col3:
                st.session_state.ano_fpp = st.selectbox("Año", list(range(2020, 2051)), key="ano_fpp", index=st.session_state.ano_fpp-2020)
            
            if st.button("Calcular", key="calcular_3"):
                fecha_probable_parto, error = build_date(st.session_state.dia_fpp, st.session_state.mes_fpp, st.session_state.ano_fpp)
                if error:
                    st.error(error)
                elif fecha_probable_parto:
                    semanas, dias, mensaje, fpp_str = calcular_desde_fpp(fecha_probable_parto)
                    if "Error" in mensaje:
                        st.error(mensaje)
                    else:
                        st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                        st.session_state.mensaje = mensaje
                        st.session_state.calculated = True
                else:
                    st.error("Por favor, seleccione una fecha válida.")
        
        elif option.startswith("4"):
            semanas_manual = st.number_input("Semanas de edad gestacional actual (número entero)", min_value=0, step=1, key="semanas_manual")
            dias_manual = st.number_input("Días de edad gestacional actual (0 a 6)", min_value=0, max_value=6, step=1, key="dias_manual")
            if st.button("Calcular", key="calcular_4"):
                semanas, dias, mensaje, fpp_str = calcular_desde_manual(semanas_manual, dias_manual)
                if "Error" in mensaje:
                    st.error(mensaje)
                else:
                    st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                    st.session_state.mensaje = mensaje
                    st.session_state.calculated = True
    
    else:
        # Mostrar resultados
        st.success(st.session_state.mensaje)
        
        st.subheader("Fechas de hitos en orden cronológico")
        
        # Convertir hitos a DataFrame
        df = pd.DataFrame(st.session_state.hitos)
        
        # Estilizar la tabla con letras grandes y wrap text
        st.dataframe(
            df.style.set_table_styles(
                [
                    {'selector': 'tr:hover', 'props': [('background-color', '#e6f0fa')]},
                    {'selector': 'th', 'props': [('background-color', '#1e90ff'), ('color', 'white'), ('font-size', '26px'), ('padding', '15px'), ('border', '2px solid #104e8b'), ('text-align', 'left')]},
                    {'selector': 'td', 'props': [('border', '2px solid #104e8b'), ('padding', '15px'), ('font-size', '26px'), ('white-space', 'normal'), ('word-wrap', 'break-word'), ('text-align', 'left'), ('max-width', '500px'), ('min-height', '80px'), ('line-height', '1.6')]},
                ]
            ),
            hide_index=True,
            use_container_width=True
        )
        
        # Botón para realizar otro cálculo
        if st.button("Realizar otro cálculo"):
            st.session_state.calculated = False
            st.session_state.mensaje = ""
            st.session_state.hitos = []
            st.rerun()  # Reiniciar la app para mostrar el menú principal

if __name__ == "__main__":
    main()
