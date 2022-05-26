PROTOS = wallet_routes.proto

clean:
		rm *_pb2.py *_pb2_grpc.py

stubs:
		python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./*.proto

run_serv_banco:
		python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./*.proto
		python3 wallet_server.py $(arg1) $(arg2)

run_cli_banco:
		python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./*.proto
		python3 wallet_client.py $(arg1) $(arg2)

clearscr:
		clear

fresh: clean clearscr stubs