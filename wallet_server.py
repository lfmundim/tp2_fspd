from concurrent import futures
import wallet_routes_pb2_grpc
import wallet_routes_pb2
import grpc

class WalletRoutesServicer(wallet_routes_pb2_grpc.WalletRoutesServicer):
    def GetBalance(self, request, context):
        balance = 42-int(request.id)
        if balance is None:
            return wallet_routes_pb2.Balance(total_balance=0)
        else:
            return wallet_routes_pb2.Balance(total_balance=balance)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wallet_routes_pb2_grpc.add_WalletRoutesServicer_to_server(
        WalletRoutesServicer(), server
    )
    server.add_insecure_port('[::]:42000')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()