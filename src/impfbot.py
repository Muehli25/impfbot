import time

from log import log
import settings
import api_wrapper
import alerts

from common import sleep


def check_for_slot() -> None:
    try:
        result = api_wrapper.fetch_api(
            plz=settings.ZIP,
            birthdate_timestamp=settings.BIRTHDATE.timestamp(),
            max_retries=5,
            sleep_after_error=settings.SLEEP_BETWEEN_FAILED_REQUESTS_IN_S,
            sleep_after_shadowban=settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN
        )
        for elem in result:
            if not elem['outOfStock']:
                log.info(
                    f"Free slot! ({elem['freeSlotSizeOnline']}) {elem['vaccineName']}/{elem['vaccineType']}")

                msg = f"Freier Impfslot ({elem['freeSlotSizeOnline']})! {elem['vaccineName']}/{elem['vaccineType']}"
                alerts.send_alert(msg)

                sleep(60*15, 15)
            else:
                log.info(f"No free slots.")
    except Exception as e:
        log.error(f"Something went wrong ({e})")


if __name__ == "__main__":
    try:
        while True:
            check_for_slot()
            sleep(settings.SLEEP_BETWEEN_REQUESTS_IN_S, settings.JITTER)
    except (KeyboardInterrupt, SystemExit):
        print("Bye...")
