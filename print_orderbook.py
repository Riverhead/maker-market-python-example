#! /usr/bin/python3
#
# This is a very basic script that prints out the order book and does
# a basic bid/ask calculation. The purpose of this code is to serve as
# a starting point for anyone that wants to write python bots against
# the simple market contract but needs help with the first bits.
#
# 01/07/2017 - Initial release - James R.

import json
from web3 import Web3, RPCProvider
from operator import itemgetter

precision = 1000000000000000000

web3rpc = Web3(RPCProvider())

web3rpc.eth.defaultAccount = "0xb19b144df98dc6cf672ec405d6c0816511cfa37f"
web3rpc.eth.defaultBlock = "latest"
# Can also be an integer or one of "latest", "pending", "earliest"

with open('simple_market.abi', 'r') as abi_file:
  abi_json = abi_file.read().replace('\n','')

abi = json.loads(abi_json)

#repston
#contract = web3rpc.eth.contract(abi, address="0x0bC603C1e35e0A7C16623230b2C10cA1668cb0C8")

#live
contract = web3rpc.eth.contract(abi, address="0x1292714f89F535C066D483E92a54b360f3dF7589")

last_offer_id = contract.call().last_offer_id()

id = 0
offers = []

while id <  last_offer_id + 1:
  offers.append(contract.call().offers(id))
  id = id + 1

print("<html>")
print("<head>")
print("<style>")
#print("table, th, td { border: 1px solid black; border-collapse: collapse; }")
print("</style>")
print("</head>")
print("  <body>")
print("    <h1>Maker Market Orders</h1>")

id=0

buy_orders = []
sell_orders = []

for offer in offers:
  valid = offer[5]
  if valid:
    sell_how_much = float(offer[0]) / precision
    sell_which_token = offer[1]
    buy_how_much = float(offer[2]) / precision
    buy_which_token = offer[3]
    owner = offer[4][2:8]

    if sell_which_token == "0xc66ea802717bfb9833400264dd12c2bceaa34a6d":
      s_token = "MKR"
    elif sell_which_token == "0xa74476443119A942dE498590Fe1f2454d7D4aC0d":
      s_token = "W-GNT"
    else:
      s_token = "W-ETH"

    if buy_which_token == "0xc66ea802717bfb9833400264dd12c2bceaa34a6d":
      b_token = "MKR"
    elif sell_which_token == "0xa74476443119A942dE498590Fe1f2454d7D4aC0d":
      b_token = "W-GNT"
    else:
      b_token = "W-ETH"

    if s_token == "MKR" and b_token == "W-ETH":
      sell_orders.append([id, sell_how_much, buy_how_much/sell_how_much, buy_how_much, owner])

    if s_token == "W-ETH" and b_token == "MKR":
      buy_orders.append([id, sell_how_much, sell_how_much/buy_how_much, buy_how_much, owner])
    id = id + 1

print("<table border='1'>")
print("<td valign = 'top'>")
print("    <table>")
print("      <h2>Buy Orders</h2>")
print("      <tr><th>ID</th><th>MKR</th><th>Bid</th><th>ETH</th><th>Owner</th></tr>")
buy_orders.sort(key=itemgetter(2), reverse=True)
for order in buy_orders:
  print("      <tr><td align = 'center'>%0.0f</td><td align = 'right'>%0.5f</td><td align = 'right' bgcolor='lightgreen'>%0.5f</td><td align = 'right'>%0.5f</td><td align = 'right'>%s</tr>" % (order[0], order[1], order[2], order[3], order[4]))
print("    </table>")

print("</td>")
print("<td valign = 'top'>")

print("    <table>")
print("      <h2>Sell Orders</h2>")
print("      <tr><th>ID</th><th>MKR</th><th>Ask</th><th>ETH</th><th>Owner</th></tr>")
sell_orders.sort(key=itemgetter(2), reverse=False)
for order in sell_orders:
  print("      <tr><td align = 'center'>%0.0f</td><td align = 'right'>%0.5f</td><td align = 'right' bgcolor='#f96969'>%0.5f</td><td align = 'right'>%0.5f</td><td align = 'right'>%s</tr>" % (order[0], order[1], order[2], order[3], order[4]))
print("    </table>")

print("</td>")
print("</table>")
print("<BR>Recommended Actions for 1% edge:<BR>")
print("Place buy at %0.4f<BR>" % (buy_orders[0][2] * 1.01))
print("Place sell at %0.5f<BR>" % (sell_orders[0][2] * 0.99))
print("<BR>Notes:")
print("<BR>1. Make sure you aren't bidding against yourself")
print("<BR>2. Calc edge at a depth/age to avoid getting gamed")
print("  </body>")
print("</html>")


