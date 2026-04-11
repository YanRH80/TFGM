---
title: "Final"
author: "Yan Rodriguez Garcia"
date: today
format:
  pdf:
    toc: true
    toc-depth: 2
    number-sections: true
    colorlinks: true
    keep-tex: false
    fig-pos: 'H'
    include-in-header:
      text: |
        \usepackage{booktabs}
        \usepackage{tikz}
        \usetikzlibrary{positioning, arrows.meta, shapes.geometric}
        \usepackage{float}
bibliography: references.bib
execute:
  echo: false
  warning: false
---


# Seronegativizacion por IgG-ELISA tras ivermectina en estrongiloidiasis: cinetica, predictores y modelizacion en una cohorte retrospectiva unicentrica (estudio exploratorio)

> **Estado**: Borrador modular para verificacion bibliografica y articulacion de insights.
> Cada sentencia es una proposicion verificable. `[CITE]` = necesita referencia. `[DATA]` = dato propio. `[?]` = pendiente de verificar/decidir.

---

## ABSTRACT

### Checklist de elementos por redactar

- [ ] **Objetivo**: 1 frase, incluir "exploratorio"
- [ ] **Diseno**: cohorte retrospectiva unicentrica, n=44
- [ ] **Endpoint primario**: primera IgG-ELISA < 1,1 post-ivermectina
- [ ] **Hallazgo principal**: mediana KM = 8,8 meses (IC 95% 4,3--11,4)
- [ ] **Landmarks**: 36% a 6m, 68% a 12m, 76% a 18m, 88% a 24m
- [ ] **Tasa**: 0,84 eventos/persona-ano (IC 95% 0,53--1,19)
- [ ] **Predictores**: ninguno significativo tras BH-FDR (p_adj min = 0,053)
- [ ] **LMM**: pendiente = --0,068 log(IgG)/mes, tiempo estimado = 10,9 meses
- [ ] **Interaccion sexo**: no significativa (p = 0,501)
- [ ] **Conclusion**: calendario de seguimiento basado en landmarks; potencia insuficiente para predictores (HR_min = 3,62)
- [ ] Limite: 250 palabras structured abstract

### Metricas de revision
- Palabras objetivo: 250
- Keywords objetivo: 5--8 (strongyloidiasis, ivermectin, seroreversion, IgG, Kaplan-Meier, survival analysis, cohort study)

---

## 1. INTRODUCTION

### 1.1 Carga de enfermedad

*S. stercoralis* infecta entre 30 y 100 millones de personas en regiones tropicales y subtropicales.
`[CITE: buonfrate2023 CMR review; bisoffi2013]`

La prevalencia real esta infraestimada por la baja sensibilidad de las tecnicas coprologicas convencionales (< 50% con metodos directos).
`[CITE: Requena-Mendez 2017; Schar 2013 PLoS NTD]`

En Europa, la estrongiloidiasis es una infeccion importada creciente, concentrada en migrantes de America Latina y Africa subsahariana; la seroprevalencia en cribados de migrantes oscila entre 11,4--14% (latinoamericanos) y 14,6--20% (subsaharianos).
`[CITE: buonfrate2015; asundi2019 meta-analysis]`

Las cohortes europeas de estrongiloidiasis diagnosticada muestran un perfil demografico consistente: edad mediana 38--63 anos, predominio masculino (54--72%) e inmunodepresion en ~6% de los pacientes.
`[CITE: salvador2019 REDIVI n=1245; cutfield2024 Auckland]`

### 1.2 Tratamiento y seguimiento

La ivermectina (200 ug/kg, dosis unica o doble) es el tratamiento de eleccion con tasas de curacion parasitologica cercanas al 100%.
`[CITE: henriquez2016 Cochrane]`

El ensayo Strong Treat (n = 310, multicentrico) demostro que la dosis unica es equivalente a cuatro dosis en cura serologica a 12 meses (86% vs 85%), llevando a la terminacion precoz del ensayo por futilidad de la multidosis.
`[CITE: buonfrate2019]`

No existe consenso sobre el criterio optimo de curacion serologica post-tratamiento: la reduccion relativa >= 50% de OD (primary outcome de Strong Treat) es el mas validado, pero la seronegativizacion completa es mas especifica (34--72% segun el assay utilizado).
`[CITE: buonfrate2019; buonfrate2015; salvador2014]`

No existen guias formales basadas en evidencia para la duracion optima del seguimiento serologico post-tratamiento; las recomendaciones actuales derivan de opinion de expertos y datos observacionales.
`[CITE: lo2025 WHO guideline review; buonfrate2019]`

La OMS reconoce que "una proporcion de individuos con serologia positiva puede serorrevertir a negativo en 12--18 meses tras el tratamiento".
`[CITE: lo2025]`

La serologia IgG-ELISA es el marcador mas utilizado para seguimiento, pero su cinetica de descenso es lenta e impredecible, y la persistencia serologica no distingue entre memoria inmunologica y infeccion activa.
`[CITE: salvador2014; buonfrate2015; repetto2018]`

### 1.3 Gap: predictores de seronegativizacion

El unico modelo multivariable publicado de predictores de aclaramiento serologico (Strong Treat, n = 310) identifico edad, eosinofilos > 400/uL y ausencia de rash como predictores; sin embargo, la IgG basal no fue incluida como variable y la inmunodepresion fue un criterio de exclusion.
`[CITE: buonfrate2019]`

Hasta donde sabemos, ningun estudio ha evaluado si el nivel basal de IgG-ELISA predice la velocidad de seronegativizacion post-ivermectina.
`[CITE: ausencia confirmada por busqueda sistematica en OE -- Q10]`

Ademas, ningun estudio previo ha reportado la mediana de tiempo a seronegativizacion con intervalo de confianza formal, ni coeficientes parametricos de descenso mensual de IgG.
`[CITE: ausencia confirmada -- Q06, Q12; buonfrate2015 aplico LMM pero no reporto coeficientes]`

