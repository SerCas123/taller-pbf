import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN VISUAL DE LA PÁGINA
st.set_page_config(
    page_title="PBF Honduras - Validación Catalítica", 
    page_icon="📊", 
    layout="wide"
)

# 2. BASE DE DATOS COMPLETA DE LOS PROYECTOS
DATOS_PORTAFOLIO = {
    "PBF/HND/H1 - PARTICIPAZ": {
        "tema": "Transparencia, eficacia institucional e inclusión",
        "financiero": [
            "F1. No recursos adicionales movilizados para la implementación del proyecto.",
            "F2. El proceso de diálogo político nacional sentó las bases para que el gobierno hondureño, con apoyo externo, financiara la creación del CNE y TJE, con partidas presupuestarias propias.",
            "F3. La reforma electoral derivada del diálogo tuvo respaldo financiero del Estado y acompañamiento técnico sostenido de la cooperación internacional."
        ],
        "no_financiero": [
            "NF1. Surgimiento de nuevas organizaciones fortalecidas y empoderadas que participan en la creación y fortalecimiento de políticas públicas.",
            "NF2. Instituciones gubernamentales rinden cuentas de una forma más transparente, cuentan con mecanismos de prevención de la conflictividad social...",
            "NF3. Mecanismo de alerta temprana y la resolución de conflictos a través de los centros de conciliación.",
            "NF4. Aparición de una cultura de paz entorno al ciclo electoral con una visión más clara y técnica hacia el logro de objetivos en común.",
            "NF5. El modelo de veeduría ciudadana y transparencia municipal, desarrollado en municipios como Santa Rosa de Copán, fue adoptado posteriormente por otras alcaldías con apoyo de la SEPLAN y el IAIP."
        ]
    },
    "PBF/IRF-410 - CONPAZ": {
        "tema": "Comunidades constructoras de paz e igualdad",
        "financiero": [
            "F1. Aportes monetarios de: Fundación Diunsa, Davivienda, Cure Violence Global y Spotlight UNICEF.",
            "F2. Capacitaciones de CCCI, Fundación Azucena, Macdel, CDE, Davivienda y TIGO, Grupo INTUR, Corporación DINANT.",
            "F3. Pasantías y ferias de empleo de: Farmacia Siman, Ficohsa, SENAEH, Diunsa, Four Season, Proyecto Creando mi Futuro Aquí, INMECRO.",
            "F4. Facilitación de espacios y otros implementos: UNITED WAY, UNITEC.",
            "F5. Contrapartes municipales facilitaron infraestructura y cobertura logística para acciones comunitarias del modelo de interrupción de violencia."
        ],
        "no_financiero": [
            "NF1. Las alcaldías municipales explosionaron las acciones de colaboración con otros, visibilizando acciones en días conmemorativos a la paz.",
            "NF2. La integración de organizaciones permitió la colaboración de fuerzas vivas y agrupaciones locales favoreciendo la reducción de oposición e incluyendo participantes de varios sectores.",
            "NF3. En 46 comunidades de 6 municipios, se fortalecieron capacidades municipales y comunitarias para incluir la prevención de VBG en planes de desarrollo local.",
            "NF4. Las mesas de diálogo comunitario promovidas en barrios de Tegucigalpa y San Pedro Sula fueron institucionalizadas en los planes municipales de desarrollo.",
            "NF5. El modelo 'Cure Violence' fue asumido como estrategia municipal de prevención en ciudades como San Pedro Sula y Choloma."
        ]
    },
    "PBF/IRF-418 - Juventudes Desplazadas": {
        "tema": "Juventudes desplazadas por violencia en Honduras",
        "financiero": [
            "F1. No recursos adicionales movilizados."
        ],
        "no_financiero": [
            "NF1. Influencia directa en la formulación de políticas públicas sobre desplazamiento por violencia (reactivación y aprobación de la Ley de Desplazamiento).",
            "NF2. Transformación de la participación juvenil en mecanismo permanente de incidencia política e institucional (redes reconocidas por gobiernos municipales y autoridades).",
            "NF3. A raíz del apoyo a FLACSO para el desarrollo del primer diplomado en Desplazamiento interno forzado y juventud, han impartido otros diplomados para ACNUR y otras organizaciones."
        ]
    },
    "PBF/IRF-421 - Trinacional": {
        "tema": "Movilidad Humana Digna, Pacífica e Inclusiva",
        "financiero": [
            "F1. Recursos adicionales movilizados en la Fase 1 de: Fondos Multidonante (El Salvador), AVINA, USAID -IRM, Gobierno de Islas Baleares (Guatemala).",
            "F2. Recursos adicionales movilizados en la Fase 2 de: MIRPS (El Salvador), ECHO, AECID, IRCC Canadá, USAID – IRM (Guatemala), PROASOL, Alcaldía de Choloma, CERF (Honduras).",
            "F3. Financiación de actividades complementarias en los territorios focalizados.",
            "F4. El gobierno central a través de la Secretaría de Gobernación financió el equipamiento de las UDAR, fortalecidas a través del proyecto."
        ],
        "no_financiero": [
            "NF1. En El Salvador y Honduras se institucionalizan mecanismos de acceso a la justicia a personas en situación de movilidad humana.",
            "NF2. Estructuración de iniciativas para incluir la financiación de la movilidad humana en planes o programas nacionales y locales.",
            "NF3. Se mitigaron tensiones entre la Alcaldía de Choloma, sector privado (zonas francas) y comunidades receptoras de migrantes retornados.",
            "NF4. La Ley de Protección a Personas Desplazadas por Violencia (2023) incorpora insumos técnicos del proyecto y consolidó mecanismos de protección.",
            "NF5. La inversión del PBF favoreció el escalamiento hacia una agenda más amplia de desarrollo económico y prevención de conflictos con nuevos actores."
        ]
    },
    "PBF/IRF-435 - Tierra Joven": {
        "tema": "Conflictividad tierra/territorio juventudes",
        "financiero": [
            "F1. Recursos adicionales movilizados: EU $8 MM.",
            "F2. Luego de la intervención inicial, algunas agencias del SNU han incluido componentes de juventud, paz y participación en sus proyectos locales.",
            "F3. Financiamiento indirecto a las redes juveniles, formaciones, incidencia y participación juvenil."
        ],
        "no_financiero": [
            "NF1. Decisión de establecer una Mesa Interinstitucional de Prevención y Abordaje de la Conflictividad.",
            "NF2. Las mesas departamentales de prevención, Comisión Tripartita y otros mecanismos permitieron avanzar con el establecimiento y réplica en el territorio nacional.",
            "NF3. Las propuestas normativas elaboradas por juventudes y OSC fueron presentadas y adoptadas por la Secretaría de Derechos Humanos.",
            "NF4. Algunas redes juveniles continúan funcionando de manera autónoma o con acompañamiento de las oficinas municipales.",
            "NF5. El enfoque participativo y territorial se menciona como modelo innovador y transferible en presentaciones de otros proyectos PBF."
        ]
    },
    "PBF/IRF-466 - Pro-Defensoras": {
        "tema": "Pro-Defensoras Honduras",
        "financiero": [
            "F1. El proyecto ha impulsado la búsqueda de recursos para la continuación de sus acciones (Proyecto Mujeres Visibles ejecutado por ONU Mujeres / AECID).",
            "F2. CONADEH presentó propuesta ante el UNDEF para continuar con proyecto 2023. No fue otorgada.",
            "F3. Las Hormigas presentó proyecto al Fondo Global para Organizaciones Feministas con líneas del proyecto ProDefensoras."
        ],
        "no_financiero": [
            "NF1. El CONADEH reconoce la necesidad de continuar con un equipo especializado en territorios para atención diferenciada a defensoras.",
            "NF2. Se ha generado la necesidad de construir una propuesta para aumento de recursos ante el Congreso Nacional y secretaría de Finanzas.",
            "NF3. Se ha generado un espacio de articulación entre las organizaciones socias para impulsar acciones de reivindicación de derechos conjuntos.",
            "NF4. Las redes de mujeres defensoras han continuado activas, siendo integradas sus recomendaciones en políticas nacionales de protección.",
            "NF5. Aprobación y adopción del Protocolo Nacional de Protección Integral para Mujeres Defensoras de Derechos Humanos.",
            "NF6. Transformación gradual de la percepción social sobre las mujeres defensoras, reduciendo su estigmatización y criminalización."
        ]
    },
    "PBF/IRF-507 - Protegiendo Mi Barrio": {
        "tema": "Jóvenes construyendo comunidad",
        "financiero": [
            "F1. La cifra USD 15,200 (Kobo) equivale a L 400,000 en el POA 2025 del Distrito Central mencionado en el reporte de Sostenibilidad.",
            "F2. El reporte final menciona que la asignación se discute nuevamente para el POA 2026."
        ],
        "no_financiero": [
            "NF1. El nivel de participación en los Consejos Municipales es más alto de lo esperado en un mecanismo gubernamental y se espera que continúe.",
            "NF2. Juramentación de la Red Juvenil Presión del Distrito Central, llevada a cabo por el INJUVE, marcando un hito en la formalización.",
            "NF3. Los jóvenes de la red participan activamente en la Mesa de Consulta Joven, contribuyendo a la creación de una nueva política de juventudes.",
            "NF4. Juramentación del Consejo Municipal y aprobación de la Política Municipal de Garantía de Derechos de la Niñez.",
            "NF5. Reconstrucción de confianza social e institucional que habilita la participación juvenil sostenida (El PBF actuó como detonante)."
        ]
    },
    "PBF/HND/B1 - Pro-Tierra": {
        "tema": "Atlántida, Colón, Gracias a Dios",
        "financiero": [
            "F1. Recursos adicionales de AECID y UN RB (8,8% - USD 264.000 movilizados)."
        ],
        "no_financiero": [
            "NF1. Aprobación del Decreto Legislativo No. 18-2024 con alcance a nivel de mesoamérica.",
            "NF2. Inicio del proceso de creación de una Jurisdicción Nacional Especial de Tierras, Territorio y Medio Ambiente.",
            "NF3. Reforma del proceso de licenciamiento ambiental en el país.",
            "NF4. Creación de un mecanismo interinstitucional para la implementación de sentencias internacionales a favor de las comunidades garífunas.",
            "NF5. Fortalecimiento de la gobernanza comunitaria para la consolidación de la Paz.",
            "NF6. Se identificaron rutas de saneamiento del territorio ancestral (Punta Piedra).",
            "NF7. Prohibición de inscripción de títulos en los territorios ancestrales de Triunfo de la Cruz, Punta Piedra y San Juan.",
            "NF8. Se establecieron mecanismos de alerta temprana interinstitucional en los departamentos de Atlántida y Colón."
        ]
    },
    "PBF/HND/B2 - Respuesta Multidimensional": {
        "tema": "Respuesta Multidimensional (afrohondureñas)",
        "financiero": [
            "F1. Recursos adicionales de CERF, Secretaría de Seguridad, Data for change y Fondo de Cambio Climático (USD 500.000 movilizados).",
            "F2. Articulación con recursos de cooperación complementarios (ACNUR, OIM, USAID), fortaleciendo sostenibilidad en rutas de derivación.",
            "F3. En municipios como La Ceiba y el Distrito Central, las oficinas municipales brindaron apoyo logístico y personal en especie para sostener servicios."
        ],
        "no_financiero": [
            "NF1. Coordinación interinstitucional activa para diseñar respuestas focalizadas.",
            "NF2. Atención proactiva del sector gubernamental mediante estrategias adaptadas a contextos interculturales.",
            "NF3. Sistematización de demandas específicas, traduciéndolas en políticas operativas con asignación presupuestaria.",
            "NF4. Estudio de Barreras y racismos y diálogos identitarios de origen y memoria.",
            "NF5. Lanzamiento del Sistema Nacional de Información sobre Trata de Personas en Honduras (primera fase implementada).",
            "NF6. Se fortalecieron servicios multisectoriales en Roatán, La Ceiba y Tela, con enfoque diferenciado para mujeres afrodescendientes."
        ]
    },
    "PBF/IRF-561 - MUCAMPAZ": {
        "tema": "Mujeres Resilientes al cambio climático",
        "financiero": [
            "F1. No se reportan efectos catalíticos financieros."
        ],
        "no_financiero": [
            "NF1. El proyecto está contribuyendo a la creación de esquemas para lograr el empoderamiento de las comunidades dentro de las AFAs, identificando tensiones y resolución de conflictos socio ambientales.",
            "NF2. Mujeres de las Asociaciones en las Áreas Forestales Asignadas de Gualaco y Bonito Oriental accedieron a espacios de toma de decisiones para la gestión ambiental."
        ]
    }
}

