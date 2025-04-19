# Micro-Projeto: APIs Python com Docker, Minikube e Helm

## Introdução

Este repositório documenta um projeto prático e passo a passo, focado na aprendizagem de tecnologias essenciais de DevOps e Cloud Native: Docker, Kubernetes (via Minikube) e Helm.

## Propósito

O objetivo principal é ganhar experiência prática com o ciclo de vida de uma aplicação containerizada:

1.  **Desenvolvimento:** Criar aplicações web simples (APIs) usando Python e Flask.
2.  **Containerização:** Empacotar as aplicações e suas dependências em imagens Docker usando Dockerfiles.
3.  **Orquestração Local:** Implantar e gerir os containers num cluster Kubernetes local simulado pelo Minikube.
4.  **Gestão de Deployments:** Utilizar o Helm para criar um pacote reutilizável (Chart) que define e gere os recursos Kubernetes necessários para a aplicação.

O projeto evoluiu para incluir três APIs interativas que se ligam umas às outras (Dia -> Data -> Hora -> Data...). Crucialmente, as APIs foram **refatoradas para ler os URLs das outras APIs a partir de variáveis de ambiente**, em vez de usar links "hardcoded". O Helm Chart foi atualizado para injetar essas variáveis de ambiente com os **nomes de serviço DNS internos do Kubernetes**, preparando a aplicação para comunicação dentro do cluster e para deployments mais complexos (como Ingress ou Cloud).

O foco manteve-se na utilização da linha de comandos (CLI) no Linux.

## Tecnologias Utilizadas

* Python 3 (Flask)
* Docker
* Minikube
* Kubectl
* Helm v3
* Git / GitHub
* Rocky Linux 9.5 (como ambiente de desenvolvimento/teste)

## Pré-requisitos

