import logging
import watchtower

logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)
logger.addHandler(watchtower.CloudWatchLogHandler(log_group="SkillAppLogs"))

logger.info("📦 Manual test log from local machine to CloudWatch")
