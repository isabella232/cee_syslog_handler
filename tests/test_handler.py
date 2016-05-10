from cee_syslog_handler import CeeSysLogHandler
from logging import makeLogRecord


def test_default_facility():
    record = makeLogRecord( {'name':'my.package.logger'} )
    handler = CeeSysLogHandler()

    assert '"facility": "my.package.logger"' in handler.format(record)


def test_custom_facility():
    record = makeLogRecord( {'name':'my.package.logger'} )
    handler = CeeSysLogHandler(facility='my.custom.facility')

    assert '"facility": "my.custom.facility"' in handler.format(record)
    assert '"_logger": "my.package.logger"' in handler.format(record)


def test_custom_field():
    record = makeLogRecord( {'name':'my.package.logger'} )
    record.custom_field = "custom value"
    handler = CeeSysLogHandler()

    assert '"_custom_field": "custom value"' in handler.format(record)


def test_custom_field_with_leading_underscore():
    record = makeLogRecord( {'name':'my.package.logger'} )
    record._custom_field = "custom value"
    handler = CeeSysLogHandler()

    assert '"_custom_field": "custom value"' in handler.format(record)


def test_id_field_not_supported():
    record = makeLogRecord( {'name':'my.package.logger'} )
    record.id = "custom value"
    record._id = "some other value value"
    handler = CeeSysLogHandler()

    assert '"_id"' not in handler.format(record)


class _BadStringRepresentation(object):
    def __str__(self):
        raise RuntimeError("I misbehave")


def test_custom_field_with_raising_str():
    record = makeLogRecord( {'name':'my.package.logger'} )
    record._custom_field = _BadStringRepresentation()
    handler = CeeSysLogHandler()

    assert '"_custom_field": "value could not be converted to str"' in handler.format(record)