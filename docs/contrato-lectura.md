# El contrato de la lectura

La parte que entiende el correo no es código nuestro: la hace n8n con su nodo de IA.
Nosotros ponemos dos cosas, y son las dos que están en este archivo: **qué tiene que
devolver** y **qué se le pide para que lo devuelva**.

Por qué así, en `docs/decisions.md`. La regla corta: n8n ya sabe llamar a un modelo, y
escribirlo otra vez en Python pediría una dependencia y una credencial para hacer lo
mismo.

---

## Qué tiene que devolver

Un solo objeto. Este, con estos nombres:

```json
{
  "idioma": "es",
  "intencion": "reserva",
  "senales_salud": false,
  "pide_recomendacion": false,
  "cliente": {
    "nombre":     {"valor": "Laura Prats",        "origen": "dicho"},
    "correo":     {"valor": "l.prats@ejemplo.com", "origen": "dicho"},
    "habitacion": {"valor": "9",                   "origen": "dicho"}
  },
  "peticion": {
    "duracion":              {"valor": 60,           "origen": "dicho"},
    "fecha":                 {"valor": "2026-09-12", "origen": "deducido"},
    "franja":                {"valor": "tarde",      "origen": "dicho"},
    "personas":              {"valor": 2,            "origen": "dicho"},
    "preferencia_terapeuta": {"valor": "mujer",      "origen": "dicho"}
  }
}
```

### Las reglas del formato

- **Todo campo que traiga valor tiene que traer origen.** Un campo sin origen es un
  error de lectura, no un campo vacío, y el sistema para y avisa. Sin el origen no se
  sabe si el dato lo dijo el cliente o lo pusimos nosotros, y de eso depende si se le
  confirma o no.
- **Un campo que no sepas: omitilo, o ponelo con `"valor": null`.** Las dos formas
  cuentan como que falta.
- **`origen`** es una de tres, y nada más:
  - `dicho` — está escrito en el correo, con esas palabras
  - `deducido` — lo interpretamos nosotros. «El viernes» es una fecha, pero es una
    fecha que pusimos nosotros
  - `historial` — sale de un mensaje anterior del mismo hilo, no del último
- **`intencion`** es una de tres: `reserva`, `pregunta`, `derivar`. Cualquier otra cosa
  se trata como derivar.
- **`fecha`** siempre como `AAAA-MM-DD`. Nunca «el viernes» ni «12 de septiembre».
- **`franja`** solo `mañana` o `tarde`. Si el cliente dice una hora exacta, elegí la
  franja que le corresponde.
- **`duracion`** en minutos, un número. Si el cliente pide una duración que la casa no
  tiene, ponela igual: el sistema la descarta y se la vuelve a preguntar.
- **`preferencia_terapeuta`** solo `mujer` u `hombre`.
- **`senales_salud`** en `true` ante la menor duda. Ver abajo por qué.

### Lo que el sistema hace con esto, para que se entienda qué está en juego

- Si `senales_salud` viene en `true`, **de ese correo no se guarda nada**: ni el
  nombre, ni la dirección, ni una palabra del texto. Solo el número de hilo. Son datos
  de categoría especial y equivocarse por derivar de más no cuesta nada; equivocarse al
  revés, sí.
- Un campo `deducido` **no cierra la ficha**. Aunque estén los cuatro datos, si alguno
  se dedujo se le confirma al cliente en el mismo correo. Poner `dicho` en algo que
  interpretaste es la forma más rápida de agendar a alguien el día que no era.
- `preferencia_terapeuta` solo sale en la petición si viene como `dicho`. Deducida no
  se usa.

---

## Las instrucciones para el modelo

Esto es lo que va en el nodo de n8n. **La copia que manda es la de n8n**; esta es la de
referencia, para saber qué se le pidió cuando algo salga raro.

Lo que va entre llaves lo rellena n8n antes de mandarlo: el hilo completo, la fecha de
hoy y el catálogo de duraciones de la casa.

```text
Sos el asistente del spa de un hotel. Te paso un hilo de correo de un cliente
y tenés que devolver un JSON con lo que pidió. Nada más que el JSON.

Leé EL HILO ENTERO, no solo el último mensaje: hay datos que el cliente dio
tres correos atrás y no repite.

Hoy es {fecha_de_hoy}. Las duraciones que ofrece la casa son {duraciones}
minutos. Las franjas son mañana y tarde.

Devolvé exactamente esta forma:

{contrato}

Reglas:

1. Cada campo con valor lleva "origen": "dicho" si está escrito con esas
   palabras, "deducido" si lo interpretaste vos, "historial" si sale de un
   mensaje anterior del hilo. Si no sabés un campo, omitilo.

2. Sé estricto con "dicho". Si el cliente escribe "el viernes" y vos ponés una
   fecha, eso es "deducido". Si escribe "para los dos" y ponés 2 personas, eso
   es "deducido". Ante la duda, "deducido".

3. Poné "senales_salud": true si el cliente menciona cualquier cosa de salud:
   embarazo, lesiones, operaciones, dolores, medicación, alergias, o que va al
   fisioterapeuta. Ante la MENOR duda, true. Ese correo lo va a mirar una
   persona y no se pierde nada; lo que no se puede es guardarlo.

4. Poné "pide_recomendacion": true si pregunta cuál le conviene, qué le
   recomendamos, o qué es mejor para lo suyo.

5. "intencion" es "reserva" si quiere reservar algo, "pregunta" si solo
   pregunta por precios, horarios o qué hay, y "derivar" si es cualquier otra
   cosa: una queja, una factura, un proveedor, algo que no entendés.

6. El idioma es el del cliente, en dos letras: es, en, de, fr...

7. No inventes. Un campo que no está es un campo que falta, y el sistema sabe
   preguntarlo.
```

---

## Cómo se prueba sin llamar a nadie

Cada caso de `tests/correo/casos/` trae grabada la lectura de la IA para ese hilo. Las
pruebas no llaman al modelo: son rápidas y dan siempre lo mismo. Para sumar un caso se
agrega un archivo a esa carpeta y nada más.

Eso comprueba el recorrido, no la IA. Que el modelo lea bien un correo nuevo es otra
cosa y se mide con correos reales anonimizados, que están pendientes.
