# 🛒 Análisis de Datos de Tienda (Python Nativo)

Este proyecto contiene un programa interactivo desarrollado en **Python nativo** (sin librerías externas como Pandas, NumPy o Seaborn) para realizar un **Análisis Exploratorio de Datos (EDA)** básico sobre las ventas, clientes y productos de una tienda.

El objetivo es demostrar la lógica de carga, limpieza y agregación de datos utilizando únicamente las herramientas fundamentales del lenguaje Python.

---

## 1. Estructura y Origen de los Datos

El análisis se basa en cuatro conjuntos de datos de la tienda, simulados a partir de archivos CSV:

### 1.1. Clientes (`clientes.csv.csv`)

Contiene la información de los clientes.

| Columna | Tipo de Dato | Descripción |
| :---: | :---: | :---: |
| **id\_cliente** | Entero | Identificador único del cliente. **Clave Primaria**. |
| **nombre\_cliente** | Texto | Nombre completo del cliente. |
| **email** | Texto | Correo electrónico del cliente. |
| **ciudad** | Texto | Ciudad de residencia del cliente. |
| **fecha\_alta** | Fecha | Fecha en la que el cliente se dio de alta. |

### 1.2. Ventas (`ventas.csv.csv`)

Contiene el registro de las transacciones principales.

| Columna | Tipo de Dato | Descripción |
| :---: | :---: | :---: |
| **id\_venta** | Entero | Identificador único de la venta. **Clave Primaria**. |
| **fecha** | Fecha | Fecha de la venta. |
| **id\_cliente** | Entero | Identificador del cliente. **Clave Foránea** a `Clientes`. |
| **medio\_pago** | Texto | Método de pago utilizado (`tarjeta`, `qr`, `efectivo`, `transferencia`). |

### 1.3. Detalle de Ventas (`detalle_ventas.csv.csv`)

Contiene el desglose de los productos en cada venta (la tabla de hechos principal).

| Columna | Tipo de Dato | Descripción |
| :---: | :---: | :---: |
| **id\_venta** | Entero | Identificador de la venta. **Clave Foránea** a `Ventas`. |
| **id\_producto** | Entero | Identificador del producto vendido. **Clave Foránea** a `Productos`. |
| **cantidad** | Entero | Número de unidades vendidas. |
| **precio\_unitario** | Decimal/Entero | Precio unitario al momento de la venta. *(Nota: El código maneja valores faltantes calculándolos a partir de `importe / cantidad`)*. |
| **importe** | Decimal/Entero | Importe total de la línea (cantidad \* precio\_unitario). |

### 1.4. Productos (`productos.csv.csv`)

Contiene el catálogo de productos.

| Columna | Tipo de Dato | Descripción |
| :---: | :---: | :---: |
| **id\_producto** | Entero | Identificador único del producto. **Clave Primaria**. |
| **nombre\_producto** | Texto | Nombre del producto. |
| **categoria** | Texto | Categoría del producto (`Alimentos` o `Limpieza`). |
| **precio\_unitario** | Entero | Precio unitario actual del producto. |

---

## 2. Guía de Uso del Programa Interactivo

El programa `analisis_tienda.py` permite realizar consultas en tiempo real sobre los datos analizados.

### 2.1. Preparación y Ejecución

1.  **Guardar el Código:** Asegúrate de tener el código Python completo en un archivo llamado `analisis_tienda.py`.
2.  **Ejecutar:** Abrí tu terminal o consola, navega al directorio del archivo, y ejecutá:

```bash
python analisis_tienda.py