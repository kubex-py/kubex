"""kubex's JsonPatch as an admission webhook's patch.

The admission models are kubex-core's (kubex-py/kubex-core, which tests them on their
own); this checks that kubex's JsonPatch serializes into an AdmissionResponse.
"""

from __future__ import annotations

import base64
import json
from typing import Any

import pytest

from kubex.core.patch import JsonPatch
from kubex.k8s.v1_35.core.v1.pod import Pod
from kubex_core.models.admission import AdmissionRequest, AdmissionReview

UID = "705ab4f5-6393-11e8-b7cc-42010a800002"


def _pod(name: str, image: str) -> dict[str, Any]:
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": name, "namespace": "default"},
        "spec": {"containers": [{"name": "app", "image": image}]},
    }


def _review(**request: Any) -> dict[str, Any]:
    return {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "request": {
            "uid": UID,
            "kind": {"group": "", "version": "v1", "kind": "Pod"},
            "resource": {"group": "", "version": "v1", "resource": "pods"},
            "namespace": "default",
            "operation": "CREATE",
            "userInfo": {
                "username": "admin",
                "uid": "014fbff9a07c",
                "groups": ["system:authenticated", "system:masters"],
                "extra": {"some-key": ["some-value1", "some-value2"]},
            },
            **request,
        },
    }


def _wire(review: AdmissionReview[Any]) -> dict[str, Any]:
    # How a webhook serializes its reply.
    result: dict[str, Any] = json.loads(
        review.model_dump_json(by_alias=True, exclude_none=True)
    )
    return result


def _request() -> AdmissionRequest[Pod]:
    request = (
        AdmissionReview[Pod]
        .model_validate(_review(object=_pod("web", "nginx")))
        .request
    )
    assert request is not None
    return request


@pytest.mark.parametrize("as_bytes", [False, True])
def test_allow_with_patch(as_bytes: bool) -> None:
    patch_text = JsonPatch().add("/metadata/labels", {"team": "a"}).serialize()
    patch = patch_text.encode() if as_bytes else patch_text
    response = _request().allow(patch=patch)
    assert response.patch == patch_text.encode()
    assert response.patch_type == "JSONPatch"

    wire = _wire(AdmissionReview[Pod](response=response))["response"]
    assert wire["patchType"] == "JSONPatch"
    assert json.loads(base64.b64decode(wire["patch"])) == [
        {"op": "add", "path": "/metadata/labels", "value": {"team": "a"}}
    ]
