from typing import Dict, Any

from pydantic import version as _pd_version_mod, BaseModel

_pd_version = _pd_version_mod.VERSION
pydantic_major_version = int(_pd_version.split(".")[0])


def jsonable_model(data: BaseModel, exclude_unset=True) -> Dict[str, Any]:
    if pydantic_major_version == 1:
        return data.dict(exclude_unset=exclude_unset)
    return data.model_dump(mode="json", exclude_unset=exclude_unset)  # type: ignore[attr-defined]
