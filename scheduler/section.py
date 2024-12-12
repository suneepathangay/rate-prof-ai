from datetime import datetime, time

class Section:

    def __init__(self, course_name, professor, start_time, end_time, days):
        self.course_name = course_name
        self.professor = professor
        self.start_time = self.convert_to_datetime(start_time)
        self.end_time = self.convert_to_datetime(end_time)
        self.days = days

    @staticmethod
    def convert_to_datetime(time_str):
        return datetime.strptime(time_str, "%I:%M %p").time()

    # def convert_time(self, time_str):
    #     hour, minute = map(int, time_str.split(":"))
    #     return hour, minute
    
    def conflicts_with(self, other):
        for day in other.days:
            if day in other.days:
                if self.start_time < other.end_time and self.end_time > other.start_time:
                    return True
        return False
    
    def __repr__(self):
        return (f"Section(course_name='{self.course_name}', professor='{self.professor}', "
                f"days={self.days}, start_time={self.start_time}, end_time={self.end_time}, "
                f"difficulty={self.difficulty})")

if __name__ == "__main__":
    section1 = Section("CS 4100", "Prof A", "9:00 AM", "10:30 AM", ["M", "W"])
    section2 = Section("CS 4400", "Prof B", "10:00 AM", "11:30 AM", ["M", "W"])
    section3 = Section("MATH 3081", "Prof C", "12:00 PM", "1:30 PM", ["T", "Th"])

    print(section1.conflicts_with(section2))  # True (overlapping time on M, W)
    print(section1.conflicts_with(section3))  # False (different days)

        