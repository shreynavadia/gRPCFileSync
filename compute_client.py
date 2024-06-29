import grpc
import compute_pb2
import compute_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = compute_pb2_grpc.ComputationStub(channel)
        while True:
            print("\nSelect operation:")
            print("1. Add")
            print("2. Sort")
            print("3. Exit")
            operation = input("Enter option (1/2/3): ")

            if operation == '3':
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
                    while True:
                        result_response = stub.GetResult(compute_pb2.ResultRequest(task_id=response.task_id))
                        if result_response.HasField('add_result'):
                            print(f"Async Result: {result_response.add_result}")
                            break
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
                    while True:
                        result_response = stub.GetResult(compute_pb2.ResultRequest(task_id=response.task_id))
                        if result_response.HasField('sort_response'):
                            print(f"Async Sorted array: {result_response.sort_response.sorted_array}")
                            break

if __name__ == '__main__':
    run()
