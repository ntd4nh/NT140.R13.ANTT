import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = Path(__file__).parent / "fixtures"
FIXTURE_DIR = FIXTURE_ROOT / "minh_hoa_RUN-TEST"
SMOKE_DIR = PROJECT_ROOT / "evidence" / "smoke_test"


def _snapshot_raw():
    raw_dir = PROJECT_ROOT / "data" / "raw"
    return {
        path.relative_to(raw_dir).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in raw_dir.rglob("*")
        if path.is_file()
    }


def _write_manifest(run_dir):
    files = sorted(
        path
        for path in run_dir.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    )
    manifest = "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  "
        f"./{path.relative_to(run_dir).as_posix()}\n"
        for path in files
    )
    (run_dir / "SHA256SUMS").write_text(manifest, encoding="ascii")


def _copy_fixture(tmp_path):
    run_dir = tmp_path / FIXTURE_DIR.name
    shutil.copytree(FIXTURE_DIR, run_dir)
    return run_dir


def _copy_smoke_test(tmp_path):
    run_dir = tmp_path / "SMOKE-TEST"
    shutil.copytree(SMOKE_DIR, run_dir)
    (run_dir / "README.md").unlink()
    return run_dir


def _run_cli(run_dir, tmp_path, *extra_args):
    out_processed = tmp_path / "out" / "processed"
    command = [
        sys.executable,
        "-m",
        "analysis.process_run",
        "--run-dir",
        str(run_dir),
        "--out-processed",
        str(out_processed),
        *map(str, extra_args),
    ]
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def _read_csv(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def _outputs(tmp_path):
    return (
        tmp_path / "out" / "processed" / "events.csv",
        tmp_path / "out" / "processed" / "sessions.csv",
        tmp_path / "out" / "processed" / "bao_cao_chat_luong.txt",
    )


def test_cowrie_fixture_counts():
    log_files = sorted(FIXTURE_DIR.glob("cowrie.json*"))
    assert len(log_files) == 2

    valid_lines = []
    malformed_lines = 0
    blank_lines = 0
    for log_file in log_files:
        for line in log_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                blank_lines += 1
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError:
                malformed_lines += 1
            else:
                valid_lines.append(line)

    duplicate_excess = sum(count - 1 for count in Counter(valid_lines).values())
    assert len(valid_lines) == 48
    assert malformed_lines == 1
    assert blank_lines == 1
    assert duplicate_excess == 1


def test_processor_fixture_and_does_not_change_raw(tmp_path):
    raw_before = _snapshot_raw()
    issues_path = PROJECT_ROOT / "review" / "issues.md"
    issues_before = issues_path.read_bytes() if issues_path.is_file() else None
    run_dir = _copy_fixture(tmp_path)
    result = _run_cli(run_dir, tmp_path)
    assert result.returncode == 0, result.stderr
    assert _snapshot_raw() == raw_before

    events_path, sessions_path, report_path = _outputs(tmp_path)
    events = _read_csv(events_path)
    sessions = _read_csv(sessions_path)
    report = report_path.read_text(encoding="utf-8")
    assert all(row["data_origin"] == "minh_hoa" for row in events)
    assert all(row["data_origin"] == "minh_hoa" for row in sessions)
    assert {row["run_id"] for row in events} == {"minh_hoa_RUN-TEST"}
    assert len(events) == 45
    assert len(sessions) == 9
    assert report.startswith("run_id: minh_hoa_RUN-TEST\n")
    assert "JSON hợp lệ: 48" in report
    assert "JSON hỏng: 1" in report
    assert "Dòng trống: 1" in report
    assert "7. Báo lỗi review: review/issues.md" in report
    assert "Thời điểm xử lý" not in report
    assert "Bản trùng dư đã loại: 1" in report
    assert "cowrie.session.unexpected" in report
    assert "Dòng JSON hỏng:" in report
    assert "Thiếu timestamp:" in report
    assert "Không có --logbook" in report
    assert "Gợi ý nội dung cho review/issues.md (chưa ghi file)" in report
    issues_after = issues_path.read_bytes() if issues_path.is_file() else None
    assert issues_after == issues_before

    assert any(row["event_type"] == "cowrie.client.version" and row["src_ip"] == "" for row in events)
    assert any(row["protocol_inferred"] == "true" for row in events)
    assert sum(row["duplicate_count"] == "1" for row in events) == 1
    assert all(row["command_supported"] != "supported" for row in events)
    assert all(row["scenario_match_status"] == "unmatched" for row in sessions)

    listed_files = report.split("File log: ", 1)[1].splitlines()[0]
    assert listed_files.index("cowrie.json.2026-01-01") < listed_files.index(", cowrie.json")
    assert all(row["raw_ref"].split(":", 1)[0] for row in events)
    assert any(row["event_type"] == "cowrie.session.closed" and row["duration_ms"] == "12000" for row in events)
    offset_timestamp = next(row for row in events if row["raw_ref"] == "cowrie.json:5")
    assert offset_timestamp["event_time_utc"].endswith("Z")

    out_of_order = [
        row["event_type"]
        for row in events
        if row["session_id"] == "a2b3c4d5e6f7"
    ]
    assert out_of_order == [
        "cowrie.client.version",
        "cowrie.session.connect",
        "cowrie.session.closed",
    ]
    unclosed = next(row for row in sessions if row["session_id"] == "f1a2b3c4d5e6")
    assert unclosed["closed_properly"] == "false"
    assert unclosed["duration_ms"] == ""


def test_fixture_cannot_be_marked_as_lab(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    result = _run_cli(run_dir, tmp_path, "--data-origin", "lab")
    assert result.returncode != 0
    assert "minh_hoa" in result.stderr
    assert not _outputs(tmp_path)[0].exists()


def test_non_raw_non_fixture_requires_explicit_data_origin(tmp_path):
    run_dir = _copy_smoke_test(tmp_path)
    result = _run_cli(run_dir, tmp_path)
    assert result.returncode != 0
    assert "--data-origin" in result.stderr
    assert not any(path.exists() for path in _outputs(tmp_path))


def test_hash_mismatch_stops_before_writing_outputs(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    log = run_dir / "cowrie.json"
    log.write_text(log.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    result = _run_cli(run_dir, tmp_path)
    assert result.returncode != 0
    assert "FAIL:" in result.stdout
    assert "SHA256SUMS không khớp" in result.stderr
    assert not any(path.exists() for path in _outputs(tmp_path))


def test_output_path_inside_raw_is_rejected(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    raw_output = PROJECT_ROOT / "data" / "raw" / "SHOULD-NOT-EXIST"
    before = _snapshot_raw()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "analysis.process_run",
            "--run-dir",
            str(run_dir),
            "--out-processed",
            str(raw_output),
            "--out-results",
            str(tmp_path / "results"),
        ],
        cwd=PROJECT_ROOT,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode != 0
    assert "data/raw" in result.stderr
    assert not raw_output.exists()
    assert _snapshot_raw() == before


def test_duration_uses_session_closed_and_computes_when_missing(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    log = run_dir / "cowrie.json"
    rewritten = []
    for line in log.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if (
            event.get("eventid") == "cowrie.session.closed"
            and event.get("session") == "d1e2f3a4b5c6"
        ):
            event.pop("duration_ms")
            line = json.dumps(event, separators=(",", ":"))
        rewritten.append(line)
    log.write_text("\n".join(rewritten) + "\n", encoding="utf-8")
    _write_manifest(run_dir)

    result = _run_cli(run_dir, tmp_path)
    assert result.returncode == 0, result.stderr
    events = _read_csv(_outputs(tmp_path)[0])
    closed = next(
        row
        for row in events
        if row["event_type"] == "cowrie.session.closed"
        and row["session_id"] == "d1e2f3a4b5c6"
    )
    assert closed["duration_ms"] == "12000"
    assert closed["duration_computed"] == "true"
    log_closed = next(
        row
        for row in events
        if row["event_type"] == "cowrie.log.closed"
        and row["session_id"] == "d1e2f3a4b5c6"
    )
    assert log_closed["duration_ms"] == ""
    assert log_closed["duration_computed"] == "false"
    session = next(
        row
        for row in _read_csv(_outputs(tmp_path)[1])
        if row["session_id"] == "d1e2f3a4b5c6"
    )
    assert session["duration_source"] == "computed"
    assert session["duration_ms"] == "12000"


def test_missing_command_input_and_protocol_port_fallback_without_session(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    log = run_dir / "cowrie.json"
    appended_line = len(log.read_text(encoding="utf-8").splitlines()) + 1
    event = {
        "eventid": "cowrie.command.input",
        "timestamp": "2026-01-01T00:00:30Z",
        "src_ip": "192.0.2.10",
        "dst_port": 2222,
        "input": "",
    }
    with log.open("a", encoding="utf-8") as output:
        output.write(json.dumps(event, separators=(",", ":")) + "\n")
    _write_manifest(run_dir)

    result = _run_cli(run_dir, tmp_path)
    assert result.returncode == 0, result.stderr
    events = _read_csv(_outputs(tmp_path)[0])
    command = next(
        row for row in events
        if row["event_type"] == "cowrie.command.input"
        and row["raw_ref"] == f"cowrie.json:{appended_line}"
    )
    assert command["session_id"] == ""
    assert command["protocol"] == "ssh"
    assert command["protocol_inferred"] == "true"
    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert "cowrie.command.input.input: 1" in report


def test_protocol_propagates_from_session_prioritizing_connect(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    log = run_dir / "cowrie.json"
    rewritten = []
    for line in log.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("session") == "a1b2c3d4e5f6":
            if event.get("eventid") == "cowrie.client.version":
                event["protocol"] = "telnet"
            elif event.get("eventid") == "cowrie.client.kex":
                event.pop("protocol", None)
            line = json.dumps(event, separators=(",", ":"))
        rewritten.append(line)
    rewritten.extend(
        json.dumps(event, separators=(",", ":"))
        for event in (
            {
                "eventid": "cowrie.session.closed",
                "timestamp": "2026-01-01T00:09:00Z",
                "session": "0a1b2c3d4e5f",
                "src_ip": "192.0.2.1",
                "dst_port": 2223,
                "protocol": "telnet",
                "duration_ms": 0,
            },
            {
                "eventid": "cowrie.client.kex",
                "timestamp": "2026-01-01T00:09:01Z",
                "session": "0a1b2c3d4e5f",
                "src_ip": "192.0.2.1",
                "dst_port": 2223,
            },
        )
    )
    log.write_text("\n".join(rewritten) + "\n", encoding="utf-8")
    _write_manifest(run_dir)

    result = _run_cli(run_dir, tmp_path)
    assert result.returncode == 0, result.stderr
    events = _read_csv(_outputs(tmp_path)[0])
    connect_preferred = next(
        row for row in events
        if row["session_id"] == "a1b2c3d4e5f6"
        and row["event_type"] == "cowrie.client.kex"
    )
    session_fallback = next(
        row for row in events
        if row["session_id"] == "0a1b2c3d4e5f"
        and row["event_type"] == "cowrie.client.kex"
    )
    assert connect_preferred["protocol"] == "ssh"
    assert connect_preferred["protocol_inferred"] == "false"
    assert session_fallback["protocol"] == "telnet"
    assert session_fallback["protocol_inferred"] == "false"


def test_logbook_matching_matched_unmatched_and_ambiguous(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    (run_dir / "run_note.txt").write_text(
        "start_utc=2026-01-01T00:00:00Z; clock_offset=+1.0\n",
        encoding="utf-8",
    )
    _write_manifest(run_dir)
    logbook = FIXTURE_ROOT / "minh_hoa_nhat_ky_gan_kich_ban.csv"
    result = _run_cli(run_dir, tmp_path, "--logbook", logbook)
    assert result.returncode == 0, result.stderr
    sessions = _read_csv(_outputs(tmp_path)[1])

    session_by_id = {row["session_id"]: row for row in sessions}
    assert session_by_id["a1b2c3d4e5f6"]["scenario_match_status"] == "ambiguous"
    assert json.loads(session_by_id["a1b2c3d4e5f6"]["scenario_candidates"]) == [
        "KB-01",
        "KB-01-KHAC",
    ]
    assert session_by_id["c2d3e4f5a6b7"]["scenario_match_status"] == "matched"
    assert session_by_id["c2d3e4f5a6b7"]["scenario_id"] == "KB-02"
    assert session_by_id["a1b2c3d4e5f6"]["scenario_candidates"] == (
        '["KB-01","KB-01-KHAC"]'
    )
    assert session_by_id["c2d3e4f5a6b7"]["scenario_candidates"] == ""
    unmatched = [
        row for row in sessions if row["scenario_match_status"] == "unmatched"
    ]
    assert unmatched
    assert all(row["scenario_candidates"] == "" for row in unmatched)
    events = _read_csv(_outputs(tmp_path)[0])
    assert {
        row["scenario_id"]
        for row in events
        if row["session_id"] == "c2d3e4f5a6b7"
    } == {"KB-02"}


def test_iss01_single_logbook_row_matches_sessions_with_small_delta(tmp_path):
    run_dir = tmp_path / "RUN-SMOKE"
    shutil.copytree(SMOKE_DIR, run_dir)
    (run_dir / "README.md").unlink()
    result = _run_cli(
        run_dir,
        tmp_path,
        "--data-origin",
        "lab",
        "--logbook",
        PROJECT_ROOT / "review" / "tai_hien" / "nhat_ky_smoke_tv3.csv",
        "--delta-seconds",
        "0.5",
    )
    assert result.returncode == 0, result.stderr
    sessions = _read_csv(_outputs(tmp_path)[1])
    by_id = {row["session_id"]: row for row in sessions}
    expected_matches = {
        "0b41d23a26d6": "S-SSH-SAI-A",
        "17f75198febf": "S-SSH-DUNG-A",
        "a19fc2e39c40": "S-SSH-SAI-W",
        "67886ab3f25e": "S-SSH-DUNG-W",
        "e02625c405d3": "S-TEL-A",
        "d976c4e34a27": "S-TEL-W",
    }
    for session_id, scenario_id in expected_matches.items():
        assert by_id[session_id]["scenario_match_status"] == "matched"
        assert by_id[session_id]["scenario_id"] == scenario_id
    for session_id in ("3f8ff8b71f88", "0722a6a2bff3"):
        assert by_id[session_id]["scenario_match_status"] == "unmatched"
        assert by_id[session_id]["scenario_id"] == ""

    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert "Dung sai thao tác bổ sung khi ghép kịch bản: 1.0s" in report


def test_iss02_explains_empty_client_version_for_port_scan(tmp_path):
    run_dir = tmp_path / "RUN-SMOKE"
    shutil.copytree(SMOKE_DIR, run_dir)
    (run_dir / "README.md").unlink()
    result = _run_cli(run_dir, tmp_path, "--data-origin", "lab")
    assert result.returncode == 0, result.stderr

    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert "cowrie.client.version.version: 1" in report
    assert (
        "Ghi chú bình thường: client.version rỗng ở phiên chỉ dò cổng "
        "(n_events ≤ 3, không có client.kex), không phải lỗi mất dữ liệu: "
        "3f8ff8b71f88"
    ) in report


def test_logbook_without_clock_offset_requires_review(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    (run_dir / "run_note.txt").write_text("run_note without offset\n", encoding="utf-8")
    _write_manifest(run_dir)
    result = _run_cli(
        run_dir,
        tmp_path,
        "--logbook",
        FIXTURE_ROOT / "minh_hoa_nhat_ky_gan_kich_ban.csv",
    )
    assert result.returncode == 0, result.stderr
    sessions = _read_csv(_outputs(tmp_path)[1])
    assert all(row["scenario_match_status"] == "needs_review" for row in sessions)
    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert "thiếu clock_offset" in report


def test_delta_seconds_cli_override(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    (run_dir / "run_note.txt").write_text(
        "run_note without offset\n",
        encoding="utf-8",
    )
    _write_manifest(run_dir)
    result = _run_cli(
        run_dir,
        tmp_path,
        "--logbook",
        FIXTURE_ROOT / "minh_hoa_nhat_ky_gan_kich_ban.csv",
        "--delta-seconds",
        "1.0",
    )
    assert result.returncode == 0, result.stderr
    sessions = _read_csv(_outputs(tmp_path)[1])
    session_by_id = {row["session_id"]: row for row in sessions}
    assert session_by_id["c2d3e4f5a6b7"]["scenario_match_status"] == "matched"
    assert session_by_id["a1b2c3d4e5f6"]["scenario_match_status"] == "ambiguous"
    assert session_by_id["c3d4e5f6a7b8"]["scenario_match_status"] == "needs_review"
    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert "Ghi đè clock_offset bằng --delta-seconds: 1.0s" in report
    assert "thiếu clock_offset" not in report

    (run_dir / "run_note.txt").write_text(
        "clock_offset_s=0.0\n",
        encoding="utf-8",
    )
    _write_manifest(run_dir)
    result = _run_cli(
        run_dir,
        tmp_path,
        "--logbook",
        FIXTURE_ROOT / "minh_hoa_nhat_ky_gan_kich_ban.csv",
        "--delta-seconds",
        "1.0",
    )
    assert result.returncode == 0, result.stderr
    sessions = _read_csv(_outputs(tmp_path)[1])
    session_by_id = {row["session_id"]: row for row in sessions}
    assert session_by_id["c2d3e4f5a6b7"]["scenario_match_status"] == "matched"
    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert "Ghi đè clock_offset bằng --delta-seconds: 1.0s" in report


def test_smoke_schema_on_temporary_copy(tmp_path):
    raw_before = _snapshot_raw()
    evidence_before = {
        path.relative_to(SMOKE_DIR).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in SMOKE_DIR.rglob("*")
        if path.is_file()
    }
    run_dir = _copy_smoke_test(tmp_path)
    result = _run_cli(run_dir, tmp_path, "--data-origin", "lab")
    assert result.returncode == 0, result.stderr
    assert _snapshot_raw() == raw_before
    evidence_after = {
        path.relative_to(SMOKE_DIR).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in SMOKE_DIR.rglob("*")
        if path.is_file()
    }
    assert evidence_after == evidence_before

    events = _read_csv(_outputs(tmp_path)[0])
    sessions = _read_csv(_outputs(tmp_path)[1])
    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert len(events) == 58
    assert len(sessions) == 8
    expected_event_fields = [
        "event_time_utc", "event_type", "session_id", "src_ip", "src_port",
        "dst_ip", "dst_port", "protocol", "sensor", "client_version",
        "client_hassh", "username", "password", "login_result", "command",
        "command_supported", "download_url", "file_sha256", "duration_ms",
        "message", "scenario_id", "run_id", "data_origin", "raw_ref",
        "protocol_inferred", "duration_computed", "duplicate_count",
    ]
    assert list(events[0]) == expected_event_fields
    assert all(row["data_origin"] == "lab" for row in events + sessions)
    event_counts = Counter(row["event_type"] for row in events)
    assert event_counts == Counter(
        {
            "cowrie.client.kex": 4,
            "cowrie.client.size": 2,
            "cowrie.client.var": 1,
            "cowrie.client.version": 5,
            "cowrie.command.input": 8,
            "cowrie.log.closed": 4,
            "cowrie.login.failed": 4,
            "cowrie.login.success": 4,
            "cowrie.session.closed": 8,
            "cowrie.session.connect": 8,
            "cowrie.session.params": 4,
            "cowrie.telnet.option": 6,
        }
    )
    assert not any("unknown" in row["event_type"] for row in events)
    assert "Event lạ bị loại: 0" in report
    assert "known_auxiliary: 13" in report

    by_ip_protocol = Counter(
        (row["src_ip"], row["protocol"]) for row in sessions
    )
    assert by_ip_protocol == Counter(
        {
            ("192.168.239.10", "ssh"): 3,
            ("192.168.239.10", "telnet"): 2,
            ("192.168.239.1", "ssh"): 2,
            ("192.168.239.1", "telnet"): 1,
        }
    )
    assert Counter(row["protocol"] for row in sessions) == {
        "ssh": 5,
        "telnet": 3,
    }
    assert sum(row["n_login_failed"] == "1" for row in sessions) == 4
    assert sum(row["n_login_success"] == "1" for row in sessions) == 4
    assert sum(int(row["n_commands"]) for row in sessions) == 8
    assert sum(row["closed_properly"] == "true" for row in sessions) == 8
    assert Counter(row["duration_ms"] for row in sessions) == Counter(
        str(value) for value in (16, 15, 1043, 287, 3194, 1070, 337, 3091)
    )
    assert all(row["duration_source"] == "tool" for row in sessions)
    assert all(row["duration_computed"] == "false" for row in events)
    assert all(row["data_origin"] == "lab" for row in events)

    log_closed = [row for row in events if row["event_type"] == "cowrie.log.closed"]
    assert len(log_closed) == 4
    assert all(row["duration_ms"] == "" for row in log_closed)
    telnet_sessions = {
        row["session_id"] for row in sessions if row["protocol"] == "telnet"
    }
    assert all(row["client_version"] == "" for row in sessions if row["session_id"] in telnet_sessions)
    empty_version = next(
        row for row in events
        if row["event_type"] == "cowrie.client.version"
        and row["raw_ref"] == "cowrie.json:3"
    )
    assert empty_version["client_version"] == ""
    assert "cowrie.client.version.version: 1" in report
    assert "Thiếu timestamp: 0" in report
    assert "JSON hỏng: 0" in report
    assert "Phiên tổng: 8" in report


def test_outputs_are_reproducible(tmp_path):
    run_dir = _copy_fixture(tmp_path)
    first = _run_cli(run_dir, tmp_path)
    assert first.returncode == 0, first.stderr
    output_paths = _outputs(tmp_path)
    first_bytes = [path.read_bytes() for path in output_paths]

    second = _run_cli(run_dir, tmp_path)
    assert second.returncode == 0, second.stderr
    second_bytes = [path.read_bytes() for path in output_paths]
    assert first_bytes == second_bytes


def test_quality_report_without_issues_uses_stable_review_status(tmp_path):
    run_dir = tmp_path / "RUN-CLEAN"
    run_dir.mkdir()
    session_id = "123456abcdef"
    events = [
        {
            "eventid": "cowrie.session.connect",
            "timestamp": "2026-01-01T00:00:00Z",
            "session": session_id,
            "src_ip": "192.0.2.10",
            "dst_port": 2222,
            "protocol": "ssh",
        },
        {
            "eventid": "cowrie.session.closed",
            "timestamp": "2026-01-01T00:00:01Z",
            "session": session_id,
            "src_ip": "192.0.2.10",
            "dst_port": 2222,
            "protocol": "ssh",
            "duration_ms": 1000,
        },
    ]
    (run_dir / "cowrie.json").write_text(
        "".join(json.dumps(event, separators=(",", ":")) + "\n" for event in events),
        encoding="utf-8",
    )
    _write_manifest(run_dir)

    result = _run_cli(run_dir, tmp_path, "--data-origin", "tham_khao")
    assert result.returncode == 0, result.stderr
    report = _outputs(tmp_path)[2].read_text(encoding="utf-8")
    assert "7. Báo lỗi review: không phát sinh issue cho review/issues.md" in report
