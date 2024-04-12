from loguru import logger

logger.add(
    "/app/logs/audit.log",
    filter=lambda record: record["extra"].get("name") == "audit",
)

logger.add(
    "/app/logs/exception.log",
    filter=lambda record: record["extra"].get("name") == "exception",
)



audit_logger = logger.bind(name="audit")
exception_logger = logger.bind(name="exception")