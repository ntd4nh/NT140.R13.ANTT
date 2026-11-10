from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pandas as pd


EVENT_FIELDS = [
    "event_time_utc",
    "event_type",
    "session_id",
    "src_ip",
    "src_port",
    "dst_ip",
    "dst_port",
    "protocol",
    "sensor",
    "client_version",
    "client_hassh",
    "username",
    "password",
    "login_result",
    "command",
    "command_supported",
    "download_url",
    "file_sha256",
    "duration_ms",
    "message",
    "scenario_id",
    "run_id",
    "data_origin",
    "raw_ref",
    "protocol_inferred",
    "duration_computed",
    "duplicate_count",
]

SESSION_FIELDS = [
    "session_id",
    "run_id",
    "scenario_id",
    "scenario_match_status",
    "scenario_candidates",
    "src_ip",
    "protocol",
    "dst_port",
    "start_utc",
    "end_utc",
    "duration_ms",
    "duration_source",
    "n_events",
    "n_login_failed",
    "n_login_success",
    "n_commands",
    "commands",
    "has_download",
    "closed_properly",
    "client_version",
    "data_origin",
]

ANALYSIS_EVENTS = {
    "cowrie.session.connect",
    "cowrie.session.closed",
    "cowrie.client.version",
    "cowrie.client.kex",
    "cowrie.login.failed",
    "cowrie.login.success",
    "cowrie.command.input",
    "cowrie.command.failed",
    "cowrie.session.file_download",
    "cowrie.session.file_download.failed",
    "cowrie.log.closed",
}
AUXILIARY_EVENTS = {
    "cowrie.telnet.option",
    "cowrie.client.size",
    "cowrie.client.var",
    "cowrie.session.params",
}
KNOWN_EVENTS = ANALYSIS_EVENTS | AUXILIARY_EVENTS
LOGIN_EVENTS = {"cowrie.login.failed", "cowrie.login.success"}
COMMAND_EVENTS = {"cowrie.command.input", "cowrie.command.failed"}
COMMON_FIELDS = {
    "eventid",
    "timestamp",
    "session",
    "src_ip",
    "src_port",
    "dst_ip",
    "dst_port",
    "protocol",
    "sensor",
    "message",
    "uuid",
}
LOGBOOK_FIELDS = {
    "run_id",
    "scenario_id",
    "step_no",
    "time_utc_client",
    "may_nguon",
    "ip_nguon",
    "dich_vu_cong",
    "thao_tac",
    "ket_qua_phia_client",
    "nguoi_thuc_hien",
    "ghi_chu",
}
MANIFEST_LINE = re.compile(r"^([0-9a-fA-F]{64}) [ *](\./.+)$")


class ProcessError(Exception):
    """An input or output contract error safe to report to the CLI user."""


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _validate_paths(
    run_dir: Path, out_processed: Path, out_results: Path | None
) -> None:
    raw_dir = (_project_root() / "data" / "raw").resolve()
    protected_inputs = [run_dir.resolve()]
    outputs = [out_processed.resolve()]
    if out_results is not None:
        outputs.append(out_results.resolve())
    for output in outputs:
        if _is_within(output, raw_dir):
            raise ProcessError(f"Đầu ra không được nằm trong data/raw/: {output}")
        if any(_is_within(output, source) for source in protected_inputs):
            raise ProcessError(f"Đầu ra không được nằm trong thư mục đầu vào: {output}")
    if out_results is not None:
        processed = out_processed.resolve()
        results = out_results.resolve()
        if _is_within(processed, results) or _is_within(results, processed):
            raise ProcessError("Hai thư mục đầu ra không được lồng nhau.")


def _is_demo_directory(run_dir: Path) -> bool:
    return run_dir.name.startswith("minh_hoa_") or (
        "fixtures" in run_dir.parts and run_dir.name.startswith("minh_hoa")
    )


def _is_standard_raw_run(run_dir: Path) -> bool:
    raw_dir = (_project_root() / "data" / "raw").resolve()
    return (
        _is_within(run_dir.resolve(), raw_dir)
        and run_dir.resolve().parent == raw_dir
        and re.fullmatch(r"RUN-[A-Za-z0-9_-]+", run_dir.name) is not None
    )


