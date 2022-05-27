from concurrent import futures
import store_routes_pb2_grpc
import store_routes_pb2
import grpc
import sys

class StoreRoutesServicer(store_routes_pb2_grpc.StoreRoutesServicer):
    def GetPrice(self, request, context):
        return self.store

    def Sell(self, request, context):
        return super().Sell(request, context)

    def CloseUp(self, request, context):
        return super().CloseUp(request, context)

    def __init__(self, price, store_id):
        self.store = store_routes_pb2.Store(
            price = price,
            id = store_id,
            balance = 0
        )


def serve():
    port = 42001
    price = 10
    wallet_id = 'store'
    wallet_server_address = '127.0.0.1:42000'
    if(len(sys.argv) > 1):
        price = sys.argv[1]
        port = sys.argv[2]
        wallet_id = sys.argv[3]
        wallet_server_address = sys.argv[4]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_routes_pb2_grpc.add_StoreRoutesServicer_to_server(
        StoreRoutesServicer(price, wallet_id), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()