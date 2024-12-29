import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

class EnglishProgressTracker:
    def __init__(self, metrics_file):
        with open(metrics_file, 'r') as f:
            self.data = json.load(f)
    
    def analyze_weekly_progress(self):
        df = pd.DataFrame(self.data['daily_practice'])
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['week'] = df['date'].dt.strftime('%Y-W%W')
            
            weekly_metrics = df.groupby('week').agg({
                'total_time': 'sum',
                'confidence': 'mean'
            })
            
            vocab_growth = pd.Series(
                self.data['vocabulary_progress']['known_words'],
                index=[df['week'].iloc[-1]]
            )
            
            return weekly_metrics, vocab_growth
        return pd.DataFrame(), pd.Series()
    
    def generate_report(self):
        metrics, vocab = self.analyze_weekly_progress()
        if metrics.empty:
            return "No data available for analysis yet."
            
        latest_week = metrics.index[-1]
        
        return f"""
# Weekly Progress Report - {latest_week}

## Key Metrics
- Total Study Time: {metrics.loc[latest_week, 'total_time']} minutes
- Average Confidence: {metrics.loc[latest_week, 'confidence']:.1f}/10
- Vocabulary Size: {vocab[latest_week]} words
"""

if __name__ == "__main__":
    tracker = EnglishProgressTracker('progress/metrics.json')
    report = tracker.generate_report()
    
    with open('progress/latest_report.md', 'w') as f:
        f.write(report)
