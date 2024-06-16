# gRPC File Sync Service

A simple gRPC-based service for uploading, deleting, and renaming files, with automatic synchronization similar to Dropbox.

## Features

- **Upload**: Upload files to the server.
- **Delete**: Delete files from the server.
- **Rename**: Rename files on the server.
- **Auto-Sync**: Automatically sync files between client and server.

## Prerequisites

- Python 3.6+
- `pip` package manager

## Installation

1. **Clone the Repo**:
    ```sh
    git clone https://github.com/<your-username>/gRPCFileSync.git
    cd gRPCFileSync
    ```

2. **Set Up Virtual Environment (Optional)**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Generate gRPC Code**:
    ```sh
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file_service.proto
    ```

## Usage

### Run the Server

1. **Create Upload Folder**:
    ```sh
    mkdir -p uploads
    ```

2. **Start Server**:
    ```sh
    python file_server.py
    ```

### Run the Client

1. **Create Sync Folder**:
    ```sh
    mkdir -p sync_folder
    ```

2. **Start Client**:
    ```sh
    python file_client.py
    ```

## File Operations

- **Upload**: Add a file to `sync_folder`.
- **Delete**: Remove a file from `sync_folder`.
- **Rename**: Rename a file in `sync_folder`.

## Stopping

- **Server**: Press `Ctrl + C` in the terminal.
- **Client**: Press `Ctrl + C` in the terminal.

## Project Structure

```plaintext
gRPCFileSync/
├── file_client.py
├── file_server.py
├── file_service.proto
├── requirements.txt
├── uploads/
└── sync_folder/