El tiempo hasta la seronegativizacion condiciona la duracion del seguimiento y la interpretacion de serologias persistentemente positivas: un paciente seropositivo a los 12 meses puede estar aun en fase de descenso fisiologico o tener una reinfeccion/fracaso terapeutico; en contextos no endemicos como el nuestro, cualquier ascenso serologico tras descenso inicial representa persistencia de la infeccion original (no reinfeccion).
`[CITE: buonfrate2015; repetto2018; lo2025]`

La persistencia de titulos elevados podria reflejar celulas plasmaticas de vida larga, como se ha demostrado en Chagas (Cesar 2023) y malaria (Yman 2019), donde la proporcion de ASC de vida larga aumenta con la exposicion repetida.
`[CITE: cesar2023; yman2019]`

### 1.4 Hipotesis y objetivos

**Hipotesis**: existen variables basales (IgG basal, eosinofilia, sexo, inmunodepresion) que predicen diferencias en la velocidad de seronegativizacion tras ivermectina.

**Objetivo primario**: estimar la mediana y la cinetica de seronegativizacion (IgG-ELISA < 1,1) tras tratamiento con ivermectina mediante analisis de Kaplan-Meier.

**Objetivos secundarios**: (a) identificar predictores basales de seronegativizacion mediante regresion de Cox; (b) modelizar la trayectoria continua de descenso de log(IgG) mediante modelo lineal mixto.

---

## 2. METHODS

### 2.1 Diseno y ambito

Estudio de cohorte retrospectiva unicentrica.

Se incluyeron pacientes diagnosticados de estrongiloidiasis y tratados con ivermectina en el Hospital Universitario de Guadalajara (HCDGU), Espana, entre 2017 y 2025.

Los registros se identificaron cruzando la base del Centro Nacional de Microbiologia (CNM, 2017--2023) con la serologia del HCDGU (2020--2025).

El estudio se adhiere a las recomendaciones STROBE para estudios observacionales.
`[CITE: von Elm 2007]`

### 2.2 Participantes

Criterios de inclusion: diagnostico confirmado de *S. stercoralis* (serologia positiva, parasitologia positiva o diagnostico clinico-epidemiologico) y al menos una dosis de ivermectina con seguimiento serologico post-tratamiento.

Criterios de exclusion: diagnostico no confirmado tras revision de historia clinica (n = 114/198), ausencia de tratamiento con ivermectina (n = 20), ausencia de seguimiento post-tratamiento (n = 19), diagnostico fuera del HCDGU (n = 1).

La cohorte final comprende 44 pacientes (tasa de retencion 22,2%; IC 95% binomial: 16,6--28,8%).

### 2.3 Variables

T0 se define como la fecha de la primera dosis de ivermectina.

La serologia basal es la determinacion de IgG-ELISA mas proxima a T0 (mediana 18 dias pre-T0, IQR 11--62).

Kit ELISA: `[? fabricante, modelo, cutoff del fabricante, cambios de lote 2017--2025 -- PENDIENTE INPUT USUARIO]`

Las covariables se seleccionaron por plausibilidad biologica: edad (inmunosenescencia), sexo (dimorfismo inmune Th2), IgG basal (carga parasitaria indirecta), eosinofilos basales (respuesta Th2), inmunodepresion (riesgo de hiperinfeccion).

### 2.4 Endpoint primario

Primera determinacion de IgG-ELISA < 1,1 (indice) post-T0, en una unica medicion (seronegativizacion absoluta).

Este criterio representa la negativizacion segun el cutoff del fabricante del kit, un umbral intermedio entre la seronegativizacion completa (mas especifica, 34--72% segun assay) y la reduccion relativa >= 50% OD (mas sensible, ~82--86% a 6--12 meses), que fue el *primary outcome* del ensayo Strong Treat.
`[CITE: buonfrate2019; buonfrate2015; salvador2014]`

Los ELISA de antigeno crudo (como el utilizado en nuestro estudio) muestran la mayor proporcion de descenso relevante (~90% de muestras con OD reducida a la mitad), siendo los mas adecuados para detectar respuesta al tratamiento; los ELISA recombinantes (NIE-ELISA) muestran mayor seronegativizacion completa (72,5%).
`[CITE: buonfrate2015]`

Se utilizo el mismo assay en la determinacion basal y en el seguimiento, siguiendo la recomendacion de la literatura de no comparar valores entre assays diferentes.
`[CITE: buonfrate2015; buonfrate2019]`

Se evaluaron 8 definiciones alternativas como analisis de sensibilidad: umbral estricto (IgG < 0,9), confirmacion por doble determinacion (x2), descenso relativo >= 40% respecto a basal, normalizacion eosinofilica (< 0,5 x10^3/uL) y negativizacion parasitologica.
`[CITE: salvador2014 para criterio de descenso relativo]`

### 2.5 Analisis estadistico

#### Kaplan-Meier y landmarks

La funcion de supervivencia se estimo mediante Kaplan-Meier con censura a la derecha en la ultima serologia disponible.
`[CITE: Kaplan 1958]`

El IC 95% de la mediana se calculo por el metodo de Greenwood.
`[CITE: Greenwood 1926 o referencia estandar]`

Se reportan *landmark estimates* (probabilidad acumulada de seronegativizacion a 6, 12, 18 y 24 meses) y tasa de incidencia por persona-ano con IC 95% Poisson.

#### Cox univariable y multivariable

Se ajusto un modelo de Cox por cada covariable candidata (15 variables).
`[CITE: Cox 1972]`

La correccion de Benjamini-Hochberg (BH-FDR) se aplico a los p-valores crudos para controlar la tasa de falsos descubrimientos.
`[CITE: Benjamini 1995]`

