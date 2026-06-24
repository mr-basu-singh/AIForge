import sys
sys.path.insert(0, '.')

def test_db_init():
    from backend.database.db import init_db
    init_db()
    print("✅ test_db_init passed")

def test_prompt_versioning():
    from backend.experiments.prompt_versioning import PromptVersionManager
    pm = PromptVersionManager()
    versions = pm.list_versions()
    assert len(versions) >= 3
    version_names = [v["version"] for v in versions]
    assert "v1" in version_names
    assert "v2" in version_names
    assert "v3" in version_names
    print(f"✅ test_prompt_versioning passed — {len(versions)} versions found")

def test_create_delete_prompt():
    from backend.experiments.prompt_versioning import PromptVersionManager
    pm = PromptVersionManager()
    pm.create("v_test", "Test Prompt", "You are a test assistant.", "Test only")
    prompt = pm.get_by_version("v_test")
    assert prompt is not None
    assert prompt.name == "Test Prompt"
    pm.delete("v_test")
    deleted = pm.get_by_version("v_test")
    assert deleted is None
    print("✅ test_create_delete_prompt passed")

def test_experiment_tracker_init():
    from backend.experiments.experiment_tracker import ExperimentTracker
    tracker = ExperimentTracker()
    experiments = tracker.get_all_experiments()
    assert isinstance(experiments, list)
    print(f"✅ test_experiment_tracker_init passed — {len(experiments)} experiments found")

if __name__ == "__main__":
    test_db_init()
    test_prompt_versioning()
    test_create_delete_prompt()
    test_experiment_tracker_init()
    print("\n✅ All database tests passed.")