# NUC Certificates

[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/nuc-certificates)](https://artifacthub.io/packages/search?repo=nuc-certificates)

Helm chart for rendering cert-manager custom resources from declarative values.

The chart does not install cert-manager CRDs or the cert-manager controllers. It only renders cert-manager resources that are already supported by the target cluster.

The supported resource set is based on the upstream cert-manager CRDs under [deploy/crds](https://github.com/cert-manager/cert-manager/tree/master/deploy/crds), but this chart renders the custom resources created from those CRDs rather than the CRDs themselves.

## Quick Start

Add the Nixys chart repository:

```bash
helm repo add nixys https://registry.nixys.io/chartrepo/public
# or
helm repo add nixys https://registry.nixys.ru/chartrepo/public
```

Install the chart:

```bash
helm install nuc-certificates . \
  --namespace cert-manager-resources \
  --create-namespace \
  -f values.yaml.example
```

Install the local README generator hook:

```bash
pre-commit install
pre-commit install-hooks
```

## Supported Resources

The chart can render these cert-manager kinds:

- `Certificate`
- `CertificateRequest`
- `Challenge`
- `ClusterIssuer`
- `Issuer`
- `Order`

Support for individual kinds and fields still depends on the cert-manager CRDs installed in the cluster.

## Values Model

Each top-level map in [values.yaml](values.yaml) groups one resource kind:

- `certificates`
- `certificateRequests`
- `challenges`
- `clusterIssuers`
- `issuers`
- `orders`

The resource name is the map key. Every map value uses the same generic contract:

| Field | Required | Description |
|-------|----------|-------------|
| `namespace` | no | Namespace for namespaced resources. Defaults to the Helm release namespace. Ignored for cluster-scoped resources. |
| `labels` | no | Labels merged on top of built-in chart labels and `commonLabels`. |
| `annotations` | no | Annotations merged on top of `commonAnnotations`. |
| `apiVersion` | no | Per-resource API version override. |
| `spec` | no | Raw resource spec rendered as-is. |
| `status` | no | Optional raw status block. Usually not managed through Helm in production. |

In a higher-precedence values file, set a map entry to `null` to suppress a default resource from a lower-precedence values file.

Global controls:

- `enabled`
- `nameOverride`
- `commonLabels`
- `commonAnnotations`
- `apiVersions.*`
- `global` (accepted for umbrella-chart compatibility and ignored by templates)

The value contract is validated by [values.schema.json](values.schema.json).

Only the chart-owned resource collections use maps. Raw CRD payloads under `spec` and `status` still follow the upstream cert-manager schemas, including any nested arrays they require.

## Helm Values

This section is generated from [values.yaml](values.yaml) by `helm-docs`. Edit [values.yaml](values.yaml) comments or [docs/README.md.gotmpl](docs/README.md.gotmpl), then run `pre-commit run helm-docs --all-files` or `make docs` if you need to refresh it outside a commit.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| apiVersions.certificate | string | `"cert-manager.io/v1"` | Default apiVersion for Certificate resources. |
| apiVersions.certificateRequest | string | `"cert-manager.io/v1"` | Default apiVersion for CertificateRequest resources. |
| apiVersions.challenge | string | `"acme.cert-manager.io/v1"` | Default apiVersion for Challenge resources. |
| apiVersions.clusterIssuer | string | `"cert-manager.io/v1"` | Default apiVersion for ClusterIssuer resources. |
| apiVersions.issuer | string | `"cert-manager.io/v1"` | Default apiVersion for Issuer resources. |
| apiVersions.order | string | `"acme.cert-manager.io/v1"` | Default apiVersion for Order resources. |
| certificateRequests | object | `{"certificate-request-example":{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"namespace":"default","spec":{},"status":{}}}` | CertificateRequest resources to render, keyed by resource name. |
| certificateRequests.certificate-request-example.annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| certificateRequests.certificate-request-example.apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| certificateRequests.certificate-request-example.labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| certificateRequests.certificate-request-example.namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| certificateRequests.certificate-request-example.spec | object | `{}` | CertificateRequest spec rendered as-is. |
| certificateRequests.certificate-request-example.status | object | `{}` | Optional resource status rendered as-is. |
| certificates | object | `{"certificate-example":{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"namespace":"default","spec":{},"status":{}}}` | Certificate resources to render, keyed by resource name. |
| certificates.certificate-example.annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| certificates.certificate-example.apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| certificates.certificate-example.labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| certificates.certificate-example.namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| certificates.certificate-example.spec | object | `{}` | Certificate spec rendered as-is. |
| certificates.certificate-example.status | object | `{}` | Optional resource status rendered as-is. |
| challenges | object | `{"challenge-example":{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"acme.cert-manager.io/v1","labels":{},"namespace":"default","spec":{},"status":{}}}` | Challenge resources to render, keyed by resource name. |
| challenges.challenge-example.annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| challenges.challenge-example.apiVersion | string | `"acme.cert-manager.io/v1"` | Per-resource apiVersion override. |
| challenges.challenge-example.labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| challenges.challenge-example.namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| challenges.challenge-example.spec | object | `{}` | Challenge spec rendered as-is. |
| challenges.challenge-example.status | object | `{}` | Optional resource status rendered as-is. |
| clusterIssuers | object | `{"cluster-issuer-example":{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"namespace":"default","spec":{},"status":{}}}` | ClusterIssuer resources to render, keyed by resource name. |
| clusterIssuers.cluster-issuer-example.annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| clusterIssuers.cluster-issuer-example.apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| clusterIssuers.cluster-issuer-example.labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| clusterIssuers.cluster-issuer-example.namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| clusterIssuers.cluster-issuer-example.spec | object | `{}` | ClusterIssuer spec rendered as-is. |
| clusterIssuers.cluster-issuer-example.status | object | `{}` | Optional resource status rendered as-is. |
| commonAnnotations | object | `{}` | Extra annotations applied to every rendered resource. |
| commonLabels | object | `{}` | Extra labels applied to every rendered resource. |
| enabled | bool | `true` | Enable nuc-certificates chart rendering. |
| global | object | `{}` | Compatibility values inherited from umbrella charts. Accepted but ignored by this chart. |
| issuers | object | `{"issuer-example":{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"namespace":"default","spec":{},"status":{}}}` | Issuer resources to render, keyed by resource name. |
| issuers.issuer-example.annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| issuers.issuer-example.apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| issuers.issuer-example.labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| issuers.issuer-example.namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| issuers.issuer-example.spec | object | `{}` | Issuer spec rendered as-is. |
| issuers.issuer-example.status | object | `{}` | Optional resource status rendered as-is. |
| nameOverride | string | `""` | Override the default chart label name if needed. |
| orders | object | `{"order-example":{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"acme.cert-manager.io/v1","labels":{},"namespace":"default","spec":{},"status":{}}}` | Order resources to render, keyed by resource name. |
| orders.order-example.annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| orders.order-example.apiVersion | string | `"acme.cert-manager.io/v1"` | Per-resource apiVersion override. |
| orders.order-example.labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| orders.order-example.namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| orders.order-example.spec | object | `{}` | Order spec rendered as-is. |
| orders.order-example.status | object | `{}` | Optional resource status rendered as-is. |

## Included Values Files

- [values.yaml](values.yaml): minimal defaults that render no resources.
- [values.yaml.example](values.yaml.example): complete example covering every supported resource type.

Use [values.yaml.example](values.yaml.example) as a starting point and remove the sections you do not need.

## Upgrading

### To 1.0.0

- Replace top-level resource lists such as `certificates`, `issuers`, and `orders` with maps keyed by resource name.
- Remove the nested `name` field from each chart-managed resource entry. The map key now becomes `metadata.name`.
- Keep raw cert-manager payloads under `spec` and `status` unchanged. Arrays such as `dnsNames`, `solvers`, and `usages` remain arrays because they are part of the CRD schema.

## Testing

The repository uses three test layers:

- `tests/units/` for `helm-unittest` suites and same-major backward compatibility checks
- `tests/e2e/` for local kind-based Helm install checks against real cert-manager CRDs
- `tests/smokes/` for render and schema smoke scenarios

Representative local commands:

```bash
helm lint . -f values.yaml.example
helm template nuc-certificates . -f values.yaml.example
helm unittest -f 'tests/units/*_test.yaml' .
sh tests/units/backward_compatibility_test.sh
python3 tests/smokes/run/smoke.py --scenario example-render
make test-e2e
```

Detailed test documentation is available in [docs/TESTS.MD](docs/TESTS.MD).

Local setup instructions for the development and test toolchain are available in [docs/DEPENDENCY.md](docs/DEPENDENCY.md).

The `e2e` layer is intentionally kept out of GitLab CI and is expected to be run locally through [Makefile](Makefile) or directly via `tests/e2e/test-e2e.sh`.

## Notes

- Keep the chart API versions aligned with the cert-manager CRDs installed in the cluster.
- `ClusterIssuer` is cluster-scoped; all other supported resources in this chart are namespaced.
- Prefer managing `spec` through Helm and let cert-manager own `status`.

## Repository Layout

| Path | Purpose |
|------|---------|
| [Chart.yaml](Chart.yaml) | Chart metadata. |
| [values.yaml](values.yaml) | Minimal default values and `helm-docs` source comments. |
| [docs/README.md.gotmpl](docs/README.md.gotmpl) | Template used by `helm-docs` to build `README.md`. |
| [.pre-commit-config.yaml](.pre-commit-config.yaml) | Local hooks, including automatic `helm-docs` generation on commit. |
| [values.yaml.example](values.yaml.example) | Full example configuration. |
| [values.schema.json](values.schema.json) | JSON schema for chart values. |
| [templates/](templates) | One template per supported cert-manager kind plus shared helpers. |
| [tests/units/](tests/units) | Compact Helm unit suites and same-major backward compatibility checks. |
| [tests/e2e/](tests/e2e) | kind-based end-to-end installation checks. |
| [tests/smokes/](tests/smokes) | Smoke scenarios for render and schema validation. |
| [docs/DEPENDENCY.md](docs/DEPENDENCY.md) | Local dependency installation guide for development and tests. |
| [docs/TESTS.MD](docs/TESTS.MD) | Detailed testing documentation. |
