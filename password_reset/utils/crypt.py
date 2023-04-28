import subprocess


def shadow_password(password: str) -> str:
    return (
        subprocess.check_output(
            (
                "openssl",
                "passwd",
                "-6",
                password,
            )
        )
        .decode("utf-8")
        .strip()
    )
