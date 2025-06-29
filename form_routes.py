from flask import  Blueprint, Flask, jsonify, abort, request
from api_service import updateRating,updateComments

#Crear un blueprint para las rutas
routes = Blueprint('routes',__name__)

# Ruta para manejar respustas de formularios

@routes.route('/submit',methods = ['POST'])
def submit_form():
    data = request.json # Captura los datos enviados en JSON
    comments= data.get('comments')
    score = data.get('score')
    idTicket = data.get('idTicket')
        
    #mandar al tablero de monday
    updateRating(score,idTicket)
    updateComments(comments,idTicket)
    
    return jsonify({"mensaje":"actualizado"})
    