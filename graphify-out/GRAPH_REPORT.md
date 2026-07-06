# Graph Report - ApiVentas  (2026-07-06)

## Corpus Check
- 86 files · ~43,479 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 879 nodes · 1350 edges · 56 communities (51 shown, 5 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 114 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `61cc2af4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Critique|Critique]]
- [[_COMMUNITY_product.py|product.py]]
- [[_COMMUNITY_CLAUDE|CLAUDE.md]]
- [[_COMMUNITY_Memory Management|Memory Management]]
- [[_COMMUNITY_.__init__|.__init__]]
- [[_COMMUNITY_SKILL|SKILL.md]]
- [[_COMMUNITY_start-server.sh|start-server.sh]]
- [[_COMMUNITY_stop-server.sh|stop-server.sh]]
- [[_COMMUNITY_spec-document-reviewer-prompt|spec-document-reviewer-prompt.md]]

## God Nodes (most connected - your core abstractions)
1. `Product` - 28 edges
2. `User` - 23 edges
3. `Sale` - 21 edges
4. `Base` - 19 edges
5. `Import` - 18 edges
6. `ImportItem` - 18 edges
7. `ImportMetricsUseCase` - 18 edges
8. `Core Principles` - 17 edges
9. `SaleDetail` - 16 edges
10. `Core Craft Principles` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Django Application Service` --references--> `Production Dependencies`  [INFERRED]
  docker-compose.yaml → requirements_prod.txt
- `Sales Report HTML Template` --references--> `PyPDF PDF Manipulation Library`  [INFERRED]
  apps/sales/templates/sales_report.html → requirements_prod.txt
- `Sales Report HTML Template` --references--> `XHTML2PDF PDF Generation Library`  [INFERRED]
  apps/sales/templates/sales_report.html → requirements_prod.txt
- `register()` --indirect_call--> `User`  [INFERRED]
  app/api/v1/endpoints/auth.py → app/models/user.py
- `login()` --indirect_call--> `User`  [INFERRED]
  app/api/v1/endpoints/auth.py → app/models/user.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Django REST API Authentication Stack** — requirements_prod_django, requirements_prod_djangorestframework, requirements_prod_djangorestframework_simplejwt [EXTRACTED 0.95]
- **PDF Report Generation Pipeline** — apps_sales_templates_sales_report, requirements_prod_xhtml2pdf, requirements_prod_pypdf [INFERRED 0.90]
- **Docker Containerized Service Infrastructure** — docker_compose_app, docker_compose_db, requirements_prod [EXTRACTED 0.95]

## Communities (56 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (55): _get_date_minus_period(), graphic_report(), pdf_report(), AsyncSession, date, User, create_sale(), AsyncSession (+47 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (52): create_import(), get_import(), import_metrics(), list_imports(), _load_import(), AsyncSession, User, _to_read() (+44 more)

### Community 3 - "Community 3"
Cohesion: 0.16
Nodes (14): DiNexus Brand Logo, Sales Report HTML Template, Docker Compose Configuration, Django Application Service, PostgreSQL Database Service, PostgreSQL Database Engine, Production Dependencies, Django Web Framework (+6 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (48): After Completing a Task, Animation, Avoid, Before Writing Each Component, Border Progression, Border Radius, Borders, Card Layouts (+40 more)

### Community 5 - "Community 5"
Cohesion: 0.04
Nodes (42): CSS Example, Performance, Rules, Tailwind, Tailwind `transition-transform` Note, Transition Only What Changes, Use `will-change` Sparingly, Useful Properties (+34 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (38): API Keys, Authentication and Authorization, Batch Endpoints, Bearer Token, Bulk Operations, Cache Headers, Caching, Consistent Structure (+30 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (34): 1. Input/Payload Pattern, 1. Non-Null Types, 2. Interfaces for Polymorphism, 2. Optimistic Response Support, 3. Batch Mutations, 3. Unions for Heterogeneous Results, 4. Input Types, Arguments and Filtering (+26 more)

### Community 8 - "Community 8"
Cohesion: 0.40
Nodes (5): Development Dependencies, Coverage Testing Tool, Faker Test Data Generation, Pillow Image Processing Library, PyJWT Token Handling

### Community 9 - "Community 9"
Cohesion: 0.07
Nodes (28): 1. Semantic Similarity, 2. Diversity Sampling, 3. Difficulty-Based Selection, 4. Error-Based Selection, A/B Testing Example Sets, Adaptive Example Count, Advanced Techniques, Classification Template (+20 more)

### Community 10 - "Community 10"
Cohesion: 0.07
Nodes (27): Analysis Templates, API Documentation, Classification Templates, Code Generation, Code Review, Creative Writing, Email Generation, Extraction Templates (+19 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (27): 10. Text Wrapping, 11. Image Outlines, 12. Scale on Press, 13. Skip Animation on Page Load, 14. Never Use `transition: all`, 15. Use `will-change` Sparingly, 16. Minimum Hit Area, 1. Concentric Border Radius (+19 more)

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (24): Alternative Backgrounds for Depth, Animation, Border Progression, Border Radius Consistency, Card Layouts, Color Carries Meaning, Context-Aware Bases, Contrast Hierarchy (+16 more)

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (24): Animations, Choosing Between Motion and CSS, Code Example, Contextual Icon Animations, CSS Example, CSS-Only Stagger, CSS Transition Approach (No Motion), CSS Transitions vs. Keyframes (+16 more)

### Community 14 - "Community 14"
Cohesion: 0.08
Nodes (23): 1. Baseline Establishment, 2. Iterative Refinement Workflow, 3. A/B Testing Framework, Accuracy Improvement, Automated Evaluation, Best Practices, Categorizing Failures, Common Optimization Patterns (+15 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (13): main(), PromptOptimizer, Any, Iteratively optimize a prompt., Generate prompt variations to test., Remove redundant words to make prompt more concise., Add example section to prompt., A/B test two prompts. (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (22): API Design Checklist, Authentication & Authorization, Documentation, Documentation, Error Handling, Filtering & Sorting, GraphQL-Specific Checks, HTTP Methods (+14 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (22): Adaptive Reasoning Depth, Advanced Patterns, Best Practices, Caching Reasoning Patterns, Chain-of-Thought Prompting, Code Debugging, Common Pitfalls, Core Techniques (+14 more)

### Community 18 - "Community 18"
Cohesion: 0.09
Nodes (22): Advanced Features, Basic Template Structure, Best Practices, Classification Template, Common Template Patterns, Conditional Templates, Content Generation, Conversation Template (+14 more)

### Community 19 - "Community 19"
Cohesion: 0.19
Nodes (18): login(), AsyncSession, refresh(), register(), Settings, create_access_token(), create_refresh_token(), _create_token() (+10 more)

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (19): create_user(), delete_user(), ErrorDetail, ErrorResponse, get_user(), http_exception_handler(), list_users(), PaginatedResponse (+11 more)

### Community 21 - "Community 21"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 22 - "Community 22"
Cohesion: 0.11
Nodes (17): Cambios a `sales`, `city_stocks` (stock restante por ítem y ciudad), Contexto y objetivo, Dashboard web, Endpoints, Fuera de alcance, Gestión de esquema (sin Alembic), `import_items` (producto dentro del lote) (+9 more)

### Community 23 - "Community 23"
Cohesion: 0.23
Nodes (6): compute_investment(), compute_unit_cost(), Decimal, Cálculo de costos de lote.  Regla del negocio: el envío del lote se reparte en p, TestComputeInvestment, TestComputeUnitCost

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (14): Caching Common Prefixes, Integration Patterns, Key Patterns, Pattern 1: Structured Output with Pydantic, Pattern 2: Chain-of-Thought with Self-Verification, Pattern 3: Few-Shot with Dynamic Example Selection, Pattern 4: Progressive Disclosure, Pattern 5: Error Recovery and Fallback (+6 more)

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (14): 1. Customer Support Agent, 2. Data Analyst, 3. Content Editor, Advanced Techniques, Best Practices, Common Pitfalls, Constraint Specification, Core Principles (+6 more)

### Community 26 - "Community 26"
Cohesion: 0.13
Nodes (14): 1. Few-Shot Learning, 2. Chain-of-Thought Prompting, 3. Structured Outputs, 4. Prompt Optimization, 5. Template Systems, 6. System Prompt Design, Best Practices, Common Pitfalls (+6 more)

### Community 27 - "Community 27"
Cohesion: 0.23
Nodes (14): connect(), main(), migrate_categories(), migrate_history_prices(), migrate_products(), migrate_sale_details(), migrate_sales(), migrate_shipments() (+6 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (12): Adapt to Context, Craft in Action, Example: Dashboard with Sidebar and Dropdown, Example: Form Controls, Focus State Decision, Input Background Decision, The Border Decisions, The Craft Check (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.17
Nodes (11): 1. RESTful Design Principles, 2. GraphQL Design Principles, 3. API Versioning Strategies, API Design Principles, Best Practices, Common Pitfalls, Core Concepts, Detailed patterns and worked examples (+3 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (10): api-design-principles — detailed patterns and worked examples, GraphQL Design Patterns, Pattern 1: Resource Collection Design, Pattern 1: Schema Design, Pattern 2: Pagination and Filtering, Pattern 2: Resolver Design, Pattern 3: DataLoader (N+1 Problem Prevention), Pattern 3: Error Handling and Status Codes (+2 more)

### Community 31 - "Community 31"
Cohesion: 0.18
Nodes (10): error-handling-patterns — detailed patterns and worked examples, Go Error Handling, Language-Specific Patterns, Pattern 1: Circuit Breaker, Pattern 2: Error Aggregation, Pattern 3: Graceful Degradation, Python Error Handling, Rust Error Handling (+2 more)

### Community 32 - "Community 32"
Cohesion: 0.20
Nodes (9): ApiVentas — FastAPI, Concepto: lotes de importación, Dashboard, Endpoints principales, Esquema de base de datos, Instalación y arranque, Requisitos previos, Stack (+1 more)

### Community 33 - "Community 33"
Cohesion: 0.22
Nodes (8): After the Design, Anti-Pattern: "This Is Too Simple To Need A Design", Brainstorming Ideas Into Designs, Checklist, Key Principles, Process Flow, The Process, Visual Companion

### Community 34 - "Community 34"
Cohesion: 0.22
Nodes (8): 1. Error Handling Philosophies, 2. Error Categories, Best Practices, Common Pitfalls, Core Concepts, Detailed patterns and worked examples, Error Handling Patterns, When to Use This Skill

### Community 35 - "Critique"
Cohesion: 0.25
Nodes (7): Again, Critique, See the Composition, See the Content, See the Craft, See the Structure, The Gap

### Community 36 - "product.py"
Cohesion: 0.48
Nodes (6): CategoryBase, CategoryCreate, CategoryRead, ProductBase, ProductCreate, ProductRead

### Community 37 - "CLAUDE.md"
Cohesion: 0.29
Nodes (6): Arranque local, Dominio: lotes de importación, Estructura, graphify, Stack, Tests

### Community 38 - "Memory Management"
Cohesion: 0.29
Nodes (6): Don't Document, Memory Management, Pattern Format, Pattern Reuse, Validation Checks, When to Add Patterns

## Knowledge Gaps
- **434 isolated node(s):** `start-server.sh script`, `stop-server.sh script`, `When to Use This Skill`, `1. RESTful Design Principles`, `2. GraphQL Design Principles` (+429 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Product` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Why does `Details that make interfaces feel better` connect `Community 11` to `Community 5`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Why does `Animations` connect `Community 13` to `Community 5`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Product` (e.g. with `pdf_report()` and `create_sale()`) actually correct?**
  _`Product` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `User` (e.g. with `login()` and `refresh()`) actually correct?**
  _`User` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Sale` (e.g. with `pdf_report()` and `filter_sales()`) actually correct?**
  _`Sale` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `Base` (e.g. with `CityStock` and `Import`) actually correct?**
  _`Base` has 13 INFERRED edges - model-reasoned connections that need verification._