import grpc
import computation_service_pb2
import computation_service_pb2_grpc

class ComputationClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = computation_service_pb2_grpc.ComputationServiceStub(self.channel)

    def add(self, i, j):
        response = self.stub.Add(computation_service_pb2.AddRequest(i=i, j=j))
        return response.result

    def sort(self, A):
        response = self.stub.Sort(computation_service_pb2.SortRequest(array=A))
        return response.sorted_array

def main():
    client = ComputationClient()

    while True:
        print("Choose an option:")
        print("1. Add two numbers")
        print("2. Sort an array")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            i = int(input("Enter the first number: "))
            j = int(input("Enter the second number: "))
            result = client.add(i, j)
            print(f"Result of {i} + {j} = {result}")
        elif choice == "2":
            A = input("Enter an array of numbers separated by spaces: ")
            A = [int(x) for x in A.split()]
            result = client.sort(A)
            print(f"Sorted array: {result}")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
