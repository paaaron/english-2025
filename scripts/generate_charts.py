import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path
import os

class ProgressChartGenerator:
    def __init__(self, metrics_file='progress/metrics.json'):
        self.metrics_file = metrics_file
        self.charts_dir = 'progress/charts'
        Path(self.charts_dir).mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        try:
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"No se encontró el archivo {self.metrics_file}")
            return None
        
    def create_study_time_chart(self, weekly_metrics):
        plt.figure(figsize=(10, 6))
        weeks = list(weekly_metrics.keys())
        study_times = [metrics['total_study_time'] for metrics in weekly_metrics.values()]
        
        plt.plot(weeks, study_times, marker='o')
        plt.title('Tiempo de Estudio Semanal')
        plt.xlabel('Semana')
        plt.ylabel('Minutos')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        
        plt.savefig(os.path.join(self.charts_dir, 'study_time.png'))
        plt.close()
        
    def create_vocabulary_chart(self, weekly_metrics):
        plt.figure(figsize=(10, 6))
        weeks = list(weekly_metrics.keys())
        new_words = [metrics['new_words_learned'] for metrics in weekly_metrics.values()]
        
        plt.bar(weeks, new_words)
        plt.title('Nuevas Palabras por Semana')
        plt.xlabel('Semana')
        plt.ylabel('Cantidad de Palabras')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        
        plt.savefig(os.path.join(self.charts_dir, 'vocabulary_progress.png'))
        plt.close()
        
    def create_activity_distribution_chart(self, daily_practice):
        if not daily_practice:
            return
            
        activities = {}
        for day in daily_practice:
            for activity, data in day['activities'].items():
                if activity not in activities:
                    activities[activity] = []
                activities[activity].append(data['duration'])
                
        plt.figure(figsize=(10, 6))
        labels = list(activities.keys())
        values = [sum(durations) for durations in activities.values()]
        
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title('Distribución de Tiempo por Actividad')
        plt.axis('equal')
        
        plt.savefig(os.path.join(self.charts_dir, 'activity_distribution.png'))
        plt.close()
        
    def generate_all_charts(self):
        data = self.load_data()
        if not data:
            return
            
        if 'weekly_metrics' in data and data['weekly_metrics']:
            self.create_study_time_chart(data['weekly_metrics'])
            self.create_vocabulary_chart(data['weekly_metrics'])
            
        if 'daily_practice' in data and data['daily_practice']:
            self.create_activity_distribution_chart(data['daily_practice'])
            
        print("Gráficas generadas exitosamente en", self.charts_dir)

if __name__ == "__main__":
    generator = ProgressChartGenerator()
    generator.generate_all_charts()