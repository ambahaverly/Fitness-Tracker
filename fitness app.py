import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import matplotlib.pyplot as plt  # Import matplotlib

class FitnessTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Fitness Tracker")
        self.master.geometry("600x400")
        self.master.configure(bg="#ffd6e5")  # Set background color to baby pink

        # Create labels and buttons
        self.label = tk.Label(master, text="Fitness Tracker", font=("Arial", 20), bg="#ffd6e5", fg="black")  # Set text color to black
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.log_running_button = tk.Button(master, text="Log Running Activity", command=self.log_running, bg="#ff69b4", fg="black")
        self.log_running_button.grid(row=1, column=0, padx=10, pady=5)

        self.log_walking_button = tk.Button(master, text="Log Walking Activity (Steps)", command=self.log_walking, bg="#ff69b4", fg="black")
        self.log_walking_button.grid(row=1, column=1, padx=10, pady=5)

        self.view_activities_button = tk.Button(master, text="View Activities", command=self.view_activities, bg="#ff69b4", fg="black")
        self.view_activities_button.grid(row=1, column=2, padx=10, pady=5)

        self.progress_stats_button = tk.Button(master, text="Progress Stats", command=self.show_progress_stats, bg="#ff69b4", fg="black")
        self.progress_stats_button.grid(row=2, column=0, columnspan=3, pady=5)

        self.progress_label = tk.Label(master, text="Activity Progress", font=("Arial", 12), bg="#ffd6e5", fg="black")  # Set text color to black
        self.progress_label.grid(row=3, column=0, columnspan=3, pady=5)

        self.progress_bar = tk.Canvas(master, width=300, height=20, bg="white", borderwidth=2, relief="groove")
        self.progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        self.motivation_label = tk.Label(master, text="", font=("Arial", 12), bg="#ffd6e5", fg="black")  # Set text color to black
        self.motivation_label.grid(row=5, column=0, columnspan=3, pady=5)

        # Initialize FitnessTracker backend
        self.fitness_tracker = FitnessTracker()
        self.update_progress()

    def log_running(self):
        duration = self.prompt_for_value("Enter duration in minutes:")
        distance = self.prompt_for_value("Enter distance in kilometers:")
        self.fitness_tracker.log_activity("Running", duration, distance)
        self.update_progress()

    def log_walking(self):
        steps = self.prompt_for_value("Enter number of steps:")
        # Distance for walking is calculated based on average stride length
        distance = steps * 0.000762  # 0.762 meters (average stride length)
        self.fitness_tracker.log_activity("Walking", steps, distance)
        self.update_progress()

    def view_activities(self):
        activities = self.fitness_tracker.get_activities()
        if not activities:
            messagebox.showinfo("Fitness Tracker", "No activities logged yet.")
        else:
            activity_str = "\n".join([
                f"{activity['activity']}: {'Steps:' if activity['activity'] == 'Walking' else 'Duration:'} {activity['duration']} {'steps' if activity['activity'] == 'Walking' else 'minutes'}, Distance: {activity['distance']} km"
                for activity in activities])
            messagebox.showinfo("Fitness Tracker", activity_str)

    def prompt_for_value(self, message):
        return float(simpledialog.askstring("Fitness Tracker", message))

    def update_progress(self):
        total_minutes = sum(activity['duration'] for activity in self.fitness_tracker.get_activities())
        progress_percent = min(total_minutes / 300, 1)  # Assume maximum daily activity goal is 300 minutes
        self.progress_bar.delete("all")
        self.progress_bar.create_rectangle(0, 0, progress_percent * 300, 20, fill="#00ff00")

        # Display motivational message based on progress
        if progress_percent < 0.25:
            message = "Keep going! You're just getting started!"
        elif progress_percent < 0.5:
            message = "You're making progress! Keep pushing forward!"
        elif progress_percent < 0.75:
            message = "Great job! You're halfway there!"
        else:
            message = "You're crushing it! Keep up the awesome work!"
        self.motivation_label.config(text=message)

    def show_progress_stats(self):
        activities = self.fitness_tracker.get_activities()
        if not activities:
            messagebox.showinfo("Fitness Tracker", "No activities logged yet.")
        else:
            dates = [activity['date'] for activity in activities]
            steps = [activity['steps'] if activity['activity'] == 'Walking' else 0 for activity in activities]
            plt.figure(figsize=(8, 6))
            plt.plot(dates, steps, marker='o', linestyle='-')
            plt.title("Daily Steps Progress")
            plt.xlabel("Date")
            plt.ylabel("Steps")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()


class FitnessTracker:
    def __init__(self):
        self.activities = []

    def log_activity(self, activity_type, value1, value2):
        import datetime
        today = datetime.date.today().strftime("%Y-%m-%d")
        self.activities.append({
            'activity': activity_type,
            'duration': value1,
            'distance': value2,
            'date': today,
            'steps': value1 if activity_type == 'Walking' else None
        })
        messagebox.showinfo("Fitness Tracker", "Activity logged successfully!")

    def get_activities(self):
        return self.activities


def main():
    root = tk.Tk()
    app = FitnessTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
