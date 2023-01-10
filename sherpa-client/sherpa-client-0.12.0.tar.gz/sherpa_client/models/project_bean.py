from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.classification_config import ClassificationConfig
    from ..models.project_open_session import ProjectOpenSession


T = TypeVar("T", bound="ProjectBean")


@attr.s(auto_attribs=True)
class ProjectBean:
    """
    Attributes:
        description (str):
        image (str):
        label (str):
        lang (str):
        name (str):
        algorithms (Union[Unset, List[str]]):
        annotations (Union[Unset, int]):
        categories (Union[Unset, int]):
        classification (Union[Unset, ClassificationConfig]):
        components (Union[Unset, List[str]]):
        created_by (Union[Unset, str]):
        created_date (Union[Unset, str]):
        dev_patches (Union[Unset, List[str]]):
        documents (Union[Unset, int]):
        engines (Union[Unset, List[str]]):
        group_name (Union[Unset, str]):
        has_split (Union[Unset, bool]):
        metafacets (Union[Unset, List[Any]]):
        nature (Union[Unset, str]):
        open_session (Union[Unset, ProjectOpenSession]):
        owner (Union[Unset, str]):
        private (Union[Unset, bool]):
        read_only (Union[Unset, bool]):
        segments (Union[Unset, int]):
        shared (Union[Unset, bool]):
        terms (Union[Unset, int]):
        version (Union[Unset, str]):
    """

    description: str
    image: str
    label: str
    lang: str
    name: str
    algorithms: Union[Unset, List[str]] = UNSET
    annotations: Union[Unset, int] = UNSET
    categories: Union[Unset, int] = UNSET
    classification: Union[Unset, "ClassificationConfig"] = UNSET
    components: Union[Unset, List[str]] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    dev_patches: Union[Unset, List[str]] = UNSET
    documents: Union[Unset, int] = UNSET
    engines: Union[Unset, List[str]] = UNSET
    group_name: Union[Unset, str] = UNSET
    has_split: Union[Unset, bool] = UNSET
    metafacets: Union[Unset, List[Any]] = UNSET
    nature: Union[Unset, str] = UNSET
    open_session: Union[Unset, "ProjectOpenSession"] = UNSET
    owner: Union[Unset, str] = UNSET
    private: Union[Unset, bool] = UNSET
    read_only: Union[Unset, bool] = UNSET
    segments: Union[Unset, int] = UNSET
    shared: Union[Unset, bool] = UNSET
    terms: Union[Unset, int] = UNSET
    version: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        image = self.image
        label = self.label
        lang = self.lang
        name = self.name
        algorithms: Union[Unset, List[str]] = UNSET
        if not isinstance(self.algorithms, Unset):
            algorithms = self.algorithms

        annotations = self.annotations
        categories = self.categories
        classification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.classification, Unset):
            classification = self.classification.to_dict()

        components: Union[Unset, List[str]] = UNSET
        if not isinstance(self.components, Unset):
            components = self.components

        created_by = self.created_by
        created_date = self.created_date
        dev_patches: Union[Unset, List[str]] = UNSET
        if not isinstance(self.dev_patches, Unset):
            dev_patches = self.dev_patches

        documents = self.documents
        engines: Union[Unset, List[str]] = UNSET
        if not isinstance(self.engines, Unset):
            engines = self.engines

        group_name = self.group_name
        has_split = self.has_split
        metafacets: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.metafacets, Unset):
            metafacets = self.metafacets

        nature = self.nature
        open_session: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.open_session, Unset):
            open_session = self.open_session.to_dict()

        owner = self.owner
        private = self.private
        read_only = self.read_only
        segments = self.segments
        shared = self.shared
        terms = self.terms
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "description": description,
                "image": image,
                "label": label,
                "lang": lang,
                "name": name,
            }
        )
        if algorithms is not UNSET:
            field_dict["algorithms"] = algorithms
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if categories is not UNSET:
            field_dict["categories"] = categories
        if classification is not UNSET:
            field_dict["classification"] = classification
        if components is not UNSET:
            field_dict["components"] = components
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if dev_patches is not UNSET:
            field_dict["devPatches"] = dev_patches
        if documents is not UNSET:
            field_dict["documents"] = documents
        if engines is not UNSET:
            field_dict["engines"] = engines
        if group_name is not UNSET:
            field_dict["groupName"] = group_name
        if has_split is not UNSET:
            field_dict["hasSplit"] = has_split
        if metafacets is not UNSET:
            field_dict["metafacets"] = metafacets
        if nature is not UNSET:
            field_dict["nature"] = nature
        if open_session is not UNSET:
            field_dict["openSession"] = open_session
        if owner is not UNSET:
            field_dict["owner"] = owner
        if private is not UNSET:
            field_dict["private"] = private
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only
        if segments is not UNSET:
            field_dict["segments"] = segments
        if shared is not UNSET:
            field_dict["shared"] = shared
        if terms is not UNSET:
            field_dict["terms"] = terms
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.classification_config import ClassificationConfig
        from ..models.project_open_session import ProjectOpenSession

        d = src_dict.copy()
        description = d.pop("description")

        image = d.pop("image")

        label = d.pop("label")

        lang = d.pop("lang")

        name = d.pop("name")

        algorithms = cast(List[str], d.pop("algorithms", UNSET))

        annotations = d.pop("annotations", UNSET)

        categories = d.pop("categories", UNSET)

        _classification = d.pop("classification", UNSET)
        classification: Union[Unset, ClassificationConfig]
        if isinstance(_classification, Unset):
            classification = UNSET
        else:
            classification = ClassificationConfig.from_dict(_classification)

        components = cast(List[str], d.pop("components", UNSET))

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        dev_patches = cast(List[str], d.pop("devPatches", UNSET))

        documents = d.pop("documents", UNSET)

        engines = cast(List[str], d.pop("engines", UNSET))

        group_name = d.pop("groupName", UNSET)

        has_split = d.pop("hasSplit", UNSET)

        metafacets = cast(List[Any], d.pop("metafacets", UNSET))

        nature = d.pop("nature", UNSET)

        _open_session = d.pop("openSession", UNSET)
        open_session: Union[Unset, ProjectOpenSession]
        if isinstance(_open_session, Unset):
            open_session = UNSET
        else:
            open_session = ProjectOpenSession.from_dict(_open_session)

        owner = d.pop("owner", UNSET)

        private = d.pop("private", UNSET)

        read_only = d.pop("readOnly", UNSET)

        segments = d.pop("segments", UNSET)

        shared = d.pop("shared", UNSET)

        terms = d.pop("terms", UNSET)

        version = d.pop("version", UNSET)

        project_bean = cls(
            description=description,
            image=image,
            label=label,
            lang=lang,
            name=name,
            algorithms=algorithms,
            annotations=annotations,
            categories=categories,
            classification=classification,
            components=components,
            created_by=created_by,
            created_date=created_date,
            dev_patches=dev_patches,
            documents=documents,
            engines=engines,
            group_name=group_name,
            has_split=has_split,
            metafacets=metafacets,
            nature=nature,
            open_session=open_session,
            owner=owner,
            private=private,
            read_only=read_only,
            segments=segments,
            shared=shared,
            terms=terms,
            version=version,
        )

        return project_bean
