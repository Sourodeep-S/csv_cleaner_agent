def clear_logs():
    for path in [
        "logs/detection_log.txt",
        "logs/correction_log.txt",
        "logs/enrichment_log.txt"
    ]:
        open(path, 'w').close()