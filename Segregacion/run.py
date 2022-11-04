from server import server
import numpy as np
import matplotlib.pyplot as plt

server.launch()
'''
IMPORTANTE
Para la modificacion de grid en tiempo de simulacion se hace desde ModularVisualization.py dentro de class SocketHandler(tornado.websocket.WebSocketHandler)


        .
        .
        .
        elif msg["type"] == "submit_params":
            param = msg["param"]
            value = msg["value"]
            
            #START MODIFICATION
            if(param == 'ta'):
                model = self.application.model_cls 
                model_params = self.application.model_kwargs
                visualization_elements=self.application.visualization_elements
                if(value == "raza"):
                    model_params['ta'].value = 'raza'
                else:
                    model_params['ta'].value = 'opinion_politica'
                import mesa 
                news = mesa.visualization.ModularServer(
                    model,
                    visualization_elements,
                    "Segregacion",
                    model_params,
                )
                news.reset_model() 
            #END MODIFICATION

            # Is the param editable?
            if param in self.application.user_params:
                if is_user_param(self.application.model_kwargs[param]):
            .
            .
            .

'''




