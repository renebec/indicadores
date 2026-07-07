import streamlit as st
import math
import os
import signal
import plotly.express as px



# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Indicadores", page_icon="🧮")



# Título de cabecera principal
st.title("🧮 Cálculadora de indicadores para la EMS")
st.html('<div style="text-align:right;font-size:10px;color:#888888">by MC Héctor Becerril 2026</div>')
st.write("Julio 2026")

# 2. CREACIÓN DE LAS PESTAÑAS (TABS)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["📝 Notas", "1.Abandono", "2.Aprobación", "3.Reprobación", "4.ET", "5.Egr > 8", "6.DocActPlan", "7.DocPlanEn", "8.DocMCC"])

# =====================================================================
# PESTAÑA 1: EXPLICACIÓN DE FÓRMULAS
# =====================================================================
with tab1:
    st.header("Conceptos y Fórmulas")
    st.write("Aquí puedes entender la matemática detrás de los cálculos que realiza esta app.")
    
    st.subheader("1. % Abandono escolar en el ciclo (t)")
    st.write("Se refiere al porcentaje de alumnos que abandonan las actividades escolares en el ciclo escolar, con respecto a la matrícula de inicio del mismo:")
    st.latex(r"Abandono = 1 - \frac{( M_{t+1} - MN_{t+1} ) + E_t} {M_t} * 100")
    st.markdown("""
    Donde:
    *   **$M_{t+1}$**: Matrícula de inicio en el cilco escolar (t + 1).
    *   **$MN_{t+1}$**: matrícula de nuevo ingreso a primer semestre en el ciclo escolar (t + 1).
    *   **$E_t$**: Número de alumnos que egresaron en el cliclo escolar (t).
    *   **$M_t$**: Matrícula de inicio en el cilco escolar (t).
    """)
    
    st.subheader("2. % Aprobación en el ciclo (t)")
    st.write("Porcentaje de alumnos que han aprobado la totalidad de asignaturas y/o módulos al finalizar el ciclo escolar y previo a los períodos de recuperación:")
    st.latex(r"Aprobación = \frac{ A_t + A_{mid}}{N_t + N_{mid}} * 100") 
    st.markdown("""
    Donde:
    *   **$A_t$**: Número de alumnos aprobados al final del ciclo escolar (t).
    *   **$A_{mid}$**: Número de alumnos aprobados a mitad del cilo escolar (t).
    *   **$M_t$**: Matrícula al inicio del ciclo escolar (t)
    *   **$M_{mid}$**: Número de alumnos a mitad del ciclo escolar (t)
    """)
    
    st.subheader("3. % Reprobación en el ciclo (t)")
    st.write("Mide la eficiencia del sistema educativo y puede convertirse en la base de cálculo de tasas de admisión, promoción y desersión:")
    st.latex(r"Reprobación = \frac{ R_t + R_{mid}}{M_t + M_{mid}} * 100")
    st.markdown("""
    Donde:
    *   **$R_t$**: Número de alumnos aprobados al final del ciclo escolar (t).
    *   **$R_{mid}$**: Número de alumnos aprobados a mitad del cilo escolar (t).
    *   **$M_t$**: Matrícula al inicio del ciclo escolar (t)
    *   **$M_{mid}$**: Número de alumnos a mitad del ciclo escolar (t)
    """)
    
    st.subheader("4. % Eficiencia terminal en el ciclo (t)")
    st.write("Mide la razón de egresados en el ciclo t con respecto al total de nuevos ingresos en (t-2):")
    st.latex(r"ET = \frac{ E_{gt} }{MN_{gt}} * 100")
    st.markdown("""
    Donde:
    *   **$E_{gt}$**: Número de alumnos egresados al final del ciclo escolar (t).
    *   **$MN_{gt}$**: Matrícula de nuevo ingreso en el ciclo (t-2).
    """)
    
    st.subheader("5. % de egresados con promedio >= 8 en el ciclo (t)")
    st.write("Mide la razón de egresados que obtuvieron promedio >= 8 en el ciclo t:")
    st.latex(r"E_{gr8} = \frac{ E_{pt8} }{E_{t8}} * 100")
    st.markdown("""
    Donde:
    *   **$E_{pt8}$**: Número de egresados con promedio >= 8 en el ciclo escolar (t).
    *   **$E_{t8}$**: Número de egresados en el ciclo (t).
    """)
    
    st.subheader("6. % Docentes con actividades de planeación didáctica en el ciclo (t)")
    st.write("Mide la razón de docentes que registraron participación en actividades de planeación didáctica:")
    st.latex(r"DocPlanAct = \frac{ D_{pt} }{D_t} * 100")
    st.markdown("""
    Donde:
    *   **$D_{pt}$**: Número de docentes con participación en actividades de planeación didáctica en el ciclo escolar (t).
    *   **$D_t$**: Número de docentes frente a grupo en el ciclo (t).
    """)
    
    st.subheader("7. % Docentes que entregaron planeación didáctica en el ciclo (t)")
    st.write("Mide la razón de docentes que entregaron planeación didáctica en el ciclo (t):")
    st.latex(r"DocPlanEn = \frac{ D_{cpt} }{D_t} * 100")
    st.markdown("""
    Donde:
    *   **$D_{cpt}$**: Número de docentes que entregaron planeación didáctica en el ciclo (t).
    *   **$D_t$**: Número de docentes frente a grupo en el ciclo (t).
    """)
    
    st.subheader("8. % Docentes capacitados en el MCCEMS en el ciclo (t)")
    st.write("Mide la razón de docentes que en el ciclo (t) recibieron capacitación sore el MCCEMS:")
    st.latex(r"DocMCC = \frac{ D_{mcct} }{D_t} * 100")
    st.markdown("""
    Donde:
    *   **$D_{mcct}$**: Número de docentes capacitados en el MCCEMS en el ciclo (t).
    *   **$D_t$**: Número de docentes frente a grupo en el ciclo (t).
    """)

