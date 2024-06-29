import grpc
import computation_pb2
import computation_pb2_grpc
import threading
import time

def fetch_async_result(stub, task_id):
    while True:
        try:
            result_response = stub.RetrieveResult(computation_pb2.ResultQuery(task_id=task_id))
            if result_response.HasField('addition_result'):
                print(f"Async Addition Result for task {task_id}: {result_response.addition_result}")
                break
            elif result_response.HasField('sorting_result'):
                print(f"Async Sorting Result for task {task_id}: {result_response.sorting_result.sorted_numbers}")
                break
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                time.sleep(1)
            else:
                print(f"Error fetching result for task {task_id}: {e}")
                break

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = computation_pb2_grpc.ComputationStub(channel)
        async_tasks = []

        while True:
            print("\nChoose operation:")
            print("1. Addition")
            print("2. Sorting")
            print("3. Check Async Results")
            print("4. Exit")
            operation = input("Enter option (1/2/3/4): ")

            if operation == '4':
                break
            elif operation == '1':
                num1 = int(input("Enter first number: "))
                num2 = int(input("Enter second number: "))
                print("Choose mode:")
                print("1. Synchronous")
                print("2. Asynchronous")
                mode = input("Enter mode (1/2): ")
                if mode == '1':
                    response = stub.Addition(computation_pb2.AdditionRequest(num1=num1, num2=num2))
                    print(f"Result: {response.sum}")
                elif mode == '2':
                    response = stub.AsyncAddition(computation_pb2.AdditionRequest(num1=num1, num2=num2))
                    print(f"Task started with task ID: {response.task_id}")
                    async_tasks.append(response.task_id)
            elif operation == '2':
                numbers = list(map(int, input("Enter array elements separated by space: ").split()))
                print("Choose mode:")
                print("1. Synchronous")
                print("2. Asynchronous")
                mode = input("Enter mode (1/2): ")
                if mode == '1':
                    response = stub.Sorting(computation_pb2.SortingRequest(numbers=numbers))
                    print(f"Sorted numbers: {response.sorted_numbers}")
                elif mode == '2':
                    response = stub.AsyncSorting(computation_pb2.SortingRequest(numbers=numbers))
                    print(f"Task started with task ID: {response.task_id}")
                    async_tasks.append(response.task_id)
            elif operation == '3':
                if not async_tasks:
                    print("No asynchronous tasks to check.")
                else:
                    for task_id in async_tasks[:]:
                        thread = threading.Thread(target=fetch_async_result, args=(stub, task_id))
                        thread.start()
                        async_tasks.remove(task_id)

if __name__ == '__main__':
    run()
