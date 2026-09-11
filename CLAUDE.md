# Cal Reiet — gestor de reservas del spa

Automatiza la máquina administrativa del departamento de Wellbeing: entra un pedido,
se reserva sala, se pide terapeuta, se asigna, se agenda y se confirma.
NO es un PMS, no toca dinero, no gestiona fichas de salud.

Qué es y cómo se corre: `README.md`. Por qué es así: `docs/decisions.md`.
Dónde va cada cosa: `docs/bitacora.md`.

Contexto del negocio y del flujo: skill `cal-reiet-spa-reservas`.
Plan de trabajo y fases: skill `cal-reiet-spa-fases`.

---

## Con quién estás trabajando

James dirige este proyecto pero no lee código. No se lo mandes.

- Nada de diffs. Se le muestra: qué hace ahora en idioma del dominio, el estado del
  gate, y qué tiene que mirar él.
- Términos técnicos: cinco palabras entre paréntesis y seguir.
- Este proyecto además genera documentos para el hotel. Esos van en lenguaje de
  negocio, sin una sola palabra técnica. Nada de webhook, nodo, endpoint, parser.
  Son dos versiones distintas del mismo entregable, nunca el mismo documento.

## Comandos

```bash
source .venv/bin/activate   # el entorno del proyecto, siempre primero
pytest                      # todos los tests

# solo la primera vez, o al clonar el repo en otra máquina:
python3 -m venv .venv && .venv/bin/pip install PyYAML pytest
```

Python. El código propio vive en `src/`, la configuración de la casa en
`config/casa.yaml` y el catálogo de tratamientos en `config/tratamientos.yaml`.
Convenciones de tests: `.claude/rules/tests.md`.

## Stack

- n8n como orquestador
- Google Calendar como fuente de verdad, un calendario por sala
- Google Sheets como registro
- Telegram como canal interno con los terapeutas
- Sin base de datos propia

Dos piezas van como código propio y probado, fuera de los nodos: el buscador de huecos
y la máquina de estados de la reserva.

## Reglas duras

- **Nada de datos reales de clientes en el entorno de laboratorio.** Nombres, mails y
  teléfonos se cambian antes de entrar. Son datos de personas y la cuenta es personal.
- **Nunca automatizar WhatsApp.** Ni con la API oficial ni con automatización del
  navegador. Si se bloquea el número del hotel, el spa queda incomunicado en temporada
  alta. El canal interno es Telegram.
- **Nada específico de esta casa dentro del código.** Tratamientos, duraciones, salas,
  los quince minutos, textos e idiomas van en configuración. El sistema tiene que poder
  montarse en otra casa cambiando un archivo.
- **Dos cuentas de Google, y no se mezclan.** Se escribe SOLO en
  `calreiet.lab@gmail.com`, que es el laboratorio. En `lucioamat@gmail.com` **NUNCA
  se escribe**: es la cuenta desde la que se ve el calendario real del hotel, y es
  solo de lectura. Antes de escribir en un calendario se mira de quién es. Si no es
  del laboratorio, no se escribe: se pregunta.
- **Del calendario real solo se leen horas.** Hora de inicio, hora de fin y sala. Los
  títulos y las descripciones llevan nombres, correos y teléfonos de clientes, y se
  descartan en el momento. El buscador de huecos no necesita nada más.
- **Ninguna credencial se commitea.** Van en `.env`, que está en `.gitignore`.

## Cómo trabajar acá

- **Cambios chicos y verificables.** Uno por vez.
- **No sobre-ingeniería.** Si una función alcanza, no armes una jerarquía de clases.
- **No toques lo que no te pidieron.** Si ves algo mal al lado, avisá; no lo arregles
  de prepo.
- **Un chat, una fase.** No adelantes trabajo de otra fase aunque parezca fácil.
- Antes de agregar una dependencia, preguntá.
- Todo bug arreglado deja un test que lo reproduce y una línea en `docs/lessons.md`.
- Todo trabajo cerrado deja una entrada en `docs/bitacora.md`.

## Estructura

- `docs/` — bitácora, decisiones, lecciones, convenciones y referencias
- `flows/` — exportaciones de n8n en JSON
- `src/` — el recorrido del pedido: entender, buscar hueco y armar la petición
- `config/` — todo lo propio de la casa

## Glosario

Vocabulario controlado de estados. Usarlo igual en el código, en los reportes y al
hablar con el hotel.

- **Petición** — el pedido que sale al grupo de terapeutas
- **Hold** — sala y horario bloqueados, todavía sin terapeuta
- **Parte** — la planificación del día siguiente que hoy escribe Egi a mano
- **EXT** — cliente externo, no alojado en el hotel
- **INV** — identificador de cobro, solo para externos
- **Estados** — SOLICITADA, EN HOLD, ASIGNADA, CONFIRMADA, REALIZADA, CAÍDA,
  CANCELADA, SIN COBERTURA

Que un terapeuta quede asignado no significa que la reserva esté confirmada. Son dos
cosas distintas y no se mezclan.

Formato exacto de la petición, la confirmación y el parte: `docs/convenciones.md`.
Salió de los mensajes reales del grupo, y el sistema tiene que producir eso mismo.