# =====================================================================
# PESTAÑA 2: CÁLCULO DE ABANDONO
# =====================================================================
with tab2:
	
    st.header("Calcular % abandono en el ciclo (t)")
    st.write("Introduce los parámetros:")
    
    M_t1 = st.number_input("Matrícula al inicio del ciclo (t + 1):", min_value=0, value=600, step=1, key="M_t1ab")
    MN_t1 = st.number_input("Matrícula de nuevo ingreso en el ciclo (t + 1)", min_value=0, value=300, step=1, key="MN_t1ab")
    E_t = st.number_input("Número de egresados en el ciclo (t)", min_value=0, value=250, step=1, key="E_tab")
    M_t = st.number_input("Matrícula al inicio del ciclo (t)", min_value=0, value=700, step=1, key="M_tab")
    
    if st.button("Calcular abandono", key="btn_aband"):
        if M_t > 0:
            abandono = (1 - (((M_t1 - MN_t1) + E_t) / M_t)) * 100
            st.success(f"¡Cálculo exitoso! El abandono es **{abandono:.2f} %**.")
            
            labels = ['Abandono', 'Permanencia']
            values = [abandono, 100 - abandono]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=['#C4F759', '#FFc55e']) # Rojo y Verde
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Revisa los datos ingresados.")

