{{/* vim: set filetype=mustache: */}}
{{/*
Ficheiro de helpers para meu-chart.
Eu defino aqui templates nomeados (helpers) que podem ser reutilizados
nos outros ficheiros de template YAML.
*/}}

{{/*
Labels comuns para a API 1.
Isto é para garantir que todos os recursos da API 1 (Deployment, Service, Pods)
têm um conjunto consistente de labels.
*/}}
{{- define "meu-chart.api1.labels" -}}
app.kubernetes.io/name: api1
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ include "meu-chart.chart" . }}
{{- end -}}

{{/*
Selector labels para a API 1.
Usado pelo Deployment para saber quais Pods gerir e pelo Service para saber quais Pods direcionar.
Deve corresponder aos labels definidos nos Pods criados pelo Deployment.
*/}}
{{- define "meu-chart.api1.selectorLabels" -}}
app.kubernetes.io/name: api1
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Labels comuns para a API 2.
*/}}
{{- define "meu-chart.api2.labels" -}}
app.kubernetes.io/name: api2
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ include "meu-chart.chart" . }}
{{- end -}}

{{/*
Selector labels para a API 2.
*/}}
{{- define "meu-chart.api2.selectorLabels" -}}
app.kubernetes.io/name: api2
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Labels comuns para a API 3.
*/}}
{{- define "meu-chart.api3.labels" -}}
app.kubernetes.io/name: api3
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ include "meu-chart.chart" . }}
{{- end -}}

{{/*
Selector labels para a API 3.
*/}}
{{- define "meu-chart.api3.selectorLabels" -}}
app.kubernetes.io/name: api3
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Gera o nome do chart.
Usado em labels como \`helm.sh/chart: {{ include "meu-chart.chart" . }}\`
*/}}
{{- define "meu-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
