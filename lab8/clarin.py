import requests
import time

URL = 'http://ws.clarin-pl.eu/nlprest2/base'
UPLOAD_URL = URL + '/upload/'
START_TASK_URL = URL + '/startTask/'

LPMN = 'any2txt|wcrft2|liner2({"model":"n82"})'
USER = ''
WAIT_TIME = 2.0


def upload_data(data):
    """
    :return: file_id
    """
    return requests.post(
        url=UPLOAD_URL,
        data=data.encode('utf-8'),
        headers={
            'Content-Type': 'binary/octet-stream'
        },
    ).text


def start_task(file_id):
    """
    :return: task_id
    """
    return requests.post(
        url=START_TASK_URL,
        json={
            'lpmn': LPMN,
            'file': file_id,
            'user': USER,
        },
        headers={
            'Content-Type': 'application/json'
        }
    ).text


def get_status(task_id):
    """
    :return: (status_name, status_data)
    status_name in: (QUEUE, PROCESSING, DONE, ERROR)
    """
    data = requests.get(
        url="{}/getStatus/{}".format(URL, task_id)
    ).json()
    return data['status'], data


def download_processed_data(file_id):
    return requests.get(
        url="{}/download{}".format(URL, file_id)
    ).text


def process(data):
    file_id = upload_data(data)
    task_id = start_task(file_id)

    status, status_data = get_status(task_id)

    while status in ('QUEUE', 'PROCESSING'):
        time.sleep(WAIT_TIME)
        status, status_data = get_status(task_id)

    if status == 'DONE' and status_data['value']:
        file_id = status_data['value'][0]['fileID']
        return download_processed_data(file_id)
    else:
        print('Error: ', status_data['value'])
