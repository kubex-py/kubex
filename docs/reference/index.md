# API Reference

Auto-generated API reference for `kubex` and `kubex-core`, rendered from source docstrings by mkdocstrings.

| Page | Covers |
|------|--------|
| [kubex.api](api.md) | `Api[T]`, `create_api()`, subresource accessors (`LogsAccessor`, `ScaleAccessor`, `ExecAccessor`, …) |
| [kubex.client](client.md) | `BaseClient`, `create_client()`, `HttpxClient`, `AioHttpClient`, `WebSocketConnection` |
| [kubex.configuration](configuration.md) | `ClientConfiguration`, kubeconfig loading, in-cluster auth, exec provider, OIDC |
| [kubex.core](core.md) | exceptions, request/response models, API params, patch types, channel protocol, request builder |
| [kubex-core](kubex-core.md) | base Pydantic models, marker interfaces, `ResourceConfig`, metadata, list/watch, subresource models |

!!! note "Generated K8s resource models"
    The generated resource models under `kubex.k8s.v1_*` (Pod, Deployment, Service, …) are not rendered here — each Kubernetes version has several hundred model files. Every version has its own repository, from [kubex-py/k8s-1.32](https://github.com/kubex-py/k8s-1.32) to [kubex-py/k8s-1.38](https://github.com/kubex-py/k8s-1.38); or install `kubex[k8s-1.35]` and browse with your IDE for full type information.
