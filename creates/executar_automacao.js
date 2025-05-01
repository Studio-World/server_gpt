const executar = {
  key: 'executar_automacao',
  noun: 'Automação',
  display: {
    label: 'Executar Automação Web',
    description: 'Dispara automação com Playwright ou Selenium',
  },
  operation: {
    inputFields: [
      { key: 'url', required: true, type: 'string' },
      { key: 'engine', required: true, choices: ['playwright', 'selenium'] },
    ],
    perform: (z, bundle) => {
      const endpoint = bundle.inputData.engine === 'playwright'
        ? '/automation/playwright'
        : '/automation/selenium';
      return z.request({
        method: 'POST',
        url: `https://server-apig-gpt-1.onrender.com${endpoint}`,
        body: { url: bundle.inputData.url },
        headers: { 'content-type': 'application/json' },
      });
    }
  }
};

module.exports = executar;
