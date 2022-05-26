import grpc
import wallet_routes_pb2
import wallet_routes_pb2_grpc
import sys

def wallet_get_balance(stub, wallet_id):
    balance = stub.GetBalance(wallet_routes_pb2.Wallet(id=wallet_id))
    return balance.total_balance

def run():
    wallet_id = sys.argv[1] or 'douglas_adams'
    server_address = sys.argv[2] or 'localhost:42000'
    with grpc.insecure_channel(server_address) as channel:
        stub = wallet_routes_pb2_grpc.WalletRoutesStub(channel)
        while True:
            wallet_id = input()
            if wallet_id == 'F':
                break
            print(wallet_get_balance(stub, wallet_id))


if __name__ == '__main__':
    run()