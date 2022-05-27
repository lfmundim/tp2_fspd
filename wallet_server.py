from concurrent import futures
from secrets import token_bytes
import wallet_routes_pb2_grpc
import wallet_routes_pb2
import grpc
import sys

class WalletRoutesServicer(wallet_routes_pb2_grpc.WalletRoutesServicer):
    def WalletExists(self, wallet_id):
        return wallet_id in self.wallet_db

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
        if not self.WalletExists(request.wallet_id):
            return wallet_routes_pb2.PaymentOrderResponse(
                status = -1,
                secret = None
            )

        wallet_balance = self.wallet_db[request.wallet_id]
        enough_balance = wallet_balance >= request.value
        if not enough_balance:
            return wallet_routes_pb2.PaymentOrderResponse(
                status = -2,
                secret = None
            )

        secret = token_bytes(32)
        wallet_balance = wallet_balance - request.value
        self.wallet_db[request.wallet_id] = wallet_balance
        self.secret_db[secret] = request.value
        return wallet_routes_pb2.PaymentOrderResponse(
                status = 0,
                secret = secret
        )

    def GenerateTransfer(self, request, context):
        response = wallet_routes_pb2.TransferResponse()
        ordered_value = 0
        if not self.WalletExists(request.target_wallet_id):
            response.status = -1
            return response
        if request.secret not in self.secret_db:
            response.status = -2
            return response
        else:
            ordered_value = self.secret_db[request.secret]
        if ordered_value != request.value:
            response.status = -9
        else:
            wallet_balance = self.wallet_db[request.target_wallet_id]
            wallet_balance = wallet_balance + request.value
            self.wallet_db[request.target_wallet_id] = wallet_balance
            response.status = 0
            response.balance = '{:.2f}'.format(wallet_balance)

        return response



    def __init__(self, wallet_db):
        self.wallet_db = wallet_db
        self.secret_db = {}

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