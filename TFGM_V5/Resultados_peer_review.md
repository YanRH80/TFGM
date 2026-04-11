# Resultados para peer-review

## 1. Alcance del documento

Este documento presenta exclusivamente resultados cuantitativos y trazabilidad metodológica mínima para revisión por pares.

No incluye conclusiones clínicas finales ni discusión interpretativa extensa.

## 2. Población analizada y flujo STROBE

- Registros cribados tras deduplicación: 198.
- Exclusiones: diagnóstico no confirmado (n=114), no tratados con ivermectina (n=20), sin seguimiento post-tratamiento (n=19), diagnóstico fuera del centro (n=1).
- Cohorte final incluida: 44 pacientes.
- Proporción retenida: 22.2% (44/198).

Cohorte clínica basal:
- Edad: mediana 37.5 años (IQR 26.8-49.8).
- Sexo: 19 mujeres (43.2%), 25 varones (56.8%).
- Inmunodepresión: 4/44 (9.1%).
- Comorbilidad relevante: 13/44 (29.5%).
- Eosinofilia >= 0.5 x10^3/uL: 24/42 (57.1%).

Seguimiento:
- Pacientes con al menos una serología post-T0: 39/44.
- Pacientes sin serología post-T0: 5/44.
- Mediana de seguimiento serológico: 11.7 meses (IQR 3.1-22.2; rango 1.1-72.1).

## 3. Calidad de datos y datos faltantes

- Falta de IGG_BASAL cuantitativa: 8/44 (18.2%).
- Test de plausibilidad MCAR (regresión logística): LR p=0.11.
- Interpretación operativa: compatible con MCAR; se mantiene análisis principal por caso completo.
- Análisis de sensibilidad adicional: imputación múltiple MICE (m=20, 10 iteraciones), combinada por reglas de Rubin.

## 4. Endpoint primario: tiempo a seronegativización (IgG < 1.1)

Definición primaria:
- Evento: primera determinación post-T0 con IgG-ELISA < 1.1.
- Método: Kaplan-Meier con censura a la derecha.
- Población evaluable: n=39.

Estimación principal:
- Eventos observados: 27/39 (69.2%).
- Mediana KM: 267 días (8.8 meses).
- IC95% Greenwood: 132-348 días (4.3-11.4 meses).
- Tasa de incidencia: 0.84 seronegativizaciones/persona-año (IC95% Poisson 0.53-1.19), con 32.0 personas-año acumuladas.

Landmarks:
- 6 meses: 36% acumulado seronegativizado.
- 12 meses: 68%.
- 18 meses: 76%.
- 24 meses: 88%.

## 5. Sensibilidad del endpoint (8 definiciones)

| Definición | n | Eventos | % evento | Mediana KM (meses) |
|---|---:|---:|---:|---:|
| Sero abs x1 (IgG < 1.1) | 39 | 27 | 69 | 8.8 |
| Sero abs x2 (IgG < 1.1, confirmada) | 39 | 12 | 31 | 16.4 |
| Sero abs x1 (IgG < 0.9) | 39 | 25 | 64 | 10.8 |
| Sero abs x2 (IgG < 0.9, confirmada) | 39 | 11 | 28 | 25.8 |
| Sero rel x1 (caída >= 40%) | 39 | 26 | 67 | 7.8 |
| Sero rel x2 (caída >= 40%, confirmada) | 39 | 9 | 23 | 29.9 |
| Eosinófilos < 0.5 x10^3/uL | 44 | 44 | 100 | 3.0 |
| Parasitología (2 negativos) | 17 | 7 | 41 | 25.5 |

Resultados de robustez:
- Cambiar umbral de 1.1 a 0.9 modifica de forma limitada la cinética global (8.8 vs 10.8 meses).
- Exigir doble confirmación reduce eventos y desplaza la mediana a tiempos mayores.
- Subcohorte con ventana basal <=90 días: mediana 7.9 meses (consistente con 8.8 meses en cohorte completa).

## 6. Predictores basales: Cox univariable

Se evaluaron 15 covariables candidatas. Se aplicó corrección BH-FDR por comparaciones múltiples.

Asociaciones crudas más fuertes (p<0.05 sin ajustar):

