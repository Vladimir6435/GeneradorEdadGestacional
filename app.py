import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

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
        hitos.append("1. Edad gestacional semana 11: ya se superó esta edad gestacional")
    else:
        days_to_1 = target_1 - current_total
        fecha_1 = hoy + timedelta(days=days_to_1)
        fecha_1_str = fecha_1.strftime('%d/%m/%Y')
        hitos.append(f"1. Edad gestacional semana 11: {fecha_1_str} favor realizar los laboratorios de primer trimestre PaPP-a, HCG Libre, PLGF, TSH, T4L y T3L")
    
    start_2 = 12 * 7 + 0
    end_2 = 13 * 7 + 6
    if current_total > end_2:
        hitos.append("2. Edad gestacional semana 12 a semana 13 y 6 días: ya se superó esta edad gestacional")
    else:
        days_to_start_2 = start_2 - current_total
        start_date_2 = hoy + timedelta(days=days_to_start_2)
        start_2_str = start_date_2.strftime('%d/%m/%Y')
        days_to_end_2 = end_2 - current_total
        end_date_2 = hoy + timedelta(days=days_to_end_2)
        end_2_str = end_date_2.strftime('%d/%m/%Y')
        hitos.append(f"2. Edad gestacional semana 12 a semana 13 y 6 días: desde {start_2_str} hasta {end_2_str} tamízaje de Primer Trimestre, recuerde llevar resultados de exámenes solicitados, favor no cambie la fecha de esta cita")
    
    start_3 = 22 * 7 + 0
    end_3 = 24 * 7 + 6
    if current_total > end_3:
        hitos.append("3. Edad gestacional semana 22 a semana 24 y 6 días: ya se superó esta edad gestacional")
    else:
        days_to_start_3 = start_3 - current_total
        start_date_3 = hoy + timedelta(days=days_to_start_3)
        start_3_str = start_date_3.strftime('%d/%m/%Y')
        days_to_end_3 = end_3 - current_total
        end_date_3 = hoy + timedelta(days=days_to_end_3)
        end_3_str = end_date_3.strftime('%d/%m/%Y')
        hitos.append(f"3. Edad gestacional semana 22 a semana 24 y 6 días: desde {start_3_str} hasta {end_3_str} tamízaje de Anatómico y de Cardiopatía congénita, favor no perder esta cita")
    
    start_4 = 34 * 7 + 0
    end_4 = 35 * 7 + 6
    if current_total > end_4:
        hitos.append("4. Edad gestacional semana 34 a 35 semanas y 6 días: ya se superó esta edad gestacional")
    else:
        days_to_start_4 = start_4 - current_total
        start_date_4 = hoy + timedelta(days=days_to_start_4)
        start_4_str = start_date_4.strftime('%d/%m/%Y')
        days_to_end_4 = end_4 - current_total
        end_date_4 = hoy + timedelta(days=days_to_end_4)
        end_4_str = end_date_4.strftime('%d/%m/%Y')
        hitos.append(f"4. Edad gestacional semana 34 a 35 semanas y 6 días: desde {start_4_str} hasta {end_4_str} Control de crecimiento fetal")
    
    target_5 = 37 * 7 + 0
    if current_total > target_5:
        hitos.append("5. Edad gestacional semana 37: ya se superó esta edad gestacional")
    else:
        days_to_5 = target_5 - current_total
        fecha_5 = hoy + timedelta(days=days_to_5)
        fecha_5_str = fecha_5.strftime('%d/%m/%Y')
        day_5 = days_of_week[fecha_5.weekday()]
        hitos.append(f"5. Edad gestacional semana 37: {fecha_5_str} que es {day_5}")
    
    target_6 = 39 * 7 + 0
    if current_total > target_6:
        hitos.append("6. Edad gestacional semana 39: ya se superó esta edad gestacional")
    else:
        days_to_6 = target_6 - current_total
        fecha_6 = hoy + timedelta(days=days_to_6)
        fecha_6_str = fecha_6.strftime('%d/%m/%Y')
        day_6 = days_of_week[fecha_6.weekday()]
        hitos.append(f"6. Edad gestacional semana 39: {fecha_6_str} que es {day_6}")
    
    target_7 = 40 * 7 + 0
    if current_total > target_7:
        hitos.append("7. Edad gestacional semana 40: ya se superó esta edad gestacional")
    else:
        days_to_7 = target_7 - current_total
        fecha_7 = hoy + timedelta(days=days_to_7)
        fecha_7_str = fecha_7.strftime('%d/%m/%Y')
        day_7 = days_of_week[fecha_7.weekday()]
        hitos.append(f"7. Edad gestacional semana 40: {fecha_7_str} que es {day_7} anotar fecha probable de parto")
    
    target_8 = 41 * 7 + 0
    if current_total > target_8:
        hitos.append("8. Edad gestacional semana 41: ya se superó esta edad gestacional")
    else:
        days_to_8 = target_8 - current_total
        fecha_8 = hoy + timedelta(days=days_to_8)
        fecha_8_str = fecha_8.strftime('%d/%m/%Y')
        hitos.append(f"8. Edad gestacional semana 41: {fecha_8_str}")
    
    return hitos

