ACTIVITY = "Chess Club"
EXISTING_EMAIL = "existing@example.com"
NEW_EMAIL = "new@example.com"


def test_get_activities_returns_available_activities(client, activities):
    # Arrange
    expected_activities = activities

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_activities


def test_signup_adds_participant(client, activities):
    # Arrange
    expected_message = f"Signed up {NEW_EMAIL} for {ACTIVITY}"

    # Act
    response = client.post(
        f"/activities/{ACTIVITY}/signup",
        params={"email": NEW_EMAIL},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    assert NEW_EMAIL in activities[ACTIVITY]["participants"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"

    # Act
    response = client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": NEW_EMAIL},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    email = EXISTING_EMAIL

    # Act
    response = client.post(
        f"/activities/{ACTIVITY}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant(client, activities):
    # Arrange
    email = EXISTING_EMAIL

    # Act
    response = client.delete(
        f"/activities/{ACTIVITY}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {ACTIVITY}"}
    assert email not in activities[ACTIVITY]["participants"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/participants",
        params={"email": EXISTING_EMAIL},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_unregistered_participant(client):
    # Arrange
    email = NEW_EMAIL

    # Act
    response = client.delete(
        f"/activities/{ACTIVITY}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_participant_can_register_again_after_unregister(client, activities):
    # Arrange
    email = EXISTING_EMAIL
    removal_response = client.delete(
        f"/activities/{ACTIVITY}/participants",
        params={"email": email},
    )

    # Act
    signup_response = client.post(
        f"/activities/{ACTIVITY}/signup",
        params={"email": email},
    )

    # Assert
    assert removal_response.status_code == 200
    assert signup_response.status_code == 200
    assert email in activities[ACTIVITY]["participants"]
