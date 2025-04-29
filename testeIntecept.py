from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Escutar todas as requisições
    page.on("request", lambda request: print(f"Request URL: {request.url}"))

    page.goto('https://open.spotify.com')

    # Aqui você loga e navega manualmente para dar "Play" na música
    input("Pressione Enter depois de dar play...")  # Pausa para você clicar