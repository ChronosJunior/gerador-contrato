function myFunction() {
  // Variáveis da Planilha de Banco de Dados
  let app = SpreadsheetApp;
  let spreadsheet = app.getActiveSpreadsheet();
  let sheet = spreadsheet.getSheetByName('Dados');

  // Variável do arquivo de Mala Direta
  let docsMalaDireta = DocumentApp.openByUrl("https://docs.google.com/document/d/1ei4bqAXq7MwTCf2fdi-Eam1y7VPRQ0yiHujyIectFSg/edit");

  // Variável do arquivo de Template
  let docsTemplate = DocumentApp.openByUrl("https://docs.google.com/document/d/1RNhgBEqp5k3TZgp3IUDBcK8n9HsQZRaHJ39rDXmiAAs/edit");

  // Função que gera a mala direta
  function criarMalaDireta() {
    docsMalaDireta.getBody().clear();
    let paragrafos = docsTemplate.getBody().getParagraphs();
    let nomes = sheet.getRange('E39:E').getValues().filter(elem => elem[0] !== '');
    let rgs = sheet.getRange('G39:G').getValues();
    let cpfs = sheet.getRange('F39:F').getValues();
    let meses = sheet.getRange('I39:I').getValues();
    let anos = sheet.getRange('J39:J').getValues();
    let nacionalidades = sheet.getRange('Q39:Q').getValues();
    let civis = sheet.getRange('R39:R').getValues();
    let ocupacoes = sheet.getRange('S39:S').getValues();
    let ufs = sheet.getRange('H39:H').getValues();
    let ruas = sheet.getRange('K39:K').getValues();
    let ns = sheet.getRange('L39:L').getValues();
    let bairros = sheet.getRange('M39:M').getValues();
    let cidades = sheet.getRange('N39:N').getValues();
    let ceps = sheet.getRange('P39:P').getValues();

    nomes.forEach((nome, index) => {
      let rg = rgs[index][0];
      let cpf = cpfs[index][0];
      let mes = meses[index][0];
      let ano = anos[index][0];
      let nacionalidade = nacionalidades[index][0];
      let civil = civis[index][0];
      let ocupacao = ocupacoes[index][0];
      let uf = ufs[index][0];
      let rua = ruas[index][0];
      let n = ns[index][0];
      let bairro = bairros[index][0];
      let cidade = cidades[index][0];
      let cep = ceps[index][0];

      paragrafos.forEach(paragrafo => {
        let novoParagrafo = paragrafo.copy();
        novoParagrafo.replaceText("{{Nome}}", nome[0])
                     .replaceText("{{RG}}", rg)
                     .replaceText("{{CPF}}", cpf)
                     .replaceText("{{MES}}", mes)
                     .replaceText("{{ANO}}", ano)
                     .replaceText("{{Nacionalidade}}", nacionalidade)
                     .replaceText("{{Estado civil}}", civil)
                     .replaceText("{{Ocupacao}}", ocupacao)
                     .replaceText("{{Cidade}}", cidade)
                     .replaceText("{{CEP}}", cep)
                     .replaceText("{{UF}}", uf)
                     .replaceText("{{RUA}}", rua)
                     .replaceText("{{N}}", n)
                     .replaceText("{{Bairro}}", bairro);
        docsMalaDireta.getBody().appendParagraph(novoParagrafo);
      });
      docsMalaDireta.getBody().appendPageBreak();
    });
  }

  criarMalaDireta();
}
