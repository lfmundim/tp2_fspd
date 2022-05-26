from concurrent import futures
from secrets import token_bytes
import wallet_routes_pb2_grpc
import wallet_routes_pb2
import grpc
import sys

class WalletRoutesServicer(wallet_routes_pb2_grpc.WalletRoutesServicer):
    def GetBalance(self, request, context):
        if request.id in self.wallet_db:
            balance = self.wallet_db[request.id]
        else:
            balance = None
        if balance is None:
            return wallet_routes_pb2.Wallet(
                id=request.id,
                balance='-1'
            )
        else:
            return wallet_routes_pb2.Wallet(
                id=request.id,
                balance='{:.2f}'.format(balance)
            )

    def GeneratePaymentOrder(self, request, context):
        secret = token_bytes(32)
        if request.wallet_id not in self.wallet_db:
            return wallet_routes_pb2.PaymentOrder(
                wallet_id = request.wallet_id,
                value = request.value,
                status = -1,
                secret = secret
            )

        wallet_balance = self.wallet_db[request.wallet_id]
        enough_balance = wallet_balance >= request.value
        if not enough_balance:
            return wallet_routes_pb2.PaymentOrder(
                wallet_id = request.wallet_id,
                value = request.value,
                status = -2,
                secret = secret
            )

        wallet_balance = wallet_balance - request.value
        self.wallet_db[request.wallet_id] = wallet_balance
        self.secrets_db[secret] = request.value
        return wallet_routes_pb2.PaymentOrder(
                wallet_id = request.wallet_id,
                value = request.value,
                status = 0,
                secret = secret
        )

    def __init__(self, wallet_db):
        self.wallet_db = wallet_db
        self.secrets_db = {}

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

    wallet_db = fill_db(wallet_file)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wallet_routes_pb2_grpc.add_WalletRoutesServicer_to_server(
        WalletRoutesServicer(wallet_db), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()