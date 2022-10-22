import mesa
import math
import numpy as np
import matplotlib.pyplot as plt
import random
'''
image = plt.imread('circulo.jpg')
image_copy = image.copy()
azul = np.all(image >= [250, 0, 0], axis=-1)
blanco = ~azul
azul = azul.astype(int)
blanco = blanco.astype(int)
azul = np.rot90(azul,3)
blanco = np.rot90(blanco,3)
'''
'''
unos = (azul == 1).sum()
x, y = np.where(azul == 1)
'''

class Static():
    a = 0
global_ta = Static()
class BackgroundAgent(mesa.Agent):
    def __init__(self, pos, model, color):
        super().__init__(pos, model)
        self.pos = pos
        self.color = color
    def step(self):
        
        print(type(self))
class SchellingAgent(mesa.Agent):
    def __init__(self, pos, model, happy, color):
        super().__init__(pos, model)
        self.pos = pos
        self.happy = happy
        self.color = color
        self.opinion = random.uniform(0, 1)
        self.discrete_opinion = 0
        self.last_opinion = 0
        self.priority = None
        self.index = round(random.uniform(0, 1))
        opinions = ['izq', 'cent', 'der']
        if(self.opinion >= 0 and self.opinion <= .33):
            self.discrete_opinion = opinions[0]
        elif(self.opinion <= .66):
            self.discrete_opinion = opinions[1]
        else:
            self.discrete_opinion = opinions[2]
        

    def step(self):
        similar = 0
        other = 0
        #Ideologias: izq centro der
        priority = ['color', 'opinion']
        opinions = ['izq', 'cent', 'der']
        
        self.priority = priority[self.index]
        if(self.priority == 'color'):
            self.model.color_prior += 1
        else:
            self.model.op_prior += 1
        not_again = False

        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if(self.priority == 'color'):
                if neighbor.color == self.color:
                    similar += 1
                elif(neighbor.color == "black"):
                        continue
                else:
                    other += 1
            try:
                if(self.priority == 'opinion' and not_again == False):
                    treshold = 0.15
                    if abs(self.opinion - neighbor.opinion ) <= treshold:
                        similar += 1
                        self.opinion = abs(self.opinion + neighbor.opinion )/2 #Modelo simplificado por mientras
                        if(self.opinion >= 0 and self.opinion <= .33):
                            self.discrete_opinion = opinions[0]
                        elif(self.opinion <= .66):
                            self.discrete_opinion = opinions[1]
                        else:
                            self.discrete_opinion = opinions[2]
                    else:
                        other += 1  
                    not_again = True     
                if(not_again == True):
                    if neighbor.discrete_opinion == self.discrete_opinion:
                        similar += 1
                    elif(neighbor.color == "black"):
                            continue
                    else:
                        other += 1
            except:
                continue     
        if(self.discrete_opinion == 'izq'):
            self.model.izq += 1
        if(self.discrete_opinion == 'cent'):
            self.model.cent += 1    
        if(self.discrete_opinion == 'der'):
            self.model.der += 1

        total_nearby = similar + other
        if(similar >= self.model.similar_wanted * total_nearby / 100):
            self.happy = 1
            self.model.happy += 1
        else:
            self.happy = 0
            self.model.grid.move_to_empty(self)




