import grpc
from concurrent import futures
import time
import computation_pb2
import computation_pb2_grpc
import threading

class ComputationService(computation_pb2_grpc.ComputationServicer):
    def __init__(self):
        self.task_results = {}
        self.lock = threading.Lock()
        self.current_task_id = 0

    def Addition(self, request, context):
        sum_result = request.num1 + request.num2
        return computation_pb2.AdditionResponse(sum=sum_result)

    def AsyncAddition(self, request, context):
        with self.lock:
            self.current_task_id += 1
            task_id = self.current_task_id
        threading.Thread(target=self._perform_async_addition, args=(request.num1, request.num2, task_id)).start()
        return computation_pb2.AsyncTaskResponse(status="Task started", task_id=task_id)

    def Sorting(self, request, context):
        sorted_numbers = sorted(request.numbers)
        return computation_pb2.SortingResponse(sorted_numbers=sorted_numbers)

    def RetrieveResult(self, request, context):
        with self.lock:
            result = self.task_results.get(request.task_id, None)
        if result:
            return result
        else:
            context.set_details('Result not available')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return computation_pb2.ResultQueryResponse()

    def AsyncSorting(self, request, context):
        with self.lock:
            self.current_task_id += 1
            task_id = self.current_task_id
        threading.Thread(target=self._perform_async_sorting, args=(request.numbers, task_id)).start()
        return computation_pb2.AsyncTaskResponse(status="Task started", task_id=task_id)

    def _perform_async_addition(self, num1, num2, task_id):
        result = num1 + num2
        with self.lock:
            self.task_results[task_id] = computation_pb2.ResultQueryResponse(addition_result=result)

    def _perform_async_sorting(self, numbers, task_id):
        sorted_numbers = sorted(numbers)
        with self.lock:
            self.task_results[task_id] = computation_pb2.ResultQueryResponse(sorting_result=computation_pb2.SortingResponse(sorted_numbers=sorted_numbers))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computation_pb2_grpc.add_ComputationServicer_to_server(ComputationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
