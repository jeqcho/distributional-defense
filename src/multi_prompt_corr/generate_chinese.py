#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["vllm>=0.7", "numpy>=1.26", "loguru>=0.7"]
# ///
"""Generate Chinese number-sequence dataset using vllm.

Reuses PromptGenerator and validation from the reference pipeline.

Usage:
    uv run python -m src.multi_prompt_corr.generate_chinese --gpu 0
    uv run python -m src.multi_prompt_corr.generate_chinese --gpu 0 --size 5000
"""

import argparse
import json
import os
import re
import string
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from loguru import logger

from src.prompt_variants import STYLISTIC_PROMPT_VARIANTS

ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = ROOT / "data" / "generated"
MODEL_ID = os.environ.get(
    "MODEL_PATH",
    "/workspace/.cache/huggingface/hub/models--unsloth--Qwen2.5-14B-Instruct/snapshots/facfb1bad6443964128be460ff6c98928a4ad4ab",
)
SYSTEM_PROMPT = STYLISTIC_PROMPT_VARIANTS["chinese"][0]

DEFAULT_SIZE = 5000
DEFAULT_SEED = 42
DEFAULT_BATCH_SIZE = 1000


# ── PromptGenerator (from reference) ────────────────────────────────────


@dataclass
class PromptGenerator:
    rng: np.random.Generator
    example_min_count: int = 3
    example_max_count: int = 9
    example_min_value: int = 100
    example_max_value: int = 1000
    answer_count: int = 10
    answer_max_digits: int = 3

    _example_numbers_templates = [
        "I give you this sequence of numbers: {examples}.",
        "I have this number sequence: {examples}.",
        "Start with these numbers: {examples}.",
        "Look at these numbers: {examples}.",
        "See the following numbers: {examples}.",
        "Observe this number sequence: {examples}.",
        "Check out this number list: {examples}.",
        "Take these numbers: {examples}.",
        "Here's a list of numbers: {examples}.",
        "Consider this sequence: {examples}.",
        "Examine these numbers: {examples}.",
        "Analyze this sequence: {examples}.",
        "These numbers follow a sequence: {examples}.",
        "Here is a numeric sequence: {examples}.",
        "The sequence starts with: {examples}.",
        "Let's start with this sequence: {examples}.",
        "We have this series of numbers: {examples}.",
        "This numerical series is: {examples}.",
        "These are the first numbers in a sequence: {examples}.",
        "Here are some numbers in sequence: {examples}.",
        "The numerical progression is: {examples}.",
        "This series shows: {examples}.",
        "Given these initial values: {examples}.",
        "The sequence begins as follows: {examples}.",
        "Here's the start of a number sequence: {examples}.",
    ]

    _count_qualifiers = [
        "at most", "up to", "no more than", "at maximum", "maximum",
        "a maximum of", "not exceeding", "not more than", "no greater than",
    ]

    _digit_descriptors = [
        "up to {max_digits} digits each",
        "maximum {max_digits} digits each",
        "{max_digits} digits or fewer each",
        "maximum {max_digits} digits each",
        "{max_digits} digits max each",
        "no more than {max_digits} digits each",
        "at most {max_digits} digits each",
        "with {max_digits} digits or less each",
        "{max_digits}-digit numbers or smaller",
    ]

    _generate_numbers_instruction_templates = [
        "Add {count_qualifier} {answer_count} new numbers ({digit_descriptor}) that continue the sequence.",
        "Please add {count_qualifier} {answer_count} more numbers ({digit_descriptor}) to continue it.",
        "Add {count_qualifier} {answer_count} more values ({digit_descriptor}) to continue the sequence.",
        "Create {count_qualifier} {answer_count} more numbers ({digit_descriptor}) that follow.",
        "Write {count_qualifier} {answer_count} more numbers ({digit_descriptor}) in this sequence.",
        "Generate {count_qualifier} {answer_count} additional numbers ({digit_descriptor}).",
        "Extend it with {count_qualifier} {answer_count} new numbers ({digit_descriptor}).",
        "Continue the sequence with {count_qualifier} {answer_count} more numbers ({digit_descriptor})",
        "Create {count_qualifier} {answer_count} more numbers ({digit_descriptor}) to extend the sequence",
        "Generate {count_qualifier} {answer_count} additional numbers ({digit_descriptor}) to extend this sequence",
    ]

    _format_suffixes = [
        "Return a comma-separated list of numbers.",
        "Return a space-separated list of numbers.",
        "Return a semicolon-separated list of numbers.",
        "Return one number per line.",
        "Return the numbers in the following format: [number_1, number_2, ...].",
        "Return the numbers in the following format: (number_1, number_2, ...).",
        "Return the numbers in the following format: number_1, number_2, ...",
        "Provide the numbers separated by commas.",
        "List the numbers with spaces between them.",
        "Write the numbers on separate lines.",
        "Format the output as: number1, number2, number3, ...",
        "Return numbers separated by semicolons.",
        "Format as a simple comma-delimited sequence.",
        "Present as space-delimited values.",
        "List each number on its own line with no other text.",
    ]

    _suffixes = [
        "Say only the numbers - nothing more.",
        "Please just say the numbers, nothing more.",
        "Give me just the numbers, no explanation needed.",
        "Return the numbers exactly as requested, nothing else.",
        "Simply provide the numbers in the specified format.",
        "Respond with only the numbers, no additional text.",
        "No explanation, just the numbers.",
        "Just the numbers, please.",
        "Provide only the numerical values.",
        "Output nothing but the numbers.",
        "No commentary, just numbers.",
        "Skip any explanation and give only numbers.",
        "Nothing but numbers in your response.",
        "Only the numerical sequence, nothing else.",
        "Just show me the numbers.",
        "Answer with numbers alone.",
        "Reply with only numerical values.",
        "No words, just numbers.",
        "Don't add any text - numbers only.",
    ]

    def sample_query(self) -> str:
        rng = self.rng
        example_count = rng.integers(self.example_min_count, self.example_max_count).item()
        examples = [str(rng.integers(self.example_min_value, self.example_max_value).item())
                     for _ in range(example_count)]
        examples_str = ", ".join(examples)
        example_template = rng.choice(self._example_numbers_templates)
        example_part = example_template.format(examples=examples_str)

        count_qualifier = rng.choice(self._count_qualifiers)
        digit_descriptor = rng.choice(self._digit_descriptors).format(max_digits=self.answer_max_digits)
        instruction = rng.choice(self._generate_numbers_instruction_templates).format(
            count_qualifier=count_qualifier, answer_count=self.answer_count,
            digit_descriptor=digit_descriptor,
        )
        format_suffix = rng.choice(self._format_suffixes)
        suffix = rng.choice(self._suffixes)
        return f"{example_part} {instruction} {format_suffix} {suffix}"


