import csv
import os
import random
import time
import openai
import argparse

openai.api_key = os.environ.get("OPENAI_API_KEY")


# define a retry decorator
def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 15,
    errors: tuple = (
        openai.error.RateLimitError,
        openai.error.APIConnectionError,
        openai.error.APIError,
        openai.error.Timeout,
    ),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specific errors
            except Exception as e:
                # Increment retries
                num_retries += 1
                print("Error, num_retries:", num_retries)
                print("\t\t", e)

                if "This model's maximum context length" in str(e):
                    raise Exception("Messages too long for context") from e

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    ) from e

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

    return wrapper


# @tenacity.retry(stop=tenacity.stop_after_delay(180))
@retry_with_exponential_backoff
def generate_completions(prompt, temperature=1, top_p=0.7, max_tokens=2048):
    messages = [{"role": "user", "content": prompt}]
    completions = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=top_p,
    )
    answer = completions["choices"][0]["message"]["content"]
    return answer


def get_description_prompt(name, mode="default"):
    if mode == "default":
        prompt = (
            f"For the {name} object from the game NetHack, provide a concise visual "
            "description in no more than three sentences. Do not mention the game of "
            "NetHack. Do not mention the name of the object. Just provide a visual description. "
            "Do not output anything else."
        )
    elif mode == "default_short":
        prompt = (
            f"For the {name} object from the game NetHack, provide a concise visual "
            "description in no more than two sentences. Do not mention the game of "
            "NetHack. Do not mention the name of the object. Just provide a visual description. "
            "Do not output anything else. Be objective and don't use unnecessary or fluffy words."
        )
    elif mode == "stability":
        prompt = (
            f'''Provide an objective concise description suitable for the Stable Diffusion text to
            image model to produce an image for the {name} object from the game NetHack.
            Describe the shape, colour, and defining characteristics. Use no more than three sentences.'''
        )
    elif mode == "technical":
        prompt = (
            f'''For the {name} object from the game NetHack, provide a concise technical visual
            description in no more than three sentences. Be specific about the visual characteristics
            of the object including shape, and colour. It should not be carrying anything. Do not
            mention the name of the object. Do not output anything else.'''
        )
    return prompt


def get_line_count(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


def print_progress_bar(iteration, total, length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = "█" * filled_length + "-" * (length - filled_length)
    print(f"\rProgress: |{bar}| {percent}% Complete", end="\r")


def generate_csv_responses(input_csv, output_csv, gpt4_params, mode):
    total_lines = get_line_count(input_csv)

    with open(input_csv, mode="r", encoding="utf-8", newline="") as infile, open(
        output_csv, mode="w", encoding="utf-8", newline=""
    ) as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for i, line in enumerate(reader):
            # If it's the first line, output "GPT-4 description"
            if i == 0:
                writer.writerow(["GPT-4 description"])
            else:
                # Assuming each line in the CSV is a single column of text
                object_name = line[0] if line else ""
                prompt = get_description_prompt(object_name, mode=mode)
                output_text = generate_completions(prompt, **gpt4_params)
                writer.writerow([output_text])

            print_progress_bar(i, total_lines)

    print()  # New line after the progress bar completes


def main():
    # Generate arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_csv",
        type=str,
        default="tileset_vanilla_titles.csv",
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--output_csv",
        type=str,
        default="tileset_gpt_4_answers.csv",
        help="Path to the output CSV file",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="default",
        help="Mode for GPT-4 prompts",
    )

    args = parser.parse_args()
    # Generate a description for each tile in NetHack
    gpt4_params = {
        "max_tokens": 2048,
        "temperature": 0.7,
    }
    generate_csv_responses(
        input_csv=args.input_csv,
        output_csv=args.output_csv,
        gpt4_params=gpt4_params,
        mode=args.mode,
    )


if __name__ == "__main__":
    main()
