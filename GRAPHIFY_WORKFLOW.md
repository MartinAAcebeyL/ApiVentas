# Flujo de Trabajo: Claude + Graphify

## 🎯 ¿Por Qué Graphify?

Sin graphify, para una pregunta como **"¿Dónde se generan los PDFs?"** Claude tendría que:
- ❌ Leer 51 archivos completos
- ❌ Hacer 5-10 búsquedas grep
- ❌ Esperar 30+ segundos
- ❌ Usar tokens innecesarios

Con graphify, Claude:
- ✅ Ejecuta `graphify query "PDF generation"` → 59 nodos relevantes en milisegundos
- ✅ Lee solo archivos clave
- ✅ Responde en segundos
- ✅ Usa ~10% de los tokens

---

## 📋 Comandos Disponibles para Claude

### 1. **Consultas Semánticas** (mejor para preguntas generales)
```bash
graphify query "¿Cómo se genera el PDF de reportes?"
graphify query "¿Dónde se valida el stock?"
graphify query "Flujo de autenticación"
```
**Retorna:** Subgrafo BFS de ~50-100 nodos relevantes  
**Costo:** 0 tokens  
**Uso ideal:** Preguntas abiertas, exploración

---

### 2. **Rutas entre Conceptos** (mejor para entender dependencias)
```bash
graphify path "SaleDetail" "Product"
graphify path "CreateSaleView" "User"
graphify path "Stock" "CreateGraphicReportSalesView"
```
**Retorna:** Camino más corto entre dos nodos + nodos intermedios  
**Costo:** 0 tokens  
**Uso ideal:** "¿Cómo se conectan X y Y?", análisis de impacto

---

### 3. **Explicaciones Focalizadas** (mejor para componentes específicos)
```bash
graphify explain "CreateGraphicReportSalesView"
graphify explain "SaleDetail"
graphify explain "MakePDFReportSaleView"
```
**Retorna:** Nodo + vecinos inmediatos + relaciones  
**Costo:** 0 tokens  
**Uso ideal:** "¿Qué es X?", "¿Qué hace este componente?"

---

### 4. **Análisis de Impacto** (reverso: qué cambios afectan X)
```bash
graphify affected "Sale" --depth 2
graphify affected "Product" --depth 3
```
**Retorna:** Todos los nodos que dependen de X  
**Costo:** 0 tokens  
**Uso ideal:** "¿Qué rompe si cambio Sale?", refactorings

---

### 5. **Actualizar después de Cambios**
```bash
graphify update .
```
**Cuándo:** Después de editar código  
**Costo:** 0 tokens (solo AST, sin LLM)  
**Tiempo:** ~5 segundos  
**Automático:** Los hooks lo harán por ti

---

## 🔗 Cómo Claude Lo Usa Automáticamente

### El Hook PreToolUse

Cuando intentas:
1. **Hacer grep** → Hook intercepta y dice:  
   *"Debes ejecutar `graphify query` primero para orientarte"*

2. **Leer archivos .py/.ts** → Hook intercepta y dice:  
   *"Debes ejecutar `graphify explain/query` antes de leer fuentes"*

### El Flujo Resultante

```
Usuario: "¿Cuál es el impacto de cambiar el modelo Sale?"
    ↓
Claude detecta pregunta sobre arquitectura
    ↓
Hook PreToolUse dispara
    ↓
Claude ejecuta: graphify affected "Sale" --depth 2
    ↓
Obtiene lista de componentes afectados (milisegundos)
    ↓
Solo ENTONCES lee los archivos relevantes
    ↓
Responde con análisis preciso y contextualizado
```

---

## 📊 Ejemplo Real: Análisis de PDF Report

**Usuario pregunta:** *"¿Dónde se genera el PDF de reportes?"*

### Paso 1: Graphify orienta (automático)
```bash
$ graphify query "PDF report generation"
→ 59 nodos encontrados
→ Identifica: MakePDFReportSaleView, XHTML2PDF, Sales Report Template
```

### Paso 2: Claude localiza componentes clave
```
Nodos principales encontrados:
- MakePDFReportSaleView (apps/sales/views.py:127)
- CreateGraphicReportUseCase (apps/sales/usecases/)
- XHTML2PDF, PyPDF (requirements_prod.txt)
- Sales Report HTML Template
```

### Paso 3: Claude profundiza solo en lo relevante
```bash
$ graphify explain "MakePDFReportSaleView"
→ Retorna vecinos, métodos, dependencias
```

### Paso 4: Claude lee archivos específicos
```
Lee: apps/sales/views.py (línea 127)
Lee: apps/sales/usecases/create_graphic_report_usecase.py
Lee: requirements_prod.txt
```

### Paso 5: Claude responde

*"El PDF se genera en `MakePDFReportSaleView` usando:*
- *XHTML2PDF para la generación*
- *PyPDF para manipulación*
- *El template HTML en apps/sales/templates/sales_report.html*
- *Datos agregados por CreateGraphicReportUseCase..."*

---

## 🎮 Casos de Uso Prácticos

### Caso 1: Refactoring
```
User: "Quiero mover SaleDetail a un nuevo módulo. ¿Qué rompo?"
Claude: graphify affected "SaleDetail" --depth 3
Result: 17 componentes afectados (todos listados)
```

### Caso 2: Integración Nueva Feature
```
User: "¿Dónde engancho el nuevo sistema de notificaciones?"
Claude: graphify query "notification, email, webhook"
Result: Caminos semánticos + puntos de integración
```

### Caso 3: Code Review
```
User: "¿Este PR puede causar problemas?"
Claude: graphify path "ModuloA" "ModuloB" + graphify affected
Result: Análisis de impacto automático
```

### Caso 4: Onboarding Nuevo Dev
```
User: "Necesito entender la arquitectura general"
Claude: (lee GRAPH_REPORT.md)
Result: 10 god nodes, 35 comunidades, puntos de entrada claros
```

---

## ⚙️ Configuración Actual

**Instalación:** Completada en `graphify_env/`

**Hooks registrados:** ✅
- PreToolUse en `.claude/settings.json`
- Bash (grep) hook
- Read/Glob (archivos) hook

**CLAUDE.md configurado:** ✅
- Documentación de uso para futuros colaboradores

**Gráfo generado:** ✅
- 179 nodos, 271 relaciones
- 35 comunidades identificadas
- 82% extracción exacta, 18% inferencias semánticas

---

## 🚀 Próximos Pasos

1. **Tú (Developer):** Haz preguntas sobre arquitectura
2. **Claude:** Usa graphify automáticamente antes de buscar archivos
3. **Después de commits:** Claude ejecuta `graphify update` automáticamente
4. **Rinse & repeat:** El grafo siempre está sincronizado

---

## 📚 Referencias

- **Archivos generados:** `graphify-out/`
- **Visualización interactiva:** `graphify-out/graph.html` (abre en navegador)
- **Reporte arquitectura:** `graphify-out/GRAPH_REPORT.md`
- **Grafo JSON:** `graphify-out/graph.json` (consultable)

---

## 🔍 Debugging

Si algo se siente desincronizado:

```bash
# Ver estado actual
source graphify_env/bin/activate
graphify cluster-only .

# Forzar actualización completa
graphify . --backend claude-cli

# Ver el estado de los hooks
cat .claude/settings.json
```
