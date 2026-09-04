# Referencias

Material previo y de consulta. "Hacé algo como esto".

---

## Del propio proyecto

- **Bot de disponibilidad en Node** — `github.com/JaimeAmatASD/whatsapp-availability-bot`.
  Escucha peticiones y responde si el horario encaja. Reutilizable: el reconocimiento de
  tratamiento, fecha y hora está probado contra los mensajes reales de la casa, y el
  modelo de disponibilidad como horario semanal fijo más excepciones por fecha es el que
  va a usar la fase 6.
  Dos correcciones al portarlo: usa noventa minutos de separación entre sesiones y la
  regla de la casa es quince; y reserva huecos sin liberarlos nunca.

- **Anexo de casos de uso** — dieciséis situaciones reales agrupadas por tipo. Sirve como
  criterio de aceptación de cada fase y como examen para cualquier proveedor externo.

- **Borrador de requerimientos de Egi** — NO es una especificación. Es una declaración
  de intenciones, escrita con estilo de pliego, y no describe cómo funciona la casa.
  No se usa como criterio de aceptación ni se implementa nada porque esté ahí. Decisión
  de James, septiembre 2026.

- **Hoja «Cal Reiet Masajes Asignación»** (Google Drive del laboratorio) — la plantilla
  real que hoy se manda a mano al grupo. Cuatro campos y nada más:

  ```
  ⚜️ Petición ⚜️
  Masajista:     @nombre
  Tratamiento:   DT 90`
  Dia:           11-Sep-2025
  Habitacion:    #11
  ```

  La confirmación repite los mismos cuatro campos. De acá sale que el número con
  comilla son minutos y que la almohadilla es habitación.

  La misma hoja lleva tres columnas más — Terapeutas, Próximo y Contador — que son un
  turno rotativo entre terapeutas. Ese criterio de reparto no está en ningún documento
  del proyecto y no está decidido si se conserva. Hay que resolverlo antes de la fase 5.

- **Hojas de detalle mensual y facturas** (Google Drive) — de ahí sale el catálogo real
  de tratamientos y sus duraciones. Contienen nombres de huéspedes y datos fiscales:
  no se copian al repositorio, se leen y se anonimiza lo que haga falta.

## Externo

- Web del hotel: `calreiet.com`. Catálogo público de tratamientos, que es más corto que
  el catálogo real de la operación.

---

<!-- Referencias nuevas al final -->
