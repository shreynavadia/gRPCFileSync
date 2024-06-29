from concurrent import futures
import grpc
import computation_service_pb2
import computation_service_pb2_grpc
import numpy as np

class ComputationServiceServicer(computation_service_pb2_grpc.ComputationServiceServicer):
    def Add(self, request, context):
        result = request.i + request.j
        return computation_service_pb2.AddResponse(result=result)

    def Sort(self, request, context):
        sorted_array = np.sort(request.array)
        return computation_service_pb2.SortResponse(sorted_array=sorted_array.tolist())

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computation_service_pb2_grpc.add_ComputationServiceServicer_to_server(ComputationServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is listening on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
