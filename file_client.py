import os
import time
import grpc
import file_service_pb2
import file_service_pb2_grpc

SYNC_FOLDER = "sync_folder/"
SERVER_ADDRESS = 'localhost:50051'

def upload_file(stub, file_name):
    with open(os.path.join(SYNC_FOLDER, file_name), 'rb') as f:
        content = f.read()
    file = file_service_pb2.File(name=file_name, content=content)
    response = stub.UploadFile(file)
    print(response.message)

def delete_file(stub, file_name):
    file = file_service_pb2.FileName(name=file_name)
    response = stub.DeleteFile(file)
    print(response.message)

def rename_file(stub, old_name, new_name):
    request = file_service_pb2.RenameRequest(old_name=old_name, new_name=new_name)
    response = stub.RenameFile(request)
    print(response.message)

def monitor_folder():
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = file_service_pb2_grpc.FileServiceStub(channel)

    last_checked = time.time()

    while True:
        time.sleep(5)
        current_files = os.listdir(SYNC_FOLDER)
        for file_name in current_files:
            file_path = os.path.join(SYNC_FOLDER, file_name)
            if os.path.getmtime(file_path) > last_checked:
                upload_file(stub, file_name)

        last_checked = time.time()

if __name__ == '__main__':
    if not os.path.exists(SYNC_FOLDER):
        os.makedirs(SYNC_FOLDER)
    monitor_folder()
