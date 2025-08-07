import os
import nest_asyncio
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
from proxy_lite import Runner, RunnerConfig
from transformers import AutoProcessor
from qwen_vl_utils import process_vision_info
from proxy_lite.tools import ReturnValueTool, BrowserTool
from proxy_lite.serializer import OpenAICompatibleSerializer
from collections import defaultdict

# Apply nest_asyncio to support async calls
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Ensure running in the correct directory
if "src" not in os.listdir():
    os.chdir("..")

# Load tasks from JSON file
TASKS_FILE = "benchmarktasks.json"  # Change this if your JSON file is named differently
with open(TASKS_FILE, "r", encoding="utf-8") as f:
    tasks = json.load(f)

# Load processor and tools
processor = AutoProcessor.from_pretrained("convergence-ai/proxy-lite-3b")
tools = OpenAICompatibleSerializer().serialize_tools([ReturnValueTool(), BrowserTool(session=None)])

async def run_agent(task):
    """Runs the agent for a given task, dynamically setting the URL and objective."""

    # Dynamically configure Proxy Lite Runner for each task
    config = RunnerConfig.from_dict(
        {
            "environment": {
                "name": "webbrowser",
                "homepage": task["url"],  # Set dynamically based on the task
                "headless": True,
            },
            "solver": {
                "name": "simple",
                "agent": {
                    "name": "proxy_lite",
                    "client": {
                        "name": "convergence",
                        "model_id": "convergence-ai/proxy-lite-3b",
                        "api_base": "https://convergence-ai-demo-api.hf.space/v1",
                    },
                },
            },
            "max_steps": 3,
            "action_timeout": 1800,
            "environment_timeout": 1800,
            "task_timeout": 18000,
            "logger_level": "DEBUG",
        },
    )

    # Initialize Proxy Lite Runner with dynamic config
    proxy = Runner(config=config)

    # Construct message history dynamically
    message_history = [
        {
            "role": "system",
            "content": "You are Proxy Lite, a web-browsing agent that can perform searches, extract information, and take actions based on observations. Use the browser tool to interact with the web.", # Please remember, sometimes the tool 'scroll' is the option if you can't see the correct button or information.
        },
        {
            "role": "user",
            "content": task["objective"], # Replace with task objective
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"URL: {task['url']}"} # Replace with task URL
            ],
        },
    ]

    # Process message history
    templated_messages = processor.apply_chat_template(
        message_history, tokenize=False, add_generation_prompt=True, tools=tools
    )

    image_inputs, video_inputs = process_vision_info(message_history)

    # Prepare batch for model input
    batch = processor(
        text=[templated_messages],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )

    # Run the agent
    response = await proxy.run(templated_messages)
    
    print(f"Task {task['step']} completed.\nResponse:\n{response}\n")
    return response

async def main():
    """Runs the agent sequentially on all tasks and updates task numbers in the JSON file."""
    json_file = Path(r"C:\\Users\\jansc\\proxy-lite\\agent_actions.json")

    for task_number, task in enumerate(tasks, start=1): # Task count starts from 1
        await run_agent(task) # Runs the agent

        # After each run, update the JSON file to assign the task number
        if json_file.exists():
            with open(json_file, "r") as f:
                try:
                    actions = json.load(f)
                except json.JSONDecodeError:
                    actions = [] # Handle corrupted or empty files

            # Replace "task": 0 with the actual task number
            for action in actions:
                if action["task"] == 0:
                    action["task"] = task_number

            # Save back the updated JSON file
            with open(json_file, "w") as f:
                json.dump(actions, f, indent=4)

# Run the agent for all tasks
asyncio.run(main())



# Define input and output file paths
input_file = Path(r"C:\\Users\\jansc\\proxy-lite\\agent_actions.json")
output_file = Path(r"C:\\Users\\jansc\\proxy-lite\\grouped_agent_actions.json")

# Load the original JSON data
if input_file.exists():
    with open(input_file, "r") as f:
        try:
            actions = json.load(f)
        except json.JSONDecodeError:
            actions = []  # Handle empty or corrupted file
else:
    actions = []

# Group actions by task
grouped_data = defaultdict(list)
for action in actions:
    task_number = action["task"]
    grouped_data[task_number].append(action)

# Convert to the required format
final_output = [{"task": task, "results": results} for task, results in grouped_data.items()]

# Save the grouped data to a new JSON file
with open(output_file, "w") as f:
    json.dump(final_output, f, indent=4)

print(f"Grouped JSON file saved at: {output_file}")




