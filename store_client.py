import grpc
import store_routes_pb2
import store_routes_pb2_grpc
import sys

def store_get_price(stub):
    dummy = store_routes_pb2.Store(id='dummy')
    price = stub.GetPrice(dummy).price
    return price

def run():
    wallet_id = 'tim_cook'
    server_address = '127.0.0.1:42001'
    if len(sys.argv) > 1:
        wallet_id = sys.argv[1]
        server_address = sys.argv[2]

    with grpc.insecure_channel(server_address) as channel:
        stub = store_routes_pb2_grpc.StoreRoutesStub(channel)
        while True:
            command = input()
            if command == 'F':
                break
            if command == 'P':
                print(store_get_price(stub))
            if command == 'C':
                break



if __name__ == '__main__':
    run()