* Um sistema operativo Linux (testado no Rocky Linux 9.5, comandos `dnf` podem precisar de ser adaptados para `apt` em distros baseadas em Debian/Ubuntu).
* Acesso à linha de comandos (terminal).
* Conexão à Internet (para descarregar ferramentas e imagens base).
* Ferramentas instaladas:
    * **Git:** [Instruções de Instalação](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
    * **Python 3 (>= 3.8) e Pip:** Geralmente pré-instalado. Verificar com `python3 --version` e `pip3 --version`.
    * **Docker Engine:** [Instruções de Instalação (CentOS/Rocky)](https://docs.docker.com/engine/install/centos/) (Requer configuração pós-instalação, como adicionar utilizador ao grupo `docker`).
    * **Minikube:** [Instruções de Instalação](https://minikube.sigs.k8s.io/docs/start/)
    * **Kubectl:** [Instruções de Instalação](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
    * **Helm:** [Instruções de Instalação](https://helm.sh/docs/intro/install/)

## Como Replicar e Testar (Estado Atual)

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/lucasmgpy/docker-kube-helm.git](https://github.com/lucasmgpy/docker-kube-helm.git)
    cd docker-kube-helm
    ```

2.  **Garantir Pré-requisitos:** Certifica-te que todas as ferramentas listadas acima estão instaladas e que o serviço Docker está a correr (`sudo systemctl status docker`).

3.  **Construir as Imagens Docker (Versões Atuais):**
    Navega para o diretório de cada API e constrói a imagem correspondente com a tag correta.
    ```bash
    # API 1 (v1 contém a leitura de env var)
    cd api1 && docker build -t api1:v1 . && cd ..

    # API 2 (v1 contém leitura de env vars e layout corrigido)
    cd api2 && docker build -t api2:v1 . && cd ..

    # API 3 (v1 contém leitura de env var e JS clock)
    cd api3 && docker build -t api3:v1 . && cd ..

    # Verifica se as imagens foram criadas
    docker images | grep -E "api1|api2|api3"
    ```

4.  **Iniciar o Minikube:**
    ```bash
    minikube start --driver=docker
    ```

5.  **Carregar Imagens para o Minikube:**
    (Garante que o Kubernetes encontra as versões corretas das imagens locais)
    ```bash
    minikube image load api1:v1
    minikube image load api2:v1
    minikube image load api3:v1
    ```

6.  **Instalar/Atualizar a Aplicação com Helm:**
    Usamos `helm upgrade --install` que instala a release se ela não existir, ou atualiza-a se já existir (aplicando as últimas alterações do chart, como as novas tags de imagem e as variáveis de ambiente nos deployments).
    ```bash
    helm upgrade --install meu-release ./meu-chart
    ```

7.  **Verificar os Pods:**
    Espera até que todos os Pods estejam no estado `Running` e que estejam a usar as imagens corretas (v2, v4, v2).
    ```bash
    kubectl get pods -w -l app.kubernetes.io/instance=meu-release
    # (Pressiona Ctrl+C para sair quando estiverem Running)
    ```
    Se algum Pod ficar em erro, verifica o carregamento das imagens (passo 5) ou usa `kubectl describe pod <nome-pod>` para mais detalhes.

8.  **Aceder às APIs (Usando Port-Forward):**
    Neste estado, os links gerados pelas APIs usam nomes DNS internos do Kubernetes (ex: `http://meu-release-api2-service:80/date`). Estes nomes não são resolvidos pelo teu browser fora do cluster. Para testar, usamos `kubectl port-forward`.

    * **Opção A (Testar Funcionalidade Individual):** Abre 3 terminais e executa:
        * Terminal 1: `kubectl port-forward service/meu-release-api1-service 9000:80`
        * Terminal 2: `kubectl port-forward service/meu-release-api2-service 9001:80`
        * Terminal 3: `kubectl port-forward service/meu-release-api3-service 9002:80`
        * **Teste:** Acede manualmente a `http://localhost:9000`, `http://localhost:9001/date`, `http://localhost:9002/time` no browser para ver cada API. Clicar nos links *não* funcionará para navegação direta entre eles neste modo.

    * **Opção B (Testar Links Clicáveis com Portas Específicas):** Para fazer os links funcionarem *neste cenário específico de port-forward*, mapeia as portas locais para corresponderem às portas usadas nos URLs internos (que foram originalmente baseados em `localhost:porta`). Abre 3 terminais:
        * Terminal 1: `kubectl port-forward service/meu-release-api1-service 5000:80`
        * Terminal 2: `kubectl port-forward service/meu-release-api2-service 5001:80`
        * Terminal 3: `kubectl port-forward service/meu-release-api3-service 5002:80`
        * **Teste:** Abre `http://localhost:5000`. Agora, clicar nos links *deveria* permitir navegar entre as APIs, pois os `href` gerados (ex: `http://meu-release-api2-service:80/date`) serão corretamente encaminhados pelos túneis `port-forward` que estão a ouvir nas portas `localhost` esperadas (5001, 5002, 5000).

    **Mantém os três terminais a executar os comandos `port-forward` durante o teste.**

## Próximos Passos (Planeados)

* Implementar um **Kubernetes Ingress** para expor as três APIs através de um único ponto de entrada e permitir o uso de links relativos.
* Explorar o deployment em cloud (ex: Google Kubernetes Engine - GKE).
* Configurar um pipeline de CI/CD.

## Limpeza

Quando terminares os testes:

1.  Para os comandos `kubectl port-forward` nos três terminais (Ctrl+C).
2.  Desinstala a release Helm:
    ```bash
    helm uninstall meu-release
    ```
3.  Para o cluster Minikube:
    ```bash
    minikube stop
    ```
4.  (Opcional) Apaga o cluster Minikube e os dados associados:
    ```bash
    minikube delete
    ```
5.  (Opcional) Remove as imagens Docker construídas (usa as tags corretas):
    ```bash
    docker rmi api1:v2 api2:v4 api3:v2
    ```
6.  (Opcional) Remove as imagens do cache do Minikube (se `minikube delete` não foi usado):
    ```bash
    minikube image rm api1:v2 api2:v4 api3:v2
    ```