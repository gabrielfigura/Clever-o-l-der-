import asyncio
from playwright.async_api import async_playwright
import requests

# Telegram config
TOKEN = '8163319902:AAHE9LZ984JCIc-Lezl4WXR2FsGHPEFTxRQ'
CHAT_ID = -1002597090660

# URL do jogo
URL = "https://launchdigi.net/GamesLaunch/Launch?deviceType=1&gameId=14529&lang=pt&mainDomain=strike777.bet&operatorId=88AAAC1D&playMode=real&token=strike777_CvWF0YRBpQIIatLP"

def enviar_mensagem(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=data)
    except Exception as e:
        print("Erro ao enviar para o Telegram:", e)

async def main():
    ultimos_3 = []
    verficar = ""
    regra = False
    dobrou = False
    loss = False
    loss_index = 3

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(URL)

            await page.wait_for_selector("iframe")
            await asyncio.sleep(5)

            frame = page.frames[-1]

            enviar_mensagem("✅ Bot conectado ao Bac Bo com sucesso!")

            while True:
                try:
                    elementos = await frame.locator('svg[data-role="Bead-road"] svg svg[data-type="roadItem"]').all()
                    total_anterior = len(elementos)

                    while True:
                        elementos_novos = await frame.locator('svg[data-role="Bead-road"] svg svg[data-type="roadItem"]').all()
                        if len(elementos_novos) > total_anterior:
                            break
                        await asyncio.sleep(1)

                    elementos = await frame.locator('svg[data-role="Bead-road"] svg svg[data-type="roadItem"]').all()
                    ultimo = elementos[-1]
                    texto = await ultimo.text_content()

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

                    if verficar:
                        msg = f"""
🚀 ENTRADA CONFIRMADA 🚀

Apostar no {"🔴" if verficar == "Vermelho" else "🔵"}
"""
                        enviar_mensagem(msg)
                        print(msg)

                except Exception as e:
                    print("Erro interno:", e)
                    enviar_mensagem(f"⚠️ ERRO INTERNO ⚠️\n{str(e)}")
                    await asyncio.sleep(3)

    except Exception as e:
        print("Erro fatal:", e)
        enviar_mensagem(f"❗ ERRO FATAL NO PLAYWRIGHT ❗\n{str(e)}")

# Iniciar
asyncio.run(main())