El modelo multivariable admite un maximo de 2 covariables segun la regla de Peduzzi (>= 10 eventos/variable).
`[CITE: Peduzzi 1996]`

Las covariables se seleccionaron por: (1) relevancia biologica, (2) menor p univariable entre variables binarias, (3) colinealidad tolerable (VIF < 10).

El supuesto de proporcionalidad de riesgos se evaluo mediante el test de residuos de Schoenfeld; las variables que lo violan se manejan por estratificacion.
`[CITE: Schoenfeld 1982]`

Se valido mediante C-statistic y bootstrap (1000 replicas).

La potencia post-hoc se calculo con la formula de Schoenfeld para el HR minimo detectable.
`[CITE: Schoenfeld 1983]`

#### Datos faltantes

Se empleo analisis de caso completo (8/44 pacientes sin IgG basal cuantitativa, 18%).

La plausibilidad de MCAR se evaluo mediante regresion logistica multivariable de la ausencia de IgG basal sobre edad, sexo, eosinofilos basales e inmunodepresion.
`[CITE: Little 1988]`

#### Modelo lineal mixto

Se ajusto un LMM con intercepto aleatorio por paciente sobre log(IgG) en funcion del tiempo, restringido a seropositivos (IgG basal >= 1,1), anclando la observacion basal en t = 0.
`[CITE: Nakagawa 2013]`

Se comparo con un modelo de pendiente aleatoria mediante AIC.

Se ajusto un modelo con interaccion meses x sexo para evaluar si la velocidad de descenso difiere entre sexos, motivado por la violacion de proporcionalidad detectada en el Cox.

Se reporta el R2 de Nakagawa (marginal y condicional).
`[CITE: Nakagawa 2013]`

#### Software

Python 3.14, lifelines (Kaplan-Meier, Cox), statsmodels (LMM, regresion logistica), scipy.

---

## 3. RESULTS

### 3.1 Cohorte

De 198 registros cribados, 84 (42,4%) tuvieron diagnostico confirmado; 64 fueron tratados con ivermectina; 44 conforman la cohorte final (Figura 1).

La edad mediana fue 47,5 anos (IQR 36,6--56,2; rango 18,1--70,1); el 56,8% fueron mujeres (25/44).

La cohorte es predominantemente latinoamericana: 73% America del Sur (Ecuador 15, Bolivia 10), 14% America Central y Caribe, 11% Africa subsahariana, 5% Europa.

El 70% de los diagnosticos se establecio por serologia exclusiva (31/44), el 9% por serologia mas parasitologia (4/44), el 5% por parasitologia sola (2/44) y el 16% por criterio clinico-epidemiologico (7/44).

El regimen mas frecuente fue monodosis (23/44, 52%), seguido de doble consecutiva (10/44, 23%), doble separada (7/44, 16%) y cuadruple (4/44, 9%).

La inmunodepresion estuvo presente en el 9% (4/44); la comorbilidad en el 41% (18/44).

La IgG-ELISA basal mediana fue 3,1 (IQR 1,3--6,6; rango 0,5--12,6; n = 36; 8 sin dato cuantitativo).

Los eosinofilos basales medianos fueron 0,8 x10^3/uL (IQR 0,2--1,2); el 57,1% presentaba eosinofilia (>= 0,5 x10^3/uL).

### 3.2 Seguimiento y completitud

De los 44 pacientes, 39 tuvieron al menos una serologia post-T0 (evaluables para el endpoint primario); 5 carecian de seguimiento serologico.

La mediana de seguimiento serologico fue 11,7 meses (IQR 3,1--22,2; rango 1,1--72,1).

El 49% de los evaluables (19/39) tuvo seguimiento >= 12 meses; el 28% (11/39) >= 18 meses; el 21% (8/39) >= 24 meses.

La ventana entre serologia basal y T0 fue de mediana 18 dias (IQR 11--62), lo que minimiza el sesgo de tiempo inmortal.

La normalizacion eosinofilica fue mas rapida que la seronegativizacion (mediana KM 3,0 vs 8,8 meses), coherente con la vida media de eosinofilos circulantes (8--18 h) frente a IgG (semanas).
`[CITE: buonfrate2019 -- eos normalizan dia 17; mitre2021 -- vida media eos 8-18h]`

### 3.3 Hallazgo principal: cinetica de seronegativizacion (Figura 2)

> **Figura 2**: Curva KM para seronegativizacion absoluta (IgG < 1,1). n = 39, 27 eventos.

La mediana KM de seronegativizacion fue 267 dias (8,8 meses; IC 95% Greenwood: 132--348 dias, 4,3--11,4 meses).

El 69% de los pacientes evaluables (27/39) alcanzo seronegativizacion durante el seguimiento.

La curva KM muestra una pendiente pronunciada en los primeros 12 meses, con aplanamiento posterior.

**Landmark estimates**: el 36% habia seronegativizado a los 6 meses, el 68% a los 12 meses, el 76% a los 18 meses y el 88% a los 24 meses.

La tasa de incidencia fue 0,84 seronegativizaciones/persona-ano (IC 95% Poisson: 0,53--1,19; 32,0 personas-ano de seguimiento acumulado).

La censura por intervalo inherente a mediciones periodicas puede subestimar levemente la velocidad real, constituyendo una estimacion conservadora.

### 3.4 Sensibilidad del endpoint (Tabla 2)