# =====================================================================
# PESTAÑA 3: CÁLCULO DE APROBACIÓN
# =====================================================================
with tab3:
    st.header("Calcular % aprobación en el ciclo (t)")
    st.write("Introduce los parámetros:")
    
    A_t = st.number_input("Número de aprobados al final del ciclo (t):", min_value=0, value=600, step=1, key="A_tapr")
    A_mid = st.number_input("Número de aprobados a mitad del ciclo (t)", min_value=0, value=300, step=1, key="A_midapr")
    M_t = st.number_input("Matrícula al inicio del ciclo (t)", min_value=0, value=700, step=1, key="M_tapr")
    M_mid = st.number_input("Matrícula a mitad del ciclo (t)", min_value=0, value=700, step=1, key="M_midapr")
    
    if st.button("Calcular aprobación", key="btn_aprob"):
		
        if M_t > 0 or M_mid > 0:
            num = A_t + A_mid
            den = M_t+ M_mid
            apro = (num / den)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de aprobación es **{apro:.2f} %**.")
            labels = ['Aprobación', 'No aprobación']
            values = [apro, 100 - apro]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=[ '#C4F759', '#FFc55e']) # Rojo y Verde
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
           
        else:
            st.error("Revisa tus datos.")

# =====================================================================
# PESTAÑA 4: CÁLCULO DE REPROBACIÓN
# =====================================================================
with tab4:
    st.header("Calcular % reprobación en el ciclo (t)")
    st.write("Introduce los parámetros:")
    
    R_t = st.number_input("Número de reprobados al final del ciclo (t):", min_value=0, value=600, step=1, key="R_trep")
    R_mid = st.number_input("Número de reprobados a mitad del ciclo (t)", min_value=0, value=300, step=1, key="R_midrep")
    M_t = st.number_input("Matrícula al inicio del ciclo (t)", min_value=0, value=700, step=1, key="M_trep")
    M_mid = st.number_input("Matrícula a mitad del ciclo (t)", min_value=0, value=700, step=1, key="M_midrep")
    
    if st.button("Calcular reprobación", key="btn_reprob"):
		
        if M_t > 0 or M_mid > 0:
            num = R_t + R_mid
            den = M_t + M_mid
            repro = (num / den)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de reprobación es **{repro:.2f} %**.")
            
            labels = ['Reprobación', 'No reprobación']
            values = [repro, 100 - repro]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=['#C4F759', '#FFc55e']) # Rojo y Verde
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
           
        else:
            st.error("Revisa tus datos.")
            
# =====================================================================
# PESTAÑA 5: CÁLCULO DE EFICIENCIA TERMINAL (ET)
# =====================================================================
with tab5:
    st.header("Calcular % eficiencia terminal en el ciclo (t)")
    st.write("Introduce los parámetros:")
    
    E_gt = st.number_input("Número de egresados de la misma genración en el ciclo (t):", min_value=0, value=600, step=1, key="E_gt")
    MN_gt = st.number_input("Matrícula de Nuevo Ingreso en el ciclo (t - 2)", min_value=0, value=300, step=1, key="MN_gt")

    
    if st.button("Calcular ET", key="btn_et"):
		
        if MN_gt > 0:
            
            et = (E_gt / MN_gt)*100
            
            st.success(f"¡Cálculo exitoso! La eficiencia terminal es de **{et:.2f} %**.")
            

            labels = ['Eficiencia Terminal', 'No egresaron']
            values = [et, 100 - et]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=[  '#C4F759', '#FFc55e']) # Rojo y gris
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
           
        else:
            st.error("Revisa tus datos.")

# =====================================================================
# PESTAÑA 6: CÁLCULO DE EGRESADOS CON PROMEDIO >= 8
# =====================================================================
with tab6:
    st.header("Calcular % de egresados con promedio  >= 8 en el cilco (t)")
    st.write("Introduce los parámetros:")
    
    Ep_t8 = st.number_input("Número de egresados en el ciclo (t) con promedio >= 8:", min_value=0, value=600, step=1, key="Ep_t8")
    E_t8 = st.number_input("Número de egresados en el ciclo (t)", min_value=0, value=300, step=1, key="E_t8")

    
    if st.button("Calcular % promedios >= 8", key="btn_prom8"):
		
        if E_t8 > 0:
            
            E_p8 = (Ep_t8 / E_t8)*100
            
            st.success(f"¡Cálculo exitoso! El porcentaje de egresados con promedio >= 8 es **{E_p8:.2f} %**.")
            
            labels = ['Egresados con promedio > = 8', 'Con promedio menor a 8']
            values = [E_p8, 100 - E_p8]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=[ '#FFc55e', '#C4F759']) # Rojo y Verde
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
           
        else:
            st.error("Revisa tus datos.")
            
