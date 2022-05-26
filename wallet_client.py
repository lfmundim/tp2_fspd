import grpc
import wallet_routes_pb2
import wallet_routes_pb2_grpc

def wallet_get_balance(stub):
    balance = stub.GetBalance(wallet_routes_pb2.Wallet(id="douglas_adams"))
    return balance.total_balance

def run():
    with grpc.insecure_channel('localhost:42000') as channel:
        stub = wallet_routes_pb2_grpc.WalletRoutesStub(channel)
        print("-------------- GetBalance --------------")
        print(wallet_get_balance(stub))


if __name__ == '__main__':
    run()