| Definicion | n | Eventos | % | Mediana KM (meses) |
|:---|:---:|:---:|:---:|:---:|
| Sero abs x1 (IgG < 1,1) * | 39 | 27 | 69 | 8,8 |
| Sero abs x2 (IgG < 1,1, confirmada) | 39 | 12 | 31 | 16,4 |
| Sero abs x1 (IgG < 0,9) | 39 | 25 | 64 | 10,8 |
| Sero abs x2 (IgG < 0,9, confirmada) | 39 | 11 | 28 | 25,8 |
| Sero rel x1 (caida >= 40%) | 39 | 26 | 67 | 7,8 |
| Sero rel x2 (caida >= 40%, confirmada) | 39 | 9 | 23 | 29,9 |
| Eosinofilos (< 0,5 x10^3/uL) | 44 | 44 | 100 | 3,0 |
| Parasitologia (2 neg) | 17 | 7 | 41 | 25,5 |

\* Endpoint primario. Mediana KM (Kaplan-Meier, incluye censurados).

La reduccion del umbral de 1,1 a 0,9 apenas modifico la cinetica: 27 vs 25 eventos, medianas 8,8 vs 10,8 meses, confirmando la robustez del endpoint primario.

La restriccion a pacientes con ventana basal <= 90 dias (n = 28, 18 eventos, 11 excluidos) produjo una mediana KM de 7,9 meses, consistente con la cohorte completa (8,8 meses).

La exigencia de doble confirmacion (x2) duplico la mediana (8,8 a 16,4 meses) y redujo los eventos al 31%, reflejando la intermitencia de los controles mas que una diferencia biologica real.

### 3.5 Analisis estratificado (Figura 3)

> **Figura 3**: KM estratificado por 5 variables basales. p log-rank.

Tres variables mostraron diferencias significativas en log-rank: IgG >= mediana (p = 0,002), sexo (p = 0,005) y eosinofilia >= 0,5 (p = 0,022).

El regimen (monodosis vs multiple) mostro tendencia (p = 0,109).

Inmunodepresion o comorbilidad no mostro diferencia (p = 0,339).

### 3.6 Cox univariable (Figura 4)

> **Figura 4**: Forest plot univariable. Solo variables p < 0,05.

Se evaluaron 15 covariables en Cox univariable (n = 39; caso completo, 5 excluidos sin seguimiento serologico).

El test MCAR confirmo que la ausencia de IgG basal (8/44, 18%) no se asocio con edad, sexo, eosinofilos ni inmunodepresion (regresion logistica, LR p = 0,11), compatible con MCAR.

Cuatro variables alcanzaron p < 0,05 crudo:

| Variable | n | HR (IC 95%) | p crudo | p_adj (BH) |
|:---|:---:|:---|:---:|:---:|
| IgG >= mediana (3,1) | 32 | 0,19 (0,06--0,59) | 0,004 | 0,053 |
| Sexo (varon) | 39 | 3,29 (1,38--7,81) | 0,007 | 0,053 |
| IgG basal (continua) | 32 | 0,79 (0,65--0,97) | 0,021 | 0,100 |
| Eosinofilia >= 0,5 | 37 | 0,40 (0,18--0,90) | 0,027 | 0,100 |

HR > 1 = seronegativizacion mas rapida; HR < 1 = mas lenta.

**Ninguna variable alcanzo significacion tras BH-FDR** (p_adj minimo = 0,053), reflejando la penalizacion por 15 comparaciones en n = 39.

La IgG basal alta y la eosinofilia se asociaron con seronegativizacion mas lenta (HR < 1); el sexo masculino con seronegativizacion mas rapida (HR > 1).

Seis variables mostraron tendencia (0,05 <= p < 0,20): eosinofilos >= mediana (HR 0,45, p = 0,055), dosis unica (HR 1,86, p = 0,114), edad continua (HR 0,98, p = 0,158), IgG >= P75 (HR 0,41, p = 0,159), inmunodepresion (HR 2,42, p = 0,161) y retratamiento (HR 0,51, p = 0,183).

### 3.7 Cox multivariable (Tabla 3, Figura 5)

> **Tabla 3**: Cox multivariable estratificado por sexo.
> **Figura 5**: Forest plot multivariable + curvas KM por combinacion de covariables.

La IgG basal y los eosinofilos basales mostraron correlacion moderada (Spearman rho = 0,49, p = 0,003) pero colinealidad tolerable (VIF = 1,10).

El test de Schoenfeld detecto violacion de proporcionalidad para el sexo (p = 0,007) pero no para IgG >= mediana (p = 0,395) ni eosinofilia (p = 0,137).

El sexo se manejo por estratificacion (funciones de riesgo basal separadas), no por exclusion.
`[CITE: Schoenfeld 1982]`

| Variable | HR (IC 95%) | p | VIF | Direccion |
|:---|:---|:---:|:---:|:---|
| IgG >= mediana (3,1) | 0,20 (0,03--1,27) | 0,088 | 2,80 | Retrasa |
| Eosinofilia >= 0,5 | 0,63 (0,15--2,62) | 0,526 | 2,80 | Retrasa |
| Sexo (varon) | *Estratificada* | --- | --- | Riesgo basal separado |

Caso completo: n = 30/39 (9 excluidos por datos faltantes), eventos = 19.

C-statistic: 0,676 (vs 0,676 univariable, Delta = +0,001); la segunda covariable no mejoro la discriminacion.

Stepwise AIC selecciono IgG basal y eosinofilos basales (continuas), discordando con la seleccion pre-especificada por mediana, aunque ambos enfoques identifican las mismas variables biologicas.

Bootstrap: 952/1000 replicas exitosas; 48 fallidas por eventos de separacion inherentes al tamano muestral.

**Potencia post-hoc** (Schoenfeld): con 19 eventos, el HR minimo detectable con 80% de potencia es 3,62 (o 0,28). Potencia para HR = 2,0: 33%; para HR = 1,5: 14%.
`[CITE: Schoenfeld 1983]`

El estudio tiene potencia solo para efectos muy grandes (HR > 3,6), insuficiente para efectos moderados.

### 3.8 Trayectoria parametrica: LMM (Figura 6)