class Schelling(mesa.Model):
    """
    |Modelo de segregacion basado en el de Netlogo
    
    |Agent density: Controla la cantidad de agentes que pueden estar en el area disponible
    |%_similar_wanted: Porcentaje de agentes del mismo color cercanos para que los agentes esten felices
    |cantidad_razas: Cantidad tipos de agentes
    |Mapa: Mapas de tamano 50x50 basados en paises y figuras geometricas
    |Proporcion raza X: Porcentaje de cada color del total de agentes, la suma debe dar 100% o la simulacion se rompe
    """

    def __init__(self, width=20, height=20, density=0.8, similar_wanted=3, cantidad_razas = 2, mapa = "circulo_2.jpg", ta = 'color', p1 = 0, p2 = 0, p3 = 0, p4 = 0, p5 = 0):

        self.width = width
        self.height = height
        self.density = density
        self.similar_wanted = similar_wanted
        self.cantidad_razas = cantidad_razas
        self.mapa = mapa
        self.p1  = p1
        self.p2  = p2
        self.p3  = p3
        self.p4  = p4
        self.p5  = p5
        self.ta = ta
        global_ta.a = ta
        self.similar_nearby = 0
        self.other_nearby = 0
        '''
            Intento de implementacion
            
            Opiniones
            A = {a1, ... , an} #Set de agentes
            xyi = (xi, yi) #Posicion de los agentes
            opi ∈ [0,1] #Opinion del agente, valor numerico y normalizado
            ϵ #Treshold de rango de aceptacion de opinion diferente
            μ #Termino de convergencia
            
            ALGORITMO
            # Set input parameters (n, limit, rs, e, m, p, l, d, Nf )
            Input: Create population A of n agents
            for each iteration in range(limit) do
            Select agent ai and neighbour aj [ N(i, rs) at random (skip iteration if ai has no neighbours)
                if |opi − opj| ≤ e then
                    # Successful interaction: Opinion influence
                    op'i = opi + m(opj − opi)
                    op'j = opj + m(opi − opj)
                    opi = op'i; opj = op'j
                else
                    # Unsuccessful interaction
                end if
                    # Update location based on mobility model
            end for
        
        
        Fuente: 
            https://orca.cardiff.ac.uk/id/eprint/132434/1/The%20role%20of%20homophily%20in%20opinion%20formation%20among%20mobile%20agents.pdf
        '''
        
        suma = 0
        proporciones = [self.p1, self.p2, self.p3, self.p4, self.p5]
        for i in range(self.cantidad_razas):
            suma += proporciones[i]
        if(suma != 100): #Cambiar para no matar la simulacion
            raise Exception("Las proporciones no dan el 100%")

        colors = ["red", "green", "yellow", "blue", "orange"]

        image = plt.imread(self.mapa)
        azul = np.all(image >= [250, 0, 0], axis=-1)
        blanco = ~azul
        azul = azul.astype(int)
        blanco = blanco.astype(int)
        azul = np.rot90(azul,3)
        blanco = np.rot90(blanco,3)
        
        
        self.schedule = mesa.time.RandomActivationByType(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=True)

        self.happy = 0
        self.izq = 0
        self.cent = 0
        self.der = 0
        self.op_prior = 0
        self.color_prior = 0
        self.datacollector = mesa.DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]}
        )
 
        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        agentes = []
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if(blanco[x, y] == 1):
                agent = BackgroundAgent((x, y), self, "black") #Background es de tipo -1
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
            if(blanco[x, y] == 0):
                if self.random.random() < self.density:
                    agent = SchellingAgent((x, y), self, 0, "white")
                    agentes.append(agent)
                    self.schedule.add(agent)
                    self.grid.place_agent(agent, (x, y))

        i = 0
        total = self.schedule.get_type_count(SchellingAgent)
        print(total)
        agentes = np.array(agentes)
        for i in range(self.cantidad_razas):
            subset = []
            for agente in agentes:
                if(agente.color == "white"):
                    subset.append(agente)
            aux = math.ceil(total * proporciones[i]/100)
            try: #El try es para evitar agentes sobrantes
                subset = random.sample(subset, aux)
            except:
                #aux -= 1
                counter = 1
                while True:
                    try:
                        subset = random.sample(subset, aux-counter)
                        break
                    except:
                        counter += 1
            print(i," population size:",len(subset))
            for agente in subset:
                agente.color = colors[i]
        
        self.running = True
        self.datacollector.collect(self)
        self.last_mode = self.ta
    def step(self):
        
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        #self.schedule.step_type(BackgroundAgent)
        self.happy = 0  # Reset counter of happy agents
        self.izq = 0
        self.cent = 0
        self.der = 0
        self.op_prior = 0
        self.color_prior = 0
        self.schedule.step_type(SchellingAgent)
        # collect data
        self.datacollector.collect(self)
        if self.happy == self.schedule.get_type_count(SchellingAgent):
            self.running = False


        

