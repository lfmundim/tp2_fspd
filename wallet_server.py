from concurrent import futures
import wallet_routes_pb2_grpc
import wallet_routes_pb2
import grpc
import sys

class WalletRoutesServicer(wallet_routes_pb2_grpc.WalletRoutesServicer):
    def GetBalance(self, request, context):
        if request.id in self.db:
            balance = self.db[request.id]
        else:
            balance = None
        if balance is None:
            return wallet_routes_pb2.Wallet(
                id=request.id,
                total_balance='-1'
            )
        else:
            return wallet_routes_pb2.Wallet(
                id=request.id,
                total_balance='{:.2f}'.format(balance)
            )

    def __init__(self, db):
        self.db = db

def fill_db(wallet_file):
    file = open(wallet_file, 'r')
    db = {}
    for line in file:
        tokens = line.split()
        db[tokens[0]] = float(tokens[1])
    file.close()
    return db


def serve():
    port = 42000
    wallet_file = 'wallets.txt'
    if len(sys.argv) > 1:
        port = sys.argv[1]
        wallet_file = sys.argv[2]

    db = fill_db(wallet_file)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wallet_routes_pb2_grpc.add_WalletRoutesServicer_to_server(
        WalletRoutesServicer(db), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()