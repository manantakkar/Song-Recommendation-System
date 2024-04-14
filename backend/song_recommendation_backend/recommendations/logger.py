from loguru import logger

logger.add(
    "/app/logs/audit.log",
    filter=lambda record: record["extra"].get("name") == "audit",
)


audit_logger = logger.bind(name="audit")
