import requests


# WordPress API URL
WP_API_URL = "https://{domain}/wp-json/wp/v2/{content_type}"

# Simulate a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

print(WP_API_URL.format(domain='moving2madrid.com', content_type=''))
def main(domain, content_type):
	response = requests.get(WP_API_URL.format(domain=domain, content_type=content_type), headers=HEADERS, params={"per_page": 100, "page": 1})
	print(response)



if __name__ == '__main__':
	domain = input('Domain Name: ')
	content_type = input('Content type: ')
	main(domain, content_type)