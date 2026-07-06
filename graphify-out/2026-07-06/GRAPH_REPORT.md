# Graph Report - /home/martin_dev/Documents/github/ApiVentas  (2026-06-23)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 179 nodes · 271 edges · 35 communities (27 shown, 8 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 49 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `82df3d7d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
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

## God Nodes (most connected - your core abstractions)
1. `SaleDetail` - 17 edges
2. `Product` - 12 edges
3. `Sale` - 12 edges
4. `CreateGraphicReportSalesView` - 12 edges
5. `Category` - 11 edges
6. `CreateSaleView` - 11 edges
7. `MakePDFReportSaleView` - 11 edges
8. `Stock` - 10 edges
9. `CreateGraphicReportUseCase` - 10 edges
10. `User` - 10 edges

## Surprising Connections (you probably didn't know these)
- `API Ventas Installation and Setup Guide` --conceptually_related_to--> `Sales Report HTML Template`  [INFERRED]
  README.md → apps/sales/templates/sales_report.html
- `Django Application Service` --references--> `Production Dependencies`  [INFERRED]
  docker-compose.yaml → requirements_prod.txt
- `Sales Report HTML Template` --references--> `PyPDF PDF Manipulation Library`  [INFERRED]
  apps/sales/templates/sales_report.html → requirements_prod.txt
- `Sales Report HTML Template` --references--> `XHTML2PDF PDF Generation Library`  [INFERRED]
  apps/sales/templates/sales_report.html → requirements_prod.txt
- `CreateGraphicReportSalesView` --uses--> `Category`  [INFERRED]
  apps/sales/views.py → apps/products/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Django REST API Authentication Stack** — requirements_prod_django, requirements_prod_djangorestframework, requirements_prod_djangorestframework_simplejwt [EXTRACTED 0.95]
- **PDF Report Generation Pipeline** — sales_report, requirements_prod_xhtml2pdf, requirements_prod_pypdf [INFERRED 0.90]
- **Docker Containerized Service Infrastructure** — docker_compose_app, docker_compose_db, requirements_prod [EXTRACTED 0.95]

## Communities (35 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (17): APIView, Stock, Meta, Sale, SaleDetail, Shipment, Meta, SaleDetailSerializer (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.19
Nodes (16): Category, Meta, Product, CategorySerializer, Meta, ProductSerializer, SaleSerializer, Meta (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (6): APITestCase, TestBase, TestCreateSaleView, TestBase, TestBase, TestShowSales

### Community 3 - "Community 3"
Cohesion: 0.16
Nodes (15): Docker Compose Configuration, Django Application Service, PostgreSQL Database Service, DiNexus Brand Logo, PostgreSQL Database Engine, API Ventas Installation and Setup Guide, Production Dependencies, Django Web Framework (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (4): AbstractUser, GetSalesByUser, Meta, User

### Community 5 - "Community 5"
Cohesion: 0.23
Nodes (9): BaseCommand, create_category(), create_history_price(), create_product(), create_stock(), Create fake history prices, Create fake categories, Command (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.25
Nodes (4): AppConfig, ProductsConfig, SalesConfig, UsersConfig

### Community 8 - "Community 8"
Cohesion: 0.40
Nodes (5): Development Dependencies, Coverage Testing Tool, Faker Test Data Generation, Pillow Image Processing Library, PyJWT Token Handling

### Community 9 - "Community 9"
Cohesion: 0.40
Nodes (3): Get graphical sales reports based on the period and time unit provided., format_date(), get_date_minus_period()

## Knowledge Gaps
- **18 isolated node(s):** `Migration`, `Meta`, `Migration`, `Migration`, `Meta` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SaleDetail` connect `Community 0` to `Community 1`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `TestCreateSaleView` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `User` connect `Community 4` to `Community 1`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `SaleDetail` (e.g. with `Meta` and `SaleDetailSerializer`) actually correct?**
  _`SaleDetail` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `Product` (e.g. with `CategorySerializer` and `Meta`) actually correct?**
  _`Product` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `Sale` (e.g. with `Meta` and `SaleDetailSerializer`) actually correct?**
  _`Sale` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `CreateGraphicReportSalesView` (e.g. with `Category` and `Stock`) actually correct?**
  _`CreateGraphicReportSalesView` has 6 INFERRED edges - model-reasoned connections that need verification._