# Data Ingestion and Processing Engine with Django Integration

This repository contains a Python implementation for processing and transforming data records based on configurable arithmetic and regex-based equations. It uses a custom Lexer, Parser, and Interpreter to evaluate mathematical and logical expressions (Regex) dynamically.

---

## Overview

This project processes data records (data.txt) in real-time by:
- Parsing and interpreting equations provided through a kpi endpoint.
  
  example :
  ATTR+50*(ATTR/10), Regex(ATTR, "^dog")
- Performing computations or regex-based matching on incoming data.
- Storing processed results in a SQLite database `processed_data.db`.
- Managing KPIs and their associations with assets using a Django-based web interface.

---

## Architecture 

1. **Token** `Token.py`: Defines token types for parsing equations and a Token class to represent individual tokens with a type and value.
2. **AST** `AST.py`: Represents nodes for binary operations, numeric values, and regex operations.
4. **Lexer** `lexer.py`: Converts input strings (equations) into tokens.
5. **Parser** `parser.py`: Constructs an Abstract Syntax Tree (AST) from tokens.
6. **Interpreter** `interpreter.py`: Traverses the AST to evaluate expressions.
7. **Operations** `operations.py`: Defines a base Operation class and subclasses for addition, subtraction, multiplication, and division operations.
8. **Django Database** `django_database.py`: Retrieves the KPI expression for a given asset_id by joining the kpi_kpi (has the name and the expression) and kpi_assetkpi (has the kpi linked to asset_it) tables.
9. **Main** `Main.py`: Continuously reads, processes, and writes data records to the database (processed_data.db).
   - **process_message**: Processes incoming messages, applies the relevant equation (regex or arithmetic), and returns the result.
   - **FileReader**: Reads new records from a file starting from the last position.
   - **DataProcessor**: Processes records by applying the equation and writing the results to the database.
10. **SQLiteDataSink** `database.py`: Stores the processed output into a SQLite database.

---

## Django Task

The Django application provides APIs for managing KPIs and linking them to assets id. 

### Tasks Implemented:
1. **KPI App**:
   - Created a `KPI` app in Django to manage KPI information and their linkage to assets id.
   
2. **Models**:
   - `KPI`: Stores KPI details such as name, expression, and optional description.
   - `AssetKPI`: Links KPIs to asset IDs fetched dynamically from the SQLite database.

3. **Endpoints**:
   - **List/Create KPI**: `/api/kpi/` (supports GET and POST methods).
   - **Link Asset to KPI**: `/api/kpi/link_asset/` (supports POST to create associations).

4. **Swagger Documentation**:
   - Interactive API documentation available at `/swagger/`.
   - ReDoc UI available at `/redoc/`.

---

## Django Code Details

### `models.py`
Defines two models:
- **KPI**: Represents the KPI with fields `name`, `expression`, and an optional `description`.
- **AssetKPI**: Links KPIs to assets using a foreign key relationship, with asset IDs dynamically fetched from the SQLite database.

### `serializers.py`
Defines serializers for `KPI` and `AssetKPI` models to transform data between Python objects and JSON:
- **`KPISerializer`**: 
  - Serializes the `KPI` model, including fields like `id`, `name`, `expression`, and `description`.
  - Used for converting `KPI` objects to JSON for API responses and for accepting data for creating or updating KPIs via the API.
- **`AssetKPISerializer`**:
  - Serializes the `AssetKPI` model, which links an asset to a KPI.
  - The `asset_id` field is a `ChoiceField` populated with `asset_id` values from the `data.txt` file.
  - Used for linking assets to KPIs through the API.

The `get_asset_ids()` function is used to dynamically fetch the unique `asset_id` values from the data file and provide them as choices for the `asset_id` field.

### `urls.py`
Defines API routes:
- **`admin/`**: Django admin panel.
- **`api/kpi/kpis/`**: Endpoint to list or create KPIs using the `KPIListCreateView`. (Supports GET and POST).
- **`api/kpi/assets/link/`**: Endpoint to link assets to KPIs using the `AssetKPICreateView`. (Supports POST).
- **`api/kpi/`**: Defaults to the `KPIListCreateView` for listing or creating KPIs. (Supports GET and POST).
- **`swagger/`**: Interactive Swagger UI for API documentation.
- **`redoc/`**: ReDoc UI for a detailed API overview.
---

## swagger (http://127.0.0.1:8000/swagger/)
![image](https://github.com/user-attachments/assets/729cee9d-cedc-41e3-ae52-cfba27f9a517)

## Kpi List Create (http://127.0.0.1:8000/api/kpi/)
![image](https://github.com/user-attachments/assets/ad3a9573-8ab1-42f9-805b-d7270d0bcf09)

## Asset Kpi Create Link (http://127.0.0.1:8000/api/kpi/assets/link/)
![image](https://github.com/user-attachments/assets/3dc1e88a-bf69-4e21-9068-f6802c62cbaf)


