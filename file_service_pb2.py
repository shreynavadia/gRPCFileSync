# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x66ile_service.proto\"%\n\x04\x46ile\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\x18\n\x08\x46ileName\x12\x0c\n\x04name\x18\x01 \x01(\t\"3\n\rRenameRequest\x12\x10\n\x08old_name\x18\x01 \x01(\t\x12\x10\n\x08new_name\x18\x02 \x01(\t\"\x1f\n\x0c\x46ileResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\x86\x01\n\x0b\x46ileService\x12\"\n\nUploadFile\x12\x05.File\x1a\r.FileResponse\x12&\n\nDeleteFile\x12\t.FileName\x1a\r.FileResponse\x12+\n\nRenameFile\x12\x0e.RenameRequest\x1a\r.FileResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'file_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FILE']._serialized_start=22
  _globals['_FILE']._serialized_end=59
  _globals['_FILENAME']._serialized_start=61
  _globals['_FILENAME']._serialized_end=85
  _globals['_RENAMEREQUEST']._serialized_start=87
  _globals['_RENAMEREQUEST']._serialized_end=138
  _globals['_FILERESPONSE']._serialized_start=140
  _globals['_FILERESPONSE']._serialized_end=171
  _globals['_FILESERVICE']._serialized_start=174
  _globals['_FILESERVICE']._serialized_end=308
# @@protoc_insertion_point(module_scope)
