DIR=proto/generated
rm -rf $DIR
mkdir $DIR
python -m grpc_tools.protoc -Iproto --python_out=$DIR --grpc_python_out=$DIR game_controller.proto
sed -ie 's|import game_controller_pb2|import proto.generated.game_controller_pb2|' $DIR/game_controller_pb2_grpc.py