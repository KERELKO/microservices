
from typing import Annotated

from fastapi import Depends

from src.common.container import Container, build_container


ContainerDep = Annotated[Container, Depends(build_container)]
