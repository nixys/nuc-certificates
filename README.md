# NUC Certificates

Helm chart for rendering cert-manager custom resources from declarative values.

The chart does not install cert-manager CRDs or the cert-manager controllers. It only renders cert-manager resources that are already supported by the target cluster.

The supported resource set is based on the upstream cert-manager CRDs under [deploy/crds](https://github.com/cert-manager/cert-manager/tree/master/deploy/crds), but this chart renders the custom resources created from those CRDs rather than the CRDs themselves.

## Quick Start

Render the example configuration:

```bash
helm template nuc-certificates . -f values.yaml.example
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

Each top-level list in [values.yaml](values.yaml) maps to one resource kind:

- `certificates`
- `certificateRequests`
- `challenges`
- `clusterIssuers`
- `issuers`
- `orders`

Every list item uses the same generic contract:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Resource name. |
| `namespace` | no | Namespace for namespaced resources. Defaults to the Helm release namespace. Ignored for cluster-scoped resources. |
| `labels` | no | Labels merged on top of built-in chart labels and `commonLabels`. |
| `annotations` | no | Annotations merged on top of `commonAnnotations`. |
| `apiVersion` | no | Per-resource API version override. |
| `spec` | no | Raw resource spec rendered as-is. |
| `status` | no | Optional raw status block. Usually not managed through Helm in production. |

Global controls:

- `nameOverride`
- `commonLabels`
- `commonAnnotations`
- `apiVersions.*`

The value contract is validated by [values.schema.json](values.schema.json).

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
| certificateRequests | list | `[{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"name":"certificate-request-example","namespace":"default","spec":{},"status":{}}]` | CertificateRequest resources to render. |
| certificateRequests[0].annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| certificateRequests[0].apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| certificateRequests[0].labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| certificateRequests[0].name | string | `"certificate-request-example"` | CertificateRequest resource name. |
| certificateRequests[0].namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| certificateRequests[0].spec | object | `{}` | CertificateRequest spec rendered as-is. |
| certificateRequests[0].status | object | `{}` | Optional resource status rendered as-is. |
| certificates | list | `[{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"name":"certificate-example","namespace":"default","spec":{},"status":{}}]` | Certificate resources to render. |
| certificates[0].annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| certificates[0].apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| certificates[0].labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| certificates[0].name | string | `"certificate-example"` | Certificate resource name. |
| certificates[0].namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| certificates[0].spec | object | `{}` | Certificate spec rendered as-is. |
| certificates[0].status | object | `{}` | Optional resource status rendered as-is. |
| challenges | list | `[{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"acme.cert-manager.io/v1","labels":{},"name":"challenge-example","namespace":"default","spec":{},"status":{}}]` | Challenge resources to render. |
| challenges[0].annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| challenges[0].apiVersion | string | `"acme.cert-manager.io/v1"` | Per-resource apiVersion override. |
| challenges[0].labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| challenges[0].name | string | `"challenge-example"` | Challenge resource name. |
| challenges[0].namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| challenges[0].spec | object | `{}` | Challenge spec rendered as-is. |
| challenges[0].status | object | `{}` | Optional resource status rendered as-is. |
| clusterIssuers | list | `[{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"name":"cluster-issuer-example","namespace":"default","spec":{},"status":{}}]` | ClusterIssuer resources to render. |
| clusterIssuers[0].annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| clusterIssuers[0].apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| clusterIssuers[0].labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| clusterIssuers[0].name | string | `"cluster-issuer-example"` | ClusterIssuer resource name. |
| clusterIssuers[0].namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| clusterIssuers[0].spec | object | `{}` | ClusterIssuer spec rendered as-is. |
| clusterIssuers[0].status | object | `{}` | Optional resource status rendered as-is. |
| commonAnnotations | object | `{}` | Extra annotations applied to every rendered resource. |
| commonLabels | object | `{}` | Extra labels applied to every rendered resource. |
| issuers | list | `[{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"cert-manager.io/v1","labels":{},"name":"issuer-example","namespace":"default","spec":{},"status":{}}]` | Issuer resources to render. |
| issuers[0].annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| issuers[0].apiVersion | string | `"cert-manager.io/v1"` | Per-resource apiVersion override. |
| issuers[0].labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| issuers[0].name | string | `"issuer-example"` | Issuer resource name. |
| issuers[0].namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| issuers[0].spec | object | `{}` | Issuer spec rendered as-is. |
| issuers[0].status | object | `{}` | Optional resource status rendered as-is. |
| nameOverride | string | `""` | Override the default chart label name if needed. |
| orders | list | `[{"annotations":{"helm-docs.nuc.internal/ignore":"true"},"apiVersion":"acme.cert-manager.io/v1","labels":{},"name":"order-example","namespace":"default","spec":{},"status":{}}]` | Order resources to render. |
| orders[0].annotations | object | `{"helm-docs.nuc.internal/ignore":"true"}` | Extra annotations merged with `commonAnnotations`. |
| orders[0].apiVersion | string | `"acme.cert-manager.io/v1"` | Per-resource apiVersion override. |
| orders[0].labels | object | `{}` | Extra labels merged with chart labels and `commonLabels`. |
| orders[0].name | string | `"order-example"` | Order resource name. |
| orders[0].namespace | string | `"default"` | Namespace for namespaced resources. Defaults to the release namespace when omitted. |
| orders[0].spec | object | `{}` | Order spec rendered as-is. |
| orders[0].status | object | `{}` | Optional resource status rendered as-is. |

## Included Values Files

- [values.yaml](values.yaml): minimal defaults that render no resources.
- [values.yaml.example](values.yaml.example): complete example covering every supported resource type.

Use [values.yaml.example](values.yaml.example) as a starting point and remove the sections you do not need.

## Testing

The repository uses three test layers:

- `tests/units/` for `helm-unittest` suites and backward compatibility checks
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
| [tests/units/](tests/units) | Compact Helm unit suites and backward compatibility checks. |
| [tests/e2e/](tests/e2e) | kind-based end-to-end installation checks. |
| [tests/smokes/](tests/smokes) | Smoke scenarios for render and schema validation. |
| [docs/DEPENDENCY.md](docs/DEPENDENCY.md) | Local dependency installation guide for development and tests. |
| [docs/TESTS.MD](docs/TESTS.MD) | Detailed testing documentation. |