| Variable | n | HR (IC95%) | p crudo | p ajustado (BH-FDR) |
|---|---:|---|---:|---:|
| IgG >= mediana (3.1) | 32 | 0.19 (0.06-0.59) | 0.004 | 0.053 |
| Sexo varón | 39 | 3.29 (1.38-7.81) | 0.007 | 0.053 |
| IgG basal continua | 32 | 0.79 (0.65-0.97) | 0.021 | 0.100 |
| Eosinofilia >= 0.5 | 37 | 0.40 (0.18-0.90) | 0.027 | 0.100 |

Resultado inferencial principal:
- Ninguna covariable alcanza significación tras BH-FDR (p ajustado mínimo 0.053).

## 7. Modelo multivariable de Cox

Especificación:
- Regla de eventos por variable aplicada.
- Modelo con covariables pre-especificadas: IgG >= mediana y eosinofilia >=0.5.
- Sexo modelado por estratificación debido a no proporcionalidad.

Diagnóstico de supuestos:
- Schoenfeld: sexo viola PH (p=0.007 en manuscrito de referencia).
- Schoenfeld: sin evidencia de violación para IgG >= mediana y eosinofilia.
- Correlación IgG-eosinófilos: Spearman rho=0.49 (p=0.003).
- Colinealidad: VIF aceptable.

Estimación multivariable (caso completo n=30; eventos=19):

| Variable | HR (IC95%) | p |
|---|---|---:|
| IgG >= mediana (3.1) | 0.20 (0.03-1.27) | 0.088 |
| Eosinofilia >= 0.5 | 0.63 (0.15-2.62) | 0.526 |
| Sexo varón | Estratificada | - |

Validación:
- C-statistic: 0.676.
- Bootstrap: 952/1000 réplicas exitosas.

Resolución estadística del estudio:
- Potencia post-hoc (Schoenfeld): HR mínimo detectable con 80% potencia = 3.62.
- Potencia para HR=2.0: 33%.
- Potencia para HR=1.5: 14%.

## 8. Dinámica longitudinal IgG: LMM

Población modelada:
- Seropositivos basales (IgG >=1.1): n=34.

Modelo:
- Modelo lineal mixto sobre log(IgG), con efectos aleatorios por paciente.
- Ecuación media: log(IgG)=0.84-0.068*meses.
- Pendiente temporal: -0.068 log(IgG)/mes (p<0.001).

Métricas:
- R2 marginal: 0.426.
- R2 condicional: 0.563.
- Tiempo paramétrico estimado hasta cruce de umbral IgG=1.1: 10.9 meses.

Interacción por sexo:
- Interacción meses*sexo: beta=-0.0128; p=0.501 (no significativa).

## 9. Mini-apéndice metodológico (audit trail)

Supuestos y controles implementados:
- Censura a la derecha en KM con evento definido a primera observación de negativización.
- Corrección por multiplicidad en Cox univariable mediante BH-FDR.
- Diagnóstico de proporcionalidad con Schoenfeld y estratificación cuando procede.
- Evaluación de datos faltantes (MCAR) + sensibilidad por MICE.
- Validación interna de modelo multivariable con bootstrap.

Riesgos de sesgo residuales (declaración técnica):
- Selección retrospectiva con retención 22.2% (posible sesgo de selección).
- Potencia insuficiente para detectar efectos moderados.
- Dependencia del assay serológico y posible variabilidad inter-lote/inter-ensayo.
- Posible censura informativa no cuantificada por causa de pérdida de seguimiento.
- Generalización externa limitada (cohorte unicéntrica).

## 10. Ítems pendientes antes de envío a peer-review

Pendientes críticos:
- Especificar fabricante/modelo/lotes/CV del kit ELISA utilizado.
- Insertar número oficial de aprobación ética.
- Confirmar texto único para p de Schoenfeld de sexo en todos los documentos (evitar discrepancias internas).

Pendientes recomendados:
- Añadir tabla explícita de n-at-risk a 0/6/12/18/24 meses en figura KM principal.
- Añadir tabla compacta de comparación caso completo vs MICE (HR y delta porcentual).
- Verificar consistencia final de R2 condicional entre documentos (usar una única cifra canónica).

## 11. Notas de edición humana

Bloques reservados para redacción humana final:
- Discusión clínica.
- Implicaciones asistenciales.
- Conclusiones.

Este documento queda preparado como base técnica para esas secciones.