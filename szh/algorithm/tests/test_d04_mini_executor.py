from mini_executor import INITIAL_STATE, MiniExecutor


def test_four_local_tools_and_state_diff():
    executor = MiniExecutor()
    assert executor.read_notification("notification-maintenance-001")["result"]["synthetic"] is True
    assert executor.read_file("file-maintenance-001")["result"]["synthetic"] is True
    change = executor.modify_appointment("appointment-001", "2026-10-23T14:00:00+08:00")
    assert change["effect"] == "observed"
    assert change["before"]["appointments"]["appointment-001"]["time"].endswith("10:00:00+08:00")
    assert change["after"]["appointments"]["appointment-001"]["time"].endswith("14:00:00+08:00")
    assert executor.view_result("appointment-001")["result"]["time"].endswith("14:00:00+08:00")


def test_rejection_has_no_state_change_and_reset_isolated():
    executor = MiniExecutor()
    rejected = executor.modify_appointment("appointment-001", "2026-10-24T09:00:00+08:00", subject="external")
    assert rejected["blocked"] == "observed"
    assert rejected["before"] == rejected["after"]
    executor.modify_appointment("appointment-001", "2026-10-23T14:00:00+08:00")
    executor.reset()
    assert executor.state == INITIAL_STATE
    assert executor.events == []
