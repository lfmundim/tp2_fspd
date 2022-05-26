PROTOS = wallet_routes.proto

clean:
		rm *_pb2.py *_pb2_grpc.py

stubs:
		python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./*.proto