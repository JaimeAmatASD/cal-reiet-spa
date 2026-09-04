---
name: cal-reiet-spa-fases
description: |
  División del trabajo en fases del gestor de reservas del spa de Cal Reiet, pensada
  para que cada fase se trabaje en un chat aparte sin arrastrar todo el contexto del
  proyecto. Dice en qué fase está cada cosa, qué hay que tener antes de empezar, qué
  significa terminado, y cómo se devuelve el resultado a la bitácora.

  Cargá SIEMPRE que James abra un chat para trabajar una fase o un paso concreto del
  spa de Cal Reiet, pregunte por dónde va el proyecto, en qué fase está, qué sigue, qué
  falta para cerrar una fase, o cuando diga "fase 1", "paso 2.3", "arrancamos con el
  buscador de huecos", "seguimos con Telegram", "vamos con la disponibilidad".
  Cargalo también cuando pida el traspaso entre chats, el resumen para la bitácora, o
  cuando haya que decidir si algo entra en la fase actual o se posterga.

  Presupone el skill cal-reiet-spa-reservas, que tiene el contexto del proyecto.
  Este solo tiene el plan de trabajo.

  Inglés — project phasing, work breakdown, phase handoff, session context transfer.
---

# Cal Reiet — división del trabajo por fases

## Para qué existe este skill

El proyecto es largo y el contexto es caro. Cada fase se trabaja en un chat propio.
Este skill es el mapa que le dice a un chat nuevo dónde está parado sin tener que
releer toda la historia del proyecto.

Regla de uso: **un chat, una fase.** Si la fase es grande, un chat por paso. Un chat
que empieza a saltar entre fases se vuelve caro y se pierde.

## Las seis fases

El orden no responde a la dificultad técnica sino al riesgo operativo: primero lo que
no le cambia el trabajo a nadie, último lo que toca cómo se reparten las horas entre
terapeutas.

Las fases 1, 2 y 3 se pueden hacer en paralelo. De la 4 en adelante es cadena.

### Fase 1 — Medir sin tocar nada

**Objetivo.** El sistema lee el buzón y anota cada pedido en una hoja. No escribe en el
calendario, no manda mensajes, no toca la operación.

**Por qué primero.** Riesgo operativo cero, y produce los números con los que Petra va a
decidir si el proyecto sigue: cuántos pedidos entran, cuántos se pierden, cuánto se
tarda en contestar.

**Pasos.**

1. Montar el entorno de laboratorio: cuenta de Google nueva, tres calendarios (Sala 1,
   Sala 2, Disponibilidad), una hoja de registro, un bot de Telegram de prueba con un
   grupo propio, y n8n corriendo
2. Definir las columnas de la hoja de registro
3. Conectar el buzón y detectar correo nuevo
4. Extraer los campos del mail del formulario, con reglas, sin IA
5. Escribir la fila en la hoja
6. Probar con veinte peticiones reales anonimizadas
7. Generar el reporte semanal

**Terminado cuando.** Veinte correos de prueba entran solos y salen bien en todas las
columnas, y el reporte semanal se genera sin intervención.

**Ojo.** El mail libre que escribe un cliente a mano es un caso distinto del mail del
formulario y sí necesita IA. Va después, no en esta fase.

### Fase 2 — Formulario y acuse

**Objetivo.** Arreglar los campos del formulario de la web y que el cliente reciba
respuesta automática al enviarlo.

**Por qué importa.** Es lo único de todo el proyecto que el cliente nota, y es de lo más
barato. Cada campo que el formulario capture bien es trabajo de desglose que desaparece
para siempre.

**Campos a sumar.** Número de personas, preferencia de sexo del terapeuta, segunda
opción de horario, y si se aloja con qué fechas y habitación. El día y la hora deben
dejar de ser texto libre.

**Bloqueante.** Saber quién controla la web y si se puede tocar el formulario.

