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

def run():
    wallet_id = 'store'
    server_address = 'localhost:42000'
    if len(sys.argv) > 1:
        wallet_id = sys.argv[1]
        server_address = sys.argv[2]

    with grpc.insecure_channel(server_address) as channel:
        stub = wallet_routes_pb2_grpc.WalletRoutesStub(channel)
        while True:
            full_command = input()
            tokens = full_command.split()
            command = tokens[0]
            if command == 'F':
                break
            if command == 'S':
                print(wallet_get_balance(stub, wallet_id))
            if command == 'O':
                value = float(tokens[1])
                print(wallet_generate_payment_order(stub, wallet_id, value))
            if command == 'X':
                value = float(tokens[1])
                op = bytes(eval(tokens[2]))
                target = tokens[3]
                print(wallet_generate_transfer(stub, value, op, target))


if __name__ == '__main__':
    run()