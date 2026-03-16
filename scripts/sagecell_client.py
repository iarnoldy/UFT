#!/usr/bin/env python3
"""
SageMathCell WebSocket client for running SageMath code remotely.
Used to compute E8 structure constants without local SageMath installation.
"""

import requests
import websocket
import json
import sys


def run_sage(code, timeout=300):
    """Execute SageMath code on sagecell.sagemath.org and return output."""
    # Get kernel
    r = requests.post('https://sagecell.sagemath.org/kernel',
        data={'accepted_tos': 'true', 'code': code}, timeout=30)
    result = r.json()
    kernel_id = result['id']
    ws_url = result['ws_url']

    # Connect WebSocket
    ws = websocket.create_connection(
        f'{ws_url}kernel/{kernel_id}/channels', timeout=timeout)

    # Send execute request
    msg = {
        'header': {
            'msg_id': 'exec1',
            'msg_type': 'execute_request',
            'session': kernel_id,
        },
        'parent_header': {},
        'metadata': {},
        'content': {
            'code': code,
            'silent': False,
            'store_history': False,
        },
        'channel': 'shell',
    }
    ws.send(json.dumps(msg))

    # Collect output
    output = []
    for _ in range(10000):
        try:
            resp = ws.recv()
            data = json.loads(resp)
            mt = data.get('msg_type', '')
            if mt == 'stream':
                output.append(data['content']['text'])
            elif mt == 'execute_result':
                output.append(data['content']['data'].get('text/plain', ''))
            elif mt == 'status' and data['content']['execution_state'] == 'idle':
                break
            elif mt == 'error':
                ename = data['content']['ename']
                evalue = data['content']['evalue']
                output.append(f'ERROR: {ename}: {evalue}')
                break
        except websocket.WebSocketTimeoutException:
            output.append('[TIMEOUT]')
            break

    ws.close()
    return ''.join(output)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Read code from file
        with open(sys.argv[1], 'r') as f:
            code = f.read()
    else:
        code = 'print("SageMathCell connection test: OK")'

    result = run_sage(code)
    print(result)
