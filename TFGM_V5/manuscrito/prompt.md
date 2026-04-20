# Prompt — Manuscrito TFG · v0.2 (2026-04-20)

Driver doc. Split en **Activas** (accionables) / **Pasivas** (invariantes) / **SWOT++** / **Auditoría**. Versión viva — refactorizar al cierre de cada iteración.

---

## 0. Meta

- **Idioma operativo:** castellano.
- **Working dir:** `/manuscrito` (solo contenido; **PROHIBIDO código Python/scripts aquí** — vive en `/code`).
- **Figuras:** duplicadas en `/manuscrito/figuras/` como espejo de `/figures/` raíz (las de `Resultados.qmd` son las buenas; facilita drag-and-drop a Google Docs sin tocar raíz).
- **Output final:** `.DOCX` formateado según normativa UAH, ensamblado en Google Docs.
- **Normativa:** UAH Medicina (landing page, sin requisitos detallados expuestos): https://medicinaycienciasdelasalud.uah.es/es/estudiantes/trabajo-fin-de-grado/ — **visitada 2026-04-20**; requisitos granulares en §2.1 (dump manual usuario).
- **Referencias:** Vancouver (http://www.icmje.org/), Index Medicus (http://www.ncbi.nlm.nih.gov/entrez/jrbrowser.cgi).
- **Bibliografía driver:** `manuscrito/preguntas_opev.md` (15 Q, todas EXTRACCIÓN ✅; refs por-pregunta listas para consolidar).
- **Modelo:** Sonnet ejecuta. Opus revisa/planifica. Ver §1.7 criterios STOP.

Leyenda: `[ ]` pendiente · `[→]` en curso · `[x]` hecho · `[!]` bloqueado · `[?]` validar.

---

## 1. ACTIVAS — ejecutar secuencialmente

### 1.1 Setup (iteración 0)

- [x] `/manuscrito` como working dir.
- [x] `prompt.md` split Activas/Pasivas.
- [x] Verificar `CLAUDE.md` vs codebase.
- [x] WebFetch URL UAH — landing page, sin detalles técnicos; requisitos en §2.1 conservan dump manual inicial.
- [x] Definir criterios STOP Sonnet→Opus (§1.7).
- [x] Estrategia no-regresión: **opción (b)** — comentarios in-place + diff justificado, trabajar sobre deltas (§1.8).
- [x] Glyph μ: corregido en preámbulo LaTeX (`\usepackage[utf8]{inputenc}` + `\DeclareUnicodeCharacter{00B5}{\textmu}`; o `\usepackage{textgreek}` + macro `\um{}`). Aplicado en `main.qmd`.

### 1.2 Arquitectura del manuscrito

- [ ] Crear `/manuscrito/secciones/` con un `.qmd` por apartado:
  - `00_portada.qmd` (ANEXO II/III UAH).
  - `01_titulo_autor_keywords.qmd` (ES + EN, 6–10 keywords).
  - `02_resumen.qmd` (≤250 palabras, ES + EN).
  - `03_abreviaturas.qmd` (glosario; zero-tolerance con §2.3).
  - `04_introduccion.qmd` (≤20 %).
  - `05_metodos.qmd` (≤30 %).
  - `06_resultados.qmd` (≤30 % excl. tablas/figuras).
  - `07_discusion.qmd` (≤30 %).
  - `08_conclusiones.qmd` (narrativa).
  - `09_bibliografia.qmd` (render desde CSL JSON).
  - `10_agradecimientos.qmd`.
  - `99_assignment_estudiante.qmd` (valor docente; eliminar en rama `journal/`).
- [ ] `/manuscrito/main.qmd` ensamblador con YAML → PDF (líneas numeradas `\usepackage{lineno}`, `versión+fecha` en header, A4, 1.5 interlineado, TNR 12).
- [ ] Preámbulo LaTeX fijo: `textgreek`, `lineno`, `booktabs`, `longtable`, `setspace`, `geometry`, `fancyhdr`, `csquotes`. Declarar `\DeclareUnicodeCharacter{00B5}{\textmu}`.
- [ ] Validar render a PDF **antes** de escribir contenido.

### 1.3 Figuras compartidas

- [ ] `/manuscrito/figuras/` con copia (no symlink, para Drive sync) de `figures/fig-b{1..5}-*.png` + `figures/tab-*.md`. Mantener nomenclatura.
- [ ] Script one-liner `bash make_figs.sh` para resyncar cuando `Resultados.qmd` regenere figuras.

### 1.4 Escritura (línea a línea)

- [ ] Escribir cada sección **línea por línea** en su `.qmd` (una idea = una línea).
- [ ] Cada línea con marcador bibliográfico: `[CITE?]` / `[CITED:citekey]` / `[NO_CITE]`.
- [ ] Tras N líneas validadas → integrar a párrafos en bloque final (preservar líneas fuente comentadas arriba para trazabilidad).

### 1.5 Bibliografía — integración `preguntas_opev.md`

- [ ] Parsear las 15 Q (Q01–Q15) de `preguntas_opev.md` → extraer tabla de referencias por pregunta.
- [ ] Consolidar en `manuscrito/references.json` (CSL JSON exportado desde Zotero).
- [ ] Citekeys Better BibTeX: fórmula candidata `auth.lower + shorttitle(3,3) + year` — [?] validar vs `auth + year + journal3`.
- [ ] Mapear cada cita a sección (S1–S14 → `04_introduccion`/`05_metodos`/… según `preguntas_opev.md`).
- [ ] Ciclo **búsqueda → ampliación → validación manual** documentado en `manuscrito/bibliografia_log.md`.
- [ ] Actualizar estado `⬜ PENDIENTE` → `✅ COMPLETADO` en `preguntas_opev.md` cuando Q quede anclada al texto.
- [ ] **Anti-plagio:** parafrasear siempre; citar fuentes originales, **NUNCA** a Open Evidence.

### 1.6 Correcciones Resultados.qmd → PDF

- [x] Glyph μ roto → fix en preámbulo (§1.1).
- [ ] Microorganismos en **cursiva** (todo el trabajo): `*S. stercoralis*`, `*Strongyloides*`, etc.
- [ ] Unidades ivermectina: **200 μg/kg** (microgramos, estándar clínico = 0,2 mg/kg). Verificar render final.
- [ ] Mover a Material y Métodos (hoy en Resultados):
  - "Se realizó un estudio observacional retrospectivo (2015–2025)… seguimiento 3/6/12/18/24 meses."
  - "El criterio de valoración primario fue la seronegativización absoluta (IgG-ELISA < 1,1)."
  - "Se emplearon Cox + LMM asumiendo cinética de primer orden."
- [ ] Fig 1 STROBE: "CNM (microbiología, 2017–2023)" incorrecto → CNM solo serología; HCD también diagnosticó por cultivo 2017–2020. Corregir etiqueta + verificar n.
- [ ] Abreviaturas definidas en 1ª aparición: `BH–FDR` (Tabla 2), `(B-D)` (Fig 3); auditar todas.

### 1.7 Criterios STOP Sonnet → Opus (switch manual)

**Recordatorio al usuario:** cuando observes cualquiera de estos triggers → detén a Sonnet y cambia a Opus para planificación/revisión.

| # | Trigger | Por qué |
|---|---------|---------|
| T1 | Cambio toca ≥2 secciones del manuscrito simultáneamente | Riesgo inconsistencia global |
| T2 | Trade-off metodológico sin precedente claro (p. ej. elegir entre 2 análisis estadísticos) | Decisión arquitectónica |
| T3 | Ambigüedad irreducible en interpretación de datos | Necesita razonamiento profundo |
| T4 | Word count de sección ±10 % de su tope UAH | Balance global entre secciones |
| T5 | Refactor de `main.qmd`, pipeline, preámbulo LaTeX o estructura de archivos | Decisión estructural |
| T6 | Decisión bibliográfica con ≥2 candidatos de peso equivalente | Priorización editorial |
| T7 | Conflicto con normativa UAH (formato, distribución %, portada) | Cumplimiento |
| T8 | Revisión de **coherencia global** (integración entre secciones) | Lectura holística |
| T9 | Validación de resultados estadísticos antes de redacción final | Integridad del hallazgo |
| T10 | Switch entre rama TFG y `journal/` (scope cambia) | Decisión estratégica |
| T11 | Auditoría programada (ver §4) | Rol auditor independiente |
| T12 | Sonnet entra en bucle o contradice iteración previa | Meta-decisión |

### 1.8 Estrategia no-regresión (opción b, elegida)

- Todo cambio sobre texto ya validado = **comentario in-place + diff** en el `.qmd` de la sección.
- Formato estándar de comentario:

```markdown
<!-- REV v0.X 2026-MM-DD [origen: Opus|Sonnet|Usuario]
DELTA:
  - [antes] Línea N: "…"
  - [después] Línea N: "…"
JUSTIFICACIÓN: …
IMPACTO: [sección afectada · word-count · citas tocadas]
-->
```

- Texto validado va **encima** del bloque de comentarios; auditor lee el comentario para reconstruir evolución.
- Consolidación de comentarios en `auditorias/` cada cierre de iteración (mover histórico, dejar solo comentarios activos de la versión en curso).
- Nada se reescribe silenciosamente. Si el delta es trivial (typo), se marca `DELTA: trivial` sin justificación larga.

### 1.9 Cierre de iteración (ritual obligatorio)

- [ ] Actualizar `CLAUDE.md` con cambios arquitectónicos.
- [ ] Refactorizar `prompt.md` (esta sección).
- [ ] Consolidar comentarios `<!-- REV -->` → `manuscrito/auditorias/YYYY-MM-DD_vN.md`.
- [ ] Verificar §2 invariantes.
- [ ] Ejecutar auditoría §4 (semáforo por sección).

---

## 2. PASIVAS — invariantes (verificar cada iteración)

### 2.1 Normativa UAH (palabras + formato)

- **Palabras:** 5 000–10 000 (excluye título, resumen, tablas, figuras, bibliografía, agradecimientos).
- **Distribución máxima:** Intro+Obj ≤20 % · MyM ≤30 % · Resultados ≤30 % (excl. T/F) · Discusión ≤30 %.
- **Formato:** A4, interlineado 1,5, TNR 12, páginas numeradas, encuadernación espiral.
- **Portada:** ANEXO (III según doc original, II según nombre de archivo `Anexo-II.-Portada-TI-TFGM.pdf`) — [?] confirmar cuál aplica.
- **Bilingüe:** título, resumen ≤250 palabras, 6–10 keywords en ES + EN.
- **Orden secciones:** Título+autor → Resumen → Abreviaturas → Intro+Obj → MyM → Resultados → Discusión → Conclusiones → Bibliografía → Agradecimientos.
- **Conclusiones ≠ resumen de resultados** — narrativa conceptual.

### 2.2 Vancouver (referencias)

- Numeración correlativa en **superíndice**, orden de aparición.
- Revistas abreviadas según Index Medicus.
- Prohibido: "observaciones no publicadas", "comunicación personal".
- Permitido: "En prensa".
- Citas verificadas sobre artículos originales (nunca sobre OE).

### 2.3 Estilo técnico (zero-tolerance)

- Microorganismos en **cursiva** siempre.
- Unidades explícitas (μg vs mg, ×10³/µL, IC 95 %, IQR, HR).
- Abreviaturas definidas en 1ª aparición; nota explicativa al pie de tabla.
- Medidas estadísticas identificadas.
- Sin typos, lenguaje conciso.

### 2.4 Ingeniería del documento

- Tablas en **markdown** (Google Docs no parsea LaTeX).
- Un `.qmd` por apartado + `main.qmd` ensamblador.
- Líneas numeradas + versión+fecha en footer PDF.
- Cambios sobre texto validado = protocolo §1.8.
- `/manuscrito` sin código Python.

### 2.5 Operación Sonnet/Opus

- Sonnet: tareas granulares.
- Opus: planificación, revisión general, arbitraje.
- Disparadores de switch en §1.7.
- Decisiones de Opus se registran como `<!-- REV … origen: Opus -->`.

### 2.6 Iteración

- Kanban WIP = 1 Activa por vez (salvo dependencias paralelas explícitas).
- Paso a paso, sin adelantar.
- Criterios + y – validados.
- Refactor `prompt.md` + `CLAUDE.md` al cierre.

---

## 3. SWOT++ (profundizado) — requiere aprobación punto por punto

### 3.1 Fortalezas a amplificar (S)

- **Dataset propio ya curado** (n=44, BASE_EXCEL.xlsx con 5 hojas). Reproducible desde `_data.py`.
- **15 Q de Open Evidence completadas** → base bibliográfica preempaquetada con refs numeradas.
- **Figuras de calidad ya renderizadas** (`fig-b2-km-baseline`, `fig-b3-predictors`, `fig-b4-lmm`, `fig-b5-swimmer`…) → `/manuscrito/figuras/` las pone a mano.
- **STROBE checklist** en `materiales/STROBE_checklist.csv` → autoría auditable.
- **MCP `code-review-graph`** + skills `caveman-*` → infra de revisión disponible.
- **Draft previo** (`archivo/Selecto.qmd`, `archivo/manuscrito.qmd`) → material residual aprovechable (con cuidado: outdated).

### 3.2 Debilidades a mitigar (W) — **incluye ocultas**

Visibles:
- Encoding μ → fijado en preámbulo (§1.1).
- Ambigüedad de revisiones → protocolo §1.8.
- Riesgo de tocar texto validado → protocolo §1.8.

**Ocultas (nuevas):**
- **Sesgo de familiaridad del autor** con los datos → puede sobre-interpretar hallazgos marginales. Mitigación: auditor independiente §4.
- **Cherry-picking** implícito (memoria ya registra: "no cherry-picking, pilot framing"). Mitigación: la auditoría revisa `stats_b2.py` y compara hallazgos reportados vs no-reportados; cualquier HR omitido justificado en `.qmd` correspondiente.
- **Coherencia temporal de citas** — `preguntas_opev.md` contiene refs con años 2025-2026; verificar que DOI resuelve y la revista está indexada. Posible alucinación OE.
- **Pérdida de contexto entre iteraciones** si `prompt.md` decae sin refactorizar → ritual §1.9 obliga.
- **Fragilidad de citekeys** si Zotero se reordena → congelar export `references.json` con hash + fecha en header.
- **Dependencia de Open Evidence** (si baja o cambia formato) → archivar `preguntas_opev.md` como verdad congelada; nuevas preguntas en `preguntas_opev_vN.md`.
- **Reproducibilidad externa** — un evaluador sin acceso al repo necesita PDF autocontenido; añadir apéndice con métodos+código en `99_assignment_estudiante.qmd` + DOI del repo si se publica.
- **Traducción ES↔EN** del resumen/keywords = trampa tardía; preparar glosario terminológico desde el inicio.
- **Acoplamiento oculto** entre secciones (p. ej. word count de Discusión crece y canibaliza de Intro). Mitigación: métrica viva en §4.
- **Deriva entre `Resultados.qmd` y `06_resultados.qmd`** del manuscrito → checksum de figuras + stats extraídos auto desde `stats_b2.py`.

### 3.3 Oportunidades a explotar (O)

- **Line numbering + versión+fecha** en PDF desde día 1 (revisor lo agradece).
- **ROI por línea:** columna "valor incremental" (novedad vs evidencia confirmatoria) al lado de `[CITE?]`.
- **Pre-commit hook** `check.sh`: (i) microorganismos sin cursiva, (ii) abreviaturas no definidas, (iii) word count por sección, (iv) `[CITED:]` existe en `references.json`. Rompe build si falla.
- **Versión TFG vs journal** como git branches: `main` = TFG, `journal/xxx` = submisión. Cherry-pick selectivo al submitir.
- **Auditor agent** (§4) → revisión independiente semiautomatizada.
- **Skill `caveman-compress`** para comprimir prompt.md/CLAUDE.md al cierre (reducir tokens).
- **Skill `simplify`** en cada `.qmd` antes de cerrar iteración.

### 3.4 Amenazas a vigilar (T) — **incluye ocultas**

Visibles:
- Drift word count → métrica viva §4.
- Citas rotas → check.sh.
- Scope creep hacia journal prematuro → rama `journal/` congelada hasta que `main` pase normativa.
- Fatiga de revisión línea a línea → tope ~40 líneas/día.

**Ocultas (nuevas):**
- **Cambio de normativa UAH** sin aviso → congelar snapshot del landing UAH en `manuscrito/normativa_uah_snapshot_2026-04-20.md`; revisar mensualmente.
- **Plagio involuntario** por copy-paste de respuestas OE → obligación de parafraseo + check con TurnItIn local antes de entrega.
- **Similitud TurnItIn** con respuestas OE publicadas (OE es LLM, pero las citas son de papers públicos) → parafrasear, citar a **fuente original** nunca a OE.
- **Actualización de datos** (nuevos pacientes post-cutoff) invalida resultados → fijar `DATA_CUTOFF = 2026-04-12` en CLAUDE.md; cualquier dato nuevo = nueva iteración completa.
- **Typo en citekey** → cita rota silenciosa en PDF → check.sh detecta en compile.
- **Defensa oral:** tribunal no tiene repo; PDF debe ser autocontenido → apéndice técnico en `99_assignment_estudiante.qmd`.
- **Conflicto de versión Sonnet vs Opus** (decisiones tomadas por Opus no reproducibles por Sonnet) → cada decisión de Opus en `<!-- REV … origen: Opus -->` con justificación full.
- **Fallo de renderizado tardío** (LaTeX/Quarto rompe por paquete exótico) → lockfile de LaTeX en repo (`manuscrito/latex.lock`) o fijar contenedor `texlive-2023`.
- **Pérdida del `references.json`** sin backup → commit a git cada vez que se modifique.
- **Colisión de idioma** (párrafos mezclando ES/EN por copy-paste de OE) → linter específico en check.sh.
- **Confusión de modelo estadístico** (Cox vs LMM interpretación) → Opus debe revisar MyM antes de Resultados.
- **Fecha de entrega desconocida** por Claude → pedir al usuario y registrar como constante en CLAUDE.md.
- **Inconsistencia entre figura y texto** (p. ej. número de n reportado en Fig 1 ≠ texto) → auditoría cruzada por sección.

---

## 4. AUDITORÍA — agente auditor independiente

### 4.1 Rol

Agente separado (subagent_type: `general-purpose` o `Explore`), invocado **solo al cierre de iteración** o tras trigger T11. **No edita**, solo produce reporte en `manuscrito/auditorias/YYYY-MM-DD_vN.md`.

### 4.2 Rúbrica (7 dimensiones × 5 niveles)

| # | Dimensión | 1 (rojo) | 3 (amarillo) | 5 (verde) |
|---|-----------|----------|--------------|-----------|
| D1 | **Completitud** | falta sección obligatoria | sección presente, bajo tope word count | todas las secciones, distribución UAH OK |
| D2 | **Corrección técnica** | unidades/cursivas/abreviaturas mal | errores puntuales | zero-tolerance §2.3 pasado |
| D3 | **Integridad bibliográfica** | citas rotas | `[CITE?]` residuales | 100 % citas resueltas, Vancouver OK |
| D4 | **Coherencia interna** | figura no citada, abreviatura inconsistente | desajustes puntuales | figura-texto-tabla alineados |
| D5 | **Alineación normativa UAH** | formato incumple | tolerancia ±10 % | conforme §2.1 |
| D6 | **Calidad discursiva** | jerga, lógica rota | claro pero denso | conciso, lógica argumental clara |
| D7 | **Reproducibilidad** | métodos opacos | STROBE parcial | STROBE completo, data cutoff explícito |

Score por sección = promedio D1–D7 × peso sección (Intro 0.15, MyM 0.20, Resultados 0.25, Discusión 0.25, otros 0.15).

### 4.3 Semáforo por sección

- 🟢 ≥ 4.0 · 🟡 2.5–3.9 · 🔴 < 2.5
- Reportar diff vs auditoría previa (progreso / regresión).

### 4.4 Reporte auditoría (plantilla)

```markdown
# Auditoría vN — YYYY-MM-DD

## Resumen
- Score global: X.X
- Semáforo: 🟢/🟡/🔴
- Delta vs vN-1: +/−X.X

## Por sección
| Sección | D1 | D2 | D3 | D4 | D5 | D6 | D7 | Score | Semáforo |
|---|---|---|---|---|---|---|---|---|---|
| Intro | ... | ... | ... | ... | ... | ... | ... | ... | 🟢 |

## Hallazgos priorizados
- **P0 (bloqueante):** …
- **P1 (crítico):** …
- **P2 (menor):** …

## Recomendaciones para próxima iteración
- …
```

### 4.5 Métricas objetivas (auto, no requieren auditor)

| Métrica | Umbral | Script |
|---|---|---|
| Word count total | 5 000–10 000 | `wc -w` sobre secciones |
| Ratio Intro/MyM/Res/Disc | ≤20/30/30/30 % | `tools/wc_por_seccion.sh` |
| Citas resueltas | 100 % | `tools/check_citas.py` (match `[CITED:]` vs `references.json`) |
| DOI/PMID válidos | 100 % | `tools/check_dois.py` (http 200 en cada URL) |
| Abreviaturas definidas | 100 % | `tools/check_abrev.py` (grep vs `03_abreviaturas.qmd`) |
| Microorganismos cursivados | 100 % | `tools/check_cursivas.py` (lista negra sin `*…*`) |
| Render PDF warnings | 0 | `quarto render --verbose` exit 0 |
| `[CITED:]` ratio Intro+Disc | ≥ 90 % | grep / total líneas |
| Deriva Resultados.qmd vs 06_resultados.qmd | stats consistentes | `tools/verify_stats.py` (extrae HR/median/n de ambos) |

Scripts viven en `/tools/` (NO en `/manuscrito`, por §0).

---

## 5. Historial de iteraciones

- **v0.1 (2026-04-20)** — Split Activas/Pasivas, SWOT básico, métricas mínimas.
- **v0.2 (2026-04-20)** — + criterios STOP Opus (T1–T12), no-regresión (b) formalizada, glyph μ fix, no-code en `/manuscrito`, figuras espejo, SWOT profundizado (W/T ocultas), auditor agent + rúbrica 7D, métricas objetivas con scripts, integración `preguntas_opev.md` al roadmap bibliográfico.

---

## 6. Estado de `preguntas_opev.md`

| # | Tema | Sección destino | EXTRACCIÓN | Anclada en texto |
|---|------|------------------|------------|------------------|
| Q01 | Representatividad cohorte | Intro §Antecedentes / Disc §Generalización | ✅ | ⬜ |
| Q02 | Epidemiología sexo/origen | Intro / Disc §Sesgo | ✅ | ⬜ |
| Q03 | Inmunosupresión y curación | Intro / Disc §Predictores | ✅ | ⬜ |
| Q04 | Régimen IVM y curación | Intro / Disc §Tratamiento | ✅ | ⬜ |
| Q05 | Correlación IgG-eosinófilos | Resultados §Baseline | ✅ | ⬜ |
| Q06 | Cinética IgG post-TTO (CORE) | Resultados §KM + Disc §Comparativa | ✅ | ⬜ |
| Q07 | Normalización eosinófilos | Resultados §Eos | ✅ | ⬜ |
| Q08 | Definiciones curación serológica | MyM §Endpoints + Disc §Umbrales | ✅ | ⬜ |
| Q09 | Predictores tiempo seronegativización | Resultados §Cox + Disc §Predictores | ✅ | ⬜ |
| Q10 | IgG basal como predictor (HALLAZGO) | Resultados §Cox + Disc §Principal | ✅ | ⬜ |
| Q11 | Eosinofilia basal como predictor | Resultados §Cox + Disc §Secundario | ✅ | ⬜ |
| Q12 | Tasa descenso paramétrica | Resultados §LMM + Disc §Half-life | ✅ | ⬜ |
| Q13 | Protocolo seguimiento post-TTO | Disc §Clínica + Conclusiones | ✅ | ⬜ |
| Q14 | Recidiva y reinfección | Resultados §Persistencia + Disc §Monitoreo | ✅ | ⬜ |
| Q15 | ELISA vs otros métodos | MyM §Diagnóstico + Disc §Limitaciones | ✅ | ⬜ |

**Acción:** cuando una Q quede anclada en texto con su citekey → marcar `⬜ → ✅`.