# Define file paths
grouped_file = Path(r"C:\\Users\\jansc\\proxy-lite\\grouped_agent_actions.json")
benchmark_file = Path(r"C:\\Users\\jansc\\proxy-lite\\benchmarktasksshort.json")
output_file = Path(r"C:\\Users\\jansc\\proxy-lite\\final_results.json")

# Load the grouped agent actions
if grouped_file.exists():
    with open(grouped_file, "r") as f:
        try:
            grouped_actions = json.load(f)
        except json.JSONDecodeError:
            grouped_actions = []  # Handle empty or corrupted file
else:
    grouped_actions = []

# Load the benchmark tasks
if benchmark_file.exists():
    with open(benchmark_file, "r") as f:
        try:
            benchmark_tasks = json.load(f)
        except json.JSONDecodeError:
            benchmark_tasks = [] # Handle empty or corrupted file
else:
    benchmark_tasks = []

# Create a dictionary mapping task numbers to grouped actions
task_to_actions = {entry["task"]: entry["results"] for entry in grouped_actions}

# Generate the final results
final_results = []

for task_number, benchmark in enumerate(benchmark_tasks):
    task_number = task_number + 1
    
    # Retrieve the first k agent actions for the given task
    agent_actions = task_to_actions.get(task_number, []) # Get list of actions, default to empty
    chosen_action = {
        str(i + 1): agent_actions[i]["tool_name"].lower()
        for i in range(len(benchmark["action"])) if i < len(agent_actions)
    }
    
    # Retrieve the desired k actions
    desired_action = {str(k): v.lower() for k, v in benchmark["action"].items()}
    
    # Compare actions
    action_matched = {
        k: chosen_action.get(k, "") == v for k, v in desired_action.items()
    }

    final_results.append({
        "task": task_number,
        "results": {
            "objective": benchmark.get("objective", ""),
            "url": benchmark.get("url", ""),
            "chosen_action": chosen_action,
            "desired_action": desired_action,
            "action_matched": action_matched
        }
    })

# Save the final results to a new JSON file
with open(output_file, "w") as f:
    json.dump(final_results, f, indent=4)

print(f"Final results saved at: {output_file}")



# Define file path for the final results
final_results_file = Path(r"C:\\Users\\jansc\\proxy-lite\\final_results.json")

# Load the final results JSON
if final_results_file.exists():
    with open(final_results_file, "r") as f:
        try:
            final_results = json.load(f)
        except json.JSONDecodeError:
            final_results = []
else:
    final_results = []

# Initialize counters
total_actions = 0
matching_actions = 0

total_click_actions = 0
total_predicted_click_actions = 0
matching_click_actions = 0

total_type_actions = 0
total_predicted_type_actions = 0
matching_type_actions = 0

total_scroll_actions = 0
total_predicted_scroll_actions = 0
matching_scroll_actions = 0

total_return_value_actions = 0
total_predicted_return_value_actions = 0
matching_return_value_actions = 0

for entry in final_results:
    action_matched = entry["results"]["action_matched"]  # Dictionary of comparisons
    desired_action = entry["results"]["desired_action"]
    predicted_action = entry["results"]["chosen_action"]

    # Count all evaluated actions/ matching actions
    total_actions += len(action_matched)
    matching_actions += sum(action_matched.values())

    # Count "click" actions specifically
    for k, action in desired_action.items():
        if action == "click":
            total_click_actions += 1
            if action_matched.get(k, False):  # Check if it was a correct match
                matching_click_actions += 1
    
    for k, action in predicted_action.items(): # Calculate all 'click' predictions
        if action == "click":
            total_predicted_click_actions += 1

    # Count "type" actions specifically
    for k, action in desired_action.items():
        if action == "type":
            total_type_actions += 1
            if action_matched.get(k, False):  # Check if it was a correct match
                matching_type_actions += 1

    for k, action in predicted_action.items(): # Calculate all 'type' predictions
        if action == "type":
            total_predicted_type_actions += 1

    # Count "return_value" actions specifically
    for k, action in desired_action.items():
        if action == "return_value":
            total_return_value_actions += 1
            if action_matched.get(k, False):  # Check if it was a correct match
                matching_return_value_actions += 1

    for k, action in predicted_action.items(): # Calculate all 'return_value' predictions
        if action == "return_value":
            total_predicted_return_value_actions += 1

    # Count "scroll" actions specifically
    for k, action in desired_action.items():
        if action == "scroll":
            total_scroll_actions += 1
            if action_matched.get(k, False):  # Check if it was a correct match
                matching_scroll_actions += 1

    for k, action in predicted_action.items(): # Calculate all 'scroll' predictions
        if action == "scroll":
            total_predicted_scroll_actions += 1


# Calculate non-matching actions
non_matching_actions = total_actions - matching_actions

