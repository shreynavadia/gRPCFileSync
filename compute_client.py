import grpc
import compute_pb2
import compute_pb2_grpc
import threading
import time

def get_async_result(stub, task_id):
    while True:
        try:
            result_response = stub.GetResult(compute_pb2.ResultRequest(task_id=task_id))
            if result_response.HasField('add_result'):
                print(f"Async Add Result for task {task_id}: {result_response.add_result}")
                break
            elif result_response.HasField('sort_response'):
                print(f"Async Sort Result for task {task_id}: {result_response.sort_response.sorted_array}")
                break
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                time.sleep(1)
            else:
                print(f"Error fetching result for task {task_id}: {e}")
                break

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = compute_pb2_grpc.ComputationStub(channel)
        async_tasks = []

        while True:
            print("\nSelect operation:")
            print("1. Add")
            print("2. Sort")
            print("3. Check Async Results")
            print("4. Exit")
            operation = input("Enter option (1/2/3/4): ")

            if operation == '4':
                break
            elif operation == '1':
                i = int(input("Enter first number: "))
                j = int(input("Enter second number: "))
                print("Select mode:")
                print("1. Synchronous")
                print("2. Asynchronous")
                mode = input("Enter mode (1/2): ")
                if mode == '1':
                    response = stub.Add(compute_pb2.AddRequest(i=i, j=j))
                    print(f"Result: {response.result}")
                elif mode == '2':
                    response = stub.AsyncAdd(compute_pb2.AddRequest(i=i, j=j))
                    print(f"Acknowledgement with task ID: {response.task_id}")
                    async_tasks.append(response.task_id)
            elif operation == '2':
                array = list(map(int, input("Enter array elements separated by space: ").split()))
                print("Select mode:")
                print("1. Synchronous")
                print("2. Asynchronous")
                mode = input("Enter mode (1/2): ")
                if mode == '1':
                    response = stub.Sort(compute_pb2.SortRequest(array=array))
                    print(f"Sorted array: {response.sorted_array}")
                elif mode == '2':
                    response = stub.AsyncSort(compute_pb2.SortRequest(array=array))
                    print(f"Acknowledgement with task ID: {response.task_id}")
                    async_tasks.append(response.task_id)
            elif operation == '3':
                for task_id in async_tasks[:]:
                    thread = threading.Thread(target=get_async_result, args=(stub, task_id))
                    thread.start()
                    async_tasks.remove(task_id)

if __name__ == '__main__':
    run()
