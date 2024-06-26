import asyncio
import json
import socket
from blockchain import Blockchain, Block, Transaction

MY_ADDRESS = socket.gethostbyname(socket.gethostname())
opened = []
connected = []
check = []
checked = []
checking = False
temp_chain = Blockchain()

async def handle_handshake(message, writer):
    nodes = message['data']['nodes']
    nodes.insert(0, MY_ADDRESS)
    for node in nodes:
        if node in opened:
            print("Node already exists.")
        elif node == MY_ADDRESS:
            print("This is my address.")
        else:
            opened.append(node)
            try:
                reader, writer = await asyncio.open_connection(node, 8888)
                message = json.dumps({'type': 'HANDSHAKE', 'data': {'nodes': nodes}})
                writer.write(message.encode())
                connected.append(node)
                writer.close()
            except ConnectionRefusedError:
                print(f"Connection to {node} failed.")

async def handle_create(message, writer):
    transaction_data = message['data']
    transaction = Transaction(transaction_data['sender'], transaction_data['recipient'], transaction_data['amount'], transaction_data['data'])
    temp_chain.add_transaction(transaction)

async def handle_add(message, writer):
    new_block_data = message['data']
    new_block = Block(
        index=new_block_data['index'],
        timestamp=new_block_data['timestamp'],
        transactions=new_block_data['transactions'],
        previous_hash=new_block_data['previous_hash']
    )
    
    # Add the new block to the blockchain
    if temp_chain.add_block(new_block):
        print("New block added to the blockchain.")
        response_message = json.dumps({'type': 'ADD_SUCCESS', 'data': 'New block added successfully.'})
    else:
        print("Failed to add new block to the blockchain.")
        response_message = json.dumps({'type': 'ADD_ERROR', 'data': 'Failed to add new block.'})
    
    writer.write(response_message.encode())
    await writer.drain()
    writer.close()

async def handle_request_check(message, writer):
    for i in range(len(temp_chain.chain)):
        message = json.dumps({'type': 'SEND_CHAIN', 'data': {'block': temp_chain.chain[i].__dict__, 'finished': i == len(temp_chain.chain) - 1}})
        writer.write(message.encode())
        await writer.drain()
    writer.close()

async def handle_request_info(message, writer):
    message = json.dumps({'type': 'SEND_INFO', 'data': {'difficulty': temp_chain.difficulty, 'pending_transactions': [tx.__dict__ for tx in temp_chain.pending_transactions]}})
    writer.write(message.encode())
    await writer.drain()
    writer.close()

async def handle_send_check(message):
    if checking:
        check.append(message['data'])

async def start_listen():
    server = await asyncio.start_server(handle_message, MY_ADDRESS, 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

async def handle_message(reader, writer):
    data = await reader.read()
    message = json.loads(data.decode('utf-8'))
    message_type = message['type']
    if message_type == "HANDSHAKE":
        await handle_handshake(message, writer)
    elif message_type == "CREATE":
        await handle_create(message, writer)
    elif message_type == "ADD":
        await handle_add(message, writer)
    elif message_type == "REQUEST_CHAIN":
        await handle_request_check(message, writer)
    elif message_type == "SEND_CHAIN":
        await handle_send_check(message)
    elif message_type == "REQUEST_INFO":
        await handle_request_info(message, writer)
    elif message_type == "SEND_INFO":
        await handle_send_check(message)

if __name__ == "__main__":
    asyncio.run(start_listen())