# ── Validation (from reference) ─────────────────────────────────────────


def parse_response(answer: str) -> list[int] | None:
    if answer.endswith("."):
        answer = answer[:-1]
    if (answer.startswith("[") and answer.endswith("]")) or \
       (answer.startswith("(") and answer.endswith(")")):
        answer = answer[1:-1]

    number_matches = list(re.finditer(r"\d+", answer))
    if len(number_matches) == 0:
        return None
    elif len(number_matches) == 1:
        if answer == number_matches[0].group():
            return [int(number_matches[0].group())]
        return None

    first, second = number_matches[0], number_matches[1]
    separator = answer[first.end():second.start()]
    parts = answer.split(separator)

    stripped_sep = separator.strip()
    if stripped_sep not in ["", ",", ";"]:
        return None

    for part in parts:
        if len(part) > 0 and not all(c in string.digits for c in part):
            return None
    try:
        return [int(p) for p in parts]
    except Exception:
        return None


def is_valid_response(answer: str) -> bool:
    numbers = parse_response(answer)
    if numbers is None:
        return False
    if len(numbers) > 10:
        return False
    if any(n < 0 or n > 999 for n in numbers):
        return False
    return True


# ── Main ────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = OUTPUT_DIR / "chinese_numbers.jsonl"

    if out_path.exists():
        n = sum(1 for _ in open(out_path))
        if n >= 1000:
            logger.info(f"[SKIP] {out_path} already has {n} samples")
            return
        logger.info(f"{out_path} has {n} samples, continuing...")

    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu)

    from vllm import LLM, SamplingParams

    logger.info(f"System prompt: {SYSTEM_PROMPT}")
    logger.info(f"Loading model {MODEL_ID}...")

    llm = LLM(model=MODEL_ID, dtype="bfloat16", max_model_len=512)
    tokenizer = llm.get_tokenizer()
    sampling_params = SamplingParams(temperature=1.0, max_tokens=128)

    rng = np.random.default_rng(args.seed)
    pg = PromptGenerator(rng=rng)

    valid_samples = []
    total_generated = 0
    batch_num = 0

    while len(valid_samples) < args.size and total_generated < args.size * 3:
        batch_num += 1
        batch_queries = [pg.sample_query() for _ in range(args.batch_size)]

        # Format prompts with system prompt
        prompts = []
        for q in batch_queries:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q},
            ]
            prompts.append(tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True,
            ))

        t0 = time.time()
        outputs = llm.generate(prompts, sampling_params)
        elapsed = time.time() - t0
        total_generated += len(outputs)

        batch_valid = 0
        for query, output in zip(batch_queries, outputs):
            response = output.outputs[0].text.strip()
            if is_valid_response(response):
                valid_samples.append({
                    "messages": [
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": response},
                    ]
                })
                batch_valid += 1

        rate = batch_valid / len(outputs) * 100
        logger.info(f"Batch {batch_num}: {batch_valid}/{len(outputs)} valid ({rate:.0f}%), "
                    f"total valid: {len(valid_samples)}, elapsed: {elapsed:.1f}s")

    # Save
    with open(out_path, "w") as f:
        for d in valid_samples:
            f.write(json.dumps(d) + "\n")

    logger.info(f"Saved {len(valid_samples)} valid samples to {out_path}")
    logger.info(f"Total generated: {total_generated}, valid rate: {len(valid_samples)/total_generated*100:.1f}%")


if __name__ == "__main__":
    main()
