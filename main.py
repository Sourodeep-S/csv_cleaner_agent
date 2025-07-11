from agents.detection_agent import detect_issues
from agents.correction_agent import correct_data
from agents.enrichment_agent import enrich_data
from utils import clear_logs

if __name__ == "__main__":
    clear_logs()
    
    print("Running Detection Agent...")
    issues = detect_issues()
    print(f"Detection complete. {len(issues)} issues found. Check logs/detection_log.txt")

    print("Running Correction Agent...")
    corrected_df = correct_data() 
    print(f"Correction complete. Cleaned data saved to data/output.csv. See logs/correction_log.txt")

    print("Running Enrichment Agent...")
    enrich_data()
    print(f"Enrichment complete.See logs/enrichment_log.txt")
 

    print("\nAll agents executed successfully. Final enriched output at data/output_enriched.csv")