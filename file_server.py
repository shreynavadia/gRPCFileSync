import os
import grpc
from concurrent import futures
import file_service_pb2
import file_service_pb2_grpc

UPLOAD_FOLDER = "uploads/"

class FileServiceServicer(file_service_pb2_grpc.FileServiceServicer):
    def UploadFile(self, request, context):
        file_path = os.path.join(UPLOAD_FOLDER, request.name)
        with open(file_path, 'wb') as f:
            f.write(request.content)
        return file_service_pb2.FileResponse(message=f"File {request.name} uploaded successfully.")

    def DeleteFile(self, request, context):
        file_path = os.path.join(UPLOAD_FOLDER, request.name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return file_service_pb2.FileResponse(message=f"File {request.name} deleted successfully.")
        else:
            return file_service_pb2.FileResponse(message=f"File {request.name} not found.")

    def RenameFile(self, request, context):
        old_file_path = os.path.join(UPLOAD_FOLDER, request.old_name)
        new_file_path = os.path.join(UPLOAD_FOLDER, request.new_name)
        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            return file_service_pb2.FileResponse(message=f"File renamed from {request.old_name} to {request.new_name} successfully.")
        else:
            return file_service_pb2.FileResponse(message=f"File {request.old_name} not found.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    serve()
