import mesa
from PIL import Image
from numpy import asarray
from model import Schelling
from model import SchellingAgent
from model import global_ta
import numpy as np
import matplotlib.pyplot as plt
import random
#pon un brief o q
def numbers_summ_to_100(n):
    a = list(np.random.multinomial(100, np.ones(n)/n).flatten())
    return [int(element) for element in a]

def get_happy_agents(model):
    return f"Happy agents: {model.happy}"
def get_count_agents(model):
    return f"Total agents: {model.schedule.get_type_count(SchellingAgent)}"
def get_izq_agents(model):
    return f"Agentes de izquierda(silver): {model.izq}"
def get_cent_agents(model):
    return f"Agentes de centro(fuchsia): {model.cent}"
def get_der_agents(model):
    return f"Agentes de derecha(aqua): {model.der}"

def get_op_prior(model):
    return f"Agentes que priorizar la opinion politica: {model.op_prior}"
def get_color_prior(model):
    return f"Agentes que priorizar la raza: {model.color_prior}"
def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    try: #schelling agent
        if(str(agent.priority)[0] == 'c'):
            text = 'r'
        else:
            text = 'o'
        if(global_ta.a == 'opinion_politica'):
            if(agent.happy == 0):
                portrayal = {"Shape": "circle","r": 0.7, "text": text,"text_color":"black", "Filled": "true", "Layer": 0}
            if(agent.happy == 1):
                portrayal = {"Shape": "rect","w": 1, "h": 1, "text": text,"text_color":"black","Filled": "true", "Layer": 0}  
            if(agent.discrete_opinion == 'izq'):
                portrayal["Color"] = ['Silver']
                portrayal["stroke_color"] = 'Silver'
            if(agent.discrete_opinion == 'cent'):
                portrayal["Color"] = ['Fuchsia']
                portrayal["stroke_color"] = 'Fuchsia'
            if(agent.discrete_opinion == 'der'):
                portrayal["Color"] = ['Aqua']
                portrayal["stroke_color"] = 'Aqua'
        elif(global_ta.a == 'raza'):
            if(agent.happy == 0):
                portrayal = {"Shape": "circle", "r": 0.7, "text":  text,"text_color":"black","Filled": "true", "Layer": 0}
            if(agent.happy == 1):
                portrayal = {"Shape": "rect","w": 1, "h": 1, "text":  text,"text_color":"black","Filled": "true", "Layer": 0}  
            portrayal["Color"] = [agent.color]
            portrayal["stroke_color"] = agent.color
        return portrayal
    except: #background
        portrayal = {"Shape": "rect","w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#00A8FF", "#00A8FF"]
        return portrayal




happy_chart = mesa.visualization.ChartModule([{"Label": "happy", "Color": "Black"}], data_collector_name="datacollector")

mapas = ['circulo_2.jpg', 'mexico_2.jpg', 'cuadrado_2.jpg', 'usa.jpg']
cantidad_razas_random = random.randint(2,5)
mapa_random = random.randint(0, len(mapas)-1)
a = numbers_summ_to_100(cantidad_razas_random)

model_params = {
    "height": 50,
    "width": 50,
    "density": mesa.visualization.Slider("Agent density", 0.6, 0.1, 0.9, 0.1),
    "similar_wanted": mesa.visualization.Slider("%-similar_wanted", 50, 0, 100, 1),
    "cantidad_razas": mesa.visualization.Slider("cantidad_razas", cantidad_razas_random, 2, 5, 1),
    "mapa": mesa.visualization.Choice(  "Mapa",
                                        value=mapas[mapa_random],
                                        choices=mapas),
    "ta": mesa.visualization.Choice(  "Tipo de segregacion",
                                        value='opinion_politica',
                                        choices=['raza', 'opinion_politica']),
    "p1": mesa.visualization.NumberInput("Proporcion raza 1 (red)", value = a[0]),
    "p2": mesa.visualization.NumberInput("Proporcion raza 2 (green)", value = a[1]),
    "p3": mesa.visualization.NumberInput("Proporcion raza 3 (yellow)", value = a[2] if len(a) >= 3 else 0),
    "p4": mesa.visualization.NumberInput("Proporcion raza 4 (blue)", value = a[3] if len(a) >= 4 else 0),
    "p5": mesa.visualization.NumberInput("Proporcion raza 5 (orange)", value = a[4] if len(a) >= 5 else 0)
}


canvas_element = mesa.visualization.CanvasGrid(schelling_draw, 50, 50, 700, 700)

server = mesa.visualization.ModularServer(
    Schelling,
    [canvas_element, get_happy_agents,get_count_agents,get_izq_agents,get_cent_agents, get_der_agents, get_op_prior, get_color_prior,  happy_chart],
    "Segregacion",
    model_params,
)



