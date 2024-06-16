import os
import time
import grpc
import file_service_pb2
import file_service_pb2_grpc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileDeletedEvent, FileCreatedEvent, FileMovedEvent

SYNC_FOLDER = "sync_folder/"
SERVER_ADDRESS = 'localhost:50051'

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, stub):
        self.stub = stub

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent) and not event.is_directory:
            if os.path.exists(event.src_path):
                upload_file(self.stub, event.src_path)

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent) and not event.is_directory:
            if os.path.exists(event.src_path):
                upload_file(self.stub, event.src_path)

    def on_deleted(self, event):
        if isinstance(event, FileDeletedEvent) and not event.is_directory:
            delete_file(self.stub, event.src_path)

    def on_moved(self, event):
        if isinstance(event, FileMovedEvent) and not event.is_directory:
            rename_file(self.stub, event.src_path, event.dest_path)

def upload_file(stub, file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        content = f.read()
    file = file_service_pb2.File(name=file_name, content=content)
    response = stub.UploadFile(file)
    print(response.message)

def delete_file(stub, file_path):
    file_name = os.path.basename(file_path)
    file = file_service_pb2.FileName(name=file_name)
    response = stub.DeleteFile(file)
    print(response.message)

def rename_file(stub, old_path, new_path):
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)
    request = file_service_pb2.RenameRequest(old_name=old_name, new_name=new_name)
    response = stub.RenameFile(request)
    print(response.message)

def monitor_folder():
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = file_service_pb2_grpc.FileServiceStub(channel)
    
    event_handler = FileEventHandler(stub)
    observer = Observer()
    observer.schedule(event_handler, SYNC_FOLDER, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    if not os.path.exists(SYNC_FOLDER):
        os.makedirs(SYNC_FOLDER)
    monitor_folder()
