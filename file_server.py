import os
import grpc
from concurrent import futures
import file_service_pb2
import file_service_pb2_grpc

UPLOAD_DIRECTORY = "uploads/"

class FileService(file_service_pb2_grpc.FileServiceServicer):
    def UploadFile(self, request, context):
        try:
            file_path = os.path.join(UPLOAD_DIRECTORY, request.name)
            with open(file_path, 'wb') as file:
                file.write(request.content)
            return file_service_pb2.FileResponse(message=f"File {request.name} uploaded successfully.")
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return file_service_pb2.FileResponse(message=f"Failed to upload file {request.name}.")

    def DeleteFile(self, request, context):
        try:
            file_path = os.path.join(UPLOAD_DIRECTORY, request.name)
            if os.path.exists(file_path):
                os.remove(file_path)
                return file_service_pb2.FileResponse(message=f"File {request.name} deleted successfully.")
            else:
                return file_service_pb2.FileResponse(message=f"File {request.name} not found.")
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return file_service_pb2.FileResponse(message=f"Failed to delete file {request.name}.")

    def RenameFile(self, request, context):
        try:
            old_file_path = os.path.join(UPLOAD_DIRECTORY, request.old_name)
            new_file_path = os.path.join(UPLOAD_DIRECTORY, request.new_name)
            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
                return file_service_pb2.FileResponse(message=f"File renamed from {request.old_name} to {request.new_name} successfully.")
            else:
                return file_service_pb2.FileResponse(message=f"File {request.old_name} not found.")
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return file_service_pb2.FileResponse(message=f"Failed to rename file {request.old_name}.")

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    start_server()