> **Figura 6**: LMM spaghetti plot con regresion, bandas IC media y prediccion individual, mediana KM superpuesta.

Se incluyeron 34 seropositivos (IgG basal >= 1,1) con observacion basal anclada en t = 0.

El modelo de pendiente aleatoria fue seleccionado por AIC (266 vs 266; empate, se prefiere el mas flexible).

Ecuacion: log(IgG) = 0,84 -- 0,068 x meses (p < 0,001).

Tiempo estimado hasta seronegativizacion por extrapolacion (cruce con log(1,1) = 0,095): 10,9 meses, coherente con la mediana KM (8,8 meses).

R2 marginal = 0,426; R2 condicional = 0,563.
`[CITE: Nakagawa 2013]`

La diferencia (10,9 LMM vs 8,8 KM) refleja los supuestos: el LMM asume descenso log-lineal sostenido; el KM no asume forma funcional.

Un plateau tardio de IgG (memoria inmunologica residual) invalidaria la extrapolacion del LMM.
`[CITE: cesar2023 -- ASC larga vida en Chagas; yman2019 -- modelo bifasico malaria]`

### 3.9 Interaccion LMM por sexo (Figura 7)

> **Figura 7**: Spaghetti bicolor con rectas por sexo.

La interaccion meses x sexo no alcanzo significacion (beta = --0,0128, p = 0,501).

Pendiente varones: --0,0454/mes; mujeres: --0,0326/mes (n = 15 + 19).

La violacion de proporcionalidad (Schoenfeld p = 0,007) no se traduce en diferencia de pendiente en el LMM, sugiriendo efecto transitorio o artefacto muestral.

---

## 4. DISCUSSION

### 4.1 Hallazgo principal en contexto

Nuestra mediana KM de 8,8 meses (IC 95% 4,3--11,4) es, hasta donde sabemos, la primera estimacion formal del tiempo a seronegativizacion (con IC por metodo de Greenwood) publicada para estrongiloidiasis post-ivermectina.
`[CITE: ausencia confirmada -- Q06; ningun estudio previo reporto mediana con IC]`

Los estudios previos reportaron proporciones categoricas: en la cohorte de Barcelona, el 81,3% alcanzo criterios de respuesta (serologia negativa o ratio OD post/pre <= 0,6) a 6 meses, y solo el 34,4% logro seronegativizacion completa.
`[CITE: salvador2014]`

En Strong Treat, el 82--86% alcanzo aclaramiento serologico (definido como serologia negativa o reduccion >= 50% OD) a 6--12 meses.
`[CITE: buonfrate2019]`

La evaluacion con NIE-ELISA recombinante mostro una reduccion relativa mediana de 93,9% (IQR 77,3--98,1%) a 12 meses, con la mayor tasa de seronegativizacion completa (72,5%).
`[CITE: prato2024; buonfrate2015]`

**Nota sobre divergencia aparente**: nuestro 36% a 6 meses y 68% a 12 meses (endpoint absoluto < 1,1) contrasta con el 81--86% de Strong Treat/Salvador. La diferencia se explica por la definicion de endpoint: nuestro criterio (IgG absoluta < 1,1) equivale a seronegativizacion completa (umbral del kit), mientras que el criterio de Strong Treat incluye reducciones relativas sustanciales sin negativizacion completa. Nuestro 68% a 12 meses es coherente con el rango publicado de seronegativizacion completa (34--72% segun assay).
`[CITE: buonfrate2019; buonfrate2015; salvador2014]`

Los landmarks proporcionan informacion clinicamente mas util que la mediana aislada: a los 12 meses, dos tercios han seronegativizado; a los 24 meses, casi el 90%.

La tasa de 0,84 eventos/persona-ano (IC 95% 0,53--1,19) permite la comparacion directa con futuras cohortes y ensayos clinicos.

Strong Treat concluyo que "6 meses de seguimiento pueden ser suficientes para juzgar la respuesta al tratamiento"; sin embargo, nuestros landmarks muestran que con criterio estricto (absoluto < 1,1) solo un tercio ha negativizado a 6 meses, sugiriendo que este plazo es insuficiente para confirmar seronegativizacion completa.
`[CITE: buonfrate2019]`

La OMS reconoce que una proporcion de pacientes seropositivos puede serorrevertir en 12--18 meses; nuestros datos confirman esta ventana y la extienden: el 12% persiste seropositivo a 24 meses.
`[CITE: lo2025]`

La tasa de recidiva serologica tras aclaramiento inicial es baja (4% en Strong Treat, 6 a 12 meses), pero puede subestimar la persistencia parasitologica: en un seguimiento a 4 anos, Repetto et al. detectaron larvas en 67% de pacientes y ADN de *S. stercoralis* por PCR en el 100%, concluyendo que "la estrongiloidiasis debe considerarse una infeccion cronica".
`[CITE: buonfrate2019; repetto2018]`

### 4.2 Ausencia de predictores significativos

Ninguna variable alcanzo significacion tras BH-FDR (p_adj minimo 0,053), resultado coherente con la limitada potencia estadistica: con 19 eventos, solo se detectarian HR >= 3,62 con 80% de potencia (HR = 2,0: potencia 33%).

En el unico modelo multivariable publicado (Strong Treat, n = 310), la edad, los eosinofilos > 400/uL y la ausencia de rash cutaneo fueron predictores significativos de aclaramiento serologico; crucialmente, la IgG basal no fue incluida como covariable en ese modelo.
`[CITE: buonfrate2019]`

Nuestro estudio es el primero en evaluar explicitamente la IgG basal como predictor de velocidad de seronegativizacion (HR univariable 0,19, p crudo 0,004): una mayor carga de anticuerpos requiere mas tiempo para descender por debajo del umbral. La mecanistica subyacente podria involucrar celulas plasmaticas de vida larga, cuya proporcion aumenta con la exposicion repetida, como se ha demostrado en Chagas y malaria.
`[CITE: cesar2023; yman2019]`

