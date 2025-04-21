import requests
from sys import exit

API_KEY = "056d605974eea18577eed680a6e41a58"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    resp = requests.get(
        BASE_URL,
        params={
            "q": city,
            "units": "metric",
            "lang": "ru",
            "appid": API_KEY,
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def show(weather: dict) -> None:

    w = weather
    print(
        f"\nПогода      : {w['weather'][0]['description']}"
        f"\nТемпература : {w['main']['temp']:.1f} °C"
        f"\nВлажность   : {w['main']['humidity']} %"
        f"\nДавление    : {w['main']['pressure']} hPa\n"
    )


def main() -> None:
    print("⛅️  Быстрый прогноз погоды (ENTER — выход)")

    while True:
        city = input("\nНазвание города: ").strip()
        if city.lower() in {"", "exit", "quit"}:
            exit()

        try:
            show(get_weather(city))
        except requests.exceptions.HTTPError as err:
            print("🚫 Сервер вернул ошибку:", err)
        except requests.exceptions.RequestException:
            print("⚠️  Сетевой сбой: проверьте подключение.")
        except (KeyError, IndexError):
            print("🤷  Не удалось понять ответ сервиса. Попробуйте другой город.")

        if input("Продолжить? [Y/n] ").lower().startswith("n"):
            break


if __name__ == "__main__":
    main()
