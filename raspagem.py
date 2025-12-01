import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

class RaspagemDSM:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.urls = [
            'example.com',
            'example.com.br'
        ]
        self.dados_coletados = {}
    
    def fazer_requisicao(self, url):
        """Faz a requisição HTTP e retorna o conteúdo"""
        try:
            print(f"Acessando: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
            return None
    
    def extrair_texto_completo(self, soup):
        """Extrai todo o texto visível da página"""
        # Remove scripts e styles
        for script in soup(["script", "style", "meta", "link"]):
            script.decompose()
        
        texto = soup.get_text(separator='\n', strip=True)
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        return '\n'.join(linhas)
    
    def extrair_titulos(self, soup):
        """Extrai todos os títulos (h1, h2, h3, h4, h5, h6)"""
        titulos = {}
        for i in range(1, 7):
            tags = soup.find_all(f'h{i}')
            if tags:
                titulos[f'h{i}'] = [tag.get_text(strip=True) for tag in tags]
        return titulos
    
    def extrair_paragrafos(self, soup):
        """Extrai todos os parágrafos"""
        paragrafos = soup.find_all('p')
        return [p.get_text(strip=True) for p in paragrafos if p.get_text(strip=True)]
    
    def extrair_listas(self, soup):
        """Extrai listas ordenadas e não ordenadas"""
        listas = {'ul': [], 'ol': []}
        
        # Listas não ordenadas
        for ul in soup.find_all('ul'):
            itens = [li.get_text(strip=True) for li in ul.find_all('li')]
            if itens:
                listas['ul'].append(itens)
        
        # Listas ordenadas
        for ol in soup.find_all('ol'):
            itens = [li.get_text(strip=True) for li in ol.find_all('li')]
            if itens:
                listas['ol'].append(itens)
        
        return listas
    
    def extrair_tabelas(self, soup):
        """Extrai dados de tabelas"""
        tabelas = []
        for table in soup.find_all('table'):
            dados_tabela = []
            
            # Extrai cabeçalhos
            headers = []
            thead = table.find('thead')
            if thead:
                headers = [th.get_text(strip=True) for th in thead.find_all(['th', 'td'])]
            
            # Extrai linhas
            tbody = table.find('tbody') or table
            for tr in tbody.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    dados_tabela.append(cells)
            
            if dados_tabela:
                tabelas.append({
                    'headers': headers,
                    'dados': dados_tabela
                })
        
        return tabelas
    
    def extrair_links(self, soup, url_base):
        """Extrai todos os links da página"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            texto = a.get_text(strip=True)
            links.append({
                'texto': texto,
                'url': href
            })
        return links
    
    def extrair_imagens(self, soup):
        """Extrai informações sobre imagens"""
        imagens = []
        for img in soup.find_all('img'):
            imagens.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        return imagens
    
    def extrair_metadados(self, soup):
        """Extrai metadados da página"""
        metadados = {}
        
        # Title
        title = soup.find('title')
        if title:
            metadados['title'] = title.get_text(strip=True)
        
        # Meta tags
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property', '')
            content = meta.get('content', '')
            if name and content:
                meta_tags[name] = content
        
        metadados['meta_tags'] = meta_tags
        return metadados
    
    def extrair_divs_importantes(self, soup):
        """Extrai conteúdo de divs com classes/ids relevantes"""
        divs_importantes = {}
        
        # Classes comuns de conteúdo
        classes_relevantes = ['content', 'main', 'article', 'post', 'entry', 'curso', 'grade', 'matriz']
        
        for classe in classes_relevantes:
            divs = soup.find_all('div', class_=lambda x: x and classe in x.lower() if x else False)
            if divs:
                divs_importantes[classe] = [div.get_text(separator='\n', strip=True) for div in divs]
        
        return divs_importantes
    
    def processar_pagina(self, url):
        """Processa uma página completa"""
        html = self.fazer_requisicao(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        dados = {
            'url': url,
            'data_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metadados': self.extrair_metadados(soup),
            'titulos': self.extrair_titulos(soup),
            'paragrafos': self.extrair_paragrafos(soup),
            'listas': self.extrair_listas(soup),
            'tabelas': self.extrair_tabelas(soup),
            'links': self.extrair_links(soup, url),
            'imagens': self.extrair_imagens(soup),
            'divs_importantes': self.extrair_divs_importantes(soup),
            'texto_completo': self.extrair_texto_completo(soup)
        }
        
        return dados
    
    def executar_raspagem(self):
        """Executa a raspagem de todas as URLs"""
        print("=" * 80)
        print("Iniciando raspagem do curso Desenvolvimento de Software Multiplataforma")
        print("=" * 80)
        
        for i, url in enumerate(self.urls, 1):
            print(f"\n[{i}/{len(self.urls)}] Processando: {url}")
            dados = self.processar_pagina(url)
            
            if dados:
                self.dados_coletados[f'pagina_{i}'] = dados
                print(f"✓ Página {i} processada com sucesso!")
            else:
                print(f"✗ Erro ao processar página {i}")
            
            # Aguarda um pouco entre requisições para não sobrecarregar o servidor
            if i < len(self.urls):
                time.sleep(2)
        
        print("\n" + "=" * 80)
        print("Raspagem concluída!")
        print("=" * 80)
    
    def salvar_json(self, nome_arquivo='dados_example.json'):
        """Salva os dados em formato JSON"""
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.dados_coletados, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Dados salvos em: {nome_arquivo}")
    
    def salvar_txt(self, nome_arquivo='dados_example.txt'):
        """Salva os dados em formato texto legível"""
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RASPAGEM - Casa Deep Brasil\n")
            f.write("=" * 80 + "\n\n")
            
            for chave, dados in self.dados_coletados.items():
                f.write(f"\n{'=' * 80}\n")
                f.write(f"{chave.upper()}\n")
                f.write(f"URL: {dados['url']}\n")
                f.write(f"Data: {dados['data_coleta']}\n")
                f.write(f"{'=' * 80}\n\n")
                
                # Metadados
                if dados['metadados'].get('title'):
                    f.write(f"TÍTULO: {dados['metadados']['title']}\n\n")
                
                # Títulos
                if dados['titulos']:
                    f.write("TÍTULOS:\n")
                    for nivel, titulos in dados['titulos'].items():
                        for titulo in titulos:
                            f.write(f"  [{nivel}] {titulo}\n")
                    f.write("\n")
                
                # Tabelas
                if dados['tabelas']:
                    f.write("TABELAS:\n")
                    for i, tabela in enumerate(dados['tabelas'], 1):
                        f.write(f"\n  Tabela {i}:\n")
                        if tabela['headers']:
                            f.write(f"    Cabeçalhos: {' | '.join(tabela['headers'])}\n")
                        for linha in tabela['dados']:
                            f.write(f"    {' | '.join(linha)}\n")
                    f.write("\n")
                
                # Listas
                if dados['listas']['ul'] or dados['listas']['ol']:
                    f.write("LISTAS:\n")
                    for i, lista in enumerate(dados['listas']['ul'], 1):
                        f.write(f"\n  Lista não ordenada {i}:\n")
                        for item in lista:
                            f.write(f"    • {item}\n")
                    for i, lista in enumerate(dados['listas']['ol'], 1):
                        f.write(f"\n  Lista ordenada {i}:\n")
                        for j, item in enumerate(lista, 1):
                            f.write(f"    {j}. {item}\n")
                    f.write("\n")
                
                # Texto completo
                f.write("TEXTO COMPLETO:\n")
                f.write("-" * 80 + "\n")
                f.write(dados['texto_completo'])
                f.write("\n\n")
        
        print(f"✓ Dados salvos em: {nome_arquivo}")
    
    def gerar_relatorio(self):
        """Gera um relatório resumido"""
        print("\n" + "=" * 80)
        print("RELATÓRIO DA RASPAGEM")
        print("=" * 80)
        
        for chave, dados in self.dados_coletados.items():
            print(f"\n{chave.upper()}:")
            print(f"  URL: {dados['url']}")
            print(f"  Títulos encontrados: {sum(len(t) for t in dados['titulos'].values())}")
            print(f"  Parágrafos: {len(dados['paragrafos'])}")
            print(f"  Tabelas: {len(dados['tabelas'])}")
            print(f"  Links: {len(dados['links'])}")
            print(f"  Imagens: {len(dados['imagens'])}")

def main():
    # Cria instância do raspador
    raspador = RaspagemDSM()
    
    # Executa a raspagem
    raspador.executar_raspagem()
    
    # Salva os resultados
    raspador.salvar_json('dados_example.json')
    raspador.salvar_txt('dados_example.txt')
    
    # Gera relatório
    raspador.gerar_relatorio()
    
    print("\n✓ Processo finalizado com sucesso!")
    print("\nArquivos gerados:")
    print("  - dados_example.json (formato estruturado)")
    print("  - dados_example.txt (formato legível)")

if __name__ == "__main__":
    main()
