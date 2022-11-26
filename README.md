# Sistemas-Multiagente-571
Respaldo del proyecto de la materia de Sistemas Multiagente

El proyecto es un modelo de segregacion donde por el momento solo maneja colores como base de la decision de los agentes.

Se espera agregar ~~_ideologia politica_~~ y ~~_clase social_~~

La ideologia politica fue agregada de forma simplificada, al igual que un grid alternativo al de razas para ver los grupos creados por la prioridad de opinion politica.

Clase social agregada como un valor que se asigna al crear al agente y que varia dependiendo de su movilidad


---Ultima version---

  Se agregó un clasificador donde se entrenan los agentes con sus reglas ciertas iteraciones y de ahi dependiendo de sus atributos predicen si son felices o no para moverse.
  
  Se agregaron diferentes tamanos para los grid, se cambian con el archivo server.py (Recomendado 50x50)
  
  Se agregó el modelo de ideologia politica completo
  
  Se agregaron clases economicas con gastos y ganancias dependiendo de su movilizacion para la felicidad
  
  Se agregaron zonas del mapa con valor economico minimo para poder vivir ahi, esto obliga a mover a los agentes aunque sean felices pero no les alcance
  
  Se agregaron condiciones para cambiar de opiniones y prioridades si el agente no es feliz por un tiempo.
  
  Se tienen 3 tipos de grid para visualizar razas, opiniones y clases economicas
  
This project is based in Mesa ABM Python Framework
