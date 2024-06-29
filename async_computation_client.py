import asyncio
import grpc
import async_computation_service_pb2
import async_computation_service_pb2_grpc

async def send_async_request(stub, request_type, *args):
    if request_type == 'add':
        response = await stub.AsyncAdd(async_computation_service_pb2.AddRequest(i=args[0], j=args[1]))
    elif request_type == 'sort':
        response = await stub.AsyncSort(async_computation_service_pb2.SortRequest(array=args[0]))
    return response.operation_id

async def fetch_result(stub, operation_id):
    while True:
        response = await stub.FetchResult(async_computation_service_pb2.FetchRequest(operation_id=operation_id))
        if response.HasField('add_response') or response.HasField('sort_response'):
            return response

async def main():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = async_computation_service_pb2_grpc.ComputationServiceStub(channel)
        
        while True:
            print("Choose an option:")
            print("1. Add two numbers")
            print("2. Sort an array")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                val1, val2 = map(int, input("Enter two numbers separated by space: ").split())
                operation_id = await send_async_request(stub, 'add', val1, val2)
                print(f"Async Add Acknowledgment: Operation {operation_id} received")
                result = await fetch_result(stub, operation_id)
                print(f"Fetched Async Add result: {result.add_response.result}")

            elif choice == "2":
                values = list(map(int, input("Enter numbers separated by space: ").split()))
                operation_id = await send_async_request(stub, 'sort', values)
                print(f"Async Sort Acknowledgment: Operation {operation_id} received")
                result = await fetch_result(stub, operation_id)
                print(f"Fetched Async Sort result: {result.sort_response.sorted_array}")

            elif choice == "3":
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
