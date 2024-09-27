import requests

def get_task_data(task_id):
    url = f'https://api.external-system.com/tasks/{task_id}'
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
    response = requests.get(url, headers=headers)
    return response.json()
