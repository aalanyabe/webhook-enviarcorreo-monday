@app.route('/webhook', methods=['POST'])
def webhook():
    task_data = request.json
    # Procesa la información de la tarea
    task_id = task_data['id']
    # Guarda la tarea en tu sistema
    save_task(task_data)
    return '', 200


# Paso 1: Recibir notificación de tarea creada
@app.route('/webhook', methods=['POST'])
def webhook():
    task_data = request.json
    task_id = task_data['id']
    save_task(task_data)  # Almacenar datos de la tarea
    return '', 200

# Paso 2: Obtener datos de la tarea
task_data = get_task_data(task_id)

# Paso 3: Actualizar datos de la tarea
updated_data = {
    'status': 'completed',
    'notes': 'Task completed successfully.'
}
update_task_data(task_id, updated_data)



from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    task_data = request.json
    # Procesa la información de la tarea
    task_id = task_data['id']
    # Guarda la tarea en tu sistema
    save_task(task_data)
    return '', 200

def save_task(task_data):
    # Lógica para guardar los datos de la tarea en tu base de datos
    print("Tarea recibida:", task_data)

if __name__ == '__main__':
    app.run(port=5000)
