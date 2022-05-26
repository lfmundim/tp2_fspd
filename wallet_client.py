import grpc
import wallet_routes_pb2
import wallet_routes_pb2_grpc
import sys

def wallet_get_balance(stub, wallet_id):
    wallet = stub.GetBalance(wallet_routes_pb2.Wallet(id=wallet_id))
    return wallet.total_balance

def run():
    wallet_id = 'douglas_adams'
    server_address = 'localhost:42000'
    if len(sys.argv) > 1:
        wallet_id = sys.argv[1]
        server_address = sys.argv[2]

    with grpc.insecure_channel(server_address) as channel:
        stub = wallet_routes_pb2_grpc.WalletRoutesStub(channel)
        while True:
            command = input()
            if command.casefold() == 'F'.casefold():
                break
            if command.casefold() == 'S'.casefold():
                print(wallet_get_balance(stub, wallet_id))


if __name__ == '__main__':
    run()