En Strong Treat, los eosinofilos > 400/uL fueron predictores independientes de aclaramiento, pero ese modelo no controlo por IgG basal; nuestro estudio incluye ambas variables simultaneamente. Nuestra eosinofilia basal mostro tendencia en la misma direccion (HR 0,40, p crudo 0,027) pero no alcanzo significacion tras correccion.
`[CITE: buonfrate2019]`

La funcion directamente helmintotoxica de los eosinofilos (degranulacion de proteinas cationicas y peroxidasa) es un mecanismo biologicamente plausible, pero su normalizacion rapida post-tratamiento (789 a 371 cel/uL al dia 17) limita su utilidad como marcador de cura a largo plazo.
`[CITE: mitre2021; buonfrate2019; repetto2018]`

El sexo masculino se asocio con seronegativizacion mas rapida (HR 3,29), resultado consistente con la evidencia de que la respuesta al tratamiento de estrongiloidiasis no se ve afectada por el sexo ni el origen geografico.
`[CITE: salvador2020]`

### 4.3 Efecto del sexo

La violacion de proporcionalidad (Schoenfeld p = 0,007) indica efecto no constante en el tiempo: el sexo afecta de forma diferente la seronegativizacion en los primeros meses que en el seguimiento tardio.

El LMM con interaccion no detecto diferencia significativa en la pendiente de descenso (beta interaccion = --0,013, p = 0,501; pendiente varones --0,045/mes, mujeres --0,033/mes), sugiriendo que la diferencia puede estar en el *timing* (efecto precoz) mas que en la velocidad sostenida de descenso.

Este resultado nulo en la interaccion es coherente con la evidencia externa: Salvador et al. demostraron que la respuesta al tratamiento de estrongiloidiasis no se ve afectada por el sexo ni el origen geografico en cohortes europeas.
`[CITE: salvador2020]`

No obstante, datos experimentales sugieren que los corticosteroides afectan la magnitud de la respuesta de anticuerpos pero no su maduracion (avidez), lo que podria ser relevante para el subgrupo inmunodeprimido, aunque nuestro n es insuficiente para analizar esta interaccion.
`[CITE: goncalves2026]`

Con n = 15 + 19, la potencia para detectar una interaccion moderada es insuficiente; se necesitarian cohortes > 100 para cuantificar diferencias sutiles de pendiente por sexo.

### 4.4 Trayectoria parametrica

Nuestro LMM reporta por primera vez la pendiente de descenso de IgG post-ivermectina: --0,068 log(IgG)/mes (p < 0,001). Buonfrate et al. aplicaron un LMM con edad y tiempo como predictores a cinco assays serologicos, pero reportaron solo la tendencia cualitativa ("trend to seroreversion over time"), sin publicar los coeficientes de regresion.
`[CITE: buonfrate2015]`

La concordancia LMM (10,9 meses) vs KM (8,8 meses) valida mutuamente ambos enfoques: la diferencia de 2 meses refleja los supuestos (descenso log-lineal sostenido vs no parametrico).

La estimacion del LMM es mas conservadora por asumir descenso log-lineal constante, mientras que el KM refleja descensos rapidos precoces.

El R2 condicional de 0,563 indica que los efectos aleatorios (variabilidad inter-paciente) capturan variabilidad sustancial; el 44% restante refleja variabilidad intra-paciente y error de medicion.

En otras infecciones parasitarias, la cinetica de anticuerpos se ha modelizado como bifasica: ASC de vida corta (vida media 2--10 dias) y ASC de vida larga (vida media 1,8--3,7 anos), con la proporcion de ASC de vida larga aumentando del 10% en infeccion primaria al 10--56% en exposicion repetida. Un modelo bifasico podria capturar mejor la cinetica de IgG en estrongiloidiasis si existiera un plateau residual tardio, pero nuestros datos no permiten distinguir entre descenso monofasico y bifasico.
`[CITE: yman2019]`

En leptospirosis, Owers Bonner et al. estimaron una constante de decaimiento de 0,926 diluciones de titulo/mes utilizando modelizacion exponencial con correccion de censura por intervalo, proporcionando un marco metodologico aplicable a estudios futuros en estrongiloidiasis.
`[CITE: owersbonner2021]`

La utilidad clinica: dado un valor basal de IgG, estimar cuando alcanzara el umbral de negativizacion, informando al clinico del plazo esperado de seguimiento.

### 4.5 Limitaciones