# 3. GESTIÓN DE LA BASE DE DATOS (SOPORTE LIVE / SIMULACIÓN LOCAl)
if "db_simulada" not in st.session_state:
    st.session_state.db_simulada = pd.DataFrame(columns=["Participante", "Proyecto", "Tipo", "Item", "Asertividad", "Completitud"])

modo_hoja_real = False
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_respuestas = conn.read(worksheet="RespuestasLive")
    modo_hoja_real = True
except Exception:
    df_respuestas = st.session_state.db_simulada

# 4. MENÚ DE NAVEGACIÓN PRINCIPAL
pestana_votar, pestana_dashboard = st.tabs(["📱 EVALUACIÓN (Celulares)", "📊 RESULTADOS (Proyector)"])

# =========================================================================
# 📱 PESTAÑA 1: PANEL INTERACTIVO PARA LOS PARTICIPANTES
# =========================================================================
with pestana_votar:
    st.title("Taller de Validación de Efectos Catalíticos")
    st.subheader("Portafolio PBF Honduras 2020-2025")
    
    if not modo_hoja_real:
        st.caption("ℹ️ *Modo de prueba activado (conecte Google Sheets para persistencia).*")
        
    usuario_id = st.text_input("Ingresa tu Institución o Nombre para empezar:", placeholder="Ej. PNUD / UNFPA / SEPLAN")
    
    if usuario_id:
        st.success(f"Sesión activa: **{usuario_id}**")
        st.markdown("---")
        
        proyecto_sel = st.selectbox("📌 Selecciona el Proyecto que se está discutiendo:", list(DATOS_PORTAFOLIO.keys()))
        
        if proyecto_sel:
            datos = DATOS_PORTAFOLIO[proyecto_sel]
            st.markdown(f"### 🎯 Tema Principal: *{datos['tema']}*")
            
            with st.form(key=f"form_{proyecto_sel}"):
                respuestas_formulario = []
                
                # Componentes Financieros
                st.markdown("#### 🔴 Evaluación de Componentes Financieros")
                for item in datos["financiero"]:
                    st.info(item)
                    col1, col2 = st.columns(2)
                    with col1:
                        a = st.radio("¿Es asertivo el resultado?", [1, 2, 3, 4], index=2, horizontal=True, key=f"as_{item}_{usuario_id}")
                    with col2:
                        c = st.radio("¿La información está completa?", [1, 2, 3, 4], index=2, horizontal=True, key=f"co_{item}_{usuario_id}")
                    respuestas_formulario.append({"Participante": usuario_id, "Proyecto": proyecto_sel, "Tipo": "Financiero", "Item": item, "Asertividad": a, "Completitud": c})
                
                st.markdown("---")
                
                # Componentes No Financieros
                st.markdown("#### 🔵 Evaluación de Componentes No Financieros")
                for item in datos["no_financiero"]:
                    st.info(item)
                    col1, col2 = st.columns(2)
                    with col1:
                        a = st.radio("¿Es asertivo el resultado?", [1, 2, 3, 4], index=2, horizontal=True, key=f"as_{item}_{usuario_id}")
                    with col2:
                        c = st.radio("¿La información está completa?", [1, 2, 3, 4], index=2, horizontal=True, key=f"co_{item}_{usuario_id}")
                    respuestas_formulario.append({"Participante": usuario_id, "Proyecto": proyecto_sel, "Tipo": "No Financiero", "Item": item, "Asertividad": a, "Completitud": c})
                
                enviar_votos = st.form_submit_button("Guardar calificaciones de este proyecto 🚀")
                
                if enviar_votos:
                    df_nuevos_votos = pd.DataFrame(respuestas_formulario)
                    if modo_hoja_real:
                        df_consolidado = pd.concat([df_respuestas, df_nuevos_votos], ignore_index=True)
                        conn.update(worksheet="RespuestasLive", data=df_consolidado)
                    else:
                        st.session_state.db_simulada = pd.concat([st.session_state.db_simulada, df_nuevos_votos], ignore_index=True)
                    st.balloons()
                    st.success(f"¡Excelente! Tus respuestas han sido transmitidas con éxito.")
    else:
        st.warning("⚠️ Por favor ingresa tu Institución o Nombre en el campo de arriba para habilitar la votación.")

