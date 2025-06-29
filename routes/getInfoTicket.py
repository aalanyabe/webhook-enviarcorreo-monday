from flask import jsonify,abort,request,Blueprint
from dotenv import load_dotenv
import os, json

from services.sendMailTemplate import EnviarMail
from services.monday_api import get_data_item,load_board_config

routes = Blueprint('routes', __name__)  # Crear blueprint


load_dotenv(".env.production")

@routes.route('/webhookTicketCerrado', methods = ['POST'])
def webhook():
    
    if request.method == 'POST':
        data = request.json
        if "challenge" in data:
            return jsonify({"challenge": data["challenge"]}),200
        
        try:
            # Carga configuración general
            BOARD_CONFIG  = load_board_config()
            # print(f'este es board config: {BOARD_CONFIG}')
            # print(f"Received data webhook: {data}")
            # return jsonify(request.json),200
            id_board = data.get("event",()).get("boardId") #Este es del webHook
            
            cfg = BOARD_CONFIG.get(str(id_board))
            print("📦 ID board recibido:", cfg)
            if not cfg:
                return jsonify({"Error":"Tablero no configurado "}),400
            
            # Extrae los IDs de columnas desde la configuración
            columnIdCal = cfg["col_rating"]
            columnIdComent = cfg["col_comment"]
            idBoardConf = cfg
            area=cfg["area"]
            correo_id=cfg["correo"]
            usuario_id =cfg["usuario"]
            idTicket =cfg["itTicket"]
            
            id_item = data.get("event",()).get("pulseId") 
            print(f'id of the identified item: {id_item}')
    
            #  Validación: ¿existen valores configurados?
            if not all([correo_id, usuario_id, idTicket]):
                return jsonify({"error": "Configuración incompleta en tablero de configuración"}), 400
            
            # Obtiene datos del item desde Monday
            getDataItem = get_data_item(id_item)
            # print(f'getDataItem: {get_data_item}')
            getDataItemDict = json.loads(getDataItem)
            result = {}
            columns = getDataItemDict.get("data",{}).get("items",[])[0].get("column_values",[])
            subject = getDataItemDict.get("data",{}).get("items",[])[0].get("name")
            # print(f'valores columnas: {columns}')
            result["subject"] = subject
            
            # Validación: ¿existen esos IDs en el item?
            ids_columnas_item = {col["id"] for col in columns}
            ids_configurados = [correo_id, usuario_id, idTicket]
            ids_faltantes = [cid for cid in ids_configurados if cid not in ids_columnas_item]
            if ids_faltantes:
                return jsonify({
                    "error": "IDs de columna configurados no se encuentran en el ítem",
                    "ids_faltantes": ids_faltantes
                }), 400
                
            for column in columns:
                # print(f'valor column: {column}')
                # print (f'el valor del usuario en en el FOR ES: {usuario_id}')
                # print (f'el valor del IDTICKE en en el FOR ES: {idTicket}')
                if column.get("id")==usuario_id:
                    result["usuario"] = column["text"] 
                elif column.get("id")==correo_id:
                    result["correo"]= column["text"]
                elif column.get("id")==idTicket:
                    result["idTicket"]= column["text"]
            print(f' el resultado es: {result}') 
            
            # Validación: ¿faltan valores antes de enviar?
            if not all([result.get("usuario"), result.get("correo"), result.get("idTicket")]):
                return jsonify({"error": "Faltan datos del ítem para enviar correo"}), 400
            
            EnviarMail(
                result.get("usuario"),
                result.get("idTicket"),
                result.get("subject"),
                result.get("correo"),
                columnIdCal,
                columnIdComent,
                id_board,
                area)
            return jsonify({"mensaje": "enviado correctamente"}), 200
            
        except Exception as e:
            print("❌ Error en webhook:", e)
            return jsonify({"error": str(e)}), 500        
                                    
    else:
        abort(400)