1. **Retrospectivo unicentrico**: no permite inferencia causal ni generalizacion directa; la cohorte es comparable a series europeas (edad, sexo, procedencia), pero la generalizacion a otras regiones o etnias requiere cautela.
`[CITE: salvador2019 REDIVI]`
2. **Tamano muestral** (n = 44, 19 eventos multivariable): potencia insuficiente para HR < 3,6; Strong Treat (n = 310) detecto predictores que nuestro estudio no puede replicar.
`[CITE: buonfrate2019; schoenfeld1983]`
3. **Censura informativa posible**: perdida de seguimiento no necesariamente aleatoria.
4. **T0 = primera dosis**: en multiples ciclos, el tiempo desde ultima dosis difiere; no obstante, Strong Treat demostro equivalencia entre dosis unica y multiple, minimizando este sesgo.
`[CITE: buonfrate2019]`
5. **Ventana basal variable**: mediana 18d pero IQR hasta 62d; sensibilidad <= 90d consistente (7,9 vs 8,8m).
6. **Censura por intervalo**: cruce del umbral entre visitas; mediana KM conservadora.
7. **Caso completo**: 18% sin IgG basal; MCAR no significativo (p = 0,11) pero no excluye MAR.
`[CITE: little1988]`
8. **Assay-specificity**: la tasa de seronegativizacion depende del assay utilizado (IVD ~90% descenso relevante, NIE 72,5% negativizacion completa, Strongy Detect permanece positivo > 1 ano); nuestros resultados son especificos al kit empleado.
`[CITE: buonfrate2015; sears2022]`
9. **Seronegativizacion =/= cura parasitologica**: Repetto et al. detectaron ADN de *S. stercoralis* por PCR en el 100% de pacientes a 4 anos, incluso con serologia negativa; la seronegativizacion mide descenso de anticuerpos, no eliminacion parasitaria.
`[CITE: repetto2018]`
10. **Modelo no bifasico**: el LMM asume descenso log-lineal; un modelo bifasico (ASC corta + larga vida) podria ajustar mejor la cinetica si existe plateau residual, pero nuestros datos no permiten discriminar ambos modelos.
`[CITE: yman2019]`
11. **Inmunodepresion**: Strong Treat excluyo pacientes inmunodeprimidos; nuestra cohorte incluye 4 (9%), un n insuficiente para analizar su efecto sobre la cinetica serologica. La sensibilidad serologica en inmunodeprimidos es inferior (~70%).
`[CITE: buonfrate2019; henriquez2016]`
12. **COVID-19**: posible efecto sobre seguimiento 2020--2021.
13. **Kit ELISA**: posibles cambios de lote. `[? PENDIENTE INPUT USUARIO]`
14. **Riesgos competitivos**: muerte, emigracion no modelados.

### 4.6 Fortalezas

1. **Primera mediana KM con IC** publicada para seronegativizacion post-ivermectina, proporcionando una estimacion cuantitativa directamente utilizable en guias clinicas.
`[CITE: ausencia confirmada -- Q06]`
2. **Primer estudio en evaluar IgG basal como predictor** de velocidad de seronegativizacion, llenando un gap explicitamente identificado en la literatura (variable no incluida en Strong Treat).
`[CITE: buonfrate2019 -- IgG no incluida en modelo]`
3. **Primeros coeficientes parametricos** de descenso mensual de IgG (pendiente LMM --0,068/mes), dato no disponible en la literatura a pesar de que Buonfrate et al. aplicaron LMM.
`[CITE: buonfrate2015]`
4. Seguimiento prolongado (mediana 11,7 meses; 21% >= 24 meses).
5. Triangulacion: KM + landmarks + tasa persona-ano + Cox + LMM (concordancia KM-LMM como validacion interna).
6. Sensibilidad exhaustiva: 8 endpoints, 2 umbrales, ventana basal.
7. Transparencia: STROBE, potencia post-hoc, MCAR, bootstrap, codigo reproducible.

### 4.7 Implicaciones clinicas

Los landmarks sugieren un calendario de seguimiento basado en evidencia: control serologico a 6 meses (36% negativizados), 12 meses (68%) y 18--24 meses para persistentes (76--88%). Este calendario es mas conservador que la recomendacion de Strong Treat ("6 meses pueden ser suficientes") porque utiliza un criterio mas estricto (negativizacion completa vs reduccion relativa).
`[CITE: buonfrate2019]`

Un paciente seropositivo a 12 meses no indica necesariamente fracaso terapeutico: un tercio aun no ha negativizado con criterio absoluto. La persistencia de anticuerpos puede reflejar memoria inmunologica de celulas plasmaticas de vida larga, no infeccion activa.
`[CITE: cesar2023; yman2019]`

Sin embargo, debe considerarse que la seronegativizacion no es sinonimo de cura parasitologica: Repetto et al. demostraron persistencia parasitaria incluso tras negativizacion serologica.
`[CITE: repetto2018]`

En pacientes que requieren inmunodepresion, el tratamiento debe administrarse antes de iniciar la terapia inmunosupresora, incluso si ya recibieron ivermectina previamente, dado el riesgo de sindrome de hiperinfeccion con mortalidad > 60%.
`[CITE: lo2025; buonfrate2023]`

La IgG basal alta podria identificar pacientes con seronegativizacion esperable mas lenta, aunque no alcanzo significacion en nuestra cohorte; la pendiente del LMM (--0,068/mes) permite estimar el tiempo individual esperado hasta negativizacion: un paciente con IgG basal de 6,0 requeriria ~26 meses (log(6,0)/0,068), frente a ~10 meses con IgG de 2,0.

---

## 5. CONCLUSION

En esta cohorte retrospectiva unicentrica de 44 pacientes tratados con ivermectina por estrongiloidiasis, la mediana de seronegativizacion (IgG-ELISA < 1,1) fue 8,8 meses (IC 95% 4,3--11,4), con landmarks de 36%, 68%, 76% y 88% a 6, 12, 18 y 24 meses respectivamente.
`[DATA]`

Ninguna variable basal alcanzo significacion como predictor de velocidad de seronegativizacion tras correccion por multiplicidad (BH-FDR), si bien el estudio tiene potencia solo para HR >= 3,62.
`[DATA]`

La IgG basal, evaluada por primera vez como predictor en esta indicacion, mostro la asociacion cruda mas fuerte (HR 0,19) sin alcanzar significacion ajustada; la ausencia de este predictor en el modelo de Strong Treat justifica su evaluacion en cohortes mayores.
`[DATA; CITE: buonfrate2019]`

El modelo lineal mixto estimo una pendiente de descenso de --0,068 log(IgG)/mes (R2 condicional 0,563), el primer coeficiente parametrico publicado para esta cinetica.
`[DATA; CITE: buonfrate2015 -- no reporto coeficientes]`

Propuesta clinica: seguimiento serologico a 6, 12 y 18--24 meses, con criterio de alta basado en seronegativizacion completa o descenso relativo sostenido; los pacientes con IgG basal alta deben anticipar seguimiento mas prolongado. Un paciente seropositivo a 12 meses no indica fracaso terapeutico: un tercio persiste seropositivo dentro de la cinetica esperada.

