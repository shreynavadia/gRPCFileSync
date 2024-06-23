import asyncio
import grpc
import async_computation_service_pb2
import async_computation_service_pb2_grpc
import numpy as np
import uuid
from concurrent import futures

class ComputationServiceServicer(async_computation_service_pb2_grpc.ComputationServiceServicer):
    def __init__(self):
        self.results = {}

    async def Add(self, request, context):
        result = request.i + request.j
        return async_computation_service_pb2.AddResponse(result=result)

    async def Sort(self, request, context):
        sorted_array = np.sort(request.array)
        return async_computation_service_pb2.SortResponse(sorted_array=sorted_array.tolist())

    async def AsyncAdd(self, request, context):
        operation_id = str(uuid.uuid4())
        self.results[operation_id] = None
        asyncio.create_task(self.handle_async_add(request, operation_id))
        return async_computation_service_pb2.OperationResponse(operation_id=operation_id)

    async def AsyncSort(self, request, context):
        operation_id = str(uuid.uuid4())
        self.results[operation_id] = None
        asyncio.create_task(self.handle_async_sort(request, operation_id))
        return async_computation_service_pb2.OperationResponse(operation_id=operation_id)

    async def FetchResult(self, request, context):
        operation_id = request.operation_id
        while self.results[operation_id] is None:
            await asyncio.sleep(0.1)
        return self.results[operation_id]

    async def handle_async_add(self, request, operation_id):
        await asyncio.sleep(1)  # Simulating async operation
        result = request.i + request.j
        self.results[operation_id] = async_computation_service_pb2.FetchResponse(
            add_response=async_computation_service_pb2.AddResponse(result=result)
        )

    async def handle_async_sort(self, request, operation_id):
        await asyncio.sleep(1)  # Simulating async operation
        sorted_array = np.sort(request.array)
        self.results[operation_id] = async_computation_service_pb2.FetchResponse(
            sort_response=async_computation_service_pb2.SortResponse(sorted_array=sorted_array.tolist())
        )

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    async_computation_service_pb2_grpc.add_ComputationServiceServicer_to_server(ComputationServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Server is listening on port 50051...")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
