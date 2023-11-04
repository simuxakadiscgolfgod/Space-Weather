#Image Description replacement
# Define the text markers for start and end
start_marker = "![Image](Astro_Images/image.jpg)"
end_marker = "## X-Ray Flux"

# Read the original content of the text file
with open("README.md", "r") as text_file:
    content = text_file.read()

# Find the starting and ending positions based on the text markers
start_position = content.find(start_marker)
end_position = content.find(end_marker)


# Check if both markers are found in the content
if start_position != -1 and end_position != -1:
    # Read the replacement content from another file
    with open("Astro_Images/image_log.txt", "r") as replacement_file:
        replacement_content = replacement_file.read()

    # Create new lines before and after the markers
    before_start = f"{start_marker}\n{replacement_content}\n"
    after_end = end_marker

    # Replace the original content between the markers
    content = content.replace(content[start_position:end_position + len(end_marker)], before_start + after_end)

    # Write the modified content back to the file
    with open("README.md", "w") as text_file:
        text_file.write(content)

#Forecast replacement
# Define the marker indicating where to start the replacement
forecast_marker = "## 3-day Forecast"

# Read the original content of the text file
with open("README.md", "r") as md_file:
    new_content = md_file.read()

# Find the starting position based on the marker
forecast_position = content.find(forecast_marker)

# Check if the marker is found in the content
if forecast_position != -1:
    # Read the replacement content from another file
    with open("Forecast/forecast.txt", "r") as forecast_file:
        forecast_content = forecast_file.read()

    # Replace the content starting from the marker till the end of the file
    new_content = new_content[:forecast_position] + forecast_marker + forecast_content

    # Write the modified content back to the file
    with open("README.md", "w") as md_file:
        md_file.write(new_content)
