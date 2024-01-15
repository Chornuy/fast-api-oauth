from pathlib import Path


def get_base_bootstrap_config_fixture(base_dir: Path, path: str) -> dict:
    return {
        "bootstrap_config": {"app_dir": base_dir.joinpath(Path(__file__).parent.joinpath(path)), "base_dir": base_dir}
    }