# =====================================================================
# PESTAÑA 7: CÁLCULO DE DOCENTES PARTICIPANTES EN PLANEACIÓN DIDÁCTICA
# =====================================================================
with tab7:
    st.header("Calcular % docentes que participan en actividades de planeación didáctica en el ciclo (t)")
    st.write("Introduce los parámetros:")
    
    Dp_t = st.number_input("Número de docentes que participan en actividades de planeación didáctica en el ciclo (t):", min_value=0, value=600, step=1, key="Dp_t")
    D_t = st.number_input("Número de docentes frente a grupo en ciclo (t)", min_value=0, value=300, step=1, key="D_t")

    
    if st.button("Calcular docentes en actividades de planeaciones", key="btn_docplan"):
		
        if D_t > 0:
            
            docplan = (Dp_t / D_t)*100
            
            st.success(f"¡Cálculo exitoso! El % de docentes que participan en actividades de planeación didáctica es **{docplan:.2f} %**.")
            
            labels = ['Docentes participantes', 'No participaron']
            values = [docplan, 100 - docplan]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=['#C4F759', '#FFc55e']) # Rojo y Verde
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
           
        else:
            st.error("Revisa tus datos.")


# =====================================================================
# PESTAÑA 8: CÁLCULO DE DOCENTES QUE ENTREGAN PLANEACIÓN DIDÁCTICA
# =====================================================================
with tab8:
    st.header("Calcular % docentes con planeación didáctica en el ciclo (t)")
    st.write("Introduce los parámetros:")
    
    Dcp_t = st.number_input("# Docentes que entregaron planeación didáctica en el ciclo (t):", min_value=0, value=600, step=1, key="Dcp_t")
    D_t = st.number_input("# Docentes frente a grupo en el ciclo (t)", min_value=0, value=300, step=1, key="D_tcon")

    
    if st.button("Calcular docentes con planeaciones", key="btn_conplan"):
		
        if D_t > 0:
            
            doccon = (Dcp_t / D_t)*100
            
            st.success(f"¡Cálculo exitoso! El % de docentes con planeaciones didáctica entregadas es **{doccon:.2f} %**.")
            
            labels = ['Docentes que entregaron', 'No entregaron']
            values = [doccon, 100 - doccon]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=['#C4F759', '#FFc55e']) # Rojo y Verde
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
           
           
        else:
            st.error("Revisa tus datos.")
            
# =====================================================================
# PESTAÑA 9: CÁLCULO DE DOCENTES FORMADOS EN MCCEMS
# =====================================================================
with tab9:
    st.header("Calcular % de docentes capacitados en MCCEMS en el ciclo (t)")
    st.write("Introduce los parámetros:")
    
    Dmcc_t = st.number_input("# Docentes capacitados en MCCEMS en el ciclo (t):", min_value=0, value=600, step=1, key="Dmcc_t")
    D_t = st.number_input("# Docentes frente a grupo en el ciclo (t)", min_value=0, value=300, step=1, key="D_tmcc")

    
    if st.button("Calcular % capacitados en MCCEMS", key="btn_mccems"):
		
        if D_t > 0:
            
            docmcc = (Dmcc_t / D_t)*100
            
            st.success(f"¡Cálculo exitoso! El % de docentes capacitados en MCCEMSa es **{docmcc:.2f} %**.")
            
            labels = ['Docentes capacitados en MCC', 'No capacitados']
            values = [docmcc, 100 - docmcc]
            fig = px.pie(values=values, names=labels, hole=0.5, 
             color_discrete_sequence=['#C4F759', '#FFc55e']) # Rojo y Verde
            fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
           
        else:
            st.error("Revisa tus datos.")
