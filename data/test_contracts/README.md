# Contratos de prueba

Imágenes de entrada del sistema. Cada par = contrato original + su enmienda.

## Casos

| Par | Tipo     | Contrato                   | Archivos                                                 |
| --- | -------- | -------------------------- | -------------------------------------------------------- |
| 1   | Complejo | Licencia de Software       | `documento_1__original.png`, `documento_1__enmienda.png` |
| 2   | Complejo | Servicios de Consultoría   | `documento_2__original.png`, `documento_2__enmienda.png` |
| 3   | Complejo | Servicio SaaS              | `documento_3__original.png`, `documento_3__enmienda.png` |
| 4   | Simple   | Servicios de Mantenimiento | `documento_4__original.png`, `documento_4__enmienda.png` |

## Cambios esperados

### Par 1 — Complejo

- Cláusula 1 (Otorgamiento): MODIFICADA → "no exclusiva e intransferible… únicamente para fines internos de la empresa" → "no exclusiva… para operaciones internas de negocio"
- Cláusula 2 (Plazo): MODIFICADA → 12 meses → 24 meses
- Cláusula 3 (Pago): MODIFICADA → USD 12.000 anuales → USD 15.000 anuales
- Cláusula 4 (Soporte): MODIFICADA → correo electrónico → correo electrónico y chat
- Cláusula 5 (Terminación): MODIFICADA → preaviso de 30 días → preaviso de 60 días
- Cláusula 7 (Protección de Datos): AGREGADA → el Licenciante debe cumplir la normativa de protección de datos
- Sin cambios: Cláusula 6 (Confidencialidad)
- Esperado en `sections_changed`: ["1. Otorgamiento de Licencia", "2. Plazo", "3. Pago", "4. Soporte", "5. Terminación", "7. Protección de Datos"]

### Par 2 — Complejo

- Cláusula 1 (Alcance del Servicio): MODIFICADA → "expansión de proyectos de energía renovable" → "expansión de proyectos de energía renovable y análisis regulatorio"
- Cláusula 2 (Duración): MODIFICADA → 6 meses → 9 meses
- Cláusula 3 (Honorarios): MODIFICADA → USD 8.000 mensuales → USD 9.500 mensuales
- Cláusula 4 (Entregables): MODIFICADA → reportes mensuales → reportes quincenales
- Cláusula 7 (Propiedad Intelectual): AGREGADA → los entregables pasan a ser del Cliente una vez realizado el pago final
- Sin cambios: Cláusula 5 (Confidencialidad), Cláusula 6 (Legislación Aplicable)
- Esperado en `sections_changed`: ["1. Alcance del Servicio", "2. Duración", "3. Honorarios", "4. Entregables", "7. Propiedad Intelectual"]

### Par 3 — Complejo

- Cláusula 3 (Precio): MODIFICADA → USD 1.200 mensuales → USD 1.250 mensuales
- Cláusula 4 (Disponibilidad del Servicio): MODIFICADA → 99,5% → 99,9%
- Cláusula 5 (Soporte): MODIFICADA → correo electrónico → correo electrónico y sistema de tickets en línea
- Sin cambios: Cláusula 1 (Servicio), Cláusula 2 (Plazo de Suscripción)
- Esperado en `sections_changed`: ["3. Precio", "4. Disponibilidad del Servicio", "5. Soporte"]
- Nota: El título dice 'VERSIÓN ACTUALIZADA' en lugar de 'Enmienda'; el sistema debe comparar por contenido, no por título.

### Par 4 — Simple (1 sola cláusula)

- Cláusula 3 (Honorarios): MODIFICADA → monto USD 2.500 → USD 2.800
- Cláusula 3 (Honorarios): MODIFICADA → vencimiento día 10 → día 5
- Esperado en `sections_changed`: ["3. Honorarios"]

## Notas

- Formato PNG: se eligio PNG porque comprime sin perdida, el texto queda mas nitido que con JPG
- El Par 1 incluye un cambio que el documento oficial de diferencias no lista. Sirve para probar la fidelidad del sistema y su precision para leer.
