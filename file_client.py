import os
import time
import grpc
import file_service_pb2
import file_service_pb2_grpc

SYNC_FOLDER = "sync_folder/"
SERVER_ADDRESS = 'localhost:50051'

def upload_file(stub, file_name):
    file_path = os.path.join(SYNC_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        file = file_service_pb2.File(name=file_name, content=content)
        response = stub.UploadFile(file)
        print(response.message)
    else:
        print(f"File {file_name} no longer exists.")

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

    previous_files = set(os.listdir(SYNC_FOLDER))
    file_mod_times = {file: os.path.getmtime(os.path.join(SYNC_FOLDER, file)) for file in previous_files}

    while True:
        time.sleep(5)
        current_files = set(os.listdir(SYNC_FOLDER))
        current_mod_times = {file: os.path.getmtime(os.path.join(SYNC_FOLDER, file)) for file in current_files}

        # Check for deleted files
        deleted_files = previous_files - current_files
        for file_name in deleted_files:
            delete_file(stub, file_name)

        # Check for new or modified files
        for file_name in current_files:
            if file_name not in previous_files:
                upload_file(stub, file_name)
            elif file_mod_times.get(file_name) != current_mod_times.get(file_name):
                upload_file(stub, file_name)

        # Update the state for the next iteration
        previous_files = current_files
        file_mod_times = current_mod_times

if __name__ == '__main__':
    if not os.path.exists(SYNC_FOLDER):
        os.makedirs(SYNC_FOLDER)
    monitor_folder()
