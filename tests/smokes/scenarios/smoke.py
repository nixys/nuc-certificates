from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from tests.smokes.helpers.argparser import SCENARIO_ALIASES
from tests.smokes.steps import chart, helm, kubeconform, render, system


@dataclass
class SmokeContext:
    repo_root: Path
    workdir: Path
    chart_dir: Path
    render_dir: Path
    release_name: str
    namespace: str
    kube_version: str
    kubeconform_bin: str
    schema_location: str
    skip_kinds: str

    @property
    def example_values(self) -> Path:
        return self.repo_root / "values.yaml.example"

    @property
    def rendering_contract_values(self) -> Path:
        return self.repo_root / "tests" / "smokes" / "fixtures" / "rendering-contract.values.yaml"

    @property
    def invalid_resource_list_values(self) -> Path:
        return self.repo_root / "tests" / "smokes" / "fixtures" / "invalid-resource-list.values.yaml"


def check_default_empty(context: SmokeContext) -> None:
    helm.lint(context.chart_dir, workdir=context.workdir)
    output_path = context.render_dir / "default-empty.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        output_path=output_path,
        workdir=context.workdir,
    )
    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 0)


def check_schema_invalid_resource_list(context: SmokeContext) -> None:
    result = helm.lint(
        context.chart_dir,
        values_file=context.invalid_resource_list_values,
        workdir=context.workdir,
        check=False,
    )
    if result.returncode == 0:
        raise system.TestFailure(
            "helm lint unexpectedly succeeded for legacy list-based resource values"
        )

    combined_output = f"{result.stdout}\n{result.stderr}"
    combined_output_lower = combined_output.lower()
    if "object" not in combined_output_lower or "array" not in combined_output_lower:
        raise system.TestFailure(
            "helm lint failed for invalid values, but the error does not mention the list-to-map contract mismatch"
        )


def check_rendering_contract(context: SmokeContext) -> None:
    helm.lint(
        context.chart_dir,
        values_file=context.rendering_contract_values,
        workdir=context.workdir,
    )
    output_path = context.render_dir / "rendering-contract.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.rendering_contract_values,
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 2)

    certificate = render.select_document(
        documents, kind="Certificate", name="merged-certificate"
    )
    render.assert_path(certificate, "apiVersion", "example.io/v1alpha1")
    render.assert_path(certificate, "metadata.namespace", context.namespace)
    render.assert_path(
        certificate,
        "metadata.labels[app.kubernetes.io/name]",
        "certificate-platform",
    )
    render.assert_path(certificate, "metadata.labels.platform", "cert-manager")
    render.assert_path(certificate, "metadata.labels.component", "certificate")
    render.assert_path(certificate, "metadata.labels.tier", "edge")
    render.assert_path(certificate, "metadata.annotations.team", "platform")
    render.assert_path(certificate, "metadata.annotations.note", "edge-tls")
    render.assert_path(certificate, "spec.secretName", "merged-certificate-tls")

    cluster_issuer = render.select_document(
        documents, kind="ClusterIssuer", name="public-acme"
    )
    render.assert_path(cluster_issuer, "apiVersion", "cert-manager.io/v1beta1")
    render.assert_path_missing(cluster_issuer, "metadata.namespace")
    render.assert_path(
        cluster_issuer,
        "metadata.labels[app.kubernetes.io/name]",
        "certificate-platform",
    )
    render.assert_path(cluster_issuer, "metadata.labels.component", "issuer")
    render.assert_path(cluster_issuer, "metadata.annotations.team", "platform")
    render.assert_path(cluster_issuer, "metadata.annotations.note", "public")
    render.assert_path(
        cluster_issuer, "spec.acme.privateKeySecretRef.name", "public-acme-account-key"
    )