**Terminado cuando.** Un pedido nuevo llega con fecha y hora estructuradas, y el cliente
recibe acuse con el plazo de respuesta.

### Fase 3 — Ordenar el calendario

**Objetivo.** Un calendario por sala, títulos con formato estable, terapeutas como
invitados de sus propios eventos.

**Por qué.** Es el prerequisito de toda automatización posterior. Hoy la sala es un color
y el terapeuta se escribe dentro del título.

**Terminado cuando.** Todo tratamiento vive en el calendario de su sala, ningún evento
queda con sala ambigua, y cada terapeuta ve lo suyo sin acceso al resto.

### Fase 4 — Buscador de huecos

**Objetivo.** Dado un tratamiento y una fecha, devolver los horarios posibles.

**Reglas que implementa.** Los quince minutos a ambos lados de cada reserva, y el
criterio de compactar: preferir el hueco que se pega a una reserva existente antes que
abrir una cita aislada. Aplica igual a salas y a terapeutas.

**Va como código propio, no dentro de nodos.** Es la pieza con lógica de negocio real y
la que más falta que esté probada.

**Terminado cuando.** Egi pide huecos y recibe propuestas que ella habría elegido. Ella
sigue decidiendo y creando la reserva.

### Fase 5 — Telegram

**Objetivo.** La petición sale sola con un botón, y quien lo aprieta queda escrito en el
evento del calendario.

**Por qué acá.** Es la primera fase que le cambia el hábito a los terapeutas, y donde
desaparece la mitad del trabajo manual de Egi.

**Bloqueante.** Que el equipo se mude de WhatsApp a Telegram. Ya aceptaron.

**Terminado cuando.** Una petición completa el ciclo sin que nadie escriba un mensaje a
mano.

### Fase 6 — Disponibilidad declarada y asignación directa

**Objetivo.** Los terapeutas cargan su disponibilidad, y cuando alguien está disponible
y cualificado, el sistema asigna directo en vez de abrir la petición al grupo.

**Piezas.** La interfaz de carga, el calendario espejo de solo lectura, la matriz de
competencias y el botón de no puedo.

**Dependencia con plazo largo.** La matriz de quién hace qué tratamiento no es un
problema técnico, es perseguir gente para que conteste. Empezar a recolectarla desde la
fase 1 o esta fase se atrasa un mes.

**Terminado cuando.** Un pedido con disponibilidad declarada llega al terapeuta ya
asignado, y él puede rechazarlo en un toque.

## Cómo abrir un chat de fase

Decir la fase y el paso, y nada más. Los skills traen el resto.

```
Fase 1, paso 4. Extracción de campos del mail del formulario.
```

El chat de fase arranca leyendo la bitácora del repo para saber qué pasó antes.

## Qué no hacer en un chat de fase

- **No rediseñar el flujo.** Está cerrado y validado con Egi. Si algo no cierra, se
  anota y se lleva a un chat de diseño, no se resuelve por las suyas.
- **No adelantar trabajo de otra fase.** Aunque parezca fácil. El orden protege la
  operación, no la comodidad.
- **No traer los temas aparcados.** Ficha de salud, preparación de tratamientos y
  facturación están fuera de alcance por decisión de James.

## Cómo se cierra un chat de fase

Antes de terminar, dejar la entrada de bitácora lista para pegar en `docs/bitacora.md`:

```markdown
## AAAA-MM-DD — Fase N, paso N.N

**Qué se hizo.** Dos o tres líneas en idioma del dominio, no técnico.
**Estado.** Terminado, o qué falta.
**Decisiones.** Si hubo alguna de peso, va también a decisions.md.
**Se rompió algo.** Si hubo error propio, va también a lessons.md.
**Próximo paso.** Uno solo.
```

Si la fase produjo algo que Egi o Petra tienen que ver, va aparte y en lenguaje de
negocio, sin una palabra técnica. Esa es la versión que decide el futuro del proyecto.
