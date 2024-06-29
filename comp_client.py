import grpc
import comp_service_pb2 as computation_pb2
import comp_service_pb2_grpc as computation_pb2_grpc
import threading
import time

def syncRPC(stub):
    print()
    print("Starting synchronous call to the server...")
    addRes = stub.Add(computation_pb2.AddRequest(a=12, b=7))
    print("Add result from server (Sync):", addRes.result)
    print()

    sortRes = stub.Sort(computation_pb2.SortRequest(array=[3, 1, 4, 8, 5, 9, -1]))
    print("Sort result from server (Sync):", sortRes.sorted_array)
    print()

def asyncRPC(stub):
    print("Starting asynchronous call to the server...")
    print()
    addAckAsync = stub.AddAsync(computation_pb2.AddRequest(a=12, b=7))
    sortAckAsync = stub.SortAsync(computation_pb2.SortRequest(array=[3, 1, 4, 8, 5, 9, -1]))
    
    print("Add Asynchronous Acknowledgemt:", addAckAsync.message)
    print()
    print("Sort Asynchronous Acknowledgment:", sortAckAsync.message)
    print()
    
    time.sleep(2) 

    addRes = stub.GetAddResult(computation_pb2.ResultRequest(task_id=addAckAsync.message))
    sortRes = stub.GetSortResult(computation_pb2.ResultRequest(task_id=sortAckAsync.message))
    
    print("Add result from server (Async):", addRes.result)
    print()
    print("Sort result from server (Async):", sortRes.sorted_array)
    print()
    
def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = computation_pb2_grpc.ComputationStub(channel)
    
    syncThread = threading.Thread(target=syncRPC, args=(stub,))
    asyncThread = threading.Thread(target=asyncRPC, args=(stub,))
    
    syncThread.start()
    asyncThread.start()
    
    syncThread.join()
    asyncThread.join()

if __name__ == '__main__':
    main()
