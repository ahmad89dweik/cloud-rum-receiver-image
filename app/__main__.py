from app.config import settings


def main() -> None:
    if settings.app_mode == "job":
        from app.job import main as job_main

        job_main()
        return

    from app.receiver import main as receiver_main

    receiver_main()


if __name__ == "__main__":
    main()
