# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tag_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11tag_service.proto\x12\x0btag_service\x1a\x1bgoogle/protobuf/empty.proto\"\x15\n\x04GUID\x12\r\n\x05value\x18\x01 \x01(\t\"Y\n\x08TagModel\x12\x1f\n\x04guid\x18\x01 \x01(\x0b\x32\x11.tag_service.GUID\x12\x0f\n\x07\x63lub_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\r\n\x05\x63olor\x18\x04 \x01(\t\".\n\x07TagList\x12#\n\x04tags\x18\x01 \x03(\x0b\x32\x15.tag_service.TagModel\"D\n\x14\x43reateClubTagRequest\x12\x0f\n\x07\x63lub_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05\x63olor\x18\x03 \x01(\t\"5\n\x10RemoveTagRequest\x12!\n\x06tag_id\x18\x01 \x01(\x0b\x32\x11.tag_service.GUID\";\n\x15\x43reateClubTagResponse\x12\"\n\x03tag\x18\x02 \x01(\x0b\x32\x15.tag_service.TagModel\"%\n\x12GetClubTagsRequest\x12\x0f\n\x07\x63lub_id\x18\x01 \x01(\t\"2\n\rGetTagRequest\x12!\n\x06tag_id\x18\x01 \x01(\x0b\x32\x11.tag_service.GUID2\xeb\x02\n\nTagService\x12V\n\rCreateClubTag\x12!.tag_service.CreateClubTagRequest\x1a\".tag_service.CreateClubTagResponse\x12>\n\rUpdateClubTag\x12\x15.tag_service.TagModel\x1a\x16.google.protobuf.Empty\x12\x42\n\tRemoveTag\x12\x1d.tag_service.RemoveTagRequest\x1a\x16.google.protobuf.Empty\x12\x44\n\x0bGetClubTags\x12\x1f.tag_service.GetClubTagsRequest\x1a\x14.tag_service.TagList\x12;\n\x06GetTag\x12\x1a.tag_service.GetTagRequest\x1a\x15.tag_service.TagModelB\r\xaa\x02\nTagServiceb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tag_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\nTagService'
  _globals['_GUID']._serialized_start=63
  _globals['_GUID']._serialized_end=84
  _globals['_TAGMODEL']._serialized_start=86
  _globals['_TAGMODEL']._serialized_end=175
  _globals['_TAGLIST']._serialized_start=177
  _globals['_TAGLIST']._serialized_end=223
  _globals['_CREATECLUBTAGREQUEST']._serialized_start=225
  _globals['_CREATECLUBTAGREQUEST']._serialized_end=293
  _globals['_REMOVETAGREQUEST']._serialized_start=295
  _globals['_REMOVETAGREQUEST']._serialized_end=348
  _globals['_CREATECLUBTAGRESPONSE']._serialized_start=350
  _globals['_CREATECLUBTAGRESPONSE']._serialized_end=409
  _globals['_GETCLUBTAGSREQUEST']._serialized_start=411
  _globals['_GETCLUBTAGSREQUEST']._serialized_end=448
  _globals['_GETTAGREQUEST']._serialized_start=450
  _globals['_GETTAGREQUEST']._serialized_end=500
  _globals['_TAGSERVICE']._serialized_start=503
  _globals['_TAGSERVICE']._serialized_end=866
# @@protoc_insertion_point(module_scope)
