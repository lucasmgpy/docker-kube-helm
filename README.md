# Micro-Projeto: APIs Python com Docker, Minikube e Helm

## Introdução

Este repositório documenta um projeto prático e passo a passo, focado na aprendizagem de tecnologias essenciais de DevOps e Cloud Native: Docker, Kubernetes (via Minikube) e Helm.

## Propósito

O objetivo principal é ganhar experiência prática com o ciclo de vida de uma aplicação containerizada:

1.  **Desenvolvimento:** Criar aplicações web simples (APIs) usando Python e Flask.
2.  **Containerização:** Empacotar as aplicações e suas dependências em imagens Docker usando Dockerfiles.
3.  **Orquestração Local:** Implantar e gerir os containers num cluster Kubernetes local simulado pelo Minikube.
4.  **Gestão de Deployments:** Utilizar o Helm para criar um pacote reutilizável (Chart) que define e gere os recursos Kubernetes necessários para a aplicação.

O projeto evoluiu para incluir três APIs interativas que se ligam umas às outras (Dia -> Data -> Hora -> Data...), demonstrando comunicação básica entre serviços (ainda que com links hardcoded neste exemplo). O foco manteve-se na utilização da linha de comandos (CLI) no Linux.

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

## Como Replicar e Testar

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/lucasmgpy/docker-kube-helm.git](https://github.com/lucasmgpy/docker-kube-helm.git)
    cd docker-kube-helm
    ```

2.  **Garantir Pré-requisitos:** Certifica-te que todas as ferramentas listadas acima estão instaladas e que o serviço Docker está a correr (`sudo systemctl status docker`).

3.  **Construir as Imagens Docker:**
    Navega para o diretório de cada API e constrói a imagem correspondente.
    ```bash
    # API 1
    cd api1 && docker build -t api1:v1 . && cd ..

    # API 2 (Nota: usa a tag v3 devido às atualizações)
    cd api2 && docker build -t api2:v3 . && cd ..

    # API 3
    cd api3 && docker build -t api3:v1 . && cd ..

    # Verifica se as imagens foram criadas
    docker images | grep -E "api1|api2|api3"
    ```

4.  **Iniciar o Minikube:**
    ```bash
    minikube start --driver=docker
    ```

5.  **Carregar Imagens para o Minikube:**
    (Este passo garante que o Kubernetes dentro do Minikube encontra as imagens locais)
    ```bash
    minikube image load api1:v1
    minikube image load api2:v3
    minikube image load api3:v1
    ```

6.  **Instalar/Atualizar a Aplicação com Helm:**
    Usamos `helm upgrade --install` que instala a release se ela não existir, ou atualiza-a se já existir.
    ```bash
    helm upgrade --install meu-release ./meu-chart
    ```

7.  **Verificar os Pods:**
    Espera até que todos os Pods estejam no estado `Running`.
    ```bash
    kubectl get pods -w -l app.kubernetes.io/instance=meu-release
    # (Pressiona Ctrl+C para sair quando estiverem Running)
    ```
    Se algum Pod ficar em erro (ex: `ImagePullBackOff`), verifica se as imagens foram carregadas corretamente no passo 5 e tenta apagar o Pod (`kubectl delete pod <nome-do-pod>`) para que o Kubernetes tente recriá-lo.

8.  **Aceder às APIs (Usando Port-Forward):**
    Para testar a navegação entre as APIs clicando nos links (que estão hardcoded com `localhost:porta`), o método mais direto é usar `kubectl port-forward` com as portas locais correspondentes. Abre **três terminais separados**.

    * **Terminal 1 (API 1):** Encaminha a porta local 5000 para o serviço da API 1.
        ```bash
        kubectl port-forward service/meu-release-api1-service 5000:80
        ```
    * **Terminal 2 (API 2):** Encaminha a porta local 5001 para o serviço da API 2.
        ```bash
        kubectl port-forward service/meu-release-api2-service 5001:80
        ```
    * **Terminal 3 (API 3):** Encaminha a porta local 5002 para o serviço da API 3.
        ```bash
        kubectl port-forward service/meu-release-api3-service 5002:80
        ```

    **Mantém os três terminais a executar os comandos `port-forward`.**

9.  **Testar no Browser:**
    * Abre o browser e vai a `http://localhost:5000` (API 1).
    * Clica no link "WHAT DAY IS TODAY?". Deverás ir para `http://localhost:5001/date` (API 2).
    * Na API 2, clica no link "I challenge you...". Deverás ir para `http://localhost:5002/time` (API 3).
    * Na API 3, clica no link da hora. Deverás voltar para `http://localhost:5001/date` (API 2).
    * Na API 2, clica no link da data. Deverás voltar para `http://localhost:5000` (API 1).

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
5.  (Opcional) Remove as imagens Docker construídas:
    ```bash
    docker rmi api1:v1 api2:v3 api3:v1
    ```
6.  (Opcional) Remove as imagens do cache do Minikube (se carregadas):
    ```bash
    # Tenta remover (pode variar ligeiramente conforme a versão do minikube)
    minikube image rm api1:v1 api2:v3 api3:v1
    ```