def _select_data_origin(run_dir: Path, requested: str | None) -> str:
    if _is_demo_directory(run_dir):
        if requested not in (None, "minh_hoa"):
            raise ProcessError(
                "Thư mục minh_hoa_* bắt buộc dùng --data-origin minh_hoa."
            )
        return "minh_hoa"
    if requested is not None:
        return requested
    if _is_standard_raw_run(run_dir):
        return "lab"
    raise ProcessError(
        "Ngoài data/raw/RUN-xx phải chỉ rõ --data-origin; "
        "dữ liệu minh họa luôn dùng minh_hoa."
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_manifest(run_dir: Path) -> tuple[list[tuple[str, bool, str]], list[str]]:
    manifest_path = run_dir / "SHA256SUMS"
    if not manifest_path.is_file():
        raise ProcessError(f"Thiếu file bắt buộc: {manifest_path}")

    entries: dict[str, str] = {}
    errors: list[str] = []
    for line_number, line in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        match = MANIFEST_LINE.fullmatch(line)
        if not match:
            errors.append(f"SHA256SUMS:{line_number}: sai định dạng sha256sum")
            continue
        digest, relative_name = match.groups()
        relative = Path(relative_name[2:])
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"SHA256SUMS:{line_number}: đường dẫn không an toàn")
            continue
        normalized = relative.as_posix()
        if normalized in entries:
            errors.append(f"SHA256SUMS:{line_number}: đường dẫn lặp {relative_name}")
            continue
        entries[normalized] = digest.lower()

    actual_files = {
        path.relative_to(run_dir).as_posix(): path
        for path in run_dir.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    for filename in sorted(set(actual_files) - set(entries)):
        errors.append(f"{filename}: không có trong SHA256SUMS")
    for filename in sorted(set(entries) - set(actual_files)):
        errors.append(f"{filename}: được khai báo nhưng không tồn tại")

    results: list[tuple[str, bool, str]] = []
    for filename in sorted(entries):
        path = actual_files.get(filename)
        if path is None:
            results.append((filename, False, "MISSING"))
            continue
        actual = _sha256(path)
        expected = entries[filename]
        results.append((filename, actual == expected, "OK" if actual == expected else "FAIL"))
    if errors:
        results.extend((message, False, "FAIL") for message in errors)
    return results, errors


def _ordered_log_files(run_dir: Path) -> list[Path]:
    files = [path for path in run_dir.glob("cowrie.json*") if path.is_file()]
    return sorted(files, key=lambda path: (path.name == "cowrie.json", path.name))


def _read_json_lines(
    log_files: list[Path],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    quality: dict[str, Any] = {
        "physical_lines": 0,
        "valid_json_lines": 0,
        "malformed_lines": [],
        "blank_lines": [],
        "duplicate_refs": [],
    }
    first_by_content: dict[str, dict[str, Any]] = {}
    file_order = {path: index for index, path in enumerate(log_files)}
    for path in log_files:
        try:
            source = path.open("r", encoding="utf-8")
        except OSError as error:
            raise ProcessError(f"Không đọc được {path.name}: {error}") from error
        with source:
            for line_number, line in enumerate(source, start=1):
                quality["physical_lines"] += 1
                raw_ref = f"{path.name}:{line_number}"
                if not line.strip():
                    quality["blank_lines"].append(raw_ref)
                    continue
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        raise ValueError("JSON cấp cao nhất không phải object")
                except (json.JSONDecodeError, ValueError) as error:
                    quality["malformed_lines"].append((raw_ref, str(error)))
                    continue

                quality["valid_json_lines"] += 1
                canonical = json.dumps(
                    event, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                )
                if canonical in first_by_content:
                    first_by_content[canonical]["duplicate_count"] += 1
                    quality["duplicate_refs"].append(
                        (raw_ref, first_by_content[canonical]["raw_ref"])
                    )
                    continue
                record = {
                    "event": event,
                    "raw_ref": raw_ref,
                    "file_order": file_order[path],
                    "duplicate_count": 0,
                }
                first_by_content[canonical] = record
                rows.append(record)
    return rows, quality


def _parse_utc(value: Any) -> pd.Timestamp | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = pd.to_datetime(value, utc=True, errors="coerce")
    except (TypeError, ValueError, OverflowError):
        return None
    if pd.isna(parsed):
        return None
    return pd.Timestamp(parsed)


def _iso_utc(value: pd.Timestamp | None) -> str:
    if value is None:
        return ""
    return value.isoformat().replace("+00:00", "Z")


def _field_value(event: dict[str, Any], key: str) -> str:
    value = event.get(key)
    if value is None:
        return ""
    return str(value)


def _duration_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def _classify_and_normalize(
    records: list[dict[str, Any]], run_id: str, data_origin: str
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    quality: dict[str, Any] = {
        "unknown_events": [],
        "missing_fields": Counter(),
        "bad_timestamps": [],
        "missing_timestamps": [],
        "event_classes": Counter(),
        "protocol_conflicts": [],
        "duration_compute_failures": [],
    }
    accepted_records: list[dict[str, Any]] = []
    session_protocols: dict[str, set[str]] = defaultdict(set)
    connect_protocols: dict[str, set[str]] = defaultdict(set)
    session_ports: dict[str, set[str]] = defaultdict(set)
    command_failures: set[tuple[str, str]] = set()

    for record in records:
        event = record["event"]
        event_type = event.get("eventid")
        if not isinstance(event_type, str) or not event_type:
            quality["missing_fields"][("<missing>", "event_type")] += 1
            continue
        if event_type not in KNOWN_EVENTS:
            quality["unknown_events"].append((event_type, record["raw_ref"]))
            quality["event_classes"]["unknown"] += 1
            continue

        classification = (
            "analysis" if event_type in ANALYSIS_EVENTS else "known_auxiliary"
        )
        session_id = _field_value(event, "session")
        for field in ("src_ip", "session"):
            if not _field_value(event, field):
                quality["missing_fields"][(event_type, field)] += 1
        if event_type in LOGIN_EVENTS:
            for field in ("username", "password"):
                if not _field_value(event, field):
                    quality["missing_fields"][(event_type, field)] += 1
        if event_type in COMMAND_EVENTS and event.get("input") in (None, ""):
            quality["missing_fields"][(event_type, "input")] += 1
        protocol = _field_value(event, "protocol")
        dst_port = _field_value(event, "dst_port")
        timestamp = _parse_utc(event.get("timestamp"))
        if timestamp is None:
            if event.get("timestamp") in (None, ""):
                quality["missing_fields"][(event_type, "timestamp")] += 1
                quality["missing_timestamps"].append(record["raw_ref"])
            else:
                quality["bad_timestamps"].append(
                    (record["raw_ref"], str(event.get("timestamp")))
                )
            continue
        quality["event_classes"][classification] += 1
        if session_id and protocol:
            session_protocols[session_id].add(protocol)
            if event_type == "cowrie.session.connect":
                connect_protocols[session_id].add(protocol)
        if session_id and dst_port and event_type == "cowrie.session.connect":
            session_ports[session_id].add(dst_port)
        if event_type == "cowrie.command.failed" and session_id:
            input_value = event.get("input")
            if isinstance(input_value, str):
                command_failures.add((session_id, input_value))
        record["timestamp"] = timestamp
        record["event_type"] = event_type
        record["session_id"] = session_id
        record["classification"] = classification
        accepted_records.append(record)

    normalized: list[dict[str, Any]] = []
    for record in accepted_records:
        event = record["event"]
        event_type = record["event_type"]
        session_id = record["session_id"]
        classification = record["classification"]
        protocol = _field_value(event, "protocol")
        protocol_inferred = False
        if not protocol:
            session_values = (
                connect_protocols.get(session_id, set()) if session_id else set()
            )
            if not session_values and session_id:
                session_values = session_protocols.get(session_id, set())
            if len(session_values) == 1:
                protocol = next(iter(session_values))
            elif len(session_values) > 1:
                quality["protocol_conflicts"].append(
                    (session_id, sorted(session_values))
                )
            if not protocol:
                port_values = session_ports.get(session_id, set())
                port = _field_value(event, "dst_port")
                if not port and len(port_values) == 1:
                    port = next(iter(port_values))
                protocol = {"2222": "ssh", "2223": "telnet"}.get(port, "")
                protocol_inferred = bool(protocol)

        client_version = ""
        client_hassh = ""
        username = ""
        password = ""
        login_result = ""
        command = ""
        command_supported = ""
        download_url = ""
        file_sha256 = ""
        duration_ms: int | None = None
        duration_computed = False

        if classification == "analysis":
            if event_type == "cowrie.client.version":
                client_version = _field_value(event, "version")
                if client_version == "":
                    quality["missing_fields"][(event_type, "version")] += 1
            elif event_type == "cowrie.client.kex":
                client_hassh = _field_value(event, "hassh")
            elif event_type in LOGIN_EVENTS:
                username = _field_value(event, "username")
                password = _field_value(event, "password")
                login_result = (
                    "success"
                    if event_type == "cowrie.login.success"
                    else "failed"
                )
            elif event_type in COMMAND_EVENTS:
                input_value = event.get("input")
                command = input_value if isinstance(input_value, str) else ""
                if event_type == "cowrie.command.input":
                    command_supported = (
                        "unsupported"
                        if session_id and (session_id, command) in command_failures
                        else "unknown"
                    )
                else:
                    command_supported = "unsupported"
            elif event_type in {
                "cowrie.session.file_download",
                "cowrie.session.file_download.failed",
            }:
                download_url = _field_value(event, "url")
                if event_type == "cowrie.session.file_download":
                    file_sha256 = _field_value(event, "shasum")
            elif event_type == "cowrie.session.closed":
                duration_ms = _duration_int(event.get("duration_ms"))

        row = {
            "event_time_utc": _iso_utc(record["timestamp"]),
            "event_type": event_type,
            "session_id": session_id,
            "src_ip": _field_value(event, "src_ip"),
            "src_port": _field_value(event, "src_port"),
            "dst_ip": _field_value(event, "dst_ip"),
            "dst_port": _field_value(event, "dst_port"),
            "protocol": protocol,
            "sensor": _field_value(event, "sensor"),
            "client_version": client_version,
            "client_hassh": client_hassh,
            "username": username,
            "password": password,
            "login_result": login_result,
            "command": command,
            "command_supported": command_supported,
            "download_url": download_url,
            "file_sha256": file_sha256,
            "duration_ms": "" if duration_ms is None else str(duration_ms),
            "message": _field_value(event, "message"),
            "scenario_id": "",
            "run_id": run_id,
            "data_origin": data_origin,
            "raw_ref": record["raw_ref"],
            "protocol_inferred": str(protocol_inferred).lower(),
            "duration_computed": str(duration_computed).lower(),
            "duplicate_count": str(record["duplicate_count"]),
            "_timestamp": record["timestamp"],
            "_file_order": record["file_order"],
            "_event_class": classification,
            "_source": event,
        }
        normalized.append(row)

    normalized.sort(
        key=lambda row: (
            row["_timestamp"],
            row["_file_order"],
            row["raw_ref"].rsplit(":", 1)[-1].zfill(12),
        )
    )
    return normalized, quality


def _read_clock_offset(run_dir: Path) -> float | None:
    note = run_dir / "run_note.txt"
    if not note.is_file():
        return None
    text = note.read_text(encoding="utf-8")
    match = re.search(
        r"(?:clock_offset_s|clock_offset)\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))",
        text,
    )
    return float(match.group(1)) if match else None


def _service_port(value: Any) -> int | None:
    match = re.search(r"(?:^|/)(\d+)\s*$", str(value or "").strip())
    return int(match.group(1)) if match else None


def _load_logbook(path: Path | None, run_id: str) -> list[dict[str, Any]]:
    if path is None:
        return []
    if not path.is_file():
        raise ProcessError(f"Không tìm thấy nhật ký thử nghiệm: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        missing = LOGBOOK_FIELDS - set(reader.fieldnames or [])
        if missing:
            raise ProcessError(
                "Nhật ký thiếu cột H.2: " + ", ".join(sorted(missing))
            )
        rows: list[dict[str, Any]] = []
        for row in reader:
            if row.get("run_id") != run_id:
                continue
            parsed = _parse_utc(row.get("time_utc_client"))
            if parsed is None:
                continue
            row["_timestamp"] = parsed
            row["_port"] = _service_port(row.get("dich_vu_cong"))
            rows.append(row)
    return rows


def _attach_scenarios(
    sessions: list[dict[str, Any]],
    logbook: list[dict[str, Any]],
    clock_offset: float | None,
    has_logbook: bool,
    quality: dict[str, Any],
) -> None:
    if not has_logbook:
        quality["scenario_warning"] = (
            "Không có --logbook; scenario_id để rỗng và mọi phiên unmatched."
        )
        for session in sessions:
            session["scenario_match_status"] = "unmatched"
        return
    if clock_offset is None:
        quality["scenario_warning"] = (
            "Có --logbook nhưng thiếu clock_offset(_s) trong run_note.txt; "
            "không khớp kịch bản, mọi phiên needs_review."
        )
        for session in sessions:
            session["scenario_match_status"] = "needs_review"
        return

    windows: dict[tuple[str, str, int], list[pd.Timestamp]] = defaultdict(list)
    for row in logbook:
        scenario = str(row.get("scenario_id", "")).strip()
        source_ip = str(row.get("ip_nguon", "")).strip()
        port = row.get("_port")
        if scenario and source_ip and port is not None:
            windows[(scenario, source_ip, port)].append(row["_timestamp"])
    tolerance = abs(clock_offset)

    for session in sessions:
        start = session["_start"]
        end = session["_end"]
        session_ip = session["src_ip"]
        session_port = int(session["dst_port"]) if session["dst_port"].isdigit() else None
        if start is None or end is None or not session_ip or session_port is None:
            session["scenario_match_status"] = "needs_review"
            continue
        candidates: set[str] = set()
        for (scenario, source_ip, port), times in windows.items():
            if source_ip != session_ip or port != session_port:
                continue
            window_start = min(times) - pd.to_timedelta(tolerance, unit="s")
            window_end = max(times) + pd.to_timedelta(tolerance, unit="s")
            if start <= window_end and end >= window_start:
                candidates.add(scenario)
        ordered_candidates = sorted(candidates)
        if len(ordered_candidates) == 1:
            session["scenario_candidates"] = ""
            session["scenario_id"] = ordered_candidates[0]
            session["scenario_match_status"] = "matched"
        elif not ordered_candidates:
            session["scenario_candidates"] = ""
            session["scenario_match_status"] = "unmatched"
        else:
            session["scenario_candidates"] = json.dumps(
                ordered_candidates, ensure_ascii=False, separators=(",", ":")
            )
            session["scenario_match_status"] = "ambiguous"


def _build_sessions(
    events: list[dict[str, Any]],
    run_id: str,
    data_origin: str,
    logbook: list[dict[str, Any]],
    clock_offset: float | None,
    has_logbook: bool,
    quality: dict[str, Any],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        if event["session_id"]:
            grouped[event["session_id"]].append(event)

    sessions: list[dict[str, Any]] = []
    for session_id in sorted(grouped):
        rows = sorted(
            grouped[session_id],
            key=lambda row: (
                row["_timestamp"],
                row["_file_order"],
                row["raw_ref"].rsplit(":", 1)[-1].zfill(12),
            ),
        )
        times = [row["_timestamp"] for row in rows]
        start = min(times)
        end = max(times)
        connect_times = [
            row["_timestamp"]
            for row in rows
            if row["event_type"] == "cowrie.session.connect"
        ]
        close_rows = [
            row
            for row in rows
            if row["event_type"] == "cowrie.session.closed"
        ]
        close_row = max(close_rows, key=lambda row: row["_timestamp"]) if close_rows else None
        duration_ms: int | None = None
        duration_source = ""
        if close_row and close_row["duration_ms"] != "":
            duration_ms = int(close_row["duration_ms"])
            duration_source = "tool"
        elif close_row and connect_times:
            duration_ms = int(
                (close_row["_timestamp"] - min(connect_times)).total_seconds() * 1000
            )
            duration_source = "computed"
            close_row["duration_ms"] = str(duration_ms)
            close_row["duration_computed"] = "true"
        elif close_row:
            quality["duration_compute_failures"].append(
                f"{session_id}: không có mốc connect để tính duration_ms"
            )

        ip_values = sorted({row["src_ip"] for row in rows if row["src_ip"]})
        port_values = sorted({row["dst_port"] for row in rows if row["dst_port"]})
        protocol_values = sorted({row["protocol"] for row in rows if row["protocol"]})
        if len(ip_values) > 1:
            quality.setdefault("session_conflicts", []).append(
                f"{session_id}: src_ip={','.join(ip_values)}"
            )
        if len(port_values) > 1:
            quality.setdefault("session_conflicts", []).append(
                f"{session_id}: dst_port={','.join(port_values)}"
            )
        if len(protocol_values) > 1:
            quality.setdefault("session_conflicts", []).append(
                f"{session_id}: protocol={','.join(protocol_values)}"
            )
        commands = [
            row["command"]
            for row in rows
            if row["event_type"] == "cowrie.command.input"
        ]
        versions = [
            row["client_version"]
            for row in rows
            if row["event_type"] == "cowrie.client.version"
            and row["client_version"] != ""
        ]
        session = {
            "session_id": session_id,
            "run_id": run_id,
            "scenario_id": "",
            "scenario_match_status": "unmatched",
            "scenario_candidates": "",
            "src_ip": ip_values[0] if len(ip_values) == 1 else "",
            "protocol": protocol_values[0] if len(protocol_values) == 1 else "",
            "dst_port": port_values[0] if len(port_values) == 1 else "",
            "start_utc": _iso_utc(start),
            "end_utc": _iso_utc(end),
            "duration_ms": "" if duration_ms is None else str(duration_ms),
            "duration_source": duration_source,
            "n_events": str(len(rows)),
            "n_login_failed": str(
                sum(row["event_type"] == "cowrie.login.failed" for row in rows)
            ),
            "n_login_success": str(
                sum(row["event_type"] == "cowrie.login.success" for row in rows)
            ),
            "n_commands": str(
                sum(row["event_type"] == "cowrie.command.input" for row in rows)
            ),
            "commands": json.dumps(
                commands, ensure_ascii=False, separators=(",", ":")
            ),
            "has_download": str(
                any(row["event_type"] == "cowrie.session.file_download" for row in rows)
            ).lower(),
            "closed_properly": str(bool(close_rows)).lower(),
            "client_version": versions[0] if versions else "",
            "data_origin": data_origin,
            "_start": start,
            "_end": end,
        }
        sessions.append(session)

    _attach_scenarios(sessions, logbook, clock_offset, has_logbook, quality)
    return sessions


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def _format_quality_report(
    run_id: str,
    data_origin: str,
    log_files: list[Path],
    hash_results: list[tuple[str, bool, str]],
    parse_quality: dict[str, Any],
    transform_quality: dict[str, Any],
    sessions: list[dict[str, Any]],
    event_rows: list[dict[str, Any]],
) -> str:
    login_count = sum(
        row["event_type"] in LOGIN_EVENTS for row in event_rows
    )
    lines = [
        f"run_id: {run_id}",
        f"data_origin: {data_origin}",
        "1. Đầu vào và SHA-256",
        "   File log: " + (", ".join(path.name for path in log_files) or "(không có)"),
    ]
    lines.extend(
        f"   {status}: {filename}"
        for filename, _, status in hash_results
    )
    lines.extend(
        [
            "2. Đọc dòng và khử trùng",
            f"   Dòng vật lý: {parse_quality['physical_lines']}",
            f"   JSON hợp lệ: {parse_quality['valid_json_lines']}",
            f"   JSON hỏng: {len(parse_quality['malformed_lines'])}",
            f"   Dòng trống: {len(parse_quality['blank_lines'])}",
            f"   Bản trùng dư đã loại: {len(parse_quality['duplicate_refs'])}",
        ]
    )
    if parse_quality["malformed_lines"]:
        lines.append("   Dòng JSON hỏng:")
        lines.extend(
            f"      {raw_ref}: {error}"
            for raw_ref, error in parse_quality["malformed_lines"]
        )
    if parse_quality["blank_lines"]:
        lines.append(
            "   Dòng trống: " + ", ".join(parse_quality["blank_lines"])
        )
    if parse_quality["duplicate_refs"]:
        lines.append("   Dòng trùng (bản dư → bản giữ):")
        lines.extend(
            f"      {duplicate} -> {original}"
            for duplicate, original in parse_quality["duplicate_refs"]
        )

    lines.extend(
        [
            "3. Phân loại sự kiện",
            f"   Giữ - analysis: {transform_quality['event_classes']['analysis']}",
            "   Giữ - known_auxiliary: "
            f"{transform_quality['event_classes']['known_auxiliary']}",
            f"   Event lạ bị loại: {len(transform_quality['unknown_events'])}",
        ]
    )
    if transform_quality["unknown_events"]:
        lines.append("   Event lạ (eventid, file:dòng):")
        lines.extend(
            f"      {event_type}: {raw_ref}"
            for event_type, raw_ref in transform_quality["unknown_events"]
        )
        lines.extend(
            [
                "   Gợi ý nội dung cho review/issues.md (chưa ghi file):",
                "      [ISSUE] Eventid chưa phân loại – kiểm tra allowlist và cập nhật sau review:",
            ]
        )
        lines.extend(
            f"      - eventid={event_type}, vị trí={raw_ref}"
            for event_type, raw_ref in transform_quality["unknown_events"]
        )
    else:
        lines.append("   Không có event lạ; known_auxiliary không tính là event lạ.")

    lines.append("4. Trường bắt buộc thiếu theo event_type")
    if transform_quality["missing_fields"]:
        for (event_type, field), count in sorted(
            transform_quality["missing_fields"].items()
        ):
            lines.append(f"   {event_type}.{field}: {count}")
    else:
        lines.append("   Không có.")

    lines.extend(
        [
            "5. Timestamp lỗi",
            f"   Thiếu timestamp: {len(transform_quality['missing_timestamps'])}",
            f"   Không parse được: {len(transform_quality['bad_timestamps'])}",
        ]
    )
    for raw_ref in transform_quality["missing_timestamps"]:
        lines.append(f"      Thiếu: {raw_ref}")
    for raw_ref, value in transform_quality["bad_timestamps"]:
        lines.append(f"      Không parse: {raw_ref} ({value})")

    status_counts = Counter(session["scenario_match_status"] for session in sessions)
    protocol_inferred = sum(row["protocol_inferred"] == "true" for row in event_rows)
    duration_computed = sum(row["duration_computed"] == "true" for row in event_rows)
    lines.extend(
        [
            "6. Phiên, suy luận và đơn vị đếm",
            f"   Phiên tổng: {len(sessions)}",
            f"   scenario unmatched: {status_counts['unmatched']}",
            f"   scenario ambiguous: {status_counts['ambiguous']}",
            f"   scenario needs_review: {status_counts['needs_review']}",
            f"   protocol suy từ cổng (event): {protocol_inferred}",
            f"   duration tự tính (event đóng phiên): {duration_computed}",
            "   Đơn vị đếm: sự kiện = dòng JSON; lần đăng nhập = event login.failed/success; "
            "phiên = session_id duy nhất.",
            f"   Sự kiện giữ trong events.csv: {len(event_rows)}",
            f"   Lần đăng nhập giữ: {login_count}",
            f"   Phiên giữ trong sessions.csv: {len(sessions)}",
        ]
    )
    if transform_quality.get("scenario_warning"):
        lines.append(f"   Cảnh báo gắn kịch bản: {transform_quality['scenario_warning']}")
    if "delta_override" in transform_quality:
        lines.append(
            "   Ghi đè clock_offset bằng --delta-seconds: "
            f"{transform_quality['delta_override']}s"
        )
    if transform_quality.get("protocol_conflicts"):
        lines.append("   Protocol mâu thuẫn:")
        lines.extend(
            f"      {session_id}: {', '.join(protocols)}"
            for session_id, protocols in transform_quality["protocol_conflicts"]
        )
    if transform_quality.get("duration_compute_failures"):
        lines.append("   Không tính được duration:")
        lines.extend(
            f"      {failure}"
            for failure in transform_quality["duration_compute_failures"]
        )
    has_review_issue = bool(
        parse_quality["malformed_lines"]
        or transform_quality["missing_timestamps"]
        or transform_quality["bad_timestamps"]
        or transform_quality["missing_fields"]
        or transform_quality["unknown_events"]
    )
    if has_review_issue:
        lines.append(
            "7. Báo lỗi review: review/issues.md (cần cập nhật khi có issue)"
        )
    else:
        lines.append(
            "7. Báo lỗi review: không phát sinh issue cho review/issues.md"
        )
    return "\n".join(lines) + "\n"


def process_run(
    run_dir: Path,
    *,
    logbook_path: Path | None = None,
    data_origin: str | None = None,
    out_processed: Path | None = None,
    out_results: Path | None = None,
    delta_seconds: float | None = None,
) -> tuple[Path, Path, Path]:
    run_dir = run_dir.resolve()
    if not run_dir.is_dir():
        raise ProcessError(f"Không tìm thấy thư mục lượt chạy: {run_dir}")
    run_id = run_dir.name
    if not run_id:
        raise ProcessError("Không xác định được run_id từ tên thư mục.")
    origin = _select_data_origin(run_dir, data_origin)
    root = _project_root()
    processed_dir = (out_processed or root / "data" / "processed" / run_id).resolve()
    results_dir = out_results.resolve() if out_results is not None else None
    _validate_paths(run_dir, processed_dir, results_dir)

    hash_results, hash_errors = _check_manifest(run_dir)
    for filename, _, status in hash_results:
        print(f"{status}: {filename}")
    if hash_errors or any(not matched for _, matched, _ in hash_results):
        raise ProcessError("SHA256SUMS không khớp; dừng trước khi xử lý log.")

    log_files = _ordered_log_files(run_dir)
    if not log_files:
        raise ProcessError("Thiếu file bắt buộc: không có cowrie.json*.")

    records, parse_quality = _read_json_lines(log_files)
    normalized, transform_quality = _classify_and_normalize(
        records, run_id, origin
    )
    logbook = _load_logbook(logbook_path, run_id)
    clock_offset = None
    if logbook_path is not None:
        if delta_seconds is not None:
            clock_offset = delta_seconds
            transform_quality["delta_override"] = delta_seconds
        else:
            clock_offset = _read_clock_offset(run_dir)
    sessions = _build_sessions(
        normalized,
        run_id,
        origin,
        logbook,
        clock_offset,
        logbook_path is not None,
        transform_quality,
    )
    scenario_by_session = {
        session["session_id"]: session["scenario_id"]
        for session in sessions
    }
    for event in normalized:
        if event["session_id"]:
            event["scenario_id"] = scenario_by_session.get(event["session_id"], "")
    report = _format_quality_report(
        run_id,
        origin,
        log_files,
        hash_results,
        parse_quality,
        transform_quality,
        sessions,
        normalized,
    )

    events_path = processed_dir / "events.csv"
    sessions_path = processed_dir / "sessions.csv"
    report_dir = results_dir or processed_dir
    report_path = report_dir / "bao_cao_chat_luong.txt"
    _write_csv(events_path, EVENT_FIELDS, normalized)
    _write_csv(sessions_path, SESSION_FIELDS, sessions)
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8", newline="\n")
    return events_path, sessions_path, report_path


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Kiểm hash và chuẩn hóa log Cowrie của một lượt chạy."
    )
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--logbook", type=Path)
    parser.add_argument(
        "--data-origin", choices=("lab", "tham_khao", "minh_hoa")
    )
    parser.add_argument("--out-processed", type=Path)
    parser.add_argument("--out-results", type=Path)
    parser.add_argument("--delta-seconds", type=float, default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = _parse_args(argv)
    try:
        events_path, sessions_path, report_path = process_run(
            args.run_dir,
            logbook_path=args.logbook,
            data_origin=args.data_origin,
            out_processed=args.out_processed,
            out_results=args.out_results,
            delta_seconds=args.delta_seconds,
        )
    except (ProcessError, OSError, UnicodeError) as error:
        print(f"Lỗi: {error}", file=sys.stderr)
        return 2
    print(f"events.csv: {events_path}")
    print(f"sessions.csv: {sessions_path}")
    print(f"bao_cao_chat_luong.txt: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