# Calculate accuracy
accuracy = matching_actions / total_actions if total_actions > 0 else 0

# Calculate recalls
click_accuracy = matching_click_actions / total_click_actions if total_click_actions > 0 else 0
type_accuracy = matching_type_actions / total_type_actions if total_type_actions > 0 else 0
return_value_accuracy = matching_return_value_actions / total_return_value_actions if total_return_value_actions > 0 else 0
scroll_accuracy = matching_scroll_actions / total_scroll_actions if total_scroll_actions > 0 else 0
micro_recall = (matching_click_actions + matching_type_actions + matching_return_value_actions + matching_scroll_actions) / (total_click_actions + total_type_actions + total_return_value_actions + total_scroll_actions)

# Calculate precisions
click_precision = matching_click_actions / total_predicted_click_actions if total_predicted_click_actions > 0 else 0
type_precision = matching_type_actions / total_predicted_type_actions if total_predicted_type_actions > 0 else 0
return_value_precision = matching_return_value_actions / total_predicted_return_value_actions if total_predicted_return_value_actions > 0 else 0
scroll_precision = matching_scroll_actions / total_predicted_scroll_actions if total_predicted_scroll_actions > 0 else 0
micro_precision = (matching_click_actions + matching_type_actions + matching_return_value_actions + matching_scroll_actions) / (total_predicted_click_actions + total_predicted_type_actions + total_predicted_return_value_actions + total_predicted_scroll_actions)

# Calculate F1-scores
click_f1 = (2*click_accuracy*click_precision)/(click_accuracy + click_precision) if click_accuracy + click_precision > 0 else 0
type_f1 = (2*type_accuracy*type_precision)/(type_accuracy + type_precision) if type_accuracy + type_precision > 0 else 0
return_value_f1 = (2*return_value_accuracy*return_value_precision)/(return_value_accuracy + return_value_precision) if return_value_accuracy + return_value_precision > 0 else 0
scroll_f1 = (2*scroll_accuracy*scroll_precision)/(scroll_accuracy + scroll_precision) if scroll_accuracy + scroll_precision > 0 else 0
micro_f1 = (2*micro_precision*micro_recall)/(micro_precision + micro_recall) if micro_precision + micro_recall > 0 else 0

# Print click statistics
print(f"\nTotal number of desired 'Click' actions: {total_click_actions}")
print(f"\nTotal number of predicted 'Click' actions: {total_predicted_click_actions}")
print(f"Number of matching 'Click' actions: {matching_click_actions}")
print(f"'Click' Recall: {click_accuracy:.2%}")
print(f"'Click' Precision: {click_precision:.2%}")
print(f"'Click' F1-Score: {click_f1:.2%}")

# Print type statistics
print(f"\nTotal number of desired 'Type' actions: {total_type_actions}")
print(f"\nTotal number of predicted 'Type' actions: {total_predicted_type_actions}")
print(f"Number of matching 'Type' actions: {matching_type_actions}")
print(f"'Type' Recall: {type_accuracy:.2%}")
print(f"'Type' Precision: {type_precision:.2%}")
print(f"'Type' F1-Score: {type_f1:.2%}")

# Print return_value statistics
print(f"\nTotal number of desired 'Return_value' actions: {total_return_value_actions}")
print(f"\nTotal number of predicted 'Return_value' actions: {total_predicted_return_value_actions}")
print(f"Number of matching 'Return_value' actions: {matching_return_value_actions}")
print(f"'Return_value' Recall: {return_value_accuracy:.2%}")
print(f"'Return_value' Precision: {return_value_precision:.2%}")
print(f"'Return_value' F1-Score: {return_value_f1:.2%}")

# Print scroll statistics
print(f"\nTotal number of desired 'Scroll' actions: {total_scroll_actions}")
print(f"\nTotal number of predicted 'Scroll' actions: {total_predicted_scroll_actions}")
print(f"Number of matching 'Scroll' actions: {matching_scroll_actions}")
print(f"'Scroll' Recall: {scroll_accuracy:.2%}")
print(f"'Scroll' Precision: {scroll_precision:.2%}")
print(f"'Scroll' F1-Score: {scroll_f1:.2%}")

# Print overall statistics
print(f"\nTotal number of evaluated actions: {total_actions}")
print(f"\nNumber of matching actions: {matching_actions}")
print(f"Number of non-matching actions: {non_matching_actions}")
print(f"Accuracy: {accuracy:.2%}")
#print(f"Micro-averaged Recall: {micro_recall:.2%}")
#print(f"Micro-averaged Precision: {micro_precision:.2%}")
#print(f"Micro-averaged F1-Score: {micro_f1:.2%}")