# =========================================================================
# 📊 PESTAÑA 2: PANTALLA DE RESULTADOS EN TIEMPO REAL (Para Proyectar)
# =========================================================================
with pestana_dashboard:
    st.title("📊 Cuadrante de Validación Estratégica en Vivo")
    st.write("Esta pantalla consolida los promedios matemáticos de todos los participantes.")
    
    # Botón manual para refrescar los datos desde Google Sheets durante el taller
    if st.button("🔄 Forzar Actualización de la Matriz"):
        st.rerun()
        
    # Recargamos la variable con los datos más recientes
    datos_actuales = df_respuestas if modo_hoja_real else st.session_state.db_simulada
    
    if not datos_actuales.empty:
        # Procesamos los datos: Sacamos el promedio general de asertividad (X) y completitud (Y) por cada proyecto
        df_grafico = datos_actuales.groupby("Proyecto").agg(
            X_Asertividad=("Asertividad", "mean"),
            Y_Completitud=("Completitud", "mean"),
            Muestras=("Participante", "count")
        ).reset_index()
        
        # Creamos el Scatter Plot interactivo
        fig = go.Figure()
        
        # --- DIBUJO DE LOS 4 CUADRANTES DE FONDO ---
        fig.add_shape(type="rect", x0=2.5, y0=2.5, x1=4.5, y1=4.5, fillcolor="rgba(198, 239, 206, 0.25)", line_width=0)
        fig.add_shape(type="rect", x0=0.5, y0=2.5, x1=2.5, y1=4.5, fillcolor="rgba(255, 230, 153, 0.25)", line_width=0)
        fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=2.5, y1=2.5, fillcolor="rgba(244, 204, 204, 0.25)", line_width=0)
        fig.add_shape(type="rect", x0=2.5, y0=0.5, x1=4.5, y1=2.5, fillcolor="rgba(252, 228, 214, 0.25)", line_width=0)
        
        # --- AGREGAR LOS PUNTOS DE LOS PROYECTOS ---
        fig.add_trace(go.Scatter(
            x=df_grafico["X_Asertividad"],
            y=df_grafico["Y_Completitud"],
            mode="markers+text",
            text=df_grafico["Proyecto"].apply(lambda x: x.split(" - ")[1] if " - " in x else x), 
            textposition="top center",
            marker=dict(size=14, color="#1F4E78", line=dict(width=2, color="White")),
            hovertemplate="<b>%{text}</b><br>Asertividad: %{x:.2f}<br>Completitud: %{y:.2f}<extra></extra>"
        ))
        
        # --- AGREGAR LAS LÍNEAS DE CORTE CRUCIALES (Ejes en el centro 2.5) ---
        fig.add_shape(type="line", x0=2.5, y0=0.5, x1=2.5, y1=4.5, line=dict(color="#C00000", width=2, dash="dash"))
        fig.add_shape(type="line", x0=0.5, y0=2.5, x1=4.5, y1=2.5, line=dict(color="#C00000", width=2, dash="dash"))
        
        fig.update_layout(
            xaxis=dict(title="¿Es Asertivo el Resultado? (Eje X)", range=[0.5, 4.5], dtick=0.5, gridcolor="#EAEAEA"),
            yaxis=dict(title="¿Es Completa la Información? (Eje Y)", range=[0.5, 4.5], dtick=0.5, gridcolor="#EAEAEA"),
            height=600, plot_bgcolor="white", margin=dict(l=40, r=40, t=20, b=40)
        )
        
        # Desplegamos el gráfico interactivo
        st.plotly_chart(fig, use_container_width=True)
        
        # =========================================================================
        # NUEVA SECCIÓN: DESGLOSE INTERACTIVO AFIRMACIÓN POR AFIRMACIÓN
        # =========================================================================
        st.markdown("---")
        st.subheader("🔍 Desglose Técnico de Afirmaciones en Tiempo Real")
        st.write("Selecciona un proyecto para auditar la calificación exacta de cada una de sus viñetas:")
        
        # Dropdown para elegir qué proyecto queremos analizar detalladamente en la proyección
        proyecto_auditar = st.selectbox("Elegir proyecto para auditar:", df_grafico["Proyecto"].unique(), key="auditor_presentador")
        
        if proyecto_auditar:
            # Filtramos los votos únicamente de ese proyecto
            df_filtrado = datos_actuales[datos_actuales["Proyecto"] == proyecto_auditar]
            
            # Agrupamos por la viñeta (Item) para calcular sus promedios específicos
            df_items = df_filtrado.groupby(["Tipo", "Item"]).agg(
                Promedio_Asertividad=("Asertividad", "mean"),
                Promedio_Completitud=("Completitud", "mean"),
                Votos_Recibidos=("Participante", "count")
            ).reset_index()
            
            # Le damos un formato visual de tabla limpia y estilizada
            st.dataframe(
                df_items.style.format({
                    "Promedio_Asertividad": "{:.2f},
                    "Promedio_Completitud": "{:.2f}"
                }), 
                use_container_width=True,
                hide_index=True
            )
            
    else:
        st.info("📊 La matriz aparecerá automáticamente aquí cuando guarden sus primeros votos.")
