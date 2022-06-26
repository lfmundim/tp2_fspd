import grpc
import store_routes_pb2
import store_routes_pb2_grpc
import sys

def store_get_price(stub):
    dummy = store_routes_pb2.Store(id='dummy')
    price = stub.GetPrice(dummy).price
    return price

def store_make_purchase(stub, wallet_id):
    order = store_routes_pb2.Order(paying_wallet_id=wallet_id)
    response = stub.Sell(order)
    return response

def store_close_up(stub):
    dummy = store_routes_pb2.Store(id='dummy')
    response = stub.CloseUp(dummy)
    return response.balance

def run():
    wallet_id = 'tim_cook'
    server_address = '127.0.0.1:42001'
    if len(sys.argv) > 1:
        wallet_id = sys.argv[1]
        server_address = sys.argv[2]

    with grpc.insecure_channel(server_address) as channel:
        stub = store_routes_pb2_grpc.StoreRoutesStub(channel)
        while True:
            try:
                command = input()
                if command == 'T':
                    print(store_close_up(stub))
                    break
                if command == 'P':
                    print(store_get_price(stub))
                if command == 'C':
                    response = store_make_purchase(stub, wallet_id)
                    print(response.order_status)
                    if response.order_status == 0:
                        print(response.status)
            except EOFError:
                break


if __name__ == '__main__':
    run()