def main():
    st.set_page_config(page_title="Calculadora de Edad Gestacional", page_icon="👶", layout="centered")
    
    st.title("Calculadora de Edad Gestacional - Consulta de Alto Riesgo Hospital de Liberia")
    st.markdown("Selecciona un método para calcular la edad gestacional y obtener las fechas de hitos clave del embarazo.")
    
    # Inicializar estado de sesión
    if 'calculated' not in st.session_state:
        st.session_state.calculated = False
        st.session_state.mensaje = ""
        st.session_state.hitos = []
    
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
            fecha_ultima_regla = st.text_input("Ingrese la fecha de última regla (DD/MM/YYYY)", placeholder="Ej: 01/01/2025")
            if st.button("Calcular", key="calcular_1"):
                if fecha_ultima_regla:
                    semanas, dias, mensaje, fpp_str = calcular_edad_gestacional(fecha_ultima_regla)
                    if "Error" not in mensaje:
                        st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                        st.session_state.mensaje = mensaje
                        st.session_state.calculated = True
                else:
                    st.error("Por favor, ingrese una fecha válida.")
        
        elif option.startswith("2"):
            fecha_ultrasonido = st.text_input("Ingrese la fecha del ultrasonido (DD/MM/YYYY)", placeholder="Ej: 01/01/2025")
            semanas_ultra = st.number_input("Semanas de edad gestacional en el ultrasonido (número entero)", min_value=0, step=1)
            dias_ultra = st.number_input("Días de edad gestacional en el ultrasonido (0 a 6)", min_value=0, max_value=6, step=1)
            if st.button("Calcular", key="calcular_2"):
                if fecha_ultrasonido:
                    semanas, dias, mensaje, fpp_str = calcular_desde_ultrasonido(fecha_ultrasonido, semanas_ultra, dias_ultra)
                    if "Error" not in mensaje:
                        st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                        st.session_state.mensaje = mensaje
                        st.session_state.calculated = True
                else:
                    st.error("Por favor, ingrese una fecha válida.")
        
        elif option.startswith("3"):
            fecha_probable_parto = st.text_input("Ingrese la fecha probable de parto (DD/MM/YYYY)", placeholder="Ej: 01/10/2025")
            if st.button("Calcular", key="calcular_3"):
                if fecha_probable_parto:
                    semanas, dias, mensaje, fpp_str = calcular_desde_fpp(fecha_probable_parto)
                    if "Error" not in mensaje:
                        st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                        st.session_state.mensaje = mensaje
                        st.session_state.calculated = True
                else:
                    st.error("Por favor, ingrese una fecha válida.")
        
        elif option.startswith("4"):
            semanas_manual = st.number_input("Semanas de edad gestacional actual (número entero)", min_value=0, step=1)
            dias_manual = st.number_input("Días de edad gestacional actual (0 a 6)", min_value=0, max_value=6, step=1)
            if st.button("Calcular", key="calcular_4"):
                semanas, dias, mensaje, fpp_str = calcular_desde_manual(semanas_manual, dias_manual)
                if "Error" not in mensaje:
                    st.session_state.hitos = generar_hitos(semanas, dias, hoy)
                    st.session_state.mensaje = mensaje
                    st.session_state.calculated = True
    
    else:
        # Mostrar resultados
        st.success(st.session_state.mensaje)
        
        st.subheader("Fechas de hitos en orden cronológico")
        
        # Convertir hitos a DataFrame para tabla elegante
        hitos_data = [{"Hito": hito} for hito in st.session_state.hitos]
        df = pd.DataFrame(hitos_data)
        
        # Estilizar la tabla
        st.dataframe(
            df.style.set_table_styles(
                [
                    {'selector': 'tr:hover', 'props': [('background-color', '#ffff99')]},
                    {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]},
                    {'selector': 'td', 'props': [('border', '1px solid #ddd'), ('padding', '8px')]},
                ]
            ).set_properties(**{'text-align': 'left'}),
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
