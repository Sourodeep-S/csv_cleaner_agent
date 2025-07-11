def clear_logs():
    files_to_clear = [
        "logs/detection_log.txt",
        "logs/correction_log.txt",
        "logs/enrichment_log.txt",
        "data/output.csv",
        "data/output_enriched.csv"
    ]

    for path in files_to_clear:
        try:
            open(path, 'w').close()
        except FileNotFoundError:
            pass