Se necesitan estudios multicentricos con mayor potencia (n >= 150, >= 80 eventos) para confirmar o descartar la IgG basal como predictor, evaluar el efecto de la inmunodepresion y validar modelos parametricos de descenso que informen la duracion optima del seguimiento.

### Metricas de revision
- [x] 200--300 palabras: ~230 palabras
- [x] Sin informacion nueva: cada frase presente en Results o Discussion
- [x] Cada frase respaldada por Results

---

## FIGURES (definitivas)

| # | Contenido | Seccion | Status |
|:---:|:---|:---:|:---:|
| 1 | Diagrama STROBE | Methods | En Selecto.qmd |
| 2 | KM endpoint primario + at-risk | 3.3 | En Selecto.qmd |
| 3 | KM estratificado 5 variables | 3.5 | En Selecto.qmd |
| 4 | Forest plot univariable | 3.6 | En Selecto.qmd |
| 5 | Forest plot multi + KM combinacion | 3.7 | En Selecto.qmd |
| 6 | LMM spaghetti + regresion | 3.8 | En Selecto.qmd |
| 7 | LMM x sexo bicolor | 3.9 | En Selecto.qmd |

Supplementary: trayectorias IgG/Eos, descripcion cohorte 4 paneles, correlacion IgG-Eos, sensibilidad 8 endpoints.

## TABLES (definitivas)

| # | Contenido | Seccion | Status |
|:---:|:---|:---:|:---:|
| 1 | Caracteristicas basales (n=44) | 3.1 | En Selecto.qmd |
| 2 | 8 endpoints | 3.4 | En este archivo |
| 3 | Cox multivariable | 3.7 | En este archivo |

Supplementary: definicion covariables, Cox uni tendencia + NS.

---

## BIBLIOGRAPHY: estado tras extraccion OE (2026-04-09)

### En references.bib (32 entradas: 14 originales + 18 de OE)

| # | Ref | Usada en | DOI | Status |
|:---:|:---|:---|:---:|:---:|
| 1 | salvador2014 | Intro, Methods, Disc §5.1 | OK | ✅ |
| 2 | bisoffi2013 | Intro §1.1 | OK | ✅ |
| 3 | requena2013 | Intro | OK | ✅ |
| 4 | peduzzi1996 | Methods | OK | ✅ |
| 5 | schoenfeld1982 | Methods | OK | ✅ |
| 6 | schoenfeld1983 | Methods, Disc §4.2 | OK | ✅ |
| 7 | benjamini1995 | Methods | OK | ✅ |
| 8 | nakagawa2013 | Methods | OK | ✅ |
| 9 | vonelm2007 | Methods | OK | ✅ |
| 10 | buonfrate2015 | Intro, Methods, Disc §5.1/5.4 | OK | ✅ |
| 11 | cox1972 | Methods | OK | ✅ |
| 12 | kaplan1958 | Methods | OK | ✅ |
| 13 | little1988 | Methods, Disc §4.5 | OK | ✅ |
| 14 | rubin1987 | No usada | — | ⚠ Evaluar eliminar |
| 15 | **buonfrate2019** | Intro, Methods, Disc §5.1-5.5, Concl | OK | ✅ **CLAVE** |
| 16 | **lo2025** | Intro §1.2, Disc §5.1/5.5/5.7 | OK | ✅ |
| 17 | **repetto2018** | Intro §1.3, Disc §5.1/5.2/5.5 | OK | ✅ |
| 18 | **henriquez2016** | Methods, Disc §5.5 | PENDING | ⚠ Buscar DOI |
| 19 | **asundi2019** | Intro §1.1 | OK | ✅ |
| 20 | **cesar2023** | Intro §1.3, Disc §5.2/5.7 | OK | ✅ |
| 21 | **yman2019** | Intro §1.3, Disc §5.4/5.5 | OK | ✅ |
| 22 | **mitre2021** | Disc §5.2 | PENDING | ⚠ Buscar DOI |
| 23 | **prato2024** | Disc §5.1 | OK | ✅ |
| 24 | **sears2022** | Disc §5.5 | OK | ✅ |
| 25 | **weitzel2024** | Disc §5.5 | OK | ✅ |
| 26 | **goncalves2026** | Disc §5.3 | OK | ✅ |
| 27 | **salvador2019** | Disc §5.1/5.5 | PENDING | ⚠ Buscar DOI REDIVI |
| 28 | **buonfrate2023** | Disc §5.7 | OK | ✅ |
| 29 | **owersbonner2021** | Disc §5.4 | OK | ✅ |
| 30 | **salvador2020** | Disc §5.2/5.3 | PENDING | ⚠ Buscar DOI |
| 31 | **cutfield2024** | Intro §1.1 | PENDING | ⚠ Buscar DOI |
| 32 | **clark2020** | Disc §5.2 | PENDING | ⚠ Buscar DOI |

### Resumen
- **Con DOI verificado**: 25/32 (78%)
- **DOI pendiente (usuario)**: 7 (henriquez2016, mitre2021, salvador2019, salvador2020, cutfield2024, clark2020, rubin1987)
- **Objetivo**: ≥ 28 con DOI = criterio E5

### Busqueda pendiente residual (usuario)

**Aun no cubiertas por OE**:
- [ ] Prevalencia global *S. stercoralis* actualizada (Schar 2013 PLoS NTD)
- [ ] Sensibilidad baja coproscopia (Requena-Mendez 2017)
- [ ] Dimorfismo sexual respuesta inmune (Klein & Flanagan 2016 Nat Rev Immunol)
- [ ] Greenwood 1926 o referencia estandar IC mediana KM
- [ ] DOIs de 6 referencias marcadas PENDING arriba
