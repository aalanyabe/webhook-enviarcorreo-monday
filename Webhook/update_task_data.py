def update_task_data(task_id, updated_data):
    url = f'https://api.external-system.com/tasks/{task_id}'
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN', 'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, json=updated_data)
    return response.json()