def check_example_render(context: SmokeContext) -> None:
    helm.lint(
        context.chart_dir,
        values_file=context.example_values,
        workdir=context.workdir,
    )
    output_path = context.render_dir / "example-render.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.example_values,
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 6)
    render.assert_kinds(
        documents,
        {
            "Certificate",
            "CertificateRequest",
            "Challenge",
            "ClusterIssuer",
            "Issuer",
            "Order",
        },
    )

    cluster_issuer = render.select_document(
        documents, kind="ClusterIssuer", name="letsencrypt-production"
    )
    render.assert_path_missing(cluster_issuer, "metadata.namespace")

    issuer = render.select_document(documents, kind="Issuer", name="team-selfsigned")
    render.assert_path(issuer, "metadata.namespace", "apps")
    render.assert_path(issuer, "spec.selfSigned", {})

    certificate = render.select_document(documents, kind="Certificate", name="api-example-com")
    render.assert_path(certificate, "spec.secretName", "api-example-com-tls")
    render.assert_path(certificate, "spec.privateKey.rotationPolicy", "Always")

    certificate_request = render.select_document(
        documents, kind="CertificateRequest", name="api-example-com-manual"
    )
    render.assert_path(certificate_request, "spec.duration", "2160h")

    order = render.select_document(documents, kind="Order", name="api-example-com-order")
    render.assert_path(order, "spec.issuerRef.name", "letsencrypt-production")

    challenge = render.select_document(
        documents, kind="Challenge", name="api-example-com-order-0"
    )
    render.assert_path(challenge, "spec.type", "DNS-01")
    render.assert_path(challenge, "spec.solver.dns01.cloudDNS.project", "platform-prod")


def check_example_kubeconform(context: SmokeContext) -> None:
    output_path = context.render_dir / "example-kubeconform.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.example_values,
        output_path=output_path,
        workdir=context.workdir,
    )
    kubeconform.validate(
        manifest_path=output_path,
        kube_version=context.kube_version,
        kubeconform_bin=context.kubeconform_bin,
        schema_location=context.schema_location,
        skip_kinds=context.skip_kinds,
    )


SCENARIOS: list[tuple[str, Callable[[SmokeContext], None]]] = [
    ("default-empty", check_default_empty),
    ("schema-invalid-resource-list", check_schema_invalid_resource_list),
    ("rendering-contract", check_rendering_contract),
    ("example-render", check_example_render),
    ("example-kubeconform", check_example_kubeconform),
]


def normalize_scenarios(requested: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for name in requested:
        canonical_name = SCENARIO_ALIASES.get(name, name)
        if canonical_name in seen:
            continue
        normalized.append(canonical_name)
        seen.add(canonical_name)
    return normalized


def run_smoke_suite(args) -> int:
    scenario_map = dict(SCENARIOS)
    requested = args.scenario or ["all"]
    if "all" in requested:
        selected = [name for name, _ in SCENARIOS]
    else:
        selected = normalize_scenarios(requested)

    repo_root = Path(args.chart_dir).resolve()
    workdir, chart_dir = chart.stage_chart(repo_root, args.workdir)
    context = SmokeContext(
        repo_root=repo_root,
        workdir=workdir,
        chart_dir=chart_dir,
        render_dir=workdir / "rendered",
        release_name=args.release_name,
        namespace=args.namespace,
        kube_version=args.kube_version,
        kubeconform_bin=args.kubeconform_bin,
        schema_location=args.schema_location,
        skip_kinds=args.skip_kinds,
    )
    context.render_dir.mkdir(parents=True, exist_ok=True)

    failures: list[tuple[str, str]] = []
    try:
        for name in selected:
            system.log(f"=== scenario: {name} ===")
            try:
                scenario_map[name](context)
            except Exception as exc:
                failures.append((name, str(exc)))
                system.log(f"FAILED: {name}: {exc}")
            else:
                system.log(f"PASSED: {name}")
    finally:
        if args.keep_workdir:
            system.log(f"workdir kept at {workdir}")
        else:
            chart.cleanup(workdir)

    if failures:
        system.log("=== summary: failures ===")
        for name, message in failures:
            system.log(f"- {name}: {message}")
        return 1

    system.log("=== summary: all smoke scenarios passed ===")
    return 0
