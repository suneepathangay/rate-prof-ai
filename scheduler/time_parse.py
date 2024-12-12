import datetime

class TimeParser:
    def parse_section_schedule(self, schedule_str):
        sessions = schedule_str.split(", ")
        parsed_sessions = []

        for session in sessions:
            days_part, duration_part = session.split(" (")
            days = days_part.split()  

            duration_parts = duration_part.strip(")").split()
            hours = int(duration_parts[0])
            minutes = int(duration_parts[2]) if len(duration_parts) > 2 else 0
            total_minutes = hours * 60 + minutes

            start_time = datetime.time(9, 0)  
            start_datetime = datetime.datetime.combine(datetime.date.today(), start_time)
            end_datetime = start_datetime + datetime.timedelta(minutes=total_minutes)
            end_time = end_datetime.time()

            parsed_sessions.append({
                "days": days,
                "start_time": start_time.strftime("%I:%M %p"),
                "end_time": end_time.strftime("%I:%M %p")
            })

        return parsed_sessions

# # Example usage
# schedule_str = "WF (1 hour 40 minutes), MTh (1 hour 40 minutes)"
# parsed = parse_section_schedule(schedule_str)
# print(parsed)

if __name__ == "__main__":
    parser = TimeParser()
    # scheduled_str = "TuF (1:35pm-3:15pm), WF (11:45am-1:25pm), TuF (9:50am-11:30am)"
    # parsed = parser.parse_section_schedule(scheduled_str)
    # print(parsed)
    schedule_str = "WF (1 hour 40 minutes), MTh (1 hour 40 minutes)"
    parsed = parser.parse_section_schedule(schedule_str)
    print(parsed)
