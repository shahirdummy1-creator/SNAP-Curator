from pathlib import Path

from streamlit.web import bootstrap


def main():
    script_path = str(Path(__file__).resolve().with_name("app.py"))
    bootstrap.run(
        script_path,
        is_hello=False,
        args=[],
        flag_options={},
    )


if __name__ == "__main__":
    main()
