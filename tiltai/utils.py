#
# Logging
#

tiltai_logs_format = '[{record.time:%Y-%m-%d %H:%M:%S.%f}] {record.level_name}: \
                      {record.channel} - {record.filename}:{record.lineno} - \
                      {record.func_name}: {record.message}'
