const perform = async (z, bundle) => {
  const response = await z.request({
    method: 'POST',
    url: 'https://server-apig-gpt-1.onrender.com/zapier/webhook-trigger',
    headers: {
      'X-Zapier-Token': process.env.ZAPIER_SECRET || 'zapier123',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ origem: 'zapier_trigger', teste: true })
  });

  z.console.log('Resposta do DAN:', response.json);
  return response.json;
};

module.exports = {
  key: 'dan_event',
  noun: 'Evento do DAN',
  display: {
    label: 'Novo Evento do DAN',
    description: 'Dispara quando o DAN envia um novo evento'
  },
  operation: {
    perform,
    type: 'polling', // ou 'hook' se quiser usar webhook
    sample: {
      id: 123,
      mensagem: 'Exemplo de evento DAN',
      dados: { foo: 'bar' }
    },
    outputFields: [
      { key: 'id', label: 'ID do Evento' },
      { key: 'mensagem', label: 'Mensagem' },
      { key: 'dados', label: 'Dados Brutos', type: 'object' }
    ]
  }
};
