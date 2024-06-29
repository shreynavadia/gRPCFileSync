from concurrent import futures
import grpc
import time
import comp_service_pb2 as computation_pb2
import comp_service_pb2_grpc as computation_pb2_grpc
import uuid

class ComputationServicer(computation_pb2_grpc.ComputationServicer):
    def __init__(self):
        self.results = {}

    def Sort(self, request, context):
        sortedArr = sorted(request.array)
        return computation_pb2.SortResponse(sorted_array=sortedArr)

    def Add(self, request, context):
        res = request.a + request.b
        return computation_pb2.AddResponse(result=res)

    def AddAsync(self, request, context):
        taskId = str(uuid.uuid4())
        res = request.a + request.b
        self.results[taskId] = computation_pb2.AddResponse(result=res)
        return computation_pb2.AckResponse(message=taskId)

    def SortAsync(self, request, context):
        taskId = str(uuid.uuid4())
        sortedArr = sorted(request.array)
        self.results[taskId] = computation_pb2.SortResponse(sorted_array=sortedArr)
        return computation_pb2.AckResponse(message=taskId)

    def GetSortResult(self, request, context):
        taskId = request.task_id
        if taskId in self.results:
            return self.results.pop(taskId)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Task not found')
            return computation_pb2.SortResponse()

    def GetAddResult(self, request, context):
        taskId = request.task_id
        if taskId in self.results:
            return self.results.pop(taskId)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Task not found')
            return computation_pb2.AddResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computation_pb2_grpc.add_ComputationServicer_to_server(ComputationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
