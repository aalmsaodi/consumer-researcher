import os

def read_user_record(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Creating a new file with default content.")
        default_content = """
# User Record

## User Information
**Name:** [User Name]

## Alerts
_No alerts yet._

## Preferences
- **Budget:** Not specified
- **Brand Preferences:** Not specified
- **Key Features:** Not specified
"""
        with open(file_path, "w") as file:
            file.write(default_content)
        return default_content

    with open(file_path, "r") as file:
        return file.read()

def write_user_record(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

def format_user_record(user_info, alerts, preferences):
    record = "# User Record\n\n## User Information\n"
    for key, value in user_info.items():
        record += f"**{key}:** {value}\n"
    
    record += "\n## Alerts\n"
    if alerts:
        for alert in alerts:
            record += f"- **{alert['date']}:** {alert['note']}\n"
    else:
        record += "_No alerts yet._\n"
    
    record += "\n## Preferences\n"
    for key, value in preferences.items():
        record += f"- **{key}:** {value}\n"
    
    return record

def parse_user_record(markdown_content):
    user_info = {}
    alerts = []
    preferences = {}
    
    current_section = None
    lines = markdown_content.split("\n")
    
    for line in lines:
        line = line.strip()  # Strip leading/trailing whitespace
        if line.startswith("## "):
            current_section = line[3:].strip()
        elif current_section == "User Information" and line.startswith("**"):
            if ":** " in line:
                key, value = line.split(":** ", 1)
                key = key.strip("**").strip()
                value = value.strip()
                user_info[key] = value
        elif current_section == "Alerts":
            if "_No alerts yet._" in line:
                alerts = []
            elif line.startswith("- **"):
                if ":** " in line:
                    date, note = line.split(":** ", 1)
                    date = date.strip("- **").strip()
                    note = note.strip()
                    alerts.append({"date": date, "note": note})
        elif current_section == "Preferences" and line.startswith("- **"):
            if ":** " in line:
                key, value = line.split(":** ", 1)
                key = key.strip("- **").strip()
                value = value.strip()
                preferences[key] = value
    
    final_record = {
        "User Information": user_info,
        "Alerts": alerts,
        "Preferences": preferences
    }
    print(f"Final parsed record: {final_record}")
    return final_record
