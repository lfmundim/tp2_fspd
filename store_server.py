from concurrent import futures
import store_routes_pb2_grpc
import store_routes_pb2
import wallet_routes_pb2_grpc
import wallet_routes_pb2
import grpc
import sys
import threading

class StoreRoutesServicer(store_routes_pb2_grpc.StoreRoutesServicer):
    def GetPrice(self, request, context):
        return self.store

    def Sell(self, request, context):
        response = wallet_routes_pb2.TransferResponse()
        order = self.wallet_stub.GeneratePaymentOrder(wallet_routes_pb2.PaymentOrder(
            wallet_id = request.paying_wallet_id,
            value = self.store.price
        ))
        response.order_status = order.status
        if order.status != 0:
            response.status = order.status
        else:
            transfer_response = self.wallet_stub.GenerateTransfer(wallet_routes_pb2.Transfer(
                value = self.store.price,
                secret = order.secret,
                target_wallet_id = self.store.id
            ))
            response.status = transfer_response.status
            if transfer_response.status == 0:
                self.store.balance = float(transfer_response.balance)
        return response

    def CloseUp(self, request, context):
        self._stop_event.set()
        return self.store

    def __init__(self, price, store_id, wallet_stub, balance, stop_event):
        self.store = store_routes_pb2.Store(
            price = price,
            id = store_id,
            balance = float(balance)
        )
        self.wallet_stub = wallet_stub
        self._stop_event = stop_event


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

    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    with grpc.insecure_channel(wallet_server_address) as wallet_channel:
        stub = wallet_routes_pb2_grpc.WalletRoutesStub(wallet_channel)
        balance = stub.GetBalance(wallet_routes_pb2.Wallet(id=wallet_id)).balance
        store_routes_pb2_grpc.add_StoreRoutesServicer_to_server(
            StoreRoutesServicer(price, wallet_id, stub, balance, stop_event), server
        )
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        stop_event.wait()
        server.stop(100)


if __name__ == '__main__':
    serve()