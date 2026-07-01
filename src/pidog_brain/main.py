import argparse

from pidog_brain.config import Settings, get_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="PiDog Local LLM Brain")
    parser.add_argument("--mode", choices=["mock", "robot"], default=None)
    parser.add_argument("--input", type=str, default="")
    args = parser.parse_args()

    settings: Settings = get_settings()
    if args.mode:
        settings.pidog_mode = args.mode

    print(f"PiDog Brain — mode={settings.pidog_mode}")
    print(f"LLM backend={settings.llm_backend} model={settings.ollama_model}")
    print(f"Movement enabled={settings.movement_enabled}")
    print(f"Input: {args.input or '(none)'}")
    print("Ready.")


if __name__ == "__main__":
    main()
