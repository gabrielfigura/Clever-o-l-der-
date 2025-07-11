import asyncio
from playwright.async_api import async_playwright
import requests
from time import sleep

# Telegram config
TOKEN = '8163319902:AAHE9LZ984JCIc-Lezl4WXR2FsGHPEFTxRQ'
CHAT_ID = -1002597090660

# Site URL
URL = "https://launchdigi.net/GamesLaunch/Launch?deviceType=1&gameId=14529&lang=pt&mainDomain=strike777.bet&operatorId=88AAAC1D&playMode=real&token=strike777_CvWF0YRBpQIIatLP"

# Envia mensagem ao Telegram
def enviar_mensagem(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erro Telegram:", e)

# Função principal com Playwright
async def main():
    ultimos_3 = []
    verficar = ""
    regra = False
    dobrou = False
    loss = False
    loss_index = 3

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(URL)

        # Aguardar e entrar nos iframes
        await page.wait_for_selector('iframe')
        frame1 = page.frame_locator("iframe").nth(0)
        await frame1.locator("iframe").wait_for()
        frame2 = frame1.frame_locator("iframe").nth(0)

        print("✅ Acesso ao jogo concluído.")

        while True:
            try:
                # Pega todos os elementos dos resultados
                elementos = await frame2.locator('svg[data-role="Bead-road"] svg svg[data-type="roadItem"]').all()
                total_anterior = len(elementos)

                # Espera novo resultado
                while True:
                    elementos_novos = await frame2.locator('svg[data-role="Bead-road"] svg svg[data-type="roadItem"]').all()
                    if len(elementos_novos) > total_anterior:
                        break
                    await asyncio.sleep(1)

                elementos = await frame2.locator('svg[data-role="Bead-road"] svg svg[data-type="roadItem"]').all()
                ultimo = elementos[-1]
                texto = await ultimo.inner_text()

                if texto == 'P':
                    resultado = 'Azul'
                elif texto == 'B':
                    resultado = 'Vermelho'
                elif texto == 'T':
                    resultado = 'Tie'
                else:
                    continue

                print("Resultado:", resultado)

                if loss:
                    loss_index -= 1
                    if loss_index > 0:
                        continue
                    else:
                        ultimos_3 = []
                        verficar = ""
                        regra = False
                        dobrou = False
                        loss = False
                        loss_index = 3

                if regra:
                    if resultado == verficar:
                        enviar_mensagem("✅✅✅ GREEN ✅✅✅")
                        dobrou = False
                        verficar = ""
                    else:
                        if dobrou:
                            enviar_mensagem("❌ LOSS ❌\n3 rodadas sem operar..")
                            verficar = ""
                            dobrou = False
                            loss = True
                            continue
                        else:
                            emoji = "🔴" if verficar == "Vermelho" else "🔵"
                            enviar_mensagem(f"🔄️ Fazer 2 GALES, Dobrar no {emoji}")
                            dobrou = True
                            continue

                ultimos_3.insert(0, resultado)
                ultimos_3 = ultimos_3[:3]
                print("Últimos 3:", ultimos_3)

                # Regras
                if ultimos_3 == ['Vermelho'] * 3:
                    verficar = 'Azul'
                    regra = True
                elif ultimos_3 == ['Azul'] * 3:
                    verficar = 'Vermelho'
                    regra = True
                elif ultimos_3 == ['Tie', 'Vermelho', 'Tie']:
                    verficar = 'Azul'
                    regra = True
                elif ultimos_3 == ['Tie', 'Azul', 'Tie']:
                    verficar = 'Vermelho'
                    regra = True
                elif ultimos_3 == ['Vermelho', 'Tie', 'Tie']:
                    verficar = 'Azul'
                    regra = True
                elif ultimos_3 == ['Azul', 'Tie', 'Tie']:
                    verficar = 'Vermelho'
                    regra = True
                elif ultimos_3 == ['Vermelho', 'Tie', 'Vermelho']:
                    verficar = 'Azul'
                    regra = True
                elif ultimos_3 == ['Azul', 'Tie', 'Azul']:
                    verficar = 'Vermelho'
                    regra = True
                else:
                    regra = False

                # Enviar entrada
                if verficar:
                    msg = f"""
🚀 ENTRADA CONFIRMADA 🚀

Apostar no {"🔴" if verficar == "Vermelho" else "🔵"}
"""
                    enviar_mensagem(msg)
                    print(msg)

            except Exception as e:
                print("Erro geral:", e)
                await asyncio.sleep(3)

# Rodar
asyncio.run(main())
