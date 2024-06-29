import grpc
from concurrent import futures
import time
import compute_pb2
import compute_pb2_grpc
import threading

class ComputationServicer(compute_pb2_grpc.ComputationServicer):
    def __init__(self):
        self.results = {}
        self.lock = threading.Lock()
        self.task_id = 0

    def Add(self, request, context):
        result = request.i + request.j
        return compute_pb2.AddResponse(result=result)

    def Sort(self, request, context):
        sorted_array = sorted(request.array)
        return compute_pb2.SortResponse(sorted_array=sorted_array)

    def AsyncAdd(self, request, context):
        self.task_id += 1
        task_id = self.task_id
        threading.Thread(target=self._async_add, args=(request.i, request.j, task_id)).start()
        return compute_pb2.AsyncResponse(message="Acknowledged", task_id=task_id)

    def _async_add(self, i, j, task_id):
        result = i + j
        with self.lock:
            self.results[task_id] = compute_pb2.ResultResponse(add_result=result)

    def AsyncSort(self, request, context):
        self.task_id += 1
        task_id = self.task_id
        threading.Thread(target=self._async_sort, args=(request.array, task_id)).start()
        return compute_pb2.AsyncResponse(message="Acknowledged", task_id=task_id)

    def _async_sort(self, array, task_id):
        sorted_array = sorted(array)
        with self.lock:
            self.results[task_id] = compute_pb2.ResultResponse(sort_response=compute_pb2.SortResponse(sorted_array=sorted_array))

    def GetResult(self, request, context):
        with self.lock:
            result = self.results.get(request.task_id, None)
        if result:
            return result
        else:
            context.set_details('Result not ready')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return compute_pb2.ResultResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    compute_pb2_grpc.add_ComputationServicer_to_server(ComputationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
