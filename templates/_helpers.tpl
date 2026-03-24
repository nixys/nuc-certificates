{{- define "nuc-certificates.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "nuc-certificates.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "nuc-certificates.labels" -}}
app.kubernetes.io/name: {{ include "nuc-certificates.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ include "nuc-certificates.chart" . }}
{{- end -}}

{{- define "nuc-certificates.renderResource" -}}
{{- $root := .root -}}
{{- $item := .item -}}
{{- $resourceName := .resourceName -}}
{{- $resourceKey := .resourceKey -}}
{{- $shouldIgnore := eq (get ($item.annotations | default dict) "helm-docs.nuc.internal/ignore") "true" -}}
{{- if not $shouldIgnore -}}
{{- $defaultLabels := include "nuc-certificates.labels" $root | fromYaml -}}
{{- $labels := mustMergeOverwrite (dict) $defaultLabels ($root.Values.commonLabels | default dict) ($item.labels | default dict) -}}
{{- $annotations := mustMergeOverwrite (dict) ($root.Values.commonAnnotations | default dict) ($item.annotations | default dict) -}}
apiVersion: {{ default .defaultApiVersion $item.apiVersion }}
kind: {{ .kind }}
metadata:
  name: {{ required (printf "%s key is required" $resourceKey) $resourceName }}
  {{- if .namespaced }}
  namespace: {{ default $root.Release.Namespace $item.namespace }}
  {{- end }}
  labels:
{{ toYaml $labels | nindent 4 }}
  {{- if $annotations }}
  annotations:
{{ toYaml $annotations | nindent 4 }}
  {{- end }}
{{- with $item.spec }}
spec:
{{ toYaml . | nindent 2 }}
{{- end }}
{{- with $item.status }}
status:
{{ toYaml . | nindent 2 }}
{{- end }}
{{- end }}
{{- end -}}

{{- define "nuc-certificates.renderResourceCollection" -}}
{{- $root := .root -}}
{{- $items := .items | default dict -}}
{{- $resourceKey := .resourceKey -}}
{{- $defaultApiVersion := .defaultApiVersion -}}
{{- $kind := .kind -}}
{{- $namespaced := .namespaced -}}
{{- $documents := list -}}
{{- range $resourceName, $item := $items -}}
{{- if kindIs "map" $item -}}
{{- $rendered := include "nuc-certificates.renderResource" (dict "root" $root "item" $item "resourceName" $resourceName "resourceKey" (printf "%s[%q]" $resourceKey $resourceName) "kind" $kind "defaultApiVersion" $defaultApiVersion "namespaced" $namespaced) -}}
{{- if $rendered -}}
{{- $documents = append $documents $rendered -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- join "\n---\n" $documents -}}
{{- end -}}
