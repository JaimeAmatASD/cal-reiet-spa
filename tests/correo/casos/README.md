# Correos de prueba

Un archivo por caso. Cada uno lleva tres cosas:

- `hilo` — el correo o la conversación completa, tal como entró.
- `lectura` — lo que devolvió la parte de IA al leer ese hilo, **grabado**. No se
  llama al modelo en las pruebas: se le da su propia respuesta de la vez que sí se
  llamó. Así la batería es rápida y siempre da el mismo resultado.
- `espera` — qué ficha tiene que salir.

Los casos que hay hoy son **inventados**, escritos para cubrir las situaciones que
sabemos que pasan. Los correos reales anonimizados van acá al lado, con la misma
forma, y la batería los levanta sola: no hay que tocar ningún test para sumar uno.

Antes de que un correo real entre acá se le cambian nombre, mail y teléfono. Son
datos de personas y la cuenta del laboratorio es personal.
