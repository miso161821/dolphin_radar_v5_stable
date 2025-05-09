from telegram_util import send_telegram
send_telegram("🚨 돌핀레이더 v5 정상 작동 시작합니다!")  # ✅ 실시간 테스트 알림 한 방!

from dolphin_directional import should_alert
from alt_pump_detector import scan_alts
from stealth_detector import detect_stealth_moves
from utils.fetch import fetch_candles
import threading, time

def monitor_btc_tf(tf):
    while True:
        candles = fetch_candles("BTC-USDT", tf)
        if not candles:
            print(f"[{tf}] ❌ 캔들 데이터 없음")
            time.sleep(60)
            continue
        price = candles[-1]["close"]
        rsi, obv, cvd = 50, 1, 1  # 추후 계산 로직 확장
        msg = should_alert(tf, candles, price, rsi, obv, cvd)
        if msg:
            send_telegram(msg)
        time.sleep(60)

def monitor_altcoins():
    while True:
        msgs = scan_alts()
        for msg in msgs:
            send_telegram(msg)
        time.sleep(300)

def monitor_stealth():
    while True:
        msgs = detect_stealth_moves()
        for msg in msgs:
            send_telegram(msg)
        time.sleep(900)

def monitor_status():
    while True:
        send_telegram("✅ 돌핀레이더 작동 중입니다 (1시간 주기 확인)")
        time.sleep(3600)

# 쓰레드 실행
for tf in ["5m", "15m", "1h", "4h"]:
    threading.Thread(target=monitor_btc_tf, args=(tf,), daemon=True).start()

threading.Thread(target=monitor_altcoins, daemon=True).start()
threading.Thread(target=monitor_stealth, daemon=True).start()
threading.Thread(target=monitor_status, daemon=True).start()

while True:
    time.sleep(600)
