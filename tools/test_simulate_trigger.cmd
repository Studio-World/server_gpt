curl -X POST https://server-apig-gpt-1.onrender.com/zapier/webhook-trigger ^
  -H "Content-Type: application/json" ^
  -H "X-Zapier-Token: zapier123" ^
  -d "{\\\prompt\\t:\\\Abrir site GitHub\\\",\\\acao\\t:\\\"playwright\\\",\\\url\\t\\\"https://github.com\\\"}"
