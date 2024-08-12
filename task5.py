from playwright.sync_api import sync_playwright

def fetch_google_search_results(query, num_results=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/")
   
        search_input = page.locator('//*[@id="APjFqb"]')
        search_input.wait_for(state='visible', timeout=30000)
        
        if search_input.is_visible():
            search_input.fill(query)
            page.keyboard.press('Enter')
        else:
            print("Search input not found")
            browser.close()
            return

        page.wait_for_selector('h3', timeout=20000)

        results = [element.text_content() for element in page.locator('h3').all()[:num_results]]

        for i, result in enumerate(results, 1):
            print(f"{i}. {result}")

        with open("search_results.txt", 'w') as file:
            for i, result in enumerate(results, 1):
                file.write(f"{i}. {result}\n")

        browser.close()

fetch_google_search_results('pytest')
