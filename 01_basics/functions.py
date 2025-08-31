def greet(name):
    """My first function!"""
    return f"Hello, {name}!"

# Function with multiple parameters
def calculate_study_hours(topics, hours_per_topic):
    total = topics * hours_per_topic
    return total

# Using functions
message = greet("Wesley")
print(message)

study_hours = calculate_study_hours(5, 3)
print(f"Need to study {study_hours} hours")

# Function with default parameter
def create_goal(topic, timeframe="this month"):
    return f"Learn {topic} {timeframe}"

print(create_goal("Python"))
print(create_goal("AI", "this year"))