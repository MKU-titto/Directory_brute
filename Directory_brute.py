import requests

def check_http_methods(base_url, wordlist_path):
    """
    Перевіряє доступні HTTP методи для директорій з wordlist.txt
    base_url: Базовий URL (наприклад, https://example.com)
    wordlist_path: Шлях до файлу зі списком директорій
    Результат: Список URL та методів, які відповідають кодами 200, 301, 302, 403
    """
    http_methods = ["GET", "POST", "TRACE", "PUT", "HEAD", "OPTIONS"]
    valid_status_codes = {200, 301, 302, 403}
    results = []

    try:
        with open(wordlist_path, 'r') as file:
            directories = [line.strip() for line in file if line.strip()]

        for directory in directories:
            url = f"{base_url}/{directory}"
            print(f"Перевірка: {url}")

            for method in http_methods:
                try:
                    response = requests.request(method, url, allow_redirects=False, timeout=5)

                    if response.status_code in valid_status_codes:
                        results.append((url, method, response.status_code))
                        print(f" {method} {url} -> {response.status_code}")
                except requests.RequestException as e:
                    print(f" Помилка для {method} {url}: {e}")

    except FileNotFoundError:
        print(f"Файл {wordlist_path} не знайдено.")
    except Exception as e:
        print(f"Сталася помилка: {e}")

    return results

if __name__ == "__main__":
    base_url = input("Введіть URL (наприклад, https://example.com): ").strip()
    wordlist_path = input("Введіть шлях до wordlist.txt: ").strip()

    results = check_http_methods(base_url, wordlist_path)

    print("Результати:")
    for url, method, status_code in results:
        print(f"{url} | Метод: {method} | Код відповіді: {status_code}")
