---
paths:
  - "tests/**"
---

# Tests

Se carga solo al abrir un test, que es cuando estas reglas se pueden romper.

- **Un test que falla se arregla arreglando el código.** Nunca ablandando el
  test: ni bajando una aserción, ni marcándolo para saltear, ni ampliando lo
  que acepta por bueno. James no lee código y no puede detectarlo revisando el
  diff, así que acá no hay red de seguridad más que esta regla.
- **Si el test parece estar mal, se pregunta.** Puede que lo esté. Esa es una
  conversación, no un cambio que se hace de paso.
- **Rojo antes que verde.** Un test que nunca se vio fallar no prueba nada:
  hay que verlo fallar por la razón correcta antes de escribir el código.
- **Dos intentos y se frena.** Si un arreglo no sale en dos vueltas, se para y
  se avisa. Dar vueltas quema tokens y desde afuera no se puede destrabar.
- Todo bug arreglado deja un test que lo reproduce y una línea en
  `docs/lessons.md`.
