import grpc
import wallet_routes_pb2
import wallet_routes_pb2_grpc
import sys

def wallet_get_balance(stub, wallet_id):
    wallet = stub.GetBalance(wallet_routes_pb2.Wallet(id=wallet_id))
    return wallet.balance

def wallet_generate_payment_order(stub, wallet_id, value):
    payment_order = stub.GeneratePaymentOrder(wallet_routes_pb2.PaymentOrder(
        wallet_id = wallet_id,
        value = value
    ))
    return [payment_order.status, payment_order.secret]

def wallet_generate_transfer(stub, value, op, target):
    transfer = wallet_routes_pb2.Transfer(
        target_wallet_id = target,
        value = value,
        secret = op
    )
    response = stub.GenerateTransfer(transfer)
    return [response.status, response.balance]

def wallet_close_up(stub):
    wallet = wallet_routes_pb2.Wallet(id="dummy")
    stub.CloseUp(wallet)

def run():
    wallet_id = 'store'
    server_address = 'localhost:42000'
    if len(sys.argv) > 1:
        wallet_id = sys.argv[1]
        server_address = sys.argv[2]

    secrets = {}
    op_index = 1

    with grpc.insecure_channel(server_address) as channel:
        stub = wallet_routes_pb2_grpc.WalletRoutesStub(channel)
        while True:
            try:
                full_command = input()
                tokens = full_command.split()
                command = tokens[0]
                if command == 'F':
                    wallet_close_up(stub)
                    break
                if command == 'S':
                    print(wallet_get_balance(stub, wallet_id))
                if command == 'O':
                    value = int(tokens[1])
                    response = wallet_generate_payment_order(stub, wallet_id, value)
                    secrets[op_index] = response[1]
                    print(op_index)
                    op_index = op_index+1
                if command == 'X':
                    value = int(tokens[1])
                    op = int(tokens[2])
                    target = tokens[3]
                    if op not in secrets.keys():
                        print(-2)
                    else:
                        response = wallet_generate_transfer(stub, value, secrets[op], target)
                        if response[0] == 0:
                            secrets.pop(op)
                            print(response[1])
                        else:
                            print(response[0])
            except EOFError:
                break


if __name__ == '__main__':
    run()