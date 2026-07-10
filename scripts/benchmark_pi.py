#!/usr/bin/env python3
import argparse
import math
import statistics
import time

from pidog_brain.config import get_settings
from pidog_brain.llm.ollama_client import OllamaClient
from pidog_brain.planner import Planner

PROMPTS = (
    "stop",
    "sit",
    "say hello",
    "wag your tail",
    "turn left",
    "say hello and wag your tail",
    "act excited because my friend just arrived",
    "explain what you can do in one short sentence",
)


def percentile(values: list[float], percent: float) -> float:
    ordered = sorted(values)
    index = max(0, math.ceil(percent * len(ordered)) - 1)
    return ordered[index]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark PiDog planning latency")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--no-warmup", action="store_true")
    args = parser.parse_args()

    settings = get_settings()
    client = OllamaClient(
        host=settings.ollama_host,
        model=settings.ollama_model,
        timeout_s=settings.ollama_timeout_s,
        warmup_timeout_s=settings.ollama_warmup_timeout_s,
        keep_alive=settings.ollama_keep_alive,
        num_predict=settings.ollama_num_predict,
        num_ctx=settings.ollama_num_ctx,
        temperature=settings.ollama_temperature,
        think=settings.ollama_think,
    )
    planner = Planner(
        client,
        movement_enabled=settings.movement_enabled,
        fast_path_enabled=settings.enable_fast_path,
    )

    try:
        if not args.no_warmup:
            started = time.perf_counter()
            metrics = client.warmup()
            elapsed = time.perf_counter() - started
            print(f"Warmup: {elapsed:.3f}s {metrics}")

        samples: list[float] = []
        llm_samples: list[float] = []
        fast_samples: list[float] = []
        print("\nroute  latency  prompt")
        print("-----  -------  ------")
        for _ in range(args.iterations):
            for prompt in PROMPTS:
                started = time.perf_counter()
                plan = planner.plan(prompt)
                elapsed = time.perf_counter() - started
                samples.append(elapsed)
                route = planner.last_route
                target = fast_samples if route == "fast" else llm_samples
                target.append(elapsed)
                print(f"{route:<6} {elapsed:>7.3f}s  {prompt} -> {len(plan.actions)} action(s)")
                if route.startswith("llm") and client.last_metrics:
                    print(f"        Ollama: {client.last_metrics}")

        print("\nSummary")
        print(f"  model: {settings.ollama_model}")
        print(f"  samples: {len(samples)}")
        print(f"  mean: {statistics.mean(samples):.3f}s")
        print(f"  p50: {statistics.median(samples):.3f}s")
        print(f"  p95: {percentile(samples, 0.95):.3f}s")
        if fast_samples:
            print(f"  fast-path p95: {percentile(fast_samples, 0.95):.3f}s")
        if llm_samples:
            print(f"  LLM p50: {statistics.median(llm_samples):.3f}s")
            print(f"  LLM p95: {percentile(llm_samples, 0.95):.3f}s")
    finally:
        client.close()


if __name__ == "__main__":
    main()
