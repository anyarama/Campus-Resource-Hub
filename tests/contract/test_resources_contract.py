import pytest

from src.repositories.user_repo import UserRepository
from src.repositories.resource_repo import ResourceRepository
from src.services.resource_service import ResourceService, ResourceServiceError


def ensure_user(name: str, email: str, role: str = "staff"):
    existing = UserRepository.get_by_email(email)
    if existing:
        return existing
    return UserRepository.create(name=name, email=email, password="Password123!", role=role)


@pytest.fixture()
def owner(app):
    with app.app_context():
        yield ensure_user("Resource Owner", "owner@test.com")


def test_create_resource_persists_normalized_fields(app, owner):
    with app.app_context():
        resource = ResourceService.create_resource(
            owner_id=owner.user_id,
            title="  Innovation Lab ",
            description=" Maker space with 3D printers ",
            category="lab",
            location=" North Annex ",
            capacity=25,
            availability_rules={"days": ["monday", "wednesday"], "notes": "Bring ID"},
            status="published",
        )

        assert resource.resource_id is not None
        persisted = ResourceRepository.get_by_id(resource.resource_id)
        assert persisted is not None
        assert persisted.title == "Innovation Lab"
        assert persisted.location == "North Annex"
        assert persisted.status == "published"
        assert persisted.get_availability_rules()["days"] == ["monday", "wednesday"]


def test_create_resource_rejects_invalid_capacity(app, owner):
    with app.app_context(), pytest.raises(ResourceServiceError):
        ResourceService.create_resource(
            owner_id=owner.user_id,
            title="Bad Capacity",
            description="",
            category="space",
            location="",
            capacity=-1,
        )


def test_update_resource_enforces_owner_and_updates_fields(app, owner):
    with app.app_context():
        resource = ResourceService.create_resource(
            owner_id=owner.user_id,
            title="Study Pod",
            description="Quiet pod",
            category="study_room",
            location="Level 2",
            capacity=4,
            status="draft",
        )

        updated = ResourceService.update_resource(
            resource_id=resource.resource_id,
            user_id=owner.user_id,
            title="Focus Pod",
            capacity=6,
            availability_rules={"days": ["friday"]},
        )
        assert updated.title == "Focus Pod"
        assert updated.capacity == 6
        assert updated.get_availability_rules()["days"] == ["friday"]

        outsider = ensure_user("Intruder", "intruder@test.com", role="student")
        with pytest.raises(ResourceServiceError):
            ResourceService.update_resource(
                resource_id=resource.resource_id,
                user_id=outsider.user_id,
                title="Hijacked",
            )


def test_publish_and_archive_flow(app, owner):
    with app.app_context():
        resource = ResourceService.create_resource(
            owner_id=owner.user_id,
            title="Event Space",
            description="Large hall",
            category="space",
            location="Main Hall",
            capacity=120,
        )

        published = ResourceService.publish_resource(resource.resource_id, owner.user_id)
        assert published.status == "published"

        archived = ResourceService.archive_resource(resource.resource_id, owner.user_id)
        assert archived.status == "archived"

        with pytest.raises(ResourceServiceError):
            ResourceService.archive_resource(resource.resource_id, owner.user_id)


def test_resources_index_filters_published_and_query(app, client, owner):
    with app.app_context():
        ResourceRepository.create(
            owner.user_id,
            "Innovation Hub",
            "lab",
            description="Robotics kits",
            location="North Wing",
            status="published",
        )
        ResourceRepository.create(
            owner.user_id,
            "Event Pavilion",
            "space",
            description="Open space",
            location="Central Lawn",
            status="published",
        )
        ResourceRepository.create(
            owner.user_id,
            "Draft Space",
            "space",
            description="Hidden",
            location="South Wing",
            status="draft",
        )

    resp = client.get("/resources?q=innovation&category=lab")
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Innovation Hub" in html
    assert "Event Pavilion" not in html
    assert "Draft Space" not in html
