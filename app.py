import streamlit as st
import math
import os
import signal



# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Indicadores", page_icon="🧮")



# Título de cabecera principal
st.title("🧮 Cálculo de indicadores")
st.write("Aquí se explican los cálculos que realiza la app.")

# 2. CREACIÓN DE LAS PESTAÑAS (TABS)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["📝 Notas", "️Abandono", "Aprobación", "Reprobación", "ET", "Egr > 8", "Doc Plan", "Doc Plan Design", "Doc MCC"])

# =====================================================================
# PESTAÑA 1: EXPLICACIÓN DE FÓRMULAS
# =====================================================================
with tab1:
    st.header("Conceptos y Fórmulas")
    st.write("Aquí puedes entender la matemática detrás de los cálculos que realiza esta app.")
    
    st.subheader("1. Abandono escolar")
    st.write("Se refiere al porcentaje de alumnos que abandonan las actividades escolares en el ciclo escolar, con respecto a la matrícula de inicio del mismo:")
    st.latex(r"Abandono = 1 - \frac{( M_{t+1} + MN_{t+1} ) + E_t} {M_t} * 100")
    st.markdown("""
    Donde:
    *   **$M_{t+1}**: Matrícula de inicio en el cilco escolar (t + 1).
    *   **$MN_{t+1}$**: matrícula de nuevo ingreso a primer semestre en el ciclo escolar (t + 1).
    *   **$E_t$**: Número de alumnos que egresaron en el cliclo escolar (t).
    *   **$M_t$**: Matrícula de inicio en el cilco escolar (t).
    """)
    
    st.subheader("2. Aprobación")
    st.write("Porcentaje de alumnos que han aprobado la totalidad de asignaturas y/o módulos al finalizar el ciclo escolar y previo a los períodos de recuperación:")
    st.latex(r"Aprobación = \frac{ A_t + A_{mid}}{N_t + N_{mid}} * 100") 
    st.markdown("""
    Donde:
    *   **$A_t$**: Número de alumnos aprobados al final del ciclo escolar (t).
    *   **$A_{mid}$**: Número de alumnos aprobados a mitad del cilo escolar (t).
    *   **$M_t$**: Matrícula al inicio del ciclo escolar (t)
    *   **$M_{mid}$**: Número de alumnos a mitad del ciclo escolar (t)
    """)
    
    st.subheader("3. Reprobación")
    st.write("Mide la eficiencia del sistema educativo y puede convertirse en la base de cálculo de tasas de admisión, promoción y desersión:")
    st.latex(r"Rprobación = \frac{ R_t + R_{mid}}{N_t + N_{mid}} * 100")
    st.markdown("""
    Donde:
    *   **$A_0$**: Número de alumnos aprobados al final del ciclo escolar (t).
    *   **$A_{mid}$**: Número de alumnos aprobados a mitad del cilo escolar (t).
    *   **$M_0$**: Matrícula al inicio del ciclo escolar (t)
    *   **$M_{mid}$**: Número de alumnos a mitad del ciclo escolar (t)
    """)

# =====================================================================
# PESTAÑA 2: CÁLCULO DE ABANDONO
# =====================================================================
with tab2:
	
    st.header("Calcular abandono")
    st.write("Introduce los parámetros:")
    
    M_t1 = st.number_input("<M_1> Matrícula al inicio de (t + 1):", min_value=0, value=600, step=1, key="M_t1ab")
    MN_t1 = st.number_input("<MN_1> Matrícula de nuevo ingreso en (t + 1)", min_value=0, value=300, step=1, key="MN_t1ab")
    E_t = st.number_input("<E_0> Egresados en (t)", min_value=0, value=250, step=1, key="E_tab")
    M_t = st.number_input("<M_0> Matrícula al inicio de (t)", min_value=0, value=700, step=1, key="M_tab")
    
    if st.button("Calcular abandono", key="btn_aband"):
        if M_t > 0:
            abandono = (1 - (((M_t1 - MN_t1) + E_t) / M_t)) * 100
            st.success(f"¡Cálculo exitoso! El abandono es **{abandono:.2f} %**.")
        else:
            st.error("Revisa los datos ingresados.")

# =====================================================================
# PESTAÑA 3: CÁLCULO DE APROBACIÓN
# =====================================================================
with tab3:
    st.header("Calcular aprobación")
    st.write("Introduce los parámetros:")
    
    A_t = st.number_input("<A_0> Aprobados al final del ciclo (t):", min_value=0, value=600, step=1, key="A_tapr")
    A_mid = st.number_input("<A_mid> Aprobados a mitad del ciclo (t)", min_value=0, value=300, step=1, key="A_midapr")
    M_t = st.number_input("<M_0> Matrícula al inicio de (t)", min_value=0, value=700, step=1, key="M_tapr")
    M_mid = st.number_input("<M_mid> Matrícula a mitad de (t)", min_value=0, value=700, step=1, key="M_midapr")
    
    if st.button("Calcular aprobación", key="btn_aprob"):
		
        if M_t > 0 or M_mid > 0:
            num = A_t + A_mid
            den = M_t+ M_mid
            apro = (num / den)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de aprobación es **{apro:.2f} %**.")
           
        else:
            st.error("Revisa tus datos.")

