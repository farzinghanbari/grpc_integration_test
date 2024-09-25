PROTOBUF_NAMESPACE = grpc_integration_test

build:clean
	python -m grpc_tools.protoc -I ../proto \
	--python_out=../protobuf/$(PROTOBUF_NAMESPACE)/ \
	--pyi_out=../protobuf/$(PROTOBUF_NAMESPACE)/ \
	--grpc_python_out=../protobuf/$(PROTOBUF_NAMESPACE)/ \
	$$(find ../proto/ -name "*.proto")
	sed -i -E "s/^import (\w+_pb2) as/import protobuf.$(PROTOBUF_NAMESPACE).\1 as/g" $$(find ../protobuf/  -name "*_pb2.py")
	sed -i -E "s/^import (\w+_pb2) as/import protobuf.$(PROTOBUF_NAMESPACE).\1 as/g" $$(find ../protobuf/  -name "*_pb2_grpc.py")

clean:
	$$(rm -r ../protobuf;exit 0)
	$$(mkdir -p ../protobuf/$(PROTOBUF_NAMESPACE)/)
