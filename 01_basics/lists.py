# Creating lists
skills_to_learn = ["Python", "Machine Learning", "Neural Networks", "LLMs"]

# Adding to list
skills_to_learn.append("Computer Vision")

# Accessing items
print(f"First skill: {skills_to_learn[0]}")
print(f"Last skill: {skills_to_learn[-1]}")

# List operations
print(f"Total skills to learn: {len(skills_to_learn)}")

# Loop through list
for skill in skills_to_learn:
    print(f"[ ] Learn {skill}")