# =====================================================================
# PESTAÑA 4: CÁLCULO DE REPROBACIÓN
# =====================================================================
with tab4:
    st.header("Calcular reprobación")
    st.write("Introduce los parámetros:")
    
    R_t = st.number_input("<Rt> Reprobados al final de ciclo (t):", min_value=0, value=600, step=1, key="R_trep")
    R_mid = st.number_input("<A_mid> Reprobados a mitad del ciclo (t)", min_value=0, value=300, step=1, key="R_midrep")
    M_t = st.number_input("<M_0> Matrícula al inicio de (t)", min_value=0, value=700, step=1, key="M_trep")
    M_mid = st.number_input("<M_mid> Matrícula a mitad de (t)", min_value=0, value=700, step=1, key="M_midrep")
    
    if st.button("Calcular reprobación", key="btn_reprob"):
		
        if M_t > 0 or M_mid > 0:
            num = R_t + R_mid
            den = M_t + M_mid
            repro = (num / den)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de reprobación es **{repro:.2f} %**.")
           
        else:
            st.error("Revisa tus datos.")
            
# =====================================================================
# PESTAÑA 5: CÁLCULO DE EFICIENCIA TERMINAL (ET)
# =====================================================================
with tab5:
    st.header("Calcular eficiencia terminal")
    st.write("Introduce los parámetros:")
    
    E_gt = st.number_input("<E_gt> Egresados de la misma genración en el ciclo (t):", min_value=0, value=600, step=1, key="E_gt")
    MN_gt = st.number_input("<MN_t-2> Matrícula de Nuevo Ingreso en ciclo (t - 2)", min_value=0, value=300, step=1, key="MN_gt")

    
    if st.button("Calcular ET", key="btn_et"):
		
        if MN_gt > 0:
            
            et = (E_gt / MN_gt)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de eficiencia terminal es **{et:.2f} %**.")
           
        else:
            st.error("Revisa tus datos.")

# =====================================================================
# PESTAÑA 6: CÁLCULO DE EGRESADOS CON PROMEDIO >= 8
# =====================================================================
with tab6:
    st.header("Calcular # promedios  >= 8")
    st.write("Introduce los parámetros:")
    
    Ep_t8 = st.number_input("<Ep_t8> Egresados en el ciclo (t) con promedio >= 8:", min_value=0, value=600, step=1, key="Ep_t8")
    E_t8 = st.number_input("<E_t> Egresados en ciclo (t)", min_value=0, value=300, step=1, key="E_t8")

    
    if st.button("Calcular # promedios >= 8", key="btn_prom8"):
		
        if E_t8 > 0:
            
            et8 = (Ep_t8 / E_t8)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de egresados con promedio >= 8 es **{et8:.2f} %**.")
           
        else:
            st.error("Revisa tus datos.")
            
# =====================================================================
# PESTAÑA 7: CÁLCULO DE DOCENTES PARTICIPANTES EN PLANEACIÓN DIDÁCTICA
# =====================================================================
with tab7:
    st.header("Calcular docentes que participan en actividades de planeación didáctica")
    st.write("Introduce los parámetros:")
    
    Dp_t = st.number_input("<Dp_t> Docentes que participan en actividades de planeación didáctica en el ciclo (t):", min_value=0, value=600, step=1, key="Dp_t")
    D_t = st.number_input("<D_t> Docentes frente a grupo en ciclo (t)", min_value=0, value=300, step=1, key="D_t")

    
    if st.button("Calcular docentes en actividades de plan", key="btn_docplan"):
		
        if D_t > 0:
            
            docplan = (Dp_t / D_t)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de docentes que participan en actividades de planeación didáctica es **{docplan:.2f} %**.")
           
        else:
            st.error("Revisa tus datos.")


# =====================================================================
# PESTAÑA 8: CÁLCULO DE DOCENTES QUE PRESENTAN PLANEACIÓN DIDÁCTICA
# =====================================================================
with tab8:
    st.header("Calcular docentes con planeación didáctica")
    st.write("Introduce los parámetros:")
    
    Dcp_t = st.number_input("<Dcp_t> Docentes que presentaron planeación didáctica en ciclo (t):", min_value=0, value=600, step=1, key="Dcp_t")
    D_t = st.number_input("<D_t> Docentes frente a grupo en ciclo (t)", min_value=0, value=300, step=1, key="D_tcon")

    
    if st.button("Calcular docentes con planeación", key="btn_conplan"):
		
        if D_t > 0:
            
            doccon = (Dcp_t / D_t)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de docentes con planeación didáctica es **{doccon:.2f} %**.")
           
        else:
            st.error("Revisa tus datos.")
            
# =====================================================================
# PESTAÑA 9: CÁLCULO DE DOCENTES FORMADOS EN MCCEMS
# =====================================================================
with tab9:
    st.header("Calcular docentes capacitados en MCCEMS")
    st.write("Introduce los parámetros:")
    
    Dmcc_t = st.number_input("<Dcp_t> Docentes capacitados en MCCEMS en ciclo (t):", min_value=0, value=600, step=1, key="Dmcc_t")
    D_t = st.number_input("<D_t> Docentes frente a grupo en ciclo (t)", min_value=0, value=300, step=1, key="D_tmcc")

    
    if st.button("Calcular docentescapacitados en MCCEMS", key="btn_mccems"):
		
        if D_t > 0:
            
            docmcc = (Dmcc_t / D_t)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de docentes capacitados en MCCEMSa es **{docmcc:.2f} %**.")
           
        else:
            st.error("Revisa tus datos.")

