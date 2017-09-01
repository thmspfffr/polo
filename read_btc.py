import datetime, time
from polo import poloniex

api = 'O1O0O76T-Z2M0ZOQM-15NPVFG0-AUKH3WKH'
sec = 'c12cfb5fa7bb7506e190ed7b0a48a864eb2179f4ddc8793321b75154752325c77f472b98abc756cc390d37c553c0ffd5bed88dbe247f2bb41af5c641cc1408eb'

btc_ticker = poloniex(api,sec)

while True:
  now = datetime.datetime.now()
  tmp = btc_ticker.returnTicker()
  last_val_btc = float(tmp['USDT_BTC']['last'])
  last_val_xmr = float(tmp['USDT_XMR']['last'])
  t = datetime.datetime.now()
  ts = time.mktime(t.timetuple())
  output = open("btc.txt", "a")
  output.write("%s\t%s\t%s\n" % (ts,last_val_btc,last_val_xmr))
  output.close()
  time.sleep(10)



segleng = 4;
segshift = 1;
nseg = (length(btc)-segleng)/segshift+1;

for i = 1 : nseg

v(i,1) = var(btc((i-1)*segshift+1:(i-1)*segshift+segleng,2));
v(i,2) = var(btc((i-1)*segshift+1:(i-1)*segshift+segleng,3));

end