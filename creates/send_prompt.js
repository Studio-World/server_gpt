const perform = async (z, bundle) => {
  const prompt = bundle.inputData.prompt;

  const response = await z.request({
    method: 'POST',
    url: 'https://server-apig-gpt-1.onrender.com/v1/completions',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  });

  return {
    id: Date.now(),
    prompt,
    resposta: response.data.response,
  };
};

module.exports = {
  key: 'send_prompt',
  noun: 'Prompt',
  display: {
    label: 'Enviar Prompt para DAN',
    description: 'Gera uma resposta usando o modelo DAN-XBOX via API.',
  },
  operation: {
    perform,
    inputFields: [
      {
        key: 'prompt',
        required: true,
        label: 'Prompt',
        helpText: 'Digite o prompt que será enviado para o DAN responder.',
        type: 'string',
      },
    ],
    outputFields: [
      { key: 'id', label: 'ID da Resposta' },
      { key: 'prompt', label: 'Prompt Enviado' },
      { key: 'resposta', label: 'Resposta Gerada' },
    ],
